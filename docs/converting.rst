Converting your code from Matlab or Python to use TDTPy
=======================================================

Connecting to a device and loading a circuit
--------------------------------------------

Matlab::
        
    iface = actxserver('RPco.X');
    if iface.ConnectRZ6('GB', 1) == 0 
        disp 'connect error'; 
    end
    if iface.ClearCOF == 0 
        disp 'clear error'; 
    end
    if iface.LoadCOF('record_microphone.rcx') == 0 
        disp 'load error'; 
    end
    if iface.Run == 0 
        disp 'run error'; 
    end

Python::

    from win32com.client import Dispatch
    try:
        pass
        iface = Dispatch('RPco.X')
        if not iface.ConnectRZ6('GB', 1):
            raise SystemError, 'connect error'
        if not iface.ClearCOF():
            raise SystemError, 'clear error'
        if not iface.LoadCOF('record_microphone.rcx'):
            raise SystemError, 'load error'
        if not iface.Run():
            raise SystemError, 'run error'
    except SystemError, e:
        print "Error: {}".format(e)

TDTPy::

    from tdt import DSPCircuit
    try:
        circuit = DSPCircuit('record_microphone', 'RZ6')
        circuit.start()
        circuit.stop()
    except DSPError, e:
        print "Error: {}".format(e)

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
    duration = circuit.cget_tag('record_dur_n', 'n', 's')

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
