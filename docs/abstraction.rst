What is abstraction?
--------------------
A key goal of TDTPy is to provide an abstraction layer between your software and
the hardware you use.  This should facilitate the process of transitioning much
of your code to hardware built by another vendor.  Consider the possible code
for communicating with two (hypothetical) pumps::

>>> import parallel
>>> parallel.Parallel(connection_settings)
>>> parallel.write("VOL\\x03\\x03")
>>> response = parallel.readline(eol='\\x03')
>>> if '?' in response:
...     raise SystemError, "The pump is not working!"
>>> else:
...     print "Volume infused is " + response[4:10]
        
>>> import win32com
>>> import actxobjects
>>> actxobjects.Pump()
>>> volume = pump.GetVolume(1, "GB")
>>> if volume == NaN:
...     raise SystemError, "The pump is messed up!"
>>> else:
...     print "Volume infused is ", volume


If your alb decides to switch over to the new pump and you h

The `volume` method knew how to communicate with the specified pump, so the
program did not need to worry about manufacturer specific logic.  If their pump
ever broke again, they could simply tell the software to use the "Old Northwest"
interface instead.  No longer did the labs need to rewrite each other's
enhancements and additions to work with their preferred pump.  It just worked.

Backends
========

DSP backend
-----------


Pump backend
------------

Right now only one pump (New Era) is supported.  I'm going to briefly expand on
how the API abstraction layer is expected to work.  New Era requires a RS-232
cable to communicate with the computer, along with some pretty arcane syntax.
If we wanted to set the infusion rate on the pump, we would need to:

    1. Know how to initialize the serial port, set it's baud rate, and close it
    properly at program exit.

    2. Remember the manufacturer-specific command syntax for setting the rate.
    Usually it's some string such as "RAT 0.300 MM<CR>".

    3. Know how to parse the pump's response (which conveys information about
    the status of the pump).

So, we'd need to do:

>>> import serial
>>> pump = serial.Serial(connection_settings)
>>> pump.write("RAT 0.300 MM\\n")
>>> result = pump.readline(eol='\\x03')

Result is typically an arcane string along the lines of "01I?".  This string
contains a single letter that indicates the status of the pump.  If the string
indicates there is an error, this needs to be converted into something the
Python exception machinery can handle.  We can typically determine what the
error is by inspecting the response string (e.g. a 'S' indicates the pump motor
is stalled) and raising a PumpHardwareError exception that displays a message
that the user can understand.

>>> from cns import equipment # see a pattern here?
>>> pump = equipment.pump()
>>> pump.rate = 0.3

Better yet, wrap it in a try/except block.

>>> from cns import equipment
>>> try:
...     pump = equipment.pump()
...     pump.rate = 0.3
>>> except PumpCommError:
...     print 'Cannot connect to pump.  Is it turned on?'
>>> except PumpHardwareError:
...     print 'Able to connect to pump, but there is a hardware problem.'

Note that :class:`PumpCommError` and :class:`PumpHardwareError` are subclasses
of :class:`PumpError`.  In turn, :class:`PumpError` is a subclass of
:class:`EquipmentError`.  Both have subclass-specific error messages.  These
error messages should be quite informative and contain information to help the
user solve the problem (e.g.  could they have forgotten to turn on something or
is a cable disconnected?).  If the error message isn't very informative, this is
considered a BUG and should be reported accordingly.  So you could simply do:

>>> from cns import equipment
>>> try:
...     pump = equipment.pump()
...     pump.rate = 0.3
>>> except EquipmentError, e:
...     print e
