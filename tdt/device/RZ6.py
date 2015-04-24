import numpy as np
import unittest

RZ6_ATTEN_BASE = 255*256*256


def split_attenuation(att):
    '''
    Split the attenuation value into two parts, one that can be realized by
    setting the hardware attenuator (the RZ6 attenuator can be set to 0, 20, 40
    or 60 dB) and the second that must be realized by scaling the waveform.

    Returns (hw_attenuation, sw_attenuation)
    ----------------------------------------
    hw_attenuation : float
        hardware attenuation setting
    sw_attenuation : float
        remaining attenuation that must be realized by scaling the waveform
    '''
    hw_step = min(int(att/20.0), 3)
    hw_att = hw_step*20.0
    sw_att = att-hw_att
    return hw_att, sw_att


def db_to_sf(db):
    sf = 10**(-db/20.0)
    return sf


def atten_to_bits(attA, attB, mute=False):
    '''
    Given the desired attenuation, determine the bit value that needs to be
    inserted into memory address 2 on the RZ6 to set the hardware attenuators
    accordingly.  This can replace the computations perfomed in the RZ6
    AudioOut macro which takes up to 12% of CPU time at 100 kHz.

    Raises ValueError if requested attenuation falls outside range of valid
    values.
    '''
    if not (0 <= attA <= 120):
        raise ValueError("Attenuation A must be between 0 and 120 dB")
    if not (0 <= attB <= 120):
        raise ValueError("Attenuation B must be between 0 and 120 dB")
    attA = min(int(attA/20), 3)
    attB = min(int(attB/20), 3) << 4
    mute = int(mute) * 256
    return RZ6_ATTEN_BASE | attA | attB | mute


def waveform_to_bits(waveform, sf):
    '''
    Scale and convert waveform to the binary data that needs to be inserted
    (via the RPvds poke component) into memory address 15 (for Out-A) or 16
    (for Out-B).  This replaces the computations performed in the RZ6 AudioOut
    macro which take up to 4% of CPU time at 100 kHz.  Used in combination with
    atten_to_bits, you can free up 16% of CPU time.
    '''
    waveform = np.asanyarray(waveform)
    waveform = waveform*sf*2e8
    waveform = waveform.astype('i')
    return (waveform | 255) ^ ((waveform >> 24) & 255)


class TestWithHardware(unittest.TestCase):

    CIRCUIT = '../components/test_RZ6_audio_out'

    def setUp(self):
        from tdt import DSPCircuit
        from os.path import dirname, join
        circuit = join(dirname(__file__), self.CIRCUIT)
        self.circuit = DSPCircuit(circuit, 'RZ6')
        self.buffer_in = self.circuit.get_buffer('in', 'w')
        self.buffer_out = self.circuit.get_buffer('out', 'r', src_type='int32',
                                                  dest_type='int32',
                                                  block_size=1)
        self.circuit.start()

    def test_waveform_to_bits(self):
        from numpy.random import random
        from numpy.testing import assert_array_equal  # noqa
        waveform = random(100e3).astype('float32')
        self.circuit.set_tag('nHi', 100e3)
        self.buffer_in.set(waveform)
        actual = self.buffer_out.acquire(1, 'running', False).ravel()
        expected = waveform_to_bits(waveform, 1)

        # Due to various vagaries of shuffling bits around, I believe the least
        # significant bit is sometimes lost when uploading to the RZ6.  This
        # results in a maximum difference between the actual and expected
        # values of 256.  It's not clear exactly what the significance of this
        # number actually is to me.
        difference = actual-expected
        self.assertTrue(difference.max() <= 256)


class TestRZ6Functions(unittest.TestCase):

    # attA, attB, expected bit value
    ATTEN_TEST_VALUES = [
        (0, 20, 16711696),
        (0, 40, 16711712),
        (0, 60, 16711728),
        (20, 0, 16711681),
        (20, 40, 16711713),
        (20, 60, 16711729),
        (40, 0, 16711682),
        (40, 20, 16711698),
        (40, 60, 16711730),
        (60, 0, 16711683),
        (60, 20, 16711699),
        (60, 40, 16711715),
    ]

    def test_attenuation_to_bits(self):
        for a, b, expected in self.ATTEN_TEST_VALUES:
            actual = atten_to_bits(a, b)
            self.assertEqual(actual, expected)

        # Ensure out of range attenuations raise an error
        self.assertRaises(ValueError, atten_to_bits, 0, 121)
        self.assertRaises(ValueError, atten_to_bits, 0, -1)
        self.assertRaises(ValueError, atten_to_bits, 121, 0)
        self.assertRaises(ValueError, atten_to_bits, -1, 0)

if __name__ == '__main__':
    unittest.main()
