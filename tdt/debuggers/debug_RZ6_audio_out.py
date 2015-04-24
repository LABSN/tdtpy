import itertools

from .. import DSPCircuit
from ..device.RZ6 import split_atten, atten_to_bits

if __name__ == '__main__':
    circuit = DSPCircuit('debug_RZ6_audio_out', 'RZ6')
    circuit.start()

    for a, b in itertools.permutations((0, 20, 40, 60), 2):
        circuit.set_tag('attA', a)
        circuit.set_tag('attB', b)
        padA = circuit.get_tag('Pad-A')
        padB = circuit.get_tag('Pad-B')
        poke = circuit.get_tag('Poke')
        guess = atten_to_bits(a, b)
        circuit.set_tag('test_val', guess)
        print('')
        print(a, b, padA, padB, poke, guess)
        # raw_input("Please check value on RZ6 LCD display")

    for a in (0, 12.5, 30, 40, 89.1):
        circuit.set_tag('attA', a)
        expected_sf = circuit.get_tag('SF-A')
        actual_att, actual_sf = split_atten(a)
        print(a, expected_sf, actual_sf)
