from os.path import abspath, split
import atexit
import numpy as np
import time

from .util import get_cof_path, connect_zbus, connect_rpcox
from .dsp_buffer import ReadableDSPBuffer, WriteableDSPBuffer
from .convert import convert
from .dsp_error import DSPError
from .constants import RCX_COEFFICIENT, RCX_CAST, RCX_STATUS_BITMASK

import logging
log = logging.getLogger(__name__)


class DSPCircuit(object):
    '''
    Wrapper around the TDT ActiveX object, RPCo.X.

    Provides several stringent checks and convenience methods to minimize
    programming errors and typos.

    circuit_name : string
        Path to circuit file.
    device_name : string
        Device to load circuit to.
    interface : {'GB', 'USB'}
        Interface to use (see TDT's ActiveX documentation on the Connect*
        methods for more information).  You almost certainly want 'GB' (which
        is the default value).
    device_id : number
        ID of device
    load : boolean (optional)
        Load circuit to specified device.  Default is True. Set to False if you
        just want to get a list of the tags available in the circuit.
    start : boolean (optional)
        Start (i.e. run) the circuit after loading it.  Default is False.
    address : two-tuple (str, int)
        Connect to the address specified as a two-tuple in (host, port) format
        using the network-aware proxy of TDT's driver.  If None, defaults to
        the TDT implementation of the RPcoX and zBUSx drivers.
    '''

    def __init__(self, circuit_name, device_name, interface='GB', device_id=1,
                 load=True, start=False, fs=None, address=None):
        self.device_name = device_name
        self.name = split(circuit_name)[1]
        self.device_id = device_id
        self.server_address = address
        self.interface = interface

        # Hint for Matlab users: _iface is the same COM object a Matlab user
        # typically works with when they call actxserver('RPco.X').  It
        # supports the exact same methods as the Matlab version.
        self._iface = connect_rpcox(device_name, interface=interface,
                                    device_id=device_id, address=address)
        self._zbus = connect_zbus(interface=interface, address=address)
        self.path = get_cof_path(abspath(circuit_name))
        if load:
            self.load()
            atexit.register(self.stop)
        else:
            self.read()
        self.inspect()

        if start:
            self.start()

    def __getstate__(self):
        '''
        Provides support for pickling, which is required by the multiprocessing
        module for launching a new process.  _iface and _zbus are PyIDispatch
        objects which do not support pickling, so we just delete them and
        pickle the rest.
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
        self._iface = connect_rpcox(self.device_name)
        self._zbus = connect_zbus(self.server_address)
        self.read()

    def read(self):
        if not self._iface.ReadCOF(self.path):
            mesg = "Unable to read %s" % self.path
            raise DSPError(self, mesg)

    def load(self):
        '''
        Clear DSP RAM set all variables to default value

        The circuit is reloaded from disk, so any recent edits to the circuit
        will be reflected in the running program.
        '''
        # Note that ClearCOF alone does not apear to reset all variables to
        # default value, so we reload the circuit as well.
        self._iface.Halt()
        if not self._iface.ClearCOF():
            mesg = "Unable to clear %s buffers" % self
            raise DSPError(self, mesg)
        if not self._iface.LoadCOF(self.path):
            mesg = 'Unable to load %s' % self.path
            raise DSPError(self, mesg)
        log.debug("Reloaded %s", self)
        self.trigger('A', 'low')
        self.trigger('B', 'low')

    def inspect(self):
        '''
        Determine what tags are available in the microcode
        '''
        # Inspect COF for available tags and their type/size
        num_tags = self._iface.GetNumOf('ParTag')
        self.tags = {}
        self.scalar_tags = []
        self.vector_tags = []
        for i in range(num_tags):
            name = self._iface.GetNameOf('ParTag', i+1)
            if not name.startswith('%'):
                tag_size = self._iface.GetTagSize(name)
                if tag_size == 0:
                    mesg = "Attempted to initialize invalid tag %s" % name
                    raise DSPError(self, mesg)
                tag_type = self._iface.GetTagType(name)
                self.tags[name] = (tag_size, tag_type)
                if tag_size == 1:
                    self.scalar_tags.append(name)
                else:
                    self.vector_tags.append(name)
                log.debug("%s: found %s (size %d, type %s)", self, name,
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
        Enhanced version of `set_tag` that converts the value

        Parameters
        ==========
        name : str
            Name of the parameter tag to write the converted value to
        value : int or float
            Value to convert
        val_unit : str
            Unit of value provided
        tag_unit : str
            Unit parameter tag requires

        Returns
        =======
        Actual value of the tag (i.e. the converted value)

        Value will be converted from val_unit to tag_unit based on the sampling
        frequency of the device (if needed).  See :module:`convert` for more
        information.
        '''
        value = convert(val_unit, tag_unit, value, self.fs)
        self.set_tag(name, value)
        return value

    def get_tag(self, name):
        '''
        Analogue of RPco.X.GetTagVal

        Parameters
        ==========
        name : str
            Name of the parameter tag to read the value from

        Raises DSPError
            If the tag does not exist or is not a scalar value (e.g. you cannot
            use this method with parameter tags linked to a buffer)
        '''
        # Check to see if tag exists
        try:
            tag_size, tag_type = self.tags[name]
        except KeyError:
            raise DSPError(self, "Tag %s does not exist" % name)
        if tag_size != 1:
            raise DSPError(self, "Tag %s is not a scalar value" % name)
        value = self._iface.GetTagVal(name)

        # The ActiveX wrapper always returns a float, regardless of whether
        # it's a bool, int or float.  Let's be sure to cast the value to the
        # correct type.
        if tag_type in RCX_CAST:
            value = RCX_CAST[tag_type](value)
        log.debug("Get %s:%s is %r", self, name, value)
        return value

    def set_tag(self, name, value):
        '''
        Analogue of RPco.X.SetTagVal

        Parameters
        ==========
        name : str
            Name of the parameter tag to write the value to
        value : int or float
            Value to write

        Raises DSPError
            If the tag does not exist or is not a scalar value (e.g. you cannot
            use this method with parameter tags linked to a buffer)
        '''
        # Check to see if tag exists
        if name not in self.tags:
            raise DSPError(self, "Tag %s does not exist" % name)
        if self.tags[name][0] != 1:
            raise DSPError(self, "Tag %s is not a scalar value" % name)
        if not self._iface.SetTagVal(name, float(value)):
            mesg = "Unable to set tag %s to %r" % (name, value)
            raise DSPError(self, mesg)
        log.debug("Set %s:%s to %r", self, name, value)

    def set_tags(self, **tags):
        '''
        Convenience function for setting the value of multiple tags

        >>> circuit.set_tags(record_duration=5, play_duration=4)
        '''
        for tag, value in tags.items():
            self.set_tag(tag, value)

    def set_coefficients(self, name, data):
        '''
        Load data to a coefficient or matrix input

        Parameters
        ==========
        name : str
            Name of the parameter tag to write the data to
        data : array-like
            Data to write to tag.  Must be 1D format (even for matrices).
            See RPvds documentation for appropriate ordering of indices for
            the component.

        Raises DSPError
            If the specified parameter tag is not linked to a coefficient input
            or the length of the data is not equal to the size of the input on
            the component.

        Note that as of 3.10.2011, RPvds' CoefLoad component appears to be
        broken (per conversation with TDT's tech support -- Mark Hanus and
        Chris Walters).  As a workaround, connect a data tag directly to the
        >K or >Coef input of the component.
        '''
        tag_size, tag_type = self.tags[name]
        if tag_type != RCX_COEFFICIENT:
            raise DSPError(self, "Tag %s is not a coefficient buffer" % name)
        if tag_size != len(data):
            mesg = "Exactly %d values must be written to tag %s"
            raise DSPError(self, mesg % (tag_size, name))
        if not self._iface.WriteTagV(name, 0, data):
            raise DSPError(self, "Unable to upload data to buffer %s" % name)

    def start(self, pause=0.25):
        '''
        Analogue of RPco.X.Run

        The circuit sometimes requires a couple hundred msec "settle" before we
        can commence data acquisition
        '''
        log.debug("starting %s", self)
        if not self._iface.Run():
            raise DSPError(self, "Unable to start circuit")
        time.sleep(pause)

    def stop(self):
        '''
        Analogue of RPco.X.Halt
        '''
        log.debug("stopping %s", self)
        if not self._iface.Halt():
            raise DSPError(self, "Unable to stop circuit")

    def trigger(self, trigger, mode='pulse'):
        '''
        Fire a zBUS or software trigger

        Parameters
        ----------
        trigger : {1-9, 'A', 'B'}
            Fire the specified trigger.  If integer, this corresponds to
            RPco.X.SoftTrg.  If 'A' or 'B', this fires the corresponding zBUS
            trigger.
        mode : {'pulse', 'high', 'low'}
            Relevant only when trigger is 'A' or 'B'.  Indicates the
            corresponding mode to set the zBUS trigger to

        Note that due to a bug in the TDT ActiveX library for versions greater
        than 56, we have no way of ensuring that zBUS trigger A or B were
        fired.
        '''
        # Convert mode string to the corresponding integer
        mode_enum = dict(pulse=0, high=1, low=2)
        # We have no way of ensuring that zBUS trigger A or B were fired
        # properly due to a bug in versions of the ActiveX library >= 57.
        if trigger == 'A':
            self._zbus.zBusTrigA(0, mode_enum[mode], 10)
        elif trigger == 'B':
            self._zbus.zBusTrigB(0, mode_enum[mode], 10)
        elif (1 <= trigger < 10) and mode == 'pulse':
            if not self._iface.SoftTrg(trigger):
                raise DSPError(self, "Could not fire soft trigger %d"
                               % trigger)
        else:
            mesg = "Unsupported trigger mode %s %s" % (trigger, mode)
            raise DSPError(self, mesg)
        log.debug('Trigger %r %s', trigger, mode)

    def get_buffer(self, data_tag, mode, *args, **kw):
        if mode == 'w':
            return WriteableDSPBuffer(self, data_tag, *args, **kw)
        elif mode == 'r':
            return ReadableDSPBuffer(self, data_tag, *args, **kw)

    def clear_buffer(self, name):
        if not self._iface.ZeroTag(name):
            raise DSPError(self, "Unable to zero tag %s" % name)

    def get_status(self, status):
        return (self._iface.GetStatus() >> RCX_STATUS_BITMASK[status]) & 1

    def is_connected(self):
        '''
        True if connection with hardware is active, False otherwise
        '''
        return self.get_status('connected')

    def is_loaded(self):
        '''
        True if microcode is loaded, False otherwise
        '''
        return self.get_status('loaded')

    def is_running(self):
        return self.get_status('running')

    def __str__(self):
        state = ''
        if self.is_connected():
            state += 'Cx'
        if self.is_loaded():
            state += 'Ld'
        if self.is_running():
            state += 'Rn'
        return "{}:{}:{}".format(self.device_name, self.name, state)

    def set_sort_windows(self, name, windows):
        '''
        Utility function for configuring TDT's SpikeSort component coefficients

        Windows should be a list of 3-tuples in the format (time, center volt,
        half-height)

        If the windows overlap in time such that they cannot be converted into
        a coefficient buffer, and error will be raised.
        '''
        tag_size, tag_type = self.tags[name]
        if tag_type != RCX_COEFFICIENT:
            raise DSPError(self, "Tag %s is not a coefficient buffer" % name)
        coefficients = np.zeros(tag_size).reshape((-1, 3))
        processed = []
        for i, window in enumerate(windows):
            t, center, height = window
            x = round(t*self.fs)
            if x in processed:
                raise DSPError(self, "Windows for %s overlap in time" % name)
            processed.append(x)
            coefficients[x] = center, height, i+1
        self.set_coefficients(name, coefficients.ravel())

    def convert(self, value, src_unit, dest_unit):
        '''
        Converts value to desired unit give the sampling frequency of the DSP.

        Parameters specified in paradigms are typically expressed as frequency
        and time while many DSP parameters are expressed in number of samples
        (referenced to the DSP sampling frequency).  This function provides a
        convenience method for converting between conventional values and the
        'digital' values used by the DSP.

        Note that for converting units of time/frequency to n/nPer, we have to
        coerce the value to a multiple of the DSP period (e.g. the number of
        'ticks' of the DSP clock).

        Appropriate strings for the unit types:

            fs
                sampling frequency
            nPer
                number of samples per period
            n
                number of samples
            s
                seconds
            ms
                milliseconds
            nPow2
                number of samples, coerced to the next greater power of 2 (used
                for ensuring efficient FFT computation)

        Given a DSP clock frequency of 10 kHz::

            >>> circuit.convert(0.5, 's', 'n')
            5000
            >>> circuit.convert(500, 'fs', 'nPer')
            20

        Given a DSP clock frequency of 97.5 kHz::

            >>> circuit.convert(5, 's', 'nPow2')
            524288

        Parameters
        ----------
        value: numerical (e.g. integer or float)
            Value to be converted
        src_unit: string
            Unit of the value
        dest_unit: string
            Destination unit

        Returns
        -------
        converted unit : numerical value
        '''
        return convert(src_unit, dest_unit, value, self.fs)

    def print_tag_info(self):
        '''
        Prints a list of tags and their current value if they are a scalar
        (buffer tags are not printed yet)

        Used as a convenience method for debugging
        '''
        for tag, (tag_size, tag_type) in self.tags.items():
            if tag_size == 1:
                print(tag, self.get_tag(tag))
