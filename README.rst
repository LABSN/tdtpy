=====
TDTPy
=====

.. image:: https://zenodo.org/badge/doi/10.5281/zenodo.17651.svg   
   :target: http://dx.doi.org/10.5281/zenodo.17651

TDTPy is a Python wrapper around `Tucker-Davis Technologies`_ `ActiveX library`_
[PDF link] (known as RPcoX) for communicating with their System 3 hardware (e.g.
the RP2.1, RX6, RZ6, etc.).

In addition to the standard operations (loading
circuits, configuring tags and reading/writing to hardware buffers), TDTPy
offers a number of high-level features that are not included in the ActiveX
library:

* **Handling type conversion** between analog and digital units (e.g. converting
  seconds to number of DSP cycles based on the CPU frequency of the hardware).
* **Remote procedure call (RPC) server** for allowing multiple processes and/or programs
  to communicate with the hardware across the same connection. The drivers
  provided by TDT do not handle concurrency issues. To handle these issues, we
  have created a RPC server that handles concurrency issues, allowing multiple
  programs to talk to the hardware simultaneously. The programs can either run
  on the same computer or on a separate computer.
* If you use the RPC server, your client code can run on **any platform** (e.g. Mac
  OSX, Unix, Solaris, etc); however, the server must run on a Windows-based
  computer.
* **Simple reads and writes.** The hardware buffers are implemented as "ring
  buffers" with various features such as multichannel storage and data
  compression. TDTPy automatically detects the configuration of the hardware
  buffer and returns a buffer object (`DSPBuffer`) that you can read/write
  to without having to deal with the intricacies of the hardware buffer itself.
* **Robust error handling.** Some methods in the ActiveX library will fail silently
  (e.g. if you try to access a nonexistent tag, attempt to write more data than
  the hardware buffer can hold, or wire up a tag to a static port). When the
  RPvds circuit is first loaded to the hardware, TDTPy will inspect the
  microcode (i.e. the RPvds circuit) and store some information about the tags
  and buffers available. All subsequent operations are validated against this
  metadata before being passed to the ActiveX library. If an invalid operation
  is attempted, a DSPError is raised with the appropriate message.

.. _Tucker-Davis Technologies: http://www.tdt.com
.. _System 3: http://www.tdt.com/products.htm 
.. _ActiveX library: http://www.tdt.com/T2Download/manuals/ActiveX_User_Reference.pdf

The minimum required dependencies to run the software are:

  - Python >= 3.7
  - NumPy >= 1.8
  - pywin32

-------
License
-------
TDTPy is distributed under the BSD license.

------------
Contributors
------------
* Brad Buran (New York University, Oregon Health & Science University)
* Eric Larson (University of Washington)
* Decibel Therapeutics, Inc.
