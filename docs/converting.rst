Converting your code from Matlab or Python to use TDTPy
=======================================================

Connecting to a device and loading a circuit
--------------------------------------------

Matlab::
        
    iface = actxserver('RPco.X');
    iface.ConnectRZ6('GB', 1);
    iface.ClearCOF;
    iface.LoadCOF('record_microphone.rcx');
    iface.Run
    iface.Halt

Python::

    from win32com.client import Dispatch
    iface = Dispatch('RPco.X')
    iface.ConnectRZ5('GB', 1)
    iface.ClearCOF()
    iface.LoadCOF('record_microphone.rcx')
    iface.Run()
    iface.Halt()

TDTPy::

    from tdt import DSPCircuit
    circuit = DSPCircuit('record_microphone', 'RZ6')
    circuit.start()
    circuit.stop()

Getting/Setting a tag value
---------------------------

Matlab::

    iface.SetTagVal('nHi', 5);
    fs = iface.GetSFreq();
    delay = 25/1000*fs;
    iface.SetTagVal('record_del_n', delay);
    duration = iface.GetTagVal('record_dur_n')/fs;

Python::

    iface.SetTagVal('nHi', 5)
    fs = iface.GetSFreq()
    delay = 25e-3*fs
    iface.SetTagVal('record_del_n', delay)
    duration = iface.GetTagVal('record_dur_n')/fs

TDTPy::

    circuit.set_tag('nHi', 5)
    circuit.cset_tag('record_del_n', 25, 's', 'n')
    duration = circuit.cget_tag('record_dur_n', 's', 'n')

Writing data to a buffer
------------------------

Matlab::
    
    iface.WriteTagV('speaker', 0, data);

Python::

    iface.WriteTagV('speaker', 0, data)

TDTPy::

    speaker = iface.get_buffer('speaker', 'w')
    speaker.write(data)

Reading data from a buffer
--------------------------

Matlab::
    
    size = iface.GetTagV('mic_i');
    data = iface.ReadTagV('speaker', 0, size);

Python::

    size = iface.GetTagV('mic_i')
    data = iface.ReadTagV('speaker', 0, size)

TDTPy::

    mic = iface.get_buffer('mic', 'r')
    data = mic.read()
