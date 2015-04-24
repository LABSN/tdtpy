import time
import ctypes
import multiprocessing as mp
import itertools

import logging

from .util import shmem_as_ndarray, NP_TO_CTYPES
from .dsp_circuit import DSPCircuit
from .shared_ring_buffer import (ReadableSharedRingBuffer,
                                 WriteableSharedRingBuffer)

log = logging.getLogger(__name__)


def monitor(circuit_info, poll_period, pipe):
    '''
    Monitor loop that will be run in the subprocess.
    '''
    global RUN
    RUN = True
    log.debug("STARTING")

    ###########################################################################
    # Internal (private) function definitions
    ###########################################################################
    def process_request(pipe, circuits, timeout):
        # Check to see if data is available.  Keep checking until the timeout
        # period is over.
        if pipe.poll(timeout):
            id, device, request, args = pipe.recv()
            log.debug("Recieved request %s with args %r", request, args)

            # TERMINATE is a special request to end the process and shutdown.
            # We communicate this to the loop via a global variable, RUN.
            if request == 'TERMINATE':
                global RUN
                RUN = False
            else:
                # Process the request
                circuit = circuits[device]
                response = getattr(circuit, request)(*args)
                # Return the result of the request (along with the id)
                pipe.send((id, response))
                return False

    def read_buffer(hw_buffer, sw_buffer):
        if hw_buffer.pending():
            data = hw_buffer.read()
            # Timeout should be set to 0 (otherwise we are defeating the point
            # of using multiprocessing).
            sw_buffer.write(data, timeout=0)

    def write_buffer(hw_buffer, sw_buffer):
        if sw_buffer.should_set():
            data = sw_buffer.read()
            hw_buffer.set(data)
            sw_buffer._ioffset.value = -1
            log.debug("Request to set buffer %s with %d samples",
                      hw_buffer, len(data))
            sw_buffer.notify()
        elif hw_buffer.available() and sw_buffer.pending():
            log.debug("Writing data to buffer")
            available = hw_buffer.available()
            pending = sw_buffer.pending()
            samples = min((available, pending))
            data = sw_buffer.read(samples)
            hw_buffer.write(data[0])
            if not sw_buffer.pending():
                sw_buffer.notify()

    ###########################################################################
    # Initialization code
    ###########################################################################
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
            ioffset = info['ioffset']
            condition = info['condition']

            hw_buffer = circuit.get_buffer(buffer_name, mode, *args, **kwargs)
            cache = shmem_as_ndarray(shmem).reshape((hw_buffer.channels, -1))

            # The mode refers to the hardware buffer itself.  If we want to
            # read from the hardware buffer, then we need to write the data to
            # the shared memory via a WriteableSharedRingBuffer.  The other
            # process will be viewing the same memory space via a
            # ReadableSharedRingBuffer.
            args = cache, iwrite, iread, ioffset, condition, circuit
            if mode == 'r':
                sw_buffer = WriteableSharedRingBuffer(*args)
                read_buffers.append((hw_buffer, sw_buffer))
            elif mode == 'w':
                sw_buffer = ReadableSharedRingBuffer(*args)
                write_buffers.append((hw_buffer, sw_buffer))

        # Ok, now that we've initialized all the buffers for this circuit, it's
        # safe to start it.  Very important!  If you are running code that
        # requires multiple devices, then you need to be sure that the circuits
        # are designed to handle being started asynchronously (e.g. use the
        # zBUS trigger).
        circuit.start()

    # Notify the parent that the process has started
    pipe.send((None, 'STARTED'))

    ###########################################################################
    # Actual event loop
    ###########################################################################
    while RUN:
        log.debug("RUNNING")
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

    # When a terminate request has been recieved via the piplein, RUN is set to
    # False and we loop through all the circuits, stopping each one.
    for circuit in circuits.values():
        circuit.stop()

    # Notify the parent process that we have successfully terminated
    pipe.send((None, 'OK'))

    # Finally, the process exits.


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

    def load_circuit(self, circuit_name, device_name, device_id=1):
        '''
        Loads circuit and prepares shared memory for interprocess communication

        Parameters
        ----------
        circuit_name : str
            Path to circuit to load
        device_name : str
            Name of TDT System3 device to load circuit to
        device_id : number
            ID of device

        Returns
        -------
        circuit : instance of DSPCircuit
            The circuit.
        '''
        self._circuit_info[(circuit_name, device_name)] = []
        # We need to store a reference to the circuit here so we can properly
        # initialize any buffers we need
        circuit = DSPCircuit(circuit_name, device_name, device_id=device_id)
        self._circuits[device_name] = circuit
        shared_circuit = SharedCircuit(self, circuit_name, device_name)
        shared_circuit.fs = circuit.fs
        return shared_circuit

    def get_buffer(self, device_name, buffer_name, mode, *args, **kwargs):
        if self.is_alive():
            raise SystemError("Cannot allocate memory for buffer cache once "
                              "process has started")

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
        ioffset = mp.Value(ctypes.c_int)

        # Reentrant lock
        condition = mp.Condition(mp.RLock())

        # Save the information we need for reinitializing the buffer once the
        # process launches
        info = dict(
            circuit_name=circuit.name,
            device=circuit.device_name, buffer_name=buffer_name, mode=mode,
            args=args, kwargs=kwargs, shmem=shmem, iwrite=iwrite,
            iread=iread, ioffset=ioffset, condition=condition)
        key = (circuit.name, circuit.device_name)
        self._circuit_info[key].append(info)

        # Initialize the shared memory space for storing data acquired from the
        # DSP hardware
        cache = shmem_as_ndarray(shmem).reshape((buffer.channels, -1))
        args = cache, iwrite, iread, ioffset, condition, circuit
        if mode == 'r':
            sh_buffer = ReadableSharedRingBuffer(*args)
        elif mode == 'w':
            sh_buffer = WriteableSharedRingBuffer(*args)

        # Copy the attributes over from the actual buffer to the shared buffer
        # so we have access to the metadata we need
        attrs = ['fs', 'channels', 'data_tag']
        for k, v in buffer.attributes(attrs).items():
            setattr(sh_buffer, k, v)
        return sh_buffer

    def start(self):
        super(DSPProcess, self).start()
        # Wait until we have recieved a message that the process has
        # successfully launched.  If we do not recive a message after 10
        # seconds or recieve the wrong response, raise an error.
        if not self._parent_pipe.poll(10):
            raise SystemError("Unable to launch process")
        else:
            id, response = self._parent_pipe.recv()
            if response != 'STARTED':
                raise SystemError("Unable to launch process")

    def run(self):
        monitor(self._circuit_info, self.poll_period, self._child_pipe)

    def _get_response(self, device_name, request, args=None, timeout=None):
        '''
        Passes along request to the other process and waits for a response.
        '''
        # Generate a unique ID that ensures that the other process is
        # responding to the correct item
        if args is None:
            args = ()
        id = self._request_id.next()
        # Send the request to the process via a queue
        log.debug('Requesting %s:%s with arguments %r', device_name, request,
                  args)
        self._parent_pipe.send((id, device_name, request, args))
        # Wait till the response is available.  If no response is recieved
        # after one second, raise an exception.
        if not self._parent_pipe.poll(timeout):
            raise IOError("No response recieved for request %s(%r)"
                          % (request, args))
        # Get the response
        id, response = self._parent_pipe.recv()
        # Make sure it's the right response (this is probably an unecessary
        # check since we are blocking)
        if id != id:  # XXX This does nothing...?
            raise IOError("Wrong response returned")
        return response

    def stop(self):
        self._parent_pipe.send((None, None, 'TERMINATE', None))
        id, response = self._parent_pipe.recv()


def partial(f, device_name, action, timeout):
    def wrapper(*args):
        return f(device_name, action, args, timeout)
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

    # List of methods whose attributes can be sent directly to the DSP process
    # (pretty much all of them at the moment).  Note that set_coefficients may
    # not work for large coefficient tables, but we'll find out (the hard way)!
    PIPELINE_METHODS = ['stop', 'get_tag', 'set_tag', 'cget_tag', 'cset_tag',
                        'trigger', 'set_coefficients']

    def __init__(self, process, circuit_name, device_name):
        self.process = process
        self.device_name = device_name
        self.name = circuit_name

    def get_buffer(self, name, *args, **kwargs):
        return self.process.get_buffer(self.device_name, name, *args, **kwargs)

    def __getattr__(self, name):
        '''
        This is just wraps up the method call into an object that can be sent
        via the queue to the other process.
        '''
        if name in self.PIPELINE_METHODS:
            return partial(self.process._get_response, self.device_name,
                           name, 5)
