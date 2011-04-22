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

Why use TDTPy?
==============

TDTPy is a Python wrapper around `Tucker-Davis Technologies`_ ActiveX library for
communicating with their System 3 hardware (e.g. the RP2.1, RX6, RZ6, etc.).  In
addition to the standard operations (loading circuits, configuring tags and
reading/writing to hardware buffers), TDTPy offers a number of high-level
features that are not included in the ActiveX library:

* Handling type conversion between analog and digital units (e.g. converting
  seconds to number of DSP cycles based on the CPU frequency of the hardware).
* Optional non-blocking input/output by launching TDTPy in a subprocess to free
  up your script for other tasks.  This is particularly useful when you are
  downloading large (e.g. 64 or more channels of neurophysiology) amounts of
  data from the hardware.
* Simple reads and writes.  The hardware buffers are implemented as "ring
  buffers" with various features such as multichannel storage and data
  compression.  TDTPy automatically detects the configuration of the hardware
  buffer and returns a buffer object (`tdt.DSPBuffer`) that you can read/write
  to without having to deal with the intricacies of the hardware buffer itself.
* Robust error handling.  Some methods in the ActiveX library will fail silently
  (e.g. if you try to access a nonexistent tag or attempt to write more data
  than the hardware buffer can hold).  When the RPvds circuit is first loaded to
  the hardware, TDTPy will inspect the microcode and store some infomration
  about the tags and buffers available.  All subsequent operations are validated
  against this metadata before being passed to the ActiveX library.  If an
  invalid operation is attempted, a DSPError is raised with the appropriate
  message.

.. _Tucker-Davis Technologies: http://www.tdt.com

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
reads data from a buffer::

    from tdt import DSPCircuit
    try:
        circuit = DSPCircuit('basic-characterization', 'RX6')
        circuit.cset_tag('acq_dur', 15, 's', 'n')  # Convert 15 s to sample number
        buffer = circuit.get_buffer('neural', 'r')
        circuit.start()
        while True:
            data = buffer.read()
            if some_condition_met:
                break
    except DSPError:
        # handle error here
    # do something with the data

If you were to do the same thing using TDT's ActiveX driver directly, the code
would be much more verbose::

    from win32com.client import Dispatch
    try:
        RX6 = Dispatch('RPco.X')
        if RX6.ConnectRX6('GB', 1) == 0:
            raise SystemError, "Cannot connect to hardware"
        if RX6.ClearCOF() == 0:
            raise SystemError, "Cannot connect clear device"
        if RX6.LoadCOF('basic-characterization.rcx') == 0:
            raise SystemError, "Cannot load circuit"
        fs = RX6.GetSFreq()
        if circuit.SetTagVal('acq_dur', int(15*fs)) == 0:
            raise SystemError, "Cannot set tag"
        if RX6.Start() == 0:
            raise SystemError, "Cannot start circuit"
        last_read_index = 0
        while True:
            next_index = RX6.GetTagVal('neural_i')
            if next_index > last_read_index:
                length = next_index - last_read_index
                data = RX6.ReadTagV('neural', last_read_index, length)
            elif next_index < last_read_index:
                length_a = RX6.GetTagSize('neural') - last_read_index
                data_a = RX6.ReadTagV('neural', last_read_index, length_a)
                data_b = RX6.ReadTagV('neural', 0, next_index)
                data = np.concatenate(data_a, data_b)
            last_read_index = next_index
            if some_condition_met:
                break
    except SystemError:
        # handle error here
    # do something with the data

Compared with the code using the TDTPy module, code working with the ActiveX
object directly requires a lot more boilerplate code.

.. note::

    There is also a problem with the default output of win32com.  Due to
    non-standard implementation of ActiveX in the TDT libraries, win32com
    defaults to an inefficient approach for certain functions on the ActiveX
    object.  For more detail, and a description of how TDTPy solves this
    problem, see `Brad Buran's post`_.

.. _Brad Buran's post: http://bradburan.com/2011/03/speeding-up-readtagv-and-readtagvex/

Key Components of TDTPy
-----------------------

`tdt.DSPProject`
    A container for all the circuits present in the system.

`tdt.DSPCircuit` 
    A wrapper around a single RPvds circuit.  Note that a single circuit maps to a
    single device (i.e. you can only have one circuit running on a single DSP at
    a time).

`tdt.DSPBuffer`
    A wrapper around a single DSP buffer object.

To intialize a project::

    project = DSPProject()

To load a circuit to a device::

    circuit = project.load_circuit('record_microphone', 'RZ6')

Lets say the circuit has the buffers microphone and speaker as well as the tags
record_duration_n and record_delay_n.  Note that both tag names end in '_n'.
This is a special naming convention that tells the backend what unit these tags
accept('n' indicates number of ticks of the DSP clock while 'ms' indicates
milliseconds).  The circuit is configured to deliver the data stored in the
speaker buffer to DAC channel 1 (which is connected to a speaker) and record the
resulting microphone waveform.  The entire process is controlled by a software
trigger.

Now we want to configure the microphone to record for a duration of 500 ms with
a 25 ms delay.  Remember that record_delay_n and record_duration_n both require
the number of samples.  Since number of samples depends on the sampling
frequency of the DSP, we would have to compute this::

    circuit.set_tag('record_delay_n', int(25e-3*RZ6.fs))
    circuit.set_tag('record_duration_n', int(500e-3*RZ6.fs))

Alternatively, we can use a convenience method that handles the unit conversion
for us (n is number of samples)::

    circuit.cset_tag('record_delay_n', 25, src_unit='ms', dest_unit='n')
    circuit.cset_tag('record_duration_n', 500, src_unit='ms', dest_unit='n')

Or, if we just rely on positional arguments::

    circuit.cset_tag('record_delay_n', 25, 'ms', 'n')
    circuit.cset_tag('record_duration_n', 500, 'ms', 'n')

Both approaches are fine; however, we recommend that you use
:func:`DSPCircuit.cset_tag` whenever possible since this makes the code more
readable.  

To write a 1 second, 1 kHz tone to the speaker buffer:

>>> from numpy import arange, sin, pi
>>> t = arange(0, dsp.convert('s', 'n', 1))/dsp.fs
>>> waveform = sin(2*pi*1e3*t)
>>> speaker.write(waveform)

Now that you've configured the circuit and are ready to record:

>>> microphone.acquire(1, 'recording', False)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

