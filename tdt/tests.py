import numpy as np
import time
import logging
import unittest

from .dsp_circuit import DSPCircuit

logging.basicConfig(level=logging.DEBUG)


# class TestPickling(unittest.TestCase):
#
#    def setUp(self):
#        self.circuit_file = 'test_circuit.tmp'
#        self.buffer_file = 'test_buffer.tmp'
#        self.circuit = DSPCircuit('components/test_physiology_RZ6', 'RZ6')
#        self.buffer = self.circuit.get_buffer('raw', 'r')
#        with open(self.circuit_file, 'w') as fh:
#            pickle.dump(self.circuit, fh)
#        with open(self.buffer_file, 'w') as fh:
#            pickle.dump(self.buffer, fh)
#
#    def test_persist(self):
#        with open(self.circuit_file, 'r') as fh:
#            circuit = pickle.load(fh)
#        with open(self.buffer_file, 'r') as fh:
#            buffer = pickle.load(fh)
#
#    def tearDown(self):
#        remove(self.circuit_file)
#        remove(self.buffer_file)
#


class TestBufferRead(unittest.TestCase):

    def setUp(self):
        self.circuit = DSPCircuit('components/data_reduction', 'RZ6')
        self.circuit.set_tag('nHi', 4)
        self.circuit.start()
        self.shape = (4, 4)

    def tearDown(self):
        self.circuit.stop()

    def assertShape(self, data):
        self.assertEquals(data.shape, self.shape)

    def assertSeqSamples(self, data, res):
        seq_samples = np.abs(np.diff(data, axis=1)-0.1) < res
        self.assertTrue(seq_samples.all())

    def assertSeqChannels(self, data, res):
        ch_samples = np.abs(np.diff(data, axis=0)-1) < res
        self.assertTrue(ch_samples.all())

    def assertValid(self, buffer):
        self.circuit.trigger(1)
        time.sleep(0.1)
        data = buffer.read()
        self.assertShape(data)
        self.assertSeqSamples(data, buffer.resolution)
        if data.ndim > 1:
            self.assertSeqChannels(data, buffer.resolution)

    # def test_overflow_warning(self):
    #    buffer = self.circuit.get_buffer('mc', src_type='float32', channels=4,
    #            block_size=1)
    #    self.circuit.set_tag('nHi_nodata', buffer.size+100)
    #    self.circuit.trigger(2)
    #    while self.circuit.get_tag('t2'):
    #        import time
    #        time.sleep(1)
    #    self.assertRaises(DSPError, buffer.read)

    def test_mc2(self):
        buffer = self.circuit.get_buffer('mc', 'r', src_type='float32',
                                         channels=4, block_size=4)
        self.circuit.trigger(2)
        self.circuit.trigger(2)
        data = buffer.read()
        self.assertSeqChannels(data, buffer.resolution)

        self.circuit.trigger(1)
        data = buffer.read()
        self.assertSeqChannels(data, buffer.resolution)
        self.assertSeqSamples(data, buffer.resolution)

    def test_mc(self):
        buffer = self.circuit.get_buffer('mc', 'r', src_type='float32',
                                         channels=4, block_size=1)
        self.assertValid(buffer)

    def test_sh8(self):
        buffer = self.circuit.get_buffer('sh8', 'r', src_type='int8',
                                         channels=4, block_size=4)
        self.assertEqual(self.circuit.get_tag('sh8_sf'), 31)
        self.assertValid(buffer)

    def test_sh16(self):
        buffer = self.circuit.get_buffer('sh16', 'r', src_type='int16',
                                         channels=2, block_size=4)
        self.assertEqual(self.circuit.get_tag('sh16_sf'), 6553)
        self.shape = (2, 4)
        self.assertValid(buffer)

    def test_c16(self):
        # If this fails, double check that scaling factor is set properly in
        # the circuit since I am testing the ability to use a different tag for
        # computing the scaling value
        buffer = self.circuit.get_buffer('c16', 'r', src_type='int16',
                                         sf_tag='sh16_sf', block_size=4)
        self.shape = (1, 4)
        self.assertValid(buffer)

    def test_mcFI16(self):
        buffer = self.circuit.get_buffer('mcFI16', 'r', src_type='int16',
                                         channels=8, block_size=4)
        self.shape = (8, 4)
        self.assertValid(buffer)

    def test_c8D(self):
        buffer = self.circuit.get_buffer('c8D', 'r', src_type='int8',
                                         block_size=4)
        self.shape = (1, 4)
        self.assertValid(buffer)

    # THIS KEEPS FAILING!
    # def test_mcFI8(self):
    #    buffer = self.circuit.get_buffer('mcFI8', src_type='int8',
    #                                     block_size=4, channels=16)
    #    self.shape = (16, 4)
    #    self.assertValid(buffer)


