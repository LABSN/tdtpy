.. TDTPy documentation master file, created by
   sphinx-quickstart on Fri Apr 22 00:15:14 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TDTPy Documentation
===================

.. note:: 

    We are still working on the documentation.  Much more to come in the next
    few weeks.  We have only tested this code with a limited set of
    configurations (e.g. the RZ5/RZ6 combo).  If this software does not work
    with your configuration, that is considered a bug!

.. module:: tdt
    :platform: Windows (requires proprietary ActiveX driver from TDT)
.. moduleauthor:: Brad Buran <bburan@alum.mit.edu>

.. note::

    If you use the remote procedure call (RPC) server provided by TDTPy to
    communicate with your hardware your client code should be able to run on any
    platform including Unix, Linux and OSX).  The RPC server, however, requires
    the proprietary ActiveX drivers provided by TDT which only run on Windows.

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
[PDF link] (known as RPcoX) for communicating with their System 3 hardware (e.g.
the RP2.1, RX6, RZ6, etc.).  In addition to the standard operations (loading
circuits, configuring tags and reading/writing to hardware buffers), TDTPy
offers a number of high-level features that are not included in the ActiveX
library:

* Handling type conversion between analog and digital units (e.g. converting
  seconds to number of DSP cycles based on the CPU frequency of the hardware).
* Remote procedure call (RPC) server for allowing multiple processes and/or programs
  to communicate with the hardware across the same connection.  The drivers
  provided by TDT do not handle concurrency issues.  To handle these issues, we
  have created a RPC server that handles concurrency issues, allowing multiple
  programs to talk to the hardware simultaneously.  The programs can either run
  on the same computer or on a separate computer.
* If you use the RPC server, your client code can run on any platform (e.g. Mac
  OSX, Unix, Solaris, etc); however, the server must run on a Windows-based
  computer.
* Simple reads and writes.  The hardware buffers are implemented as "ring
  buffers" with various features such as multichannel storage and data
  compression.  TDTPy automatically detects the configuration of the hardware
  buffer and returns a buffer object (`tdt.DSPBuffer`) that you can read/write
  to without having to deal with the intricacies of the hardware buffer itself.
* Robust error handling.  Some methods in the ActiveX library will fail silently
  (e.g. if you try to access a nonexistent tag or attempt to write more data
  than the hardware buffer can hold).  When the RPvds circuit is first loaded to
  the hardware, TDTPy will inspect the microcode (i.e. the RPvds circuit) and
  store some information about the tags and buffers available.  All subsequent
  operations are validated against this metadata before being passed to the
  ActiveX library.  If an invalid operation is attempted, a DSPError is raised
  with the appropriate message.

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

Once it's installed, install a copy of Mercurial (Hg) if you haven't already.
The source code for TDTPy is managed via the Mercurial distributed version
control system and pip requires the Hg binary to checkout a copy of TDTPy::

    $ pip install mercurial

.. note::

    Installing Mercurial from source requires a working compiler.  If the above
    command fails with the error message, "unable to find vcvarsall.bat", you
    need to install a compiler.  On Windows, you can install Microsoft Visual
    Studio 2008 Express (the `version of Visual Studio`_ is important).
    Alternatively, it may be much easier to just install the TortoiseHg_
    binaries

.. _TortoiseHg: http://tortoisehg.bitbucket.org/
.. _version of Visual Studio: http://slacy.com/blog/2010/09/python-unable-to-find-vcvarsall-bat

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

.. note:: 

    Familiarity with TDT's real-time processor visual design studio (RPvds) is
    required to follow the example below.  See the `RPvds manual`_ for more
    information.

The following examples are based on the following RPvds circuit.  If you wish to
test the circuit you may need to adapt it for your specific device (e.g. on the
RX6 the correct input channel for the microphone would be 128 and on the RZ6 you
would use the AudioIn and AudioOut macros).  The specifics for each device are
described in TDT's `System 3 manual`_.

