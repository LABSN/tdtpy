from abstract_ring_buffer import AbstractRingBuffer

class SharedRingBuffer(AbstractRingBuffer):
    '''
    Implementation that reads/writes data to a shared memory location.  Used for
    inter-process communication.  The assumption is one process only reads and
    the other process only writes.  Does not support single-write, multi-read
    (i.e. only one process can do the reading).

    Cache *must* be a view into a Numpy array.  use shmem_to_ndarray and reshape

    TODO:
        enforce directionality (i.e. you must read from one process, write from
        the other, you cannot do both)
    '''

    def __init__(self, cache, iwrite, iread):
        self._iwrite = iwrite
        self._iread = iread
        self._cache = cache
        self.channels, self.size = self._cache.shape
        self.block_size = 1

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
        return self._cache[...,offset:offset+length]

    def _write(self, offset, data):
        samples = data.shape[-1]
        self._cache[..., offset:offset+samples] = data
        return samples

class ReadableSharedRingBuffer(SharedRingBuffer):

    def _write(self, offset, data):
        raise NotImplementedError

class WriteableSharedRingBuffer(SharedRingBuffer):

    def _read(self, offset, data):
        raise NotImplementedError
