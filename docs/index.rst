.. TDTPy documentation master file, created by
   sphinx-quickstart on Fri Apr 22 00:15:14 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TDTPy Documentation
===================

.. note:: 

    We are still working on the documentation.  Much more to come in the next
    few weeks.

.. module:: tdt
    :platform: Windows (requires proprietary ActiveX driver from TDT)
.. moduleauthor:: Brad Buran <bburan@alum.mit.edu>

Contents:


.. toctree::
    :maxdepth: 2

    dsp_circuit.rst
    dsp_buffer.rst
    converting.rst
    api.rst

Why use TDTPy?
==============

TDTPy is a Python wrapper around `Tucker-Davis Technologies`_ `ActiveX library`_
[PDF link] for communicating with their System 3 hardware (e.g. the RP2.1, RX6,
RZ6, etc.).  In addition to the standard operations (loading circuits,
configuring tags and reading/writing to hardware buffers), TDTPy offers a number
of high-level features that are not included in the ActiveX library:

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

Furthermore, TDTPy was as written as part of an initial progress towards a
hardware abstraction layer.  Your experiment code should not care whether you're
using Tucker Davis' `System 3`_ hardware, `National Instruments DAQ platform`_,
a high-quality audio card, or some combination of different vendors' hardware.
A key goal of TDTPy is to begin progress towards an application programming
interface (API) that can be implemented by Python wrappers around other hardware
vendors' libraries.  By building experiment code on top of TDTPy (rather than
directly on top of TDT's ActiveX library), switching to another hardware
platform should only require the following steps:

* Identifying (or writing) a wrapper around the vendor's library that supports
  the public API that TDTPy also supports.