.. _RPvds manual: http://www.tdt.com/T2Download/manuals/RPvdsEx_Manual.pdf 
.. _System 3 manual: http://www.tdt.com/T2Download/manuals/TDTSys3_Manual.pdf 

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
waveform using the sampling frequency of the circuit.  The sampling frequency is
available as an attribute, `fs` of the DSPCircuit class.  A method,
:func:DSPCircuit.convert` facilitates unit conversions that are based on the
sampling frequency of the circuit (e.g. :math:`duration*fs` will convert
duration, in seconds, to the number of sample required for the waveform)::

    t = arange(0, circuit.convert(1, 's', 'n'))/circuit.fs
    waveform = sin(2*pi*1e3*t)

Then we open the speaker buffer for writing and write the data to the buffer.
The first argument to :func:`DSPCircuit.get_buffer` is the name of the tag
attached to the ``{>Data}`` port of the buffer component and the second argument
indicates whether the buffer should be opened for reading (r) or writing (w)::

    speaker_buffer = circuit.get_buffer('speaker', 'w')
    speaker_buffer.write(waveform)

Now that you've configured the circuit, you are ready to run it and record the
resulting waveform.  The acquire method will block until the ``running`` tag
becomes False then return the contents of the microphone buffer::

    microphone_buffer = circuit.get_buffer('microphone', 'r')
    data = microphone_buffer.acquire(1, 'running', False)

Accessing the raw ActiveX object
--------------------------------
Although DSPCircuit and DSPBuffer expose most of the functionality available via
the ActiveX object, there may be times when you need to access it directly.  You
may obtain a handle to the object via the function `tdt.util.connect_rpcox`::

    from tdt.util import connect_rpcox
    obj = connect_rpcox('RZ6', 'GB')

Running I/O in a separate process or on a separate computer
-----------------------------------------------------------

.. note::

    This code definitely works, and is reasonably fast on a localhost
    connection.  When I tested it via a client connecting using the wireless
    network there were some latency issues.  There are likely many speedups that
    can be implemented, but I don't have the time to do so right now.

Since all TDT devices share the same connection with the computer, we can only
talk to a single device at a time.  Unfortunately, TDT's hardware drivers do not
handle the requisite concurrent access issues, meaning that only one program
and/or process can safely use the hardware connection (e.g. the optical or USB
interface) at a time even if each process communicates with a different device.
Since we have two separate programs (one for generating the stimulus via the RZ6
and one for acquiring the physiology via the RZ5), we needed to find a way to
handle the requisite concurrency issues.

The simplest way to handle concurrency was to create a remote procedure call
(RPC) server.  This RPC server will listen for connections from clients
(either from the same computer or on a networked computer).  Each client will
initiate a persistent connection for the lifetime of the program and send
requests via a TCP protocol.  As these requests come in, the server will process
them sequentially (thus handling concurrency issues).  

A thread-based design for the server was considered; however, the bottleneck
currently is in the optical interface I/O speed so it is unlikely that the
additional hassle and overhead of threading will provide any significant
performance gain.

The server is meant to be a relatively thin layer around the ActiveX device
driver.  Requests from clients are essentially passed directly to the ActiveX
interface itself.  To facilitate using this code we've created a network-aware
proxy of the RPcoX client that passes off all RPcoX method calls directly to the
RPC server.  This allows you to use the server in your code without having to
rewrite your code to use `tdt.DSPProject` or `tdt.DSPCircuit`.  Assuming your
code uses `win32com.client` directly rather than using TDTPy's abstraction
layer, the following code::

    from win32com.client import Dispatch
    iface = Dispatch('RPco.X')
    iface.ConnectRZ6('GB', 1)
    zbus = Dispatch('ZBUSx')

can simply be converted to a network-aware version via::

    from tdt.dsp_server import RPcoXNET, zBUSNET
    host, port = 'localhost', 13131
    iface = RPcoXNET(address=(host, port))
    iface.ConnectRZ6('GB', 1)
    zbus = zBUSNET(address=(host, port))

Even if you prefer not to use the TDTPy abstraction layer (e.g.
`tdt.DSPProject`, `tdt.DSPCircuit` and `tdt.DSPBuffer`), I highly recommend
using TDTPy to obtain a handle to the ActiveX drivers since we have
monkeypatched the win32com connection to speed up certain calls to the ActiveX
drivers.  To obtain a handle to the standard ActiveX drivers using TDTPy::

    from tdt.util import connect_rpcox, connect_zbus
    iface = connect_rpcox('RZ6')
    zbus = connect_zbus()

To obtain a handle to the network-aware proxy using TDTPy, provide the address
argument::

    from tdt.util import connect_rpcox, connect_zbus
    host, port = 'localhost', 13131
    iface = connect_rpcox('RZ6', address=(host, port))
    zbus = connect_zbus(address=(host, port))

If you're using the TDTPy abstraction layer, simply provide an address argument
when initializing the DSPCircuit class::
    
    from tdt import DSPCircuit
    host, port = 'localhost', 13131
    circuit = DSPCircuit('play_record.rcx', 'RZ6', address=(host, port))

Now that you've rewritten  your code to use the networked version of TDTPy, you
need to start the server.  Open up a command prompt on the host computer and
type::

    >>> python -m tdt.dsp_server :13131

Now, run your client code!

.. note::

    The ActiveX drivers require a path to the circuit file that must be loaded
    to the hardware.  The circuit files *can* be stored on the client.  The network
    proxy, RPcoXNET will handle transferring the circuit files to the server for
    you.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
