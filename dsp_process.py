import time
import ctypes 
import multiprocessing as mp
import numpy as np
import itertools

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARN)

from util import shmem_as_ndarray, NP_TO_CTYPES
from dsp_circuit import DSPCircuit
from shared_ring_buffer import ReadableSharedRingBuffer, \
        WriteableSharedRingBuffer

def monitor(circuit_info, poll_period, pipe):
    '''
    Monitor loop that will be run in the subprocess.  
    '''

    ##############################################################################
    # Internal (private) function definitions
    ##############################################################################
    def process_request(pipe, circuits, timeout):
        # Check to see if data is available.  Keep checking until the timeout
        # period is over.
        if pipe.poll(timeout):
            id, device, request, args = pipe.recv()
            # Process the request
            circuit = circuits[device]
            response = getattr(circuit, request)(*args)
            # Return the result of the request (along with the id)
            pipe.send((id, response))

    def read_buffer(hw_buffer, sw_buffer):
        if hw_buffer.pending():
            data = hw_buffer.read()
            sw_buffer.write(data)

    def write_buffer(hw_buffer, sw_buffer):
        if hw_buffer.available() and sw_buffer.pending():
            samples = hw_buffer.available()
            data = sw_buffer.read(samples)
            hw_buffer.write(data)

    ##############################################################################
    # Initialization code
    ##############################################################################
    # Load the circuit first so we can use them to help initialize the buffers.
    # Once the circuit is loaded, initialize the bufers.  We do not currently
    # support read/write buffers (this would require locks, etc., and be
    # complicated to maintain and support).
    circuits = {}
    read_buffers, write_buffers = [], []
    for c_info, buffer_info in circuit_info.items():
        circuit_name, device_name = c_info
        circuit = DSPCircuit(circuit_name, device_name)
        circuits[device_name] = circuit

        for info in buffer_info:
            buffer_name = info['buffer_name']
            mode = info['mode']
            args = info['args']
            kwargs = info['kwargs']
            shmem = info['shmem']
            iwrite = info['iwrite']
            iread = info['iread']

            hw_buffer = circuit.get_buffer(buffer_name, mode, *args, **kwargs)
            cache = shmem_as_ndarray(shmem).reshape((hw_buffer.channels, -1))
            iwrite.value = 0
            iread.value = 0

            # The mode refers to the hardware buffer itself.  If we want to read
            # from the hardware buffer, then we need to write the data to the shared
            # memory via a WriteableSharedRingBuffer.  The other process will be
            # viewing the same memory space via a ReadableSharedRingBuffer.
            if mode == 'r':
                sw_buffer = WriteableSharedRingBuffer(cache, iwrite, iread)
                read_buffers.append((hw_buffer, sw_buffer))
            elif mode == 'w':
                sw_buffer = ReadableSharedRingBuffer(cache, iwrite, iread)
                write_buffers.append((hw_buffer, sw_buffer))
            print "HW BUFFER", hw_buffer.size
            print "SW BUFFER", sw_buffer.size

        # Ok, now that we've initialized all the buffers for this circuit, it's
        # safe to start it.  Very important!  If you are running code that
        # requires multiple devices, then you need to be sure that the circuits
        # are designed to handle being started asynchronously.
        circuit.start()

    ##############################################################################
    # Actual event loop
    ##############################################################################
    while True:
        start = time.time()
        for hw_buffer, sw_buffer in read_buffers:
            # Since downloading buffer data can be a bit slow, let's check in
            # between downloads to see if we need to process any other requests
            # (i.e. set_tag and get_tag).
            process_request(pipe, circuits, 0)
            read_buffer(hw_buffer, sw_buffer)

        for hw_buffer, sw_buffer in write_buffers:
            process_request(pipe, circuits, 0)
            write_buffer(hw_buffer, sw_buffer)

        # Now that we're done polling the buffers, check to see how much time
        # has elapsed.  If all tasks were completed before the buffer poll
        # period has expired, shift task to checking request queue.
        while True:
            elapsed = time.time()-start
            if elapsed >= poll_period:
                break
            process_request(pipe, circuits, poll_period-elapsed)

