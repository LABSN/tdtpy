from io import StringIO
import pickle
from tempfile import NamedTemporaryFile
import uuid
import socket
import struct
from select import select
import numpy as np
import logging
import os

# Required so that sphinx can build this on readthedocs.org
from . import actxobjects

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

TYPE_NUMPY_DATA = 0
TYPE_PICKLE_DATA = 1

# Result codes
SUCCESS = 2**0
DEV_NOT_CONNECTED = 2**1
DEV_CONNECTED = 2**2
TAG_MISSING = 2**3


def _write_preamble(sock, mid, nbytes, protocol=0):
    preamble = struct.pack('!IIH', mid, nbytes, protocol)
    sock.sendall(preamble)


def _read_preamble(sock):
    mid, nbytes, protocol = struct.unpack('!IIH', sock.recv(10))


def _read(sock):
    preamble = sock.recv(10)
    if preamble == '':
        raise socket.error('transmission terminated')
    mid, size, protocol = struct.unpack('!IIH', preamble)
    log.debug('reading message id %d with %d bytes', mid, size)
    sock.settimeout(10)

    # Ensure we load the entire buffer.  This is a blocking operation and
    # probably should be optimized away.  However, this is required for for
    # reading the raw *.rcx binary data from the client.  All other methods I
    # have tested don't require this loop.
    message = StringIO()
    while True:
        message.write(sock.recv(size))
        if message.tell() == size:
            break
    return mid, protocol, message.getvalue()


def write(sock, mid, data):
    '''
    Two protocols are currently supported.  Both share a common header format.
    '''
    # If the data is a numpy array, it is much faster to simply serialize it
    # using Numpy's own protocol.  Pickle is about 4x slower.  For all other
    # datatypes, default to the Pickle protocol.
    if isinstance(data, np.ndarray):
        size = len(data.dtype.str) + len(data.data)
        _write_preamble(sock, mid, size, TYPE_NUMPY_DATA)
        sock.sendall(data.dtype.str)
        sock.sendall(data.data)
    else:
        message = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        _write_preamble(sock, mid, len(message), TYPE_PICKLE_DATA)
        sock.sendall(message)


def read(sock):
    mid, protocol, message = _read(sock)
    if protocol == TYPE_NUMPY_DATA:
        data = np.fromstring(message[3:], dtype=message[:3])
    elif protocol == TYPE_PICKLE_DATA:
        data = pickle.loads(message)
    return mid, data


class TDTRPCServer(object):
    '''
    Remote procedure call server for communicating with TDT's System 3 hardware

    The server maintains a list of all the TDT devices that the server is
    currently communicating with.  Note that all TDT devices share the same
    connection with the computer, so we can only talk to a single device at a
    time.  Since this server processes each request sequentially rather than
    spawining each connection off to a separate thread, concurrency is handled
    by the select() loop in `run_forever`.  A thread-based design was
    considered; however, the bottleneck currently is in the optical interface
    I/O speed so it is unlikely that the additional hassle and overhead of
    threading will provide any significant performance gain.

    This is meant to be a relatively thin layer around the ActiveX device
    driver.  All messages contain a preamble (header) consisting of an integer
    (message id), half-integer (typecode) and integer (message size).  The
    message consists of three-element tuple (device_name, command_name, *args)
    where:

        device_name
            The name that you used when creating the initial connection attempt
            (e.g. the call to ConnectRZ5, Connect RX8, etc.).  Following the
            initial connection attempt, you will use that name to indicate
            which device is the target of subsequent commands.  Typically this
            name will be the device ID (e.g. 'RP2', 'RX8', 'RZ6', etc.), but
            you can certainly assign IDs such 'stim' and 'acq'.

        method_name
            The name of the command to call on the ActiveX object associated
            with the device indicated by device_name.

        args
            Tuple of arguments that will be unpacked when calling the method on
            the ActiveX object
    '''

    def __init__(self, address, connections=2, interface='GB'):
        self._connections = 2
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind(address)
        self._server.listen(connections)
        self._socks = [self._server]
        log.info('server running on %s:%s', *address)

        # A list of all devices that the server is connected to.  Since each
        # device has its own COM object instance, we need to maintain a map of
        # the device to the appropriate instance.
        self._iface = {}

        # Connect to the hardware
        self._interface = interface
        self._zbus = actxobjects.ZBUSx()
        self._zbus.ConnectZBUS(interface)
        # self._rpcox = actxobjects.RPcoX()
        # self._PA5 = actxobjects.PA5x()

    def run_forever(self, poll_interval=0.5):
        socks = self._socks
        server = self._server

        while True:
            # Timeout should be set to something reasonably low so that Ctrl-C
            # forces the server to exit without waiting forever.
            sread, swrite, serr = select(socks, socks, [], poll_interval)
            for sock in sread:
                if sock == server:
                    # This is an incoming connection request, let's accept it
                    # and set it up with the system.
                    self.handle_accept()
                else:
                    # This is probably a remote procedure call request from one
                    # of the clients.  Let's attempt to process the request  If
                    # an error is raised during the attempt, this most likely
                    # means the socket disconnected.
                    try:
                        self.handle_read(sock)
                    except socket.error:
                        self.handle_disconnect(sock)

    def handle_disconnect(self, sock):
        host, port = sock.getpeername()
        log.info('client from %s:%s disconnected', host, port)
        sock.close()
        self._socks.remove(sock)

    def handle_accept(self):
        new, (host, port) = self._server.accept()
        new.setblocking(0)
        self._socks.append(new)
        log.info('client from %s:%s connected', host, port)

    def handle_read(self, sock):
        mid, (uuid, driver, command, args) = read(sock)
        log.info('RPC request %s from %s', command, uuid)
        if command.startswith('Connect'):
            self._iface[uuid] = getattr(actxobjects, driver)()
            result = getattr(self._iface[uuid], command)(*args)
        elif command in ('LoadCOF', 'LoadCOFsf', 'ReadCOF'):
            # This is one of the TDT methods that requires a string filename.
            # Since the client is sending the data via a binary conneciton, we
            # need to convert this binary data into a temporary file whose name
            # can be passed to the method.  On platforms >= Windows NT, the
            # temporary file must be closed before it can be opened a second
            # time for reading (e.g. by the ActiveX object).  To ensure that we
            # can open it again a second time, we need to ensure that it is not
            # auto-deleted when closed.  NOTE: The *.rcx extension is required
            # for the LoadCOF method to recognize the file.
            fh = NamedTemporaryFile(suffix='.rcx', delete=False)
            fh.write(args[0])
            fh.close()
            log.info('Created temporary file %s for RCX circuit', fh.name)

            # Replace the binary file data in the argument list for the method
            # with the path to the temporary file
            args = list(args)
            args[0] = fh.name
            result = getattr(self._iface[uuid], command)(*args)
            # Now, close the temporary file we created
            os.unlink(fh.name)
        else:
            result = getattr(self._iface[uuid], command)(*args)
        write(sock, mid, result)


