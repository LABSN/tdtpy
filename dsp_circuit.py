import atexit
import numpy as np

from util import get_cof_path, connect_zbus, connect
from dsp_buffer import ReadableDSPBuffer, WriteableDSPBuffer
from convert import convert
from dsp_error import DSPError

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARN)

# There are apparently two more possible return values: 74 and 78.  It's not
# clear what these represent. 
rpcox_types = {
        65:     object,         # Undefined type
        68:     np.ndarray,     # Data buffer
        73:     int,
        83:     float,
        80:     np.ndarray,     # Coefficient buffer
        76:     bool,
        }

# Eventually I'd like to bind the device-specific variables as "constants" on
# the correct DSPCircuit so people can leverage these in their programs rather
# than having to look up the correct channel.  However, we need to compile a
# list of all the necessary module-level variables first.
RX6_DEFAULTS = {
        'DAC_CHANNEL_1':    1,
        'DAC_CHANNEL_2':    2,
        'ADC_CHANNEL_1':    128,
        'ADC_CHANNEL_2':    129,
        }

class DSPCircuit(object):

    def __init__(self, circuit_name, device, load=True):
        self.device = device
        self.circuit_name = circuit_name
        # _iface is the same COM object a Matlab user typically works with when
        # they call actxserver('RPco.X').  It supports the exact same methods as
        # the Matlab version.
        self._iface = connect(device)
        self._zbus  = connect_zbus()
        self._cof_path = get_cof_path(circuit_name)
        if load:
            self.load()
            import atexit
            atexit.register(self.stop)
        else:
            self.read()
        self.inspect()

    def __getstate__(self):
        '''
        Provides support for pickling, which is required by the multiprocessing
        module for launching a new process.  _iface and _zbus are PyIDispatch
        objects which do not support pickling, so we just delete them and pickle
        the rest.
        '''
        state = self.__dict__.copy()
        del state['_iface']
        del state['_zbus']
        return state

    def __setstate__(self, state):
        '''
        Loads the state and reconnects the COM objects
        '''
        self.__dict__.update(state)
        self._iface = connect(self.device)
        self._zbus  = connect_zbus()
        self.read()

    def read(self):
        if not self._iface.ReadCOF(self._cof_path):
            mesg = "Unable to read %s" % self._cof_path
            raise DSPError(self, mesg)

    def load(self):
        '''
        Clear DSP RAM set all variables to default value

        The circuit is reloaded from disk, so any recent edits to the circuit
        will be reflected in the running program.
        '''
        # Note that ClearCOF alone does not apear to reset all variables to
        # default value, so we reload the circuit as well.
        if not self._iface.ClearCOF():
            mesg = "Unable to clear %s buffers" % self
            raise DSPError(self, mesg)
        if not self._iface.LoadCOF(self._cof_path):
            mesg = 'Unable to load %s' % self._cof_path
            raise DSPError(self, mesg)
        log.info("Reloaded %s", self)
        self.trigger('A', 'low')
        self.trigger('B', 'low')

    def inspect(self):
        '''
        Determine what tags are available in the microcode
        '''
        # Inspect COF for available tags and their type/size
        num_tags = self._iface.GetNumOf('ParTag')
        self.tags = {}
        for i in range(num_tags):
            name = self._iface.GetNameOf('ParTag', i+1)
            if not name.startswith('%'):
                tag_size = self._iface.GetTagSize(name)
                if tag_size == 0:
                    mesg = "Attempted to initialize invalid tag %s" % name
                    raise DSPError(self, mesg)
                tag_type = self._iface.GetTagType(name)
                self.tags[name] = (tag_size, rpcox_types[tag_type])
                log.info("%s: found %s (size %d, type %s)", self, name,
                          tag_size, tag_type)
        self.fs = self._iface.GetSFreq()

    def cget_tag(self, name, tag_unit, val_unit):
        '''
        Enhanced version of `get_tag` that returns value in requested unit

        Parameters
        ----------
        name : str
            Tag name
        tag_unit : str
            Unit of tag
        val_unit : str
            Requested unit
        '''
        value = self.get_tag(name)
        return convert(tag_unit, val_unit, value, self.fs)

    def cset_tag(self, name, value, val_unit, tag_unit):
        '''
        Enhanced version of `set_tag` that converts the value before setting

        Parameters
        ----------
        name : str
            Tag name
        val_unit : str
            Requested unit
        tag_unit : str
            Unit of tag
        '''
        value = convert(val_unit, tag_unit, value, self.fs)
        self.set_tag(name, value)

    def get_tag(self, name):
        '''
        Analogue of RPco.X.GetTagVal
        '''
        # Check to see if tag exists
        if name not in self.tags:
            raise DSPError(self, "Tag %s does not exist" % name)
        if self.tags[name][0] != 1:
            raise DSPError(self, "Tag %s is not a scalar value" % name)
        value = self._iface.GetTagVal(name)
        log.debug("Get %s:%s is %r", self, name, value)
        return value

    def set_tag(self, name, value):
        '''
        Analogue of RPco.X.SetTagVal
        '''
        # Check to see if tag exists
        if name not in self.tags:
            raise DSPError(self, "Tag %s does not exist" % name)
        if self.tags[name][0] != 1:
            raise DSPError(self, "Tag %s is not a scalar value" % name)
        if not self._iface.SetTagVal(name, value):
            mesg = "Unable to set tag %s to %r" % (name, value)
            raise DSPError(self, mesg)
        log.info("Set %s:%s to %r", self, name, value)

    def start(self):
        '''
        Analogue of RPco.X.Run
        '''
        log.debug("starting %s", self)
        self._iface.Run()

    def stop(self):
        '''
        Analogue of RPco.X.Halt
        '''
        log.debug("stopping %s", self)
        self._iface.Halt()

    def trigger(self, trigger, mode='pulse'):
        # Convert mode string to the corresponding integer
        mode_enum = dict(pulse=0, high=1, low=2)
        if trigger == 'A':
            self._zbus.zBusTrigA(0, mode_enum[mode], 10)
        elif trigger == 'B':
            self._zbus.zBusTrigB(0, mode_enum[mode], 10)
        elif (1 <= trigger < 10) and mode == 'pulse':
            self._iface.SoftTrg(trigger)
        else:
            raise ValueError("Unsupported trigger mode %s %s", trigger, mode)
        log.info('Trigger %r %s', trigger, mode)

    def get_buffer(self, data_tag, mode, *args, **kw):
        if mode == 'w':
            return WriteableDSPBuffer(self, data_tag, *args, **kw)
        elif mode == 'r':
            return ReadableDSPBuffer(self, data_tag, *args, **kw)

    def __str__(self):
        return "{0}:{1}".format(self.device, self.circuit_name)
