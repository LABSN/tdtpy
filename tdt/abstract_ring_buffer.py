import logging
log = logging.getLogger(__name__)


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
    total_samples_written = 0
    total_samples_read = 0

    # Note that read_index and write_index may be overriden as property
    # getter/setters in subclasses.
    read_index = 0
    write_index = 0

    def pending(self):
        '''
        Number of filled slots waiting to be read
        '''
        return pending(self.read_index, self.write_index, self.size)

    def blocks_pending(self):
        '''
        Number of filled slots waiting to be read
        '''
        return int(self.pending()/self.block_size)*self.block_size

    def available(self):
        '''
        Number of empty slots available for writing
        '''
        return self.size-self.pending()

    def blocks_available(self):
        return int(self.available()/self.block_size)*self.block_size

    def read_all(self):
        return self.read(self.pending())

    def read(self, samples=None):
        if samples is None:
            samples = self.blocks_pending()
        elif samples > self.pending():
            mesg = 'Attempt to read %r samples failed because only ' + \
                   '%r slots are available for read'
            raise ValueError(mesg % (samples, self.pending()))

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
            mesg = 'Attempt to write %d samples failed because only ' + \
                   '%d slots are available for write'
            raise ValueError(mesg % (samples, available))

        samples_written = 0
        for o, l in wrap(samples, self.write_index, self.size):
            if not self._write(o, data[...,
                                       samples_written:samples_written+l]):
                raise SystemError('Problem with writing data to buffer')
            samples_written += l
        self.write_index = (o+l) % self.size
        self.total_samples_written += samples_written
        return samples_written

    def reset_read(self, index=None):
        '''
        Reset the read index
        '''
        if index is None:
            index = self._iface.GetTagVal(self.idx_tag)
        self.read_index = index
