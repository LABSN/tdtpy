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

def monitor(circuit, buffer_info, poll_period, pipe):
    '''
    Monitor loop that will be run in the subprocess.  
    '''

    def process_request(pipe, circuit, timeout):
        # Check to see if data is available.  Keep checking until the timeout period
        # is over.
        if pipe.poll(timeout):
            id, request, args = pipe.recv()
            # Process the request
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

    # Initialize the buffers.  We do not currently support read/write buffers.
    # You must specify whether the buffer is open for read or write.
    read_buffers, write_buffers = [], []
    for buffer_name, mode, args, kwargs, shmem, iwrite, iread in buffer_info:
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
    circuit.start()

    # Start the loop
    while True:
        start = time.time()
        for hw_buffer, sw_buffer in read_buffers:
            # Since downloading buffer data can be a bit slow, let's check in
            # between downloads to see if we need to process any other requests
            # (i.e. set_tag and get_tag).
            process_request(pipe, circuit, 0)
            read_buffer(hw_buffer, sw_buffer)

        for hw_buffer, sw_buffer in write_buffers:
            process_request(pipe, circuit, 0)
            write_buffer(hw_buffer, sw_buffer)

        # Now that we're done polling the buffers, check to see how much time
        # has elapsed.  If all tasks were completed before the buffer poll
        # period has expired, shift task to checking request queue.
        while True:
            elapsed = time.time()-start
            if elapsed >= poll_period:
                break
            process_request(pipe, circuit, poll_period-elapsed)

class DSPProcess(mp.Process):
    '''
    This is a duck-typed class meant to support the methods available on
    DSPCircuit.  It does not subclass DSPCircuit, but supports all the key
    methods you need (e.g. get_tag, set_tag, get_buffer).

    The only key difference is that you must ensure that shared memory for the
    process is allocated before you start it.  This means you must call
    `get_buffer` prior to calling `start`.  This is, in general, good practice
    anyway.
    '''

    def __init__(self, circuit_name, device_name, poll_period=0.1,
                 cache_duration=30):
        # We need to open the circuit so we can figure out how much shared
        # memory we need for the buffers.
        self.circuit = DSPCircuit(circuit_name, device_name)
        self.cache_duration = cache_duration
        self.poll_period = poll_period
        self.fs = self.circuit.fs

        # Shared information
        self._shared_buffer_data = []
        self._parent_pipe, self._child_pipe = mp.Pipe()
        self._request_id = itertools.count()

        import atexit
        atexit.register(self.terminate)

        super(DSPProcess, self).__init__(target=monitor)

    def start_dummy(self):
        monitor(self.circuit, self._shared_buffer_data, self.poll_period,
                self._child_pipe)

    def run(self):
        monitor(self.circuit, self._shared_buffer_data, self.poll_period,
                self._child_pipe)

    def _get_response(self, request, args=None, timeout=None):
        '''
        Passes along request to the other process and waits for a response.
        '''
        # Generate a unique ID that ensures that the other process is responding
        # to the correct item
        if args is None:
            args = ()
        id = self._request_id.next()
        # Send the request to the process via a queue
        self._parent_pipe.send((id, request, args))
        # Wait till the response is available.  If no response is recieved after
        # one second, raise an exception.
        if not self._parent_pipe.poll(timeout):
            mesg = "No response recieved for request %s(%r)" % (request, args)
            raise IOError, mesg
        # Get the response
        id, response = self._parent_pipe.recv()
        # Make sure it's the right response (this is probably an unecessary
        # check sinc we are blocking)
        if id != id:
            raise IOException, "Wrong response returned"
        return response

    def get_buffer(self, buffer_name, mode, *args, **kwargs):
        if self.is_alive():
            mesg = "Cannot allocate memory for buffer cache once process" + \
                   "has started"
            raise SystemError, mesg
        # Compute how much shared memory we need to allocate for the cache.  We
        # load the buffer in the parent process so we can inspect the circuit
        # and determine whether there are any pre-defined tags.
        buffer = self.circuit.get_buffer(buffer_name, mode, *args, **kwargs)
        cache_size = int(buffer.fs*self.cache_duration)*buffer.channels
        mem_type = NP_TO_CTYPES[buffer.dest_type]

        # Allocate the cache memory and create shared values used for
        # inter-process communication
        shmem = mp.RawArray(mem_type, cache_size) 
        iwrite = mp.RawValue(ctypes.c_uint)
        iread = mp.RawValue(ctypes.c_uint)

        data = (buffer_name, mode, args, kwargs, shmem, iwrite, iread)
        self._shared_buffer_data.append(data)
        cache = shmem_as_ndarray(shmem).reshape((buffer.channels, -1))
        if mode == 'r':
            sh_buffer = ReadableSharedRingBuffer(cache, iwrite, iread)
        elif mode == 'w':
            sh_buffer = WriteableSharedRingBuffer(cache, iwrite, iread)

        # Copy the attributes over from the actual buffer to the shared buffer
        # so we have access to the metadata we need
        for k, v in buffer.attributes().items():
            setattr(sh_buffer, k, v)
        return sh_buffer

    def get_tag(self, name):
        return self._get_response('get_tag', (name,))

    def set_tag(self, name, value):
        return self._get_response('set_tag', (name, value))

    def cget_tag(self, name, tag_unit, val_unit):
        return self._get_response('cget_tag', (name, tag_unit, val_unit))

    def cset_tag(self, name, value, val_unit, tag_unit):
        return self._get_response('cset_tag', (name, value, tag_unit, val_unit))

    def _read(self, offset, length):
        return self._sh_cache[:,offset:offset+length]

    def trigger(self, trigger, mode='pulse'):
        return self._get_response('trigger', (trigger, mode))

    def start(self):
        super(DSPProcess, self).start()
        # We set timeout for start to longer than the default because it takes a
        # bit of time for the circuit to load and intialize.  Let's be patient.
        return self._get_response('start', timeout=None)

    def stop(self):
        return self._get_response('stop')
