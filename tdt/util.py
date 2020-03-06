'''
Functions for loading the zBUS, PA5 and RPcoX drivers and connecting to the
specified device.  In addition to loading the appropriate ActiveX driver, some
minimal configuration is done.

Network-aware proxies of the zBUS and RPcoX drivers have been written for
TDTPy. To connect to TDT hardware that is running on a remote computer, both
the :func:`connect_zbus` and :func:`connect_rpcox` functions take the address
of the server via a tuple (hostname, port)::

    connect_rpcox('RZ6', address=(tdt_server.cns.nyu.edu, 3333))

.. autofunction:: connect_zbus
.. autofunction:: connect_rpcox
.. autofunction:: connect_pa5

.. note::

    The network-aware proxy code should be considered alpha stage.  Although it
    appears to work in our tests, we have not deployed this in our data
    aqcuisition experiments.

'''
import os
import numpy as np
import ctypes

# Initialize
import pythoncom

import pywintypes

from .dsp_error import DSPError
from . import dsp_server, actxobjects

import logging
log = logging.getLogger(__name__)


def connect_pa5(interface='GB', device_id=1, address=None):
    '''
    Connect to the PA5
    '''
    debug_string = '%d via %s interface' % (device_id, interface)
    log.debug(debug_string)
    try:
        pythoncom.CoInitialize()
        if address is None:
            driver = actxobjects.PA5x()
        else:
            driver = dsp_server.PA5NET(address)
        if not driver.ConnectPA5(interface, device_id):
            raise DSPError("PA5", "Connection failed")
        log.debug("Connected to PA5")

        return driver
    except pywintypes.com_error:
        raise ImportError('ActiveX drivers from TDT not installed')


def connect_zbus(interface='GB', address=None):
    '''
    Connect to the zBUS interface and set the zBUS A and zBUS B triggers to low

    Parameters
    ----------
    interface : {'GB', 'USB'}
        Type of interface (depends on the card that you have from TDT). See the
        TDT ActiveX documentation for clarification on which interface you
        would be using if you are still unsure.
    address : {None, (hostname, port)}
        If None, loads the ActiveX drivers directly, otherwise connects to the
        remote server specified by the hostname, port tuple.
    '''
    try:
        pythoncom.CoInitialize()
        if address is not None:
            driver = dsp_server.zBUSNET(address)
        else:
            driver = actxobjects.ZBUSx()
        if not driver.ConnectZBUS(interface):
            raise DSPError("zBUS", "Connection failed")
        log.debug("Connected to zBUS")

        # zBUS trigger is set to high for record mode, so ensure that both
        # triggers are initialized to low.
        driver.zBusTrigA(0, 2, 10)
        driver.zBusTrigB(0, 2, 10)
        log.debug("Set zBusTrigA to low")
        log.debug("Set zBusTrigB to low")
        return driver
    except pywintypes.com_error:
        raise ImportError('ActiveX drivers from TDT not installed')


def connect_rpcox(name, interface='GB', device_id=1, address=None):
    '''
    Connect to the specifed device using the RPcoX driver

    Note that the appropriate RPcoX.Connect method is called so you do not need
    to perform that step in your code.

    Parameters
    ----------
    name : {'RZ6', 'RZ5', 'RP2', ... (any valid device string) }
        Name of device (as defined by the corresponding RPcoX.Connect* method).
    interface : {'GB', 'USB'}
        Type of interface (depends on the card that you have from TDT). See the
        TDT ActiveX documentation for clarification on which interface you
        would be using if you are still unsure.
    device_id : int (default 1)
        Id of device in the rack.  Only applicable if you have more than one of
        the same device (e.g. two RX6 devices).
    address : {None, (hostname, port)}
        If None, loads the ActiveX drivers directly, otherwise connects to the
        remote server specified by the hostname, port tuple.
    '''
    pythoncom.CoInitialize()
    debug_string = '%s %d via %s interface' % (name, device_id, interface)
    log.debug(debug_string)
    if address is None:
        driver = actxobjects.RPcoX()
    else:
        driver = dsp_server.RPcoXNET(address)
    if not getattr(driver, 'Connect%s' % name)(interface, device_id):
        raise DSPError(name, "Connection failed")
    log.debug("Connected to %s", name)
    return driver


