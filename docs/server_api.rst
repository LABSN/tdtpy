DSP Server API
==============

Since all TDT devices share the same connection with the computer, we can only
talk to a single device at a time.  Unfortunately, TDT's hardware drivers do not
handle the requisite concurrent access issues, meaning that only one program
and/or process can safely use the hardware connection (e.g. the optical or USB
interface) at a time even if each process communicates with a different device.
If you have two separate programs (one for generating the stimulus and one for
data acquisition), TDTPy can handle the requisite concurrency issues.

TDTPy provides a server that manges all communication with the TDT hardware,
allowing multiple client processes to communicate safely with the hardware via
the server.  Client processes communicate with the server via network-aware
proxies of the RPcoX, PA5 and zBUS drivers.  The network-aware drivers will
relay all method calls to the server and block until the server returns a
response.  This is certainly not the most efficient way to handle the system
(e.g. if the server is busy handling a request from another process it may take
longer to receive a response).

This server is also useful for people who wish to run their code on a separate
computer (e.g. Linux or Mac OSX) while maintaining a Windows computer to run the
DSP server.

.. note::

    This code definitely works, and is reasonably fast on a localhost
    connection.  When I tested it via a client connecting using the wireless
    network there were some latency issues.  There are likely many speedups that
    can be implemented, but I don't have the time to do so right now.


Running the server
------------------

To launch the server, go to the host computer and run the following command::

    c:\\> python -m tdt.dsp_server :3333

The string `:3333` specifies which port the server listens on.

Code example
------------

Running a client process is as simple as providing an address argument to
DSPCircuit::

    from tdt import DSPCircuit
    address = ('localhost', 3333)
    circuit = DSPCircuit('record_microphone.rcx', 'RZ6', address=address)
    circuit.start()

.. note::

    The circuit files must be stored on the client.  The network proxy, RPcoXNET
    will handle transferring the circuit files to the server for you.

Converting existing code
------------------------

Assuming your code uses `win32com.client` directly rather than using TDTPy's
abstraction layer, the following code::

    from win32com.client import Dispatch
    iface = Dispatch('RPco.X')
    iface.ConnectRZ6('GB', 1)
    zbus = Dispatch('ZBUSx')

can simply be converted to a network-aware version via::

    from tdt.dsp_server import RPcoXNET, zBUSNET
    host, port = 'localhost', 3333
    iface = RPcoXNET(address=(host, port))
    iface.ConnectRZ6('GB', 1)
    zbus = zBUSNET(address=(host, port))

Even if you prefer not to use the TDTPy abstraction layer (e.g.
:class:`DSPProject`, :class:`DSPCircuit` and :class:`DSPBuffer`), I highly
recommend using TDTPy to obtain a handle to the ActiveX drivers since we have
patched the win32com connection to speed up certain calls to the ActiveX
drivers.  To rewrite the code above that utilizes the patched version of the
ActiveX drivers using TDTPy::

    from tdt.util import connect_rpcox, connect_zbus
    iface = connect_rpcox('RZ6', address=('localhost', 3333))
    zbus = connect_zbus(address=('localhost', 3333))

If you're using the TDTPy abstraction layer, simply provide an address argument
when initializing the DSPCircuit class::
    
    from tdt import DSPCircuit
    host, port = 'localhost', 3333
    circuit = DSPCircuit('play_record.rcx', 'RZ6', address=(host, port))

Server implementation
---------------------

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
rewrite your code to use :class:`DSPProject` or :class:`DSPCircuit`.

The core client classes for communicating with the server are `RPcoXNET`,
`PA5NET` and `zBUSNET` tha serve as a duck-typed proxy of the ActiveX drivers
provided by TDT::

    from tdt.dsp_server import RPcoXNET
    client = RPcoXNET('localhost', 3333)
    client.ConnectRZ5('GB', 1)
    client.LoadCOF(cof_path)

Currently all method calls are simply relayed to the server, so what's really
going on under the hood is that the call::

    client.ConnectRZ5('GB', 1)

Is translated to::

    client._send('RZ5', 'ConnectRZ5', ('GB', 1))
    return client._recv()

Alternatively, the above can be achieved via::

    from tdt.util import connect_rpcox
    client = connect_rpcox('GB', 1, ('localhost', 3333))

The \*.rcx files need to be stored on the client.  They are uploaded to the
server when the LoadCOF method is called.
