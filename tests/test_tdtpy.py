import pytest
import time

import numpy as np

from tdt import DSPProject


BASE_FS = 97656.25


@pytest.fixture
def project():
   return DSPProject()


@pytest.fixture
def circuit(project):
   circuit = project.load_circuit('RZ6-debugging.rcx', 'RZ6', 1)
   circuit.start()
   yield circuit
   circuit.stop()


@pytest.fixture
def ao1(circuit):
   return circuit.get_buffer('ao1', 'w')


@pytest.fixture
def ai1(circuit):
   return circuit.get_buffer('ai1', 'r')


@pytest.fixture
def ai3(circuit):
   # This tag can be downsampled
   return circuit.get_buffer('ai3', 'r', dec_factor=4)


def test_circuit_load(circuit):
    circuit.start()
    circuit.stop()


def test_buffer_fs(ao1, ai1, ai3):
   assert ao1.fs == BASE_FS
   assert ai1.fs == BASE_FS
   assert ai3.fs == (BASE_FS / 4)
   
   
def test_circuit_write_read(project, ao1, ai1):
   n = round(ao1.fs)
   write_samples = np.random.uniform(size=n)
   ao1.write(write_samples)
   project.trigger('A', 'high')
   time.sleep(1)
   
   # There is a two-sample delay in the circuit
   read_samples = ai1.read()[0, 2:n+2]
   np.testing.assert_allclose(write_samples, read_samples)


def test_buffer_detect_dec_factor(circuit):
   # The default decimation factor is 8 by default
   ai3 = circuit.get_buffer('ai3', 'r')
   assert ai3.fs == (BASE_FS / 8)

   
def test_circuit_write_read_dec(project, ao1, ai3):
   n = round(ao1.fs / 10)
   t = np.arange(n) / ao1.fs
   write_samples = np.sin(2 * np.pi * 50 * t)
   ao1.write(write_samples)
 
   project.trigger('A', 'high')
   time.sleep(0.1)

   n_dec = int(n / 4)
   
   # I'm not sure why we need to discard the first sample here.
   read_samples_dec = ai3.read()[0, 1:n_dec+1]

   # Due to the two-sample delay, we need to decimate the write
   # buffer starting at sample two.
   write_samples_dec = write_samples[2::4]
   np.testing.assert_allclose(write_samples_dec, read_samples_dec)
   
   
def test_circuit_incremential_write_read(project, ao1, ai1):
   n = round(ao1.fs)
   write = []
   read = []

   for i in range(10):
      write.append(np.random.uniform(size=n))

   ao1.write(write[0])
   project.trigger('A', 'high')
   for s in write[1:]:
      time.sleep(0.5)
      ao1.write(s)
      read.append(ai1.read())
   time.sleep(11*0.5)
   read.append(ai1.read())
   
   write = np.concatenate(write, axis=-1)
   read = np.concatenate(read, axis=-1)[0]
   # Be sure to correct for 2 sample delay
   np.testing.assert_allclose(write, read[2:len(write)+2])
