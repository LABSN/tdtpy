import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

import threading, multiprocessing, time
import numpy as np

from util import dtype_to_type_str, best_sf, resolution
from dsp_error import DSPError

class DSPBuffer(object):

    def __init__(self, circuit, data_tag, idx_tag=None, size_tag=None,
            sf_tag=None, cycle_tag=None, dec_tag=None, block_size=4096,
            src_type='float32', dest_type='float32', channels=1):
        '''
        In addition to the required tag, takes a number of supporting tags

        For consistency, give the supporting tags the same name as the data tag
        plus a prefix indicating their purpose:

            i
                index tag (idx_tag)
            n
                size tag (size_tag)
            sf
                scaling factor tag (sf_tag)
            c
                cycle tag (cycle_tag)
            d
                downsampling tag (dec_tag)

        For all tags, if no value is provided, the default extension is added to
        the value for the data_tag and the circuit is checked to see if the tag
        exists.  If it exists, it is used.  For example, if you have `spikes`,
        `spikes_i`, and `spikes_n` tags in your RPvds construct, you can simply
        initialize the class by passing only the name of the data tag (`spikes`)
        and it will automatically use `spikes_i` and `spikes_n` as the index and
        size tags, respectively.

        If a required tag cannot be found, an error is raised.

        Tags
        ----
        data_tag : string (required)
            Tag to read data from
        idx_tag : defaults to data_tag_i (required)
            Tag indicating current index of buffer.  For buffer reads this tag
            serves as a "handshake" (i.e. when the index changes, new data is
            available).
        size_tag : defaults to data_tag_n (optional)
            Tag indicating current size of buffer.
        sf_tag : defaults to data_tag_sf (optional)
            Tag indicating scaling factor applied to data before it is stored in
            the buffer.  
        cycle_tag : defaults to data_tag_c (optional)
            Tag indicating number of times buffer has wrapped around to
            beginning.  Used to ensure no data is lost.
        dec_tag : defaults to data_tag_d (optional)
            Tag indicating decimation factor.  Used to compute sampling
            frequency of data stored in buffer: e.g. if circuit runs at 100 kHz,
            but you only sample every 25 cycles, the actual sampling frequency
            is 4 kHz.  
            
        Parameters
        ----------
        circuit
            Circuit object buffer is attached to
        block_size : int
            Coerce data read/write to multiple of the block size.  Must be a
            multiple of the channel number.
        src_type :
            Type of data in buffer (can be a string or numpy dtype).  Valid data
            formats are float32, int32, int16 and int8.
        dest_type :
            Type to convert data to
        channels :
            Number of channels stored in buffer
        '''
        if data_tag not in circuit.tags:
            mesg = "%s: Does not have data tag %s" % (circuit, data_tag)
            raise ValueError, mesg

        self.circuit = circuit
        self._iface = circuit._iface
        self.data_tag = data_tag
        self.size_tag = size_tag
        self.channels = channels
        self.cycle = 0
        self.written = 0

        self.block_size = int(block_size)

        if size_tag is None:
            tag = data_tag + '_n'
            if tag in circuit.tags:
                size_tag = tag
                log.debug("%s: found size_tag %s", self, self.size_tag)
        elif size_tag not in circuit.tags:
            raise ValueError, "size_tag not found in circuit"
        self.size_tag = size_tag

        if idx_tag is None:
            idx_tag = data_tag + '_i'
            log.debug("%s: attempting to find idx_tag %s", self, idx_tag)
        if idx_tag not in circuit.tags:
            raise ValueError, "Index tag must be present in circuit"
        self.idx_tag = idx_tag

        # Determine scaling factor if the scaling_factor tag is available
        if sf_tag is None:
            tag = data_tag + '_sf'
            if tag in circuit.tags:
                sf_tag = tag
                log.debug("%s: found sf_tag %s", self, sf_tag)
        self.sf_tag = sf_tag
        if self.sf_tag is not None:
            self.sf = self._iface.GetTagVal(self.sf_tag)
            log.debug("%s: scaling factor is %d", self, self.sf)
        else:
            self.sf = 1
            log.debug("%s: no scaling factor found, using default", self)

        if cycle_tag is None:
            tag = data_tag + '_c'
            if tag in circuit.tags:
                cycle_tag = tag
                log.debug("%s: found cycle_tag %s", self, cycle_tag)
            else:
                log.debug("%s: no cycle tag found", self)
        self.cycle_tag = cycle_tag

        # Compute sampling frequency of data stored in buffer given the
        # decimation factor
        if dec_tag is None:
            tag = data_tag + '_d'
            if tag in circuit.tags:
                dec_tag = tag
                log.debug("%s: found dec_tag %s", self, dec_tag)
        self.dec_tag = dec_tag
        if self.dec_tag is not None:
            self.dec_factor = self._iface.GetTagVal(self.dec_tag)
            self.fs = circuit.fs/float(self.dec_factor)
        else:
            self.dec_factor = 1
            self.fs = circuit.fs
        log.debug("%s: decimation factor is %d", self, self.dec_factor)

        # Numpy's dtype function is quite powerful and accepts a variety of
        # strings as well as other dtype objects and returns the right answer.
        self.src_type = np.dtype(src_type)
        self.dest_type = np.dtype(dest_type)

        # Number of samples compressed into a single slot.  The RPvds works with
        # 32 bit words.  If we are compressing our data, calculate the number of
        # samples that are compressed into a single 32 bit word.  If src_type is
        # int8, we know we are compressing 4 samples into a single 32 bit (4
        # byte) word.
        self.compression = int(4/np.nbytes[self.src_type])

        # Query buffer for it's size in terms of slots, samples and samples per
        # channel
        self._update_size()

        # Convert our preferred representation for the data type to TDT's
        # preferred representation for the data type.
        self.vex_src_type = dtype_to_type_str(self.src_type)
        self.vex_dest_type = dtype_to_type_str(self.dest_type)

        try:
            self.resolution = resolution(self.src_type, self.sf)
        except:
            # Does the logic change if sf is not 1?  We should never see this
            # use-case but let's add a check for safety.
            if self.sf != 1:
                raise ValueError, "FIXME"
            self.resolution = np.finfo(self.src_type).resolution

        # The number of slots in the buffer must be a multiple of channel
        # number, otherwise data will be lost.  This is a requirement of the
        # RPvds circuit, so let's check to make sure this requirement is met as
        # it is a very common mistake to make.
        if (self.n_slots % self.channels) != 0:
            mesg = 'Buffer size must be a multiple of the channel number'
            raise DSPError(self, mesg)

        # Spit out debugging information
        debug = ['data_tag', 'idx_tag', 'size_tag', 'sf_tag', 'cycle_tag',
                 'dec_tag', 'src_type', 'dest_type', 'compression',
                 'resolution', 'sf', 'dec_factor', 'fs', 'n_slots', 'n_samples',
                 'size', 'n_slots_max', 'n_samples_max', 'size_max', 'channels',
                 'block_size']
        attrs = ['{0}: {1}'.format(attr, getattr(self, attr)) for attr in debug]
        log.info('Initialized %s: %s', self, ', '.join(attrs))

    def __getstate__(self):
        '''
        Provides support for pickling, which is required by the multiprocessing
        module for launching a new process.  _iface is a PyIDispatch object,
        which does not support pickling, so we just delete them and pickle the
        rest.
        '''
        state = self.__dict__.copy()
        del state['_iface']
        return state

    def __setstate__(self, state):
        '''
        Loads the state and reconnects the COM objects
        '''
        self.__dict__.update(state)
        self._iface = self.circuit._iface

    def _wrap(self, length):
        return wrap(length, self.index, self.size)

    def read(self, size=None):
        # TODO: This function may be better written as a generator.  See if this
        # is a bottleneck.
        if size is None:
            size = self.pending()

        data = [self._read(o, l) for o, l in self._wrap(size)]

        old_idx = self.index
        old_cyc = self.cycle
        if old_cyc == -1:
            old_cyc = 0

        self.index = o+l
        # If offset is 0, that means we've wrapped around to the beginning.
        # Note that the very first call to read will have an offset of 0, so
        # this will increment the cycle.
        if size != 0 and o == 0:
            self.cycle += 1

        # Check to see whether data might have been lost.  Since it's
        # possible for additional data to be written to the buffer in the
        # interval between getting the number of pending samples and
        # actually reading the data, I like to take a conservative approach
        # and use the cycle and index prior to the read for the check.
        if self.cycle_tag is not None:
            log.debug("%s: overflow check with cycle %d and index %d", self,
                     old_cyc, old_idx)
            if old_idx < self.get_index() and old_cyc < self.get_cycle():
                mesg = "Buffer overflow, data has been lost"
                raise DSPError(self, mesg)
        
        return np.concatenate(data, axis=1)

    def _read(self, offset, length):
        log.debug("%s: read offset %d, read size %d", self, offset, length)

        if length == 0:
            data = np.array([], dtype=self.dest_type)
            return data.reshape((self.channels, -1))

        # At this point, we have already done the necessary computation of
        # offset and read (via get_index and pending), so all we have to do is
        # pass those values directly to the ReadTagVEX function.
        data = self._iface.ReadTagVEX(self.data_tag, offset, length,
                self.vex_src_type, self.vex_dest_type, self.channels)
        log.debug("%s: recieved data of type %r", self, type(data[0]))
        return np.divide(data, self.sf).astype(self.dest_type)
        
    def write(self, data):
        size = len(data)
        log.debug("%s: writing %d samples", self, size)
        if size == 0:
            return
        if size > self.size:
            mesg = 'An attempt to write %d samples to %s failed because ' + \
                   'it is greater than the size of the buffer.'
            raise ValueError, mesg % (size, self)

        num_written = 0
        for o, l in self._wrap(size):
            log.debug("%s: write %d samples starting at %d", self, l, o)
            if not self._write(o, data[num_written:num_written+l]):
                raise SystemError, 'Problem with writing data to buffer'
            num_written += l
        self.index = (self.index+num_written) % self.size
        self.written += num_written
        return num_written

    def _write(self, offset, data):
        return self._iface.WriteTagV(self.data_tag, offset, data)

    def get_index(self):
        index = self._iface.GetTagVal(self.idx_tag)
        return index * self.compression / self.channels

    def get_cycle(self):
        '''
        The way the cycle is structured, it is 1-based (i.e. when the circuit
        first starts, the cycle is 1.  After wrapping around the first time, it
        is 2 and so on.
        '''
        cycle = self._iface.GetTagVal(self.cycle_tag)-1 
        log.debug("%s: cycle %d", self, cycle)
        return cycle

    def pending(self):
        '''
        Returns the number of slots that have been filled with data since the
        last read.
        '''
        old_idx = self.index
        new_idx = self.get_index()
        if new_idx < old_idx:
            size = self.size-old_idx+new_idx
        else:
            size = new_idx-old_idx
        log.debug("%s: %d samples per channel pending", self, size)
        return np.floor(size/self.block_size)*self.block_size

    def _update_size(self):
        '''
        Query current state of buffer (size and current index).  If data
        compression is being used, multiple samples can fit into a single slot
        of a RPvds buffer.  We want the index and size attributes to accurately
        reflect the number of samples per channel in the buffer, not the number
        of slots.
        
        For example, assume I am storing 16 channels in a buffer with two
        samples compressed into each slot.  After the DSP clock has counted 10
        samples, 10 samples per channel will have been stored for a total of 160
        samples.  However, only 80 slots will have been filled.  

        n_slots
            number of slots in buffer
        n_samples
            number of samples in buffer
        size
            number of samples per channel
        '''
        # update index
        slot_index = int(self._iface.GetTagVal(self.idx_tag))
        sample_index = slot_index * self.compression
        self.index = sample_index / self.channels

        # update size
        self.n_slots_max = self._iface.GetTagSize(self.data_tag)
        if self.size_tag is not None:
            self.n_slots = self._iface.GetTagVal(self.size_tag)
        else:
            self.n_slots = self.n_slots_max
            log.debug("%s: no size tag available, using GetTagSize", self)

        self.n_samples = self.n_slots * self.compression
        self.n_samples_max = self.n_slots_max * self.compression
        self.size = self.n_samples / self.channels
        self.size_max = self.n_samples_max / self.channels

    def set(self, data):
        '''Assumes data is written starting at the first index of the buffer.'''
        data = np.asarray(data)
        size = data.shape[-1]
        if size > self.size_max:
            mesg = "cannot write %d samples to buffer" % size
            raise DSPError(self, mesg)
        if self.size_tag is not None:
            self._iface.SetTagVal(self.size_tag, size)
            self._update_size()
        elif size != self.size:
            mesg = "buffer size cannot be configured"
            raise DSPError(self, mesg)

        #if not self._iface.WriteTagVEX(self.data_tag, 0, 'F32', data):
        if self.vex_src_type != 'F32':
            raise NotImplementedError
        if not self._iface.WriteTagV(self.data_tag, 0, data):
            raise DSPError(self, "write failed")
        log.debug("%s: set buffer with %d samples", self, size)
        self.written += size

    def __len__(self):
        return self.size

    def __str__(self):
        return "{0}:{1}".format(self.circuit, self.data_tag)

    def __repr__(self):
        return "<{0}:{1}:{2}:{3}>".format(self.circuit, self.data_tag,
                self.index, self.size)
