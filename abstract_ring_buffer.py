import numpy as np

def wrap(length, offset, buffer_size):
    if (offset+length) > buffer_size:
        a_length = buffer_size-offset
        b_length = length-a_length
        return ((offset, a_length), (0, b_length))
    else:
        return ((offset, length), )

def pending(old_idx, new_idx, buffer_size):
    '''
    Returns the number of slots that have been filled with data since the
    last read.
    '''
    if new_idx < old_idx:
        return buffer_size-old_idx+new_idx
    else:
        return new_idx-old_idx

class AbstractRingBuffer(object):
    '''
    Subclasses must provide the following attributes (either by setting them in
    the __init__ method or providing property getter/setters):

        * read_index
        * write_index
        * size
        * channels
        * block_size

    Also, provide implementation of the following methods:
        * _read(self, offset, length)
        * _write(self, offset, data)

    The following attributes provide information on the state of the buffer:
        * total_samples_written
        * total_samples_read

    TODO:
        * write_cycle
        * read_cycle

    '''
    total_samples_written   = 0
    total_samples_read      = 0

    # Note that read_index and write_index may be overriden as property
    # getter/setters in subclasses.
    read_index              = 0
    write_index             = 0

    def pending(self):
        '''
        Number of filled slots waiting to be read
        '''
        samples = pending(self.read_index, self.write_index, self.size)
        return int(samples/self.block_size)*self.block_size

    def available(self):
        '''
        Number of empty slots available for writing
        '''
        return self.size-self.pending()

    def read(self, samples=None):
        pending = self.pending()
        if samples is None:
            samples = pending
        elif samples > pending:
            mesg = 'Attempt to read %d samples failed because only' + \
                   '%d slots are available for read'
            raise ValueError, mesg % (samples, pending)

        data = self._get_empty_array(samples)
        samples_read = 0
        for o, l in wrap(samples, self.read_index, self.size):
            data[..., samples_read:samples_read+l] = self._read(o, l)
            samples_read += l
        self.read_index = (o+l) % self.size 
        self.total_samples_read += samples_read
        return data

    def write(self, data, force=False):
        available = self.available()
        samples = data.shape[-1]
        if samples == 0:
            return
        elif not force and (samples > available):
            mesg = 'Attempt to write %d samples failed because only' + \
                   '%d slots are available for write'
            raise ValueError, mesg % (samples, available)

        samples_written = 0
        for o, l in wrap(samples, self.write_index, self.size):
            if not self._write(o, data[..., samples_written:samples_written+l]):
                raise SystemError, 'Problem with writing data to buffer'
            samples_written += l
        self.write_index = (o+l) % self.size 
        self.total_samples_written += samples_written
        return samples_written
