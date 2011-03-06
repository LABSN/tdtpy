See <URL> for information on a custom modification to the win32com file that
optimizes transfer of large arrays of data.

To read from a buffer on a TDT DSP via the COM interface:

>>> from tdt.actxobjects import RX6
>>> RX6.ConnectRX6('GB', 1)
>>> RX6.ClearCOF()
>>> RX6.LoadCOF('basic-characterization.rcx')
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

This is a lot of boilerplate code just to load the microcode into the hardware
and initialize it.  In addition, just reading data from the buffer requires you
to continuously track the last index you read and check to see if the buffer has
wrapped around to the beginning.

>>> from tdt import DSPCircuit
>>> circuit = DSPCircuit('basic-characterization', 'RX6')
>>> buffer = circuit.get_buffer('neural')
>>> while True:
...     data = buffer.next()
...     if some_condition_met:
...         break
>>> # do something with the data

To write data to a buffer on the hardware:

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

Both approaches are fine; however, we recommend that you use `DSPCircuit.cset_tag`
whenever possible since this makes the code more readable.  Now that you've
configured the circuit and are ready to record:

>>> import time
>>> circuit.trigger(1)
>>> time.sleep(1)
>>> microphone = circuit.microphone.read()