* Writing the underlying microcode (e.g. a LabVIEW VI if you are switching
  to National Instruments' PXI) for the new hardware required to run the
  experiment.
* Changing your code to import from your new wrapper rather than TDTPy.

We have already built two programs, Neurogen_ and NeuroBehavior_, on top of
TDTPy with an eye towards ensuring that we can switch to a different hardware
platform if needed.

Key differences between TDTPy and OpenEx
========================================

Some people may note a number of similarities between the goals of the TDTPy and
TDT's OpenEx platform.  Both platforms are designed to streamline the process of
setting up and running experiments by providing high-level functionality.

* TDTPy is open-source.  OpenEx (despite the name) is not.
* Both OpenEx and TDTPy facilitate handling of buffer reads and writes provided
  you follow certain conventions in setting up your RPvds circuit.  OpenEx
  requires strict conventions (e.g. you must give your tag a four-letter name
  with a special prefix).  TDTPy allows you to use whatever names you like.
* Both TDTPy and OpenEx support running the hardware communication in a
  subprocess.  However, OpenEx does not make the data immediately available.  At
  best, there is a 10 second lag from the time the data is downloaded from the
  hardware to the time it is availabile to your script for plotting and
  analysis.  TDTPy makes the downloaded data available immediately.
* OpenEx integrates with other components produced by TDT (OpenController,
  OpenDeveloper, OpenWorkbench, etc.).  TDTPy currently does not offer the
  functionality provided by these other components.
* OpenEx requires the use of TDT's proprietary data format (TTank).  In addition
  to being a proprietary, binary format, TTank imposes certain constraints on
  how you can save your data to disk.  In contrast, TDTPy allows you to handle
  saving the data (i.e. you can dump it to a HDF5, XML, ASCII, CSV or MAT
  container).
* Integrating OpenEx with your custom scripts is somewhat of a hack.  You must
  launch OpenEx then launch your script.  TDTPy is part of your script.
* TDTPy comes with robust error-checking that catches many common coding
  mistakes (e.g. attempting to access a non-existent tag on the device) and a
  test-suite you can use to ensure your hardware is performing to spec.

Roadmap
=======

* In the write-test-debug routine of developing RPvds circuits, it would be very
  useful to have a GUI that allows you to interactively monitor and manipulate
  tag values well as visualize and manipulate data in the RPvds buffers.  We can
  leverage Enthought's powerful Traits_, TraitsGUI_ and Chaco_ packages for this
  purpose.
* Support processing pipelines for uploaded and downloaded data.  This would be
  especially useful when running TDTPy as a subprocess to offload much of the
  processing overhead to a second CPU.
* Support streaming data from RPvds buffers to disk so the main process does not
  have to handle this step as well (requires a IO library that is thread/process
  safe).

.. _Tucker-Davis Technologies: http://www.tdt.com
.. _System 3: http://www.tdt.com/products.htm 
.. _National Instruments DAQ platform: http://www.ni.com/dataacquisition/multifunction/
.. _Neurogen: http://bradburan.com/programs-and-scripts/neurogen/
.. _NeuroBehavior: http://bradburan.com/programs-and-scripts/neurobehavior/
.. _ActiveX library: http://www.tdt.com/T2Download/manuals/ActiveX_User_Reference.pdf
.. _Chaco: http://code.enthought.com/projects/chaco/ 
.. _Traits: http://code.enthought.com/projects/traits/ 
.. _TraitsGUI: http://code.enthought.com/projects/traits_gui/ 

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

To install a local copy of TDTPy that you can edit::

    $ pip install -e hg+http://bitbucket.org/bburan/tdtpy#egg=tdt

    -or-

    $ hg clone http://bitbucket.org/bburan/tdtpy tdtpy
    $ cd tdtpy
    $ python setup.py install

Code example
------------

The following examples are based on the following RPvds circuit:

.. image:: example_circuit.*

Let's start with a simple code example, using TDTPy, that loads a circuit and
reads data from a buffer::

    from numpy import arange, sin, pi
    from tdt import DSPProject, DSPError
    try:
        # Load the circuit 
        project = DSPProject()
        circuit = project.load_circuit('record_microphone.rcx', 'RZ6')
        circuit.start()

        # Configure the data tags
        circuit.cset_tag('record_del_n', 25, 'ms', 'n')
        circuit.cset_tag('record_dur_n', 500, 'ms', 'n')

        # Compute and upload the waveform
        t = arange(0, int(1*circuit.fs))/circuit.fs
        waveform = sin(2*pi*1e3*t)
        speaker_buffer = circuit.get_buffer('speaker', 'w')
        speaker_buffer.write(waveform)

        # Acquire the microphone data
        microphone_buffer = circuit.get_buffer('mic', 'r')
        data = microphone_buffer.acquire(1, 'running', False)
    except DSPError, e:
        print("Error acquiring data: {}".format(e))

If you were to do the same thing using TDT's ActiveX driver directly, the code
would be much more verbose::

    from win32com.client import Dispatch
    try:
        # Load the circuit
        RX6 = Dispatch('RPco.X')
        if RX6.ConnectRX6('GB', 1) == 0:
            raise SystemError, "Cannot connect to hardware"
        if RX6.ClearCOF() == 0:
            raise SystemError, "Cannot connect clear device"
        if RX6.LoadCOF('record_microphone.rcx') == 0:
            raise SystemError, "Cannot load circuit"

        # Configure the data tags
        fs = RX6.GetSFreq()
        if circuit.SetTagVal('record_del_n', int(25e-3*fs)) == 0:
            raise SystemError, "Cannot set tag"
        if circuit.SetTagVal('record_dur_n', int(500e-3*fs)) == 0:
            raise SystemError, "Cannot set tag"
        if RX6.Start() == 0:
            raise SystemError, "Cannot start circuit"

        # Compute and upload the waveform
        t = arange(0, int(1*fs))/fs
        waveform = sin(2*pi*1e3*t)
        RX6.WriteTagV('speaker', 0, waveform)

        # Acquire the microphone data
        if RX6.SoftTrg(1) == 0:
            raise SystemError, "Cannot send trigger"
        last_read_index = 0
        acquired_data = []
        while True:
            if RX6.GetTagV('running') == 0:
                last_loop = True
            else:
                last_loop = False
            next_index = RX6.GetTagVal('mic_i')
            if next_index > last_read_index:
                length = next_index - last_read_index
                data = RX6.ReadTagV('mic', last_read_index, length)
            elif next_index < last_read_index:
                length_a = RX6.GetTagSize('mic') - last_read_index
                data_a = RX6.ReadTagV('mic', last_read_index, length_a)
                data_b = RX6.ReadTagV('mic', 0, next_index)
                data = np.concatenate(data_a, data_b)
            acquired_data.append(data)
            last_read_index = next_index
            if last_loop:
                break
        data = np.concatenate(acquired_data)
    except SystemError, e:
        print("Error acquiring data: {}".format(e))

Compared with the code using the TDTPy module, code working with the ActiveX
object directly requires a lot more boilerplate code.

.. warning::

    Due to non-standard implementation of ActiveX in the TDT libraries, win32com
    defaults to an inefficient approach when calling certain methods in the
    ActiveX library.  This results in a significant data transfer bottleneck.
    For more detail, and a description of how TDTPy solves this problem, see
    `Brad Buran's post`_.

.. _Brad Buran's post: http://bradburan.com/2011/03/speeding-up-readtagv-and-readtagvex/

Ok, let's walk through the first example to illustrate how it works.  First, we
need to import everything we need::

    from numpy import arange, sin, pi
    from tdt import DSPProject, DSPError

Now, initialize the project and load the circuit, saved in a file named
'record_microphone.rcx' to the RZ6 DSP::

    project = DSPProject()
    circuit = project.load_circuit('record_microphone.rcx', 'RZ6')

Note that you can leave the default file extension off if desired.  If the
circuit is not in the current directory, you must provde an absolute or relative
path to the circuit.

The circuit has the buffers ``mic`` and ``speaker`` as well as the tags
``record_dur_n`` and ``record_del_n``.  Note that some tag names end in ``_n``.
This is a special naming I use to remind myself what units these tags require
('n' indicates number of ticks of the DSP clock while 'ms' indicates
milliseconds).  Both ``mic`` and ``speaker`` have two supporting tags,
``speaker_i`` and ``mic_i``, respectively, that are used by TDTPy to determine
how much data is currently in the buffer.

The circuit is configured to deliver the data stored in the
speaker buffer to DAC channel 1 (which is connected to a speaker) and record the
resulting microphone waveform.  The entire process is controlled by a software
trigger.

We want to configure the microphone to record for a duration of 500 ms with a 25
ms delay.  Remember that ``record_del_n`` and ``record_dur_n`` both require the
number of samples.  Since number of samples depends on the sampling frequency of
the DSP, we have to convert our value, which is in millseconds, to the
appropriate unit::

    circuit.set_tag('record_del_n', int(25e-3*circuit.fs))
    circuit.set_tag('record_dur_n', int(500e-3*circuit.fs))

Alternatively, we can use a convenience method that handles the unit conversion
for us (n is number of samples)::

    circuit.cset_tag('record_del_n', 25, src_unit='ms', dest_unit='n')
    circuit.cset_tag('record_dur_n', 500, src_unit='ms', dest_unit='n')

Or, if we just rely on positional arguments (which we use in the example
above)::

    circuit.cset_tag('record_del_n', 25, 'ms', 'n')
    circuit.cset_tag('record_dur_n', 500, 'ms', 'n')

All three of the  approaches are fine; however, we recommend that you use
:func:`DSPCircuit.cset_tag` whenever possible since this makes the code more
readable.  

To write a 1 second, 1 kHz tone to the speaker buffer, we first generate the
waveform::

    t = arange(0, dsp.convert('s', 'n', 1))/dsp.fs
    waveform = sin(2*pi*1e3*t)

Then we open the speaker buffer for writing and write the data to the buffer::

    speaker_buffer = circuit.get_buffer('speaker', 'w')
    speaker_buffer.write(waveform)

Now that you've configured the circuit, you are ready to run it and record the
resulting waveform:: 

    microphone_buffer = circuit.get_buffer('microphone', 'r')
    data = microphone_buffer.acquire(1, 'running', False)

The `DSPBuffer.acquire` method takes three arguments: 

* The trigger to fire, initiating data acquisition.  If None, no trigger is
  fired and acquire begins spooling data immediately.
* The tag on the DSP to monitor.  
* The value of the monitor tag that indicates data acquisition is done.

Fire trigger 1 and continuously acquire data until ``running`` tag is False::

    microphone_buffer.acquire(1, 'recording', False)

Fire trigger 1 and continuously acquire data until ``complete`` tag is True::

    microphone_buffer.acquire(1, 'complete', True)

Get the initial value of ``toggle``, fire trigger 1, then continuously acquire
data until the value of ``toggle`` changes::

    microphone_buffer.acquire(1, 'toggle', True)

Fire trigger 1 and continuously acquire data until ``index`` tag is greater or
equal to 10000::

    microphone_buffer.acquire(1, 'index', lambda x: x >= 1000)

.. note::

    The acquire method continuously donwloads data while monitoring the end
    condition.  This allows you to acquire sets of data larger than the buffer
    size without losing any data.

Accessing the raw ActiveX object
--------------------------------
Although DSPCircuit and DSPBuffer expose most of the functionality available via
the ActiveX object, there may be times when you need to access it directly.  You
may obtain a handle to the object via the function `tdt.util.connect`::

    from tdt.util import connect
    obj = connect('RZ6', 'GB')

Running I/O in a separate process
---------------------------------
TODO

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
