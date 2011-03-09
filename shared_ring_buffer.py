from abstract_ring_buffer import AbstractRingBuffer

class SharedRingBuffer(AbstractRingBuffer):
    '''
    Implementation that reads/writes data to a shared memory location.  Used for
    inter-process communication.  The assumption is one process only reads and
    the other process only writes.  Does not support single-write, multi-read
    (i.e. only one process can do the reading).

    Cache *must* be a view into a Numpy array.  use shmem_to_ndarray and reshape
    '''

    def __init__(self, cache, iwrite, iread, ioffset, lock, circuit):
        self._ioffset = ioffset
        self._iwrite = iwrite
        self._iread = iread
        self._cache = cache
        self._lock = lock
        self._circuit = circuit
        self.channels, self.size = self._cache.shape
        self.block_size = 1

        self._ioffset.value = -1
        self._iwrite.value = 0
        self._iread.value = 0

    def _get_read_index(self):
        return self._iread.value

    def _set_read_index(self, value):
        self._iread.value = int(value)

    read_index = property(_get_read_index, _set_read_index)

    def _get_write_index(self):
        return self._iwrite.value

    def _set_write_index(self, value):
        self._iwrite.value = int(value)

    write_index = property(_get_write_index, _set_write_index)

    def _read(self, offset, length):
        return self._cache[..., offset:offset+length]

    def _write(self, offset, data):
        samples = data.shape[-1]
        self._cache[..., offset:offset+samples] = data
        return samples

    def should_set(self):
        return self._ioffset.value >= 0

    # Read and write should be locked to prevent concurrent access by the two
    # proceses.  Even though one process is read-only and the other is
    # write-only, I haven't had a chance to rigorously debug what happens if we
    # don't lock access to the read/write.  The lock should be a re-entrant
    # lock.  Since set() acquires a lock and then calls write(), this allows
    # write() to acquire the same lock as well.  A simple, non-reentrant lock
    # would prevent write() from acquiring lock().
    def read(self, samples=None):
        with self._lock:
            return super(SharedRingBuffer, self).read(samples)

    def write(self, data):
        with self._lock:
            return super(SharedRingBuffer, self).write(data)

    # Locking is very important here because we need to ensure that both
    # _ioffset and the data are written before the other process has access to
    # it.
    def set(self, data):
        with self._lock:
            self._ioffset.value = 0
            self.write(data)

    def clear(self):
        with self._lock:
            self._circuit.clear_buffer(self.data_tag)

class ReadableSharedRingBuffer(SharedRingBuffer):

    def _write(self, offset, data):
        raise NotImplementedError

class WriteableSharedRingBuffer(SharedRingBuffer):

    def _read(self, offset, data):
        raise NotImplementedError
