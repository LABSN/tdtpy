.. TDTPy documentation master file, created by
   sphinx-quickstart on Fri Apr 22 00:15:14 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TDTPy Documentation
===================

.. module:: tdt.dsp_circuit
    :platform: Windows (requires proprietary ActiveX driver from TDT)
.. moduleauthor:: Brad Buran <bburan@alum.mit.edu>

Contents:


.. toctree::
   :maxdepth: 2

   dsp_buffer.rst

Getting Started
===============

Installing
----------

The easiest install method is to use Python's pip tool.  First, let's make sure
that it's installed (PythonXY and Enthought's Python Distribution do not come
with this tool by default)::

    $ easy_install pip

Once it's installed, install a copy of Mercurial (Hg) if you haven't already::

    $ pip install hg

Now, install TDTPy::

    $ pip install hg+http://bitbucket.org/bburan/tdtpy#egg=tdt

Code example
------------

Let's start with a simple code example, using TDTPy, that loads a circuit and
reads data from a buffer.

>>> from tdt import DSPCircuit
>>> circuit = DSPCircuit('basic-characterization', 'RX6')
>>> circuit.cset_tag('acq_dur', 15, 's', 'n')  # Convert 15 s to sample number
>>> buffer = circuit.get_buffer('neural', 'r')
>>> circuit.start()
>>> while True:
...     data = buffer.read()
...     if some_condition_met:
...         break
>>> # do something with the data

If you were to do the same thing using TDT's ActiveX driver directly, the code
would be much more verbose.

>>> from win32com.client import Dispatch
>>> RX6 = Dispatch('RPco.X')
>>> RX6.ConnectRX6('GB', 1)
>>> RX6.ClearCOF()
>>> RX6.LoadCOF('basic-characterization.rcx')
>>> fs = RX6.GetSFreq()
>>> circuit.SetTagVal('acq_dur', int(15*fs))   # Convert 15 s to sample number
>>> RX6.Start()
>>> last_read_index = 0
>>> while True:
...     next_index = RX6.GetTagVal('neural_i')
...     if next_index > last_read_index:
...         length = next_index - last_read_index
...         data = RX6.ReadTagV('neural', last_read_index, length)
...     elif next_index < last_read_index:
...         length_a = RX6.GetTagSize('neural') - last_read_index
...         data_a = RX6.ReadTagV('neural', last_read_index, length_a)
...         data_b = RX6.ReadTagV('neural', 0, next_index)
...         data = np.concatenate(data_a, data_b)
...     last_read_index = next_index
...     if some_condition_met:
...         break
>>> # do something with the data

Compared with the code using the TDTPy module, code working with the ActiveX
object directly requires a lot more boilerplate code to load and initialize the
circuit.  In addition, reading data from the buffer requires you to continuously
track the last index you read and check to see if the buffer has wrapped around
to the beginning.

.. note::

    There is also a problem with the default output of win32com.  Due to
    non-standard implementation of ActiveX in the TDT libraries, win32com is
    defaults to an inefficient approach for certain functions on the ActiveX
    object.  For more detail, see `Brad Buran's post`_.

.. _Brad Buran's post: http://bradburan.com/2011/03/speeding-up-readtagv-and-readtagvex/

Lets say the circuit has the buffers microphone and speaker as well as the tags
record_duration_n and record_delay_n.  Note that both tag names end in '_n'.
This is a special naming convention that tells the backend what unit these tags
accept('n' indicates number of ticks of the DSP clock while 'ms' indicates
milliseconds).  The circuit is configured to deliver the data stored in the
speaker buffer to DAC channel 1 (which is connected to a speaker) and record the
resulting microphone waveform.  The entire process is controlled by a software
trigger.

To write a 1 second, 1 kHz tone to the speaker buffer:

>>> from numpy import arange, sin, pi
>>> t = arange(0, dsp.convert('s', 'n', 1))/dsp.fs
>>> waveform = sin(2*pi*1e3*t)
>>> circuit.speaker.write(waveform)

Now we want to configure the microphone to record for a duration of 500 ms with
a 25 ms delay.  Remember that record_delay_n and record_duration_n both require
the number of samples.  Since number of samples depends on the sampling
frequency of the DSP, we would have to compute this:

>>> circuit.set_tag('record_delay_n', int(25e-3*circuit.fs))
>>> circuit.set_tag('record_duration', int(500e-3*circuit.fs))

Alternatively, we can use a convenience method that handles the unit conversion
for us (n is number of samples):

>>> circuit.cset_tag('record_delay_n', 25, src_unit='ms', dest_unit='n')
>>> circuit.cset_tag('record_duration_n', 500, src_unit='ms', dest_unit='n')

Or, if we just rely on positional arguments:

>>> circuit.cset_tag('record_delay_n', 25, 'ms', 'n')
>>> circuit.cset_tag('record_duration_n', 500, 'ms', 'n')

Both approaches are fine; however, we recommend that you use
:func:`DSPCircuit.cset_tag` whenever possible since this makes the code more
readable.  Now that you've configured the circuit and are ready to record:

>>> microphone_data = microphone.acquire(trigger=1)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