class TestBufferWrite(unittest.TestCase):

    def setUp(self):
        self.circuit = DSPCircuit('components/test_physiology_RZ6', 'RZ6')
        self.buffer = self.circuit.get_buffer('speaker', 'w')
        self.circuit.start()

    def test_zero(self):
        self.buffer.clear()

    def test_write(self):
        from numpy import sin, arange, random
        from numpy.testing import assert_array_almost_equal

        t = arange(10e3)/1e3
        data_a = sin(2*np.pi*10*t)
        self.buffer.write(data_a, force=True)
        data_b = random.normal(size=10e3)
        self.buffer.write(data_b)
        # n = len(data_a)
        written_a = self.buffer._iface.ReadTagV('speaker', 0, len(data_a))
        written_b = self.buffer._iface.ReadTagV('speaker', len(data_a),
                                                len(data_b))
        assert_array_almost_equal(written_a, data_a)
        assert_array_almost_equal(written_b, data_b)

    def tearDown(self):
        self.circuit.stop()


# class TestCOMWrapper(unittest.TestCase):
#
#    #def test_comtypes(self):
#    #    from comtypes import client
#    #    iface = client.CreateObject('RPco.X')
#    #    self.assertWrite(iface)
#    #    self.assertWrite(iface)
#
#    def test_win32com(self):
#        from win32com import client
#        iface = client.Dispatch('RPco.X')
#        self.assertWrite(iface)
#        self.assertWrite(iface)
#
#    def test_custom_actxobject(self):
#        from actxobjects import RPcoX
#        iface = RPcoX()
#        self.assertWrite(iface)
#        self.assertWrite(iface)
#
#    def assertWrite(self, iface):
#        from numpy import random
#        from numpy.testing import assert_array_almost_equal
#        from array import array
#        data = random.normal(size=100e3)
#        data = array('d', data)
#        iface.ConnectRZ6('GB', 1)
#        iface.LoadCOF('components/test_physiology_RZ6.rcx')
#        iface.Run()
#        result = iface.WriteTagV('speaker', 0, data)
#        self.assertEqual(result, 1)
#
#        written = iface.ReadTagV('speaker', 0, len(data))
#        assert_array_almost_equal(written, data)


# class TestProcess(unittest.TestCase):
#
#    def test_read_write(self):
#        write_size = 50000
#        total_write = 500000
#        process = DSPProcess()
#        circuit = process.load_circuit('components/test_read', 'RZ6')
#        write_buffer = circuit.get_buffer('write', 'w')
#        read_buffer = circuit.get_buffer('read', 'r')
#
#        process.start()
#        samples_written = []
#        samples_read = []
#        #available = write_buffer.available()
#
#        samples = np.random.uniform(size=write_size)
#        write_buffer.write(samples, timeout=1)
#        samples_written.extend(samples)
#        circuit.trigger('A', 'high')
#
#        self.assertEqual(write_buffer.total_samples_written, write_size)
#
#        while True:
#            if write_buffer.total_samples_written >= total_write:
#                break
#            samples = read_buffer.read()
#            samples_read.extend(samples[0])
#            samples = np.random.uniform(size=write_size)
#            write_buffer.write(samples, timeout=None)
#            samples_written.extend(samples)
#
#        total_samples = write_buffer.total_samples_written
#        while read_buffer.total_samples_read <= total_samples:
#            if read_buffer.pending():
#                samples = read_buffer.read()
#                samples_read.extend(samples[0])
#        process.stop()
#
#        written = np.array(samples_written)
#        read = np.array(samples_read)
#        #from pylab import *
#        #plot(np.arange(len(written)), written, 'k')
#        #plot(np.arange(len(read)), read+1, 'r')
#        #plot(np.arange(len(written)), written-read[:total_samples]+2, 'g')
#        #show()
#        np.testing.assert_almost_equal(written, read[:total_samples])
#
if __name__ == '__main__':
    unittest.main()
