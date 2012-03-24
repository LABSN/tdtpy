TDTPy Documentation
===================

.. module:: tdt
    :platform: Windows (requires proprietary ActiveX driver from TDT)
.. moduleauthor:: Brad Buran <bburan@alum.mit.edu>

.. note::

    If you use the server provided by TDTPy to communicate with your hardware
    your client code should be able to run on any platform including Unix, Linux
    and OSX).  The server, however, requires the proprietary ActiveX drivers
    provided by TDT which only run on Windows.

Contents:

.. toctree::
    :maxdepth: 2

    getting_started.rst
    code_examples.rst
    converting.rst
    dsp_circuit.rst
    dsp_buffer.rst
    api.rst
    server_api.rst

.. include:: ../readme.rst

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

.. _National Instruments DAQ platform: http://www.ni.com/dataacquisition/multifunction/
.. _Neurogen: http://bradburan.com/programs-and-scripts/neurogen/
.. _NeuroBehavior: http://bradburan.com/programs-and-scripts/neurobehavior/
.. _Chaco: http://code.enthought.com/projects/chaco/ 
.. _Traits: http://code.enthought.com/projects/traits/ 
.. _TraitsGUI: http://code.enthought.com/projects/traits_gui/ 


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
