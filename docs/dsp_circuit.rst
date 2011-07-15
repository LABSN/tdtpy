:mod:`tdt.dsp_circuit` -- Wrapper for RPvds circuit objects
===========================================================

Wrapper around a RPvds circuit.

>>> from tdt import DSPCircuit
>>> circuit = DSPCircuit('acquire_neurophysiology.rcx', 'RZ5')

Required parameters
-------------------
circuit_name : path
    Absolute or relative path pointing to the file containing the circuit
    microcde (e.g. the \*.rcx file).  
device_name : str
    Target device to load the microcode to (the name will be in the format RP2,
    RX6, RX8, RZ5, RZ6, etc.).  
device_id : int
    Specifies which of the two devices to load the microcode to.  Required only
    if you have more than one of the same device (e.g. two RP2 processors).  Use
    TDT's zBUSmon utility to look up the correct device ID.
load : boolean
    Load the circuit to the device when class is initialized?  True by default.
    Typically you would set it to False when you want to inspect the DSP
    microcode without actually running it.

If you're not sure what to enter for device_name and device_id, use TDT's
zBUSmon utility to look up the correct information.  As shown in the screenshot
below, two devices installed in the system are the RZ5_1 and RZ6_1.  The device
names are RZ5 and RZ6, respectively, while the device ID is 1 for both.  If
zBUSmon reports that you have a RZ5_1 and RZ5_2, then both device names would be
RZ5 while the device ID would be 1 and 2, respectively.

.. image:: zBUSmon_screenshot.*

Available public attributes
---------------------------
fs : float
    Sampling frequency of the circuit
tags : dictionary
    Keys are the tag names (i.e. variables) present in the DSP microcode.
    Values are a tuple of tag size and tag type.  Note that `tdt.constants`
    defines the available tag types.  For simple types (e.g. integer, float and
    boolean), the tag size will always be 1.  For buffer types, the size will
    indicate the number of 32 bit words in the buffer.

Error handling
--------------

Attempting to get/set the value of a nonexistent tag in the circuit will raise a
`DSPError`:

>>> circuit.get_tag('nonexistent_tag')
DSPError: 'nonexistent_tag' not found in circuit