class DSPProcess(mp.Process):

    def __init__(self, poll_period=0.1, cache_duration=30):
        self.cache_duration = cache_duration
        self.poll_period = poll_period

        # Shared information
        self._circuit_info = {}
        self._circuits = {}

        self._parent_pipe, self._child_pipe = mp.Pipe()
        self._request_id = itertools.count()

        import atexit
        atexit.register(self.terminate)
        super(DSPProcess, self).__init__(target=monitor)

    def load_circuit(self, circuit_name, device_name):
        self._circuit_info[(circuit_name, device_name)] = []
        # We need to store a reference to the circuit here so we can properly
        # initialize any buffers we need
        circuit = DSPCircuit(circuit_name, device_name)
        self._circuits[device_name] = circuit
        shared_circuit = SharedCircuit(self, circuit_name, device_name)
        shared_circuit.fs = circuit.fs
        return shared_circuit

    def get_buffer(self, device_name, buffer_name, mode, *args, **kwargs):
        if self.is_alive():
            mesg = "Cannot allocate memory for buffer cache once process" + \
                    "has started"
            raise SystemError, mesg

        # Compute how much shared memory we need to allocate for the cache.  We
        # load the buffer in the parent process so we can inspect the circuit
        # and determine whether there are any pre-defined tags.
        circuit = self._circuits[device_name]

        buffer = circuit.get_buffer(buffer_name, mode, *args, **kwargs)
        cache_size = int(buffer.fs*self.cache_duration)*buffer.channels
        mem_type = NP_TO_CTYPES[buffer.dest_type]

        # Allocate the cache memory and create shared values used for
        # inter-process communication
        shmem = mp.RawArray(mem_type, cache_size) 
        iwrite = mp.Value(ctypes.c_uint)
        iread = mp.Value(ctypes.c_uint)
        #iwrite = mp.RawValue(ctypes.c_uint)
        #iread = mp.RawValue(ctypes.c_uint)

        # Save the information we need for reinitializing the buffer once the
        # process launches
        info = dict(circuit_name=circuit.circuit_name,
                device=circuit.device_name, buffer_name=buffer_name, mode=mode,
                args=args, kwargs=kwargs, shmem=shmem, iwrite=iwrite,
                iread=iread)
        key = (circuit.circuit_name, circuit.device_name)
        self._circuit_info[key].append(info)

        # Initialize the shared memory space for storing data acquired from the
        # DSP hardware
        cache = shmem_as_ndarray(shmem).reshape((buffer.channels, -1))
        if mode == 'r':
            sh_buffer = ReadableSharedRingBuffer(cache, iwrite, iread)
        elif mode == 'w':
            sh_buffer = WriteableSharedRingBuffer(cache, iwrite, iread)

        # Copy the attributes over from the actual buffer to the shared buffer
        # so we have access to the metadata we need
        attrs = ['fs', 'channels']
        for k, v in buffer.attributes(attrs).items():
            setattr(sh_buffer, k, v)
        return sh_buffer

    def run(self):
        monitor(self._circuit_info, self.poll_period, self._child_pipe)

    def _get_response(self, device_name, request, args=None, timeout=None):
        '''
        Passes along request to the other process and waits for a response.
        '''
        # Generate a unique ID that ensures that the other process is responding
        # to the correct item 
        if args is None:
            args = ()
        id = self._request_id.next()
        # Send the request to the process via a queue
        self._parent_pipe.send((id, device_name, request, args))
        # Wait till the response is available.  If no response is recieved after
        # one second, raise an exception.
        if not self._parent_pipe.poll(timeout):
            mesg = "No response recieved for request %s(%r)" % (request, args)
            raise IOError, mesg
        # Get the response
        id, response = self._parent_pipe.recv()
        # Make sure it's the right response (this is probably an unecessary
        # check since we are blocking)
        if id != id:
            raise IOException, "Wrong response returned"
        return response

def partial(f, device_name, action):
    def wrapper(*args):
        return f(device_name, action, args)
    return wrapper

class SharedCircuit(object):
    '''
    This is a duck-typed class meant to support the methods available on
    DSPCircuit.  It does not subclass DSPCircuit, but supports all the key
    methods you need (e.g. get_tag, set_tag, get_buffer).

    The only key difference is that you must ensure that shared memory for the
    process is allocated before you start it.  This means you must call
    `get_buffer` prior to calling `start`.  This is, in general, good practice
    anyway.
    '''

    def __init__(self, process, circuit_name, device_name):
        self.process = process
        self.device_name = device_name
        self.circuit_name = circuit_name

    def get_buffer(self, name, *args, **kwargs):
        return self.process.get_buffer(self.device_name, name, *args, **kwargs)

    def __getattr__(self, name):
        '''
        This is just wraps up the method call into an object that can be sent
        via the queue to the other process.
        '''
        if name in ['stop', 'get_tag', 'set_tag', 'cget_tag', 'cset_tag',
                    'trigger']:
            return partial(self.process._get_response, self.device_name, name)