class _Method(object):
    '''
    Bind a RPC method to a RPC server
    '''

    def __init__(self, name, send):
        self._name = name
        self._send = send

    def __call__(self, *args):
        return self._send(self._name, *args)


class _NET(object):

    def __init__(self, address=('localhost', 13131)):
        cn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cn.connect(address)
        self._cn = cn
        self._mid = -1
        self._results = {}
        self._uuid = str(uuid.uuid4())

    def _send(self, command, *args):
        '''
        Send command to server for execution.  Returns ID that can be used to
        look up the status of the command later.
        '''
        self._mid += 1
        write(self._cn, self._mid, (self._uuid, self.driver, command, args))
        return self._receive(self._mid)

    def _receive(self, mid, timeout=None):
        new_mid, result = read(self._cn)
        if new_mid == mid:
            return result
        else:
            raise Exception

    def __getattr__(self, name):
        return _Method(name, self._send)


class PA5NET(_NET):
    '''
    Remote procedure call client used in conjunction with the TDTRPCSever

    This is essentially a network-aware version of the PA5x object that is
    designed to be a drop-in replacement (i.e. it supports all the methods and
    attributes of the native PA5x object).  Must be used in conjunction with
    TDTRPCServer.  TDTRPCServer handles concurrency issues, allowing multiple
    threads, processes and computers to connect to the hardware simultaneously.
    '''

    driver = 'PA5x'


class zBUSNET(_NET):
    '''
    Remote procedure call client used in conjunction with the TDTRPCSever

    This is essentially a network-aware version of the zBUS object that is
    designed to be a drop-in replacement (i.e. it supports all the methods and
    attributes of the native zBUS object).  Must be used in conjunction with
    TDTRPCServer.  TDTRPCServer handles concurrency issues, allowing multiple
    threads, processes and computers to connect to the hardware simultaneously.
    '''

    driver = 'ZBUSx'


class RPcoXNET(_NET):
    '''
    Remote procedure call client used in conjunction with the TDTRPCSever

    This is essentially a network-aware version of the RPcoX object that is
    designed to be a drop-in replacement (i.e. it supports all the methods and
    attributes of the native RPcoX object).  Must be used in conjunction with
    TDTRPCServer.  TDTRPCServer handles concurrency issues, allowing multiple
    threads, processes and computers to connect to the hardware simultaneously.

    Note that a few methods may require special handling (e.g. LoadCOF) and are
    stubbed out as a result.
    '''

    driver = 'RPcoX'

    def LoadCOF(self, filename):
        '''
        Note that the legacy *.rco format is currently not supported!  You must
        send the *.rcx file.
        '''
        with open(filename, 'rb') as fh:
            return self._send('LoadCOF', fh.read())

    def LoadCOFsf(self, filename, sf):
        '''
        Note that the legacy *.rco format is currently not supported!  You must
        send the *.rcx file.
        '''
        with open(filename, 'rb') as fh:
            return self._send('LoadCOFsf', fh.read(), sf)


def test_client():
    from dsp_project import DSPProject
    project = DSPProject(address=('localhost', 13131))
    filename = ('e:/programs/development/src/neurobehavior/'
                'components/positive-behavior-v2.rcx')
    circuit = project.load_circuit(filename, 'RZ6')  # noqa
    # print circuit.tags
    # circuit.start()
    # time

    # from util import connect_rpcox, connect_zbus
    # zbus = connect_zbus(('localhost', 13131))
    # iface = connect_rpcox('RZ6', 1, ('localhost', 13131))
    # print iface.ConnectRZ6('GB', 1)
    # print iface.LoadCOF(
    # print iface.Run()
    # print iface.GetTagVal('resp_dur_n')
    # print iface.Halt()
    # client = TDTClient()
    # mid = client.execute('RZ6', 'ConnectRZ6', 'GB', 1)
    # print client.get_result(mid)
    # mid = client.execute('RZ6', 'SetTagVal', 'duration', 5)
    # print client.get_result(mid)

if __name__ == '__main__':
    import argparse

    class ParseAddress(argparse.Action):

        def __call__(self, parser, args, value, option_string=None):
            host, port = value.split(':')
            setattr(args, self.dest, (host, int(port)))

    parser = argparse.ArgumentParser(description='Run TDT System 3 RPC server')
    parser.add_argument('address', action=ParseAddress, default=('', 3333))
    args = parser.parse_args()
    TDTRPCServer(address=args.address).run_forever()
