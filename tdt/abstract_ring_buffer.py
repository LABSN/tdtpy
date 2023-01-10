import logging
log = logging.getLogger(__name__)


def wrap(length, offset, buffer_size):
    if (offset+length) > buffer_size:
        a_length = buffer_size-offset
        b_length = length-a_length
        return ((offset, a_length), (0, b_length))
    else:
        return ((offset, length), )


def span(old_cycle, old_idx, new_cycle, new_idx, buffer_size):
    '''
    Returns the number of slots between new_idx and old_idx given buffer size.
    '''
    start = int((old_cycle * buffer_size) + old_idx)
    end = int((new_cycle * buffer_size) + new_idx)
    if (start > end):
        log.info('Start sample %d (C %d, I %d), end sample %d (C %d, I %d), buffer %d',
                 start, old_cycle, old_idx, end, new_cycle, new_idx, buffer_size)
        raise ValueError('Start sample higher than end sample')
    if (end - start) > buffer_size:
        raise ValueError('Number of slots exceeds buffer size')
    return end-start


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
    '''
    # This should be write_cycle * size + write_index
    total_samples_written = 0

    # This should be read_cycle * size + read_index
    total_samples_read = 0

    # This tracks the current index in the buffer. The read_index and
    # write_index may be overriden as property getter/setters in subclasses.
    read_index = 0
    write_index = 0

    # This tracks the current "loop" of the buffer. The read_cycle and
    # write_cycle may be overridden as property getter/setters in subclasses.
    read_cycle = 0
    write_cycle = 0

    def _offset_to_index(self, offset):
        if offset is None:
            offset = self.total_samples_written
        write_cycle, write_index = divmod(offset, self.size)
        log.debug('Offset %d is at cycle %d, index %d', offset, write_cycle,
                  write_index)
        log.debug('Current offset is cycle %d, index %d', self.write_cycle,
                  self.write_index)
        if self.write_cycle < write_cycle:
            raise ValueError('Offset too far back in time')
        return write_cycle, write_index

    def pending(self):
        '''
        Number of filled slots waiting to be read
        '''
        return span(self.read_cycle, self.read_index, self.write_cycle,
                       self.write_index, self.size)

    def blocks_pending(self):
        '''
        Number of filled blocks waiting to be read
        '''
        return int(self.pending()/self.block_size)*self.block_size

    def available(self, offset=None):
        '''
        Number of empty slots available for writing

        Parameters
        ----------
        offset : {None, int}
            If specified, return number of samples relative to offset. Offset
            is relative to beginning of acquisition.
        '''
        write_cycle, write_index = self._offset_to_index(offset)
        if (self.total_samples_written == 0) and (self.read_index == 0):
            return self.size
        log.debug('Available: write cycle %d index %d, '
                  'read cycle %d index %d, size %d',
                  write_cycle, write_index, self.read_cycle, self.read_index,
                  self.size)
        return self.size - \
            span(self.read_cycle, self.read_index,
                    write_cycle, write_index, self.size)

    def blocks_available(self):
        return int(self.available()/self.block_size)*self.block_size

    def read_all(self):
        return self.read(self.pending())

    def read(self, samples=None):
        try:
            if samples is None:
                samples = self.blocks_pending()
            elif samples > self.pending():
                mesg = 'Attempt to read %r samples failed because only ' + \
                    '%r slots are available for read'
                raise ValueError(mesg % (samples, self.pending()))
        except ValueError:
            raise IOError('Read was too slow and unread samples were overwritten')

        data = self._get_empty_array(samples)
        samples_read = 0
        for i, (o, l) in enumerate(wrap(samples, self.read_index, self.size)):
            data[..., samples_read:samples_read+l] = self._read(o, l)
            samples_read += l
            if i > 0:
                self.read_cycle += 1

        self.read_index = (o+l) % self.size
        self.total_samples_read += samples_read
        return data

    def write(self, data, offset=None):
        write_cycle, write_index = self._offset_to_index(offset)
        try:
            available = self.available(offset)
        except ValueError:
            raise IOError('Write was too slow and old samples were regenerated')
        samples = data.shape[-1]
        log.debug('Current write cycle %d and index %d', self.write_cycle,
                  self.write_index)
        log.debug('%d samples available for write starting at %d', available,
                  samples)

        if samples == 0:
            return
        elif samples > available:
            mesg = 'Attempt to write %d samples failed because only ' + \
                   '%d slots are available for write'
            raise ValueError(mesg % (samples, available))

        samples_written = 0
        for i, (o, l) in enumerate(wrap(samples, write_index, self.size)):
            lb = samples_written
            ub = samples_written + l
            if not self._write(o, data[..., lb:ub]):
                raise SystemError('Problem with writing data to buffer')
            samples_written += l

        if offset is not None:
            self.total_samples_written = offset + samples_written
        else:
            self.total_samples_written += samples_written
        self.write_cycle, self.write_index = \
            divmod(self.total_samples_written, self.size)
        log.debug('Write %s samples. Write pointer at %d cycles, %d index.',
                  samples_written, self.write_cycle, self.write_index)
        return samples_written

    def reset_read(self, index=None):
        '''
        Reset the read index
        '''
        if index is None:
            index = self._iface.GetTagVal(self.idx_tag)
        self.read_index = index
