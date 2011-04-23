from util import connect_zbus
from dsp_circuit import DSPCircuit
import atexit

class DSPProject(object):

    def __init__(self):
        self._circuit_info = {}
        self._circuits = {}
        self._zbus  = connect_zbus()
        atexit.register(self.stop)

    def load_circuit(self, circuit_name, device_name):
        self._circuit_info[(circuit_name, device_name)] = []
        # We need to store a reference to the circuit here so we can properly
        # initialize any buffers we need
        circuit = DSPCircuit(circuit_name, device_name)
        self._circuits[device_name] = circuit
        return circuit

    def start(self):
        for circuit in self._circuits.values():
            circuit.start()

    def stop(self):
        for circuit in self._circuits.values():
            circuit.stop()

    def trigger(self, trigger, mode='pulse'):
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
        log.info('Trigger %r %s', trigger, mode)