def get_cof_path(circuit_name):
    '''
    Given relative path, returns absolute path to circuit file.  The *.rcx
    extension may be omitted.
    '''
    search_dirs = [os.path.join(os.path.dirname(__file__), 'components'),
                   os.getcwd(), ]
    log.debug("Searching %r", search_dirs)

    success = False
    if not circuit_name.endswith('.rcx'):
        circuit_name += '.rcx'

    log.debug("Attempting to locate circuit %s", circuit_name)
    for dir in search_dirs:
        circuit_path = os.path.join(dir, circuit_name)
        log.debug('Checking %s', circuit_path)
        if os.path.exists(circuit_path):
            success = True
            break

    if not success:
        raise IOError("Could not find circuit %s" % circuit_name)
    return circuit_path


def dtype_to_type_str(data_type):
    '''
    Convert Numpy dtype to the type string required by TDT's libraries

    TDT's ActiveX ReadTagVEX and WriteTagVEX functions require the type string
    to be one of I8, I16, I32 or F32.  Any valid format for specify Numpy dtype
    is supported.

    >>> dtype_to_type_str(np.int32)
    'I32'
    >>> dtype_to_type_str(np.float32)
    'F32'
    >>> dtype_to_type_str('float32')
    'F32'
    >>> dtype_to_type_str('int8')
    'I8'

    If a certain type is not supported by TDT, a Value error is raised:

    >>> dtype_to_type_str(np.float16)
    Traceback (most recent call last):
        ...
    ValueError: Unsupported Numpy dtype
    '''
    if np.issubdtype(data_type, np.integer):
        type_code = 'I'
    elif np.issubdtype(data_type, np.floating):
        type_code = 'F'
    else:
        raise ValueError("Unsupported Numpy dtype")

    # Since dtype.itemsize is the number of bytes, and the number in the TDT
    # type string reflects bit number, we can translate it by multiplying by 8.
    # Likewise, dtype.char is 'i' for integer and 'f' for floating point
    # datatypes.
    type_str = "{0}{1}".format(type_code, data_type.itemsize*8)
    log.debug("%r TDT type string is %s", data_type, type_str)
    if type_str not in ['F32', 'I32', 'I16', 'I8']:
        raise ValueError("Unsupported dtype")
    return type_str


def best_sf(data_type, range):
    '''
    Computes the optimal scaling factor for data compression

    Parameters
    ----------
    data_type
        Data type that values are being compressed to
    range : scalar or tuple
        Expected data range.  If scalar, assumes the value falls in the range
        (-range, range)
    '''
    data_type = np.dtype(data_type)
    try:
        info = np.iinfo(data_type)
    except:
        info = np.finfo(data_type)
    return info.max/np.abs(range).max()


def resolution(data_type, scaling_factor):
    '''
    Computes resolution for data type given scaling factor

    Parameters
    ----------
    data_type : dtype
        Numpy data type (or string)
    scaling_factor : float
        Scaling factor applied to data
    '''
    data_type = np.dtype(data_type)
    if np.issubdtype(data_type, np.integer):
        return 1/float(scaling_factor)
    else:
        raise ValueError("Float data types not supported")

CTYPES_TO_NP = {
    ctypes.c_char: np.int8,
    ctypes.c_wchar: np.int16,
    ctypes.c_byte: np.int8,
    ctypes.c_ubyte: np.uint8,
    ctypes.c_short: np.int16,
    ctypes.c_ushort: np.uint16,
    ctypes.c_int: np.int32,
    ctypes.c_uint: np.int32,
    ctypes.c_long: np.int32,
    ctypes.c_ulong: np.int32,
    ctypes.c_float: np.float32,
    ctypes.c_double: np.float64,
}
# Reverse lookup
NP_TO_CTYPES = dict((np.dtype(v), k) for k, v in CTYPES_TO_NP.items())


def shmem_as_ndarray(raw_array):
    '''
    Create a ndarray wrapper around shared memory space
    '''
    address = raw_array._wrapper.get_address()
    size = raw_array._wrapper.get_size()
    dtype = CTYPES_TO_NP[raw_array._type_]

    class NDArrayView(object):
        pass

    d = NDArrayView()
    d.__array_interface__ = {
        'data': (address, False),
        'typestr': np.dtype('uint8').str,
        'descr': np.dtype('uint8').descr,
        'shape': (size,),
        'strides': None,
        'version': 3,
    }
    return np.asarray(d).view(dtype=dtype)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
