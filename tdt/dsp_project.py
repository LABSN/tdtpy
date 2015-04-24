from .util import connect_zbus
from .dsp_circuit import DSPCircuit
from .dsp_error import DSPError
import atexit

import logging
log = logging.getLogger(__name__)


class DSPProject(object):
    '''
    Used to manage loading circuits to multiple DSPs.  Mainly a convenience
    method.
    '''

    def __init__(self, address=None, interface='GB'):
        self._circuit_info = {}
        self._circuits = {}
        self._zbus = connect_zbus(interface=interface, address=address)
        self._interface = interface
        self.server_address = address
        atexit.register(self.stop)

    def load_circuit(self, circuit_name, device_name, device_id=1):
        '''
        Load the circuit to the specified device

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
        circuit = DSPCircuit(circuit_name, device_name,
                             address=self.server_address,
                             interface=self._interface,
                             device_id=device_id)
        self._circuits[device_name] = circuit
        return circuit

    def start(self):
        '''
        Start all circuits that have been loaded
        '''
        for circuit in self._circuits.values():
            circuit.start()

    def stop(self):
        '''
        Stop all circuits that have been loaded
        '''
        for circuit in self._circuits.values():
            circuit.stop()

    def trigger(self, trigger, mode='pulse'):
        '''
        Fire a zBUS trigger

        Parameters
        ----------
        trigger : {'A', 'B'}
            Fire the specified trigger.  If integer, this corresponds to
            RPco.X.SoftTrg.  If 'A' or 'B', this fires the corresponding zBUS
            trigger.
        mode : {'pulse', 'high', 'low'}
            Indicates the corresponding mode to set the zBUS trigger to

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
        else:
            mesg = "Unsupported trigger mode %s %s" % (trigger, mode)
            raise DSPError(self, mesg)
        log.debug('Trigger %r %s', trigger, mode)
