from comtypes import client
from numpy import random
from array import array
from win32com import client as wclient
from timeit import timeit

from .actxobjects import RPcoX

com_iface = client.CreateObject('RPco.X')
win_iface = wclient.Dispatch('RPco.X')
mod_iface = RPcoX()

data = random.normal(size=100e3)
setup = "from __main__ import iface, data, array"
n = 4


def test_iface(iface):
    iface.ConnectRZ6('GB', 1)
    iface.LoadCOF('components/test_physiology_RZ6.rcx')
    iface.Run()

    print("checking to see which datatypes are supported")
    try:
        print("ndarray\t", iface.WriteTagV('speaker', 0, data))
    except:
        print("error")
    print("list\t", iface.WriteTagV('speaker', 0, data.tolist()))
    print("array\t", iface.WriteTagV('speaker', 0, array('d', data)))

    print("Testing speed of calling WriteTagV")
    try:
        t = timeit("iface.WriteTagV('speaker', 0, data)", setup, number=n)/n
        print("ndarray\t", t)
    except:
        print("error")
    t = timeit("iface.WriteTagV('speaker', 0, data.tolist())",
               setup, number=n)/n
    print("list\t", t)
    t = timeit("iface.WriteTagV('speaker', 0, array('d', data))",
               setup, number=n)/n
    print("array\t", t)

    print("Testing speed of calling ReadTagV")
    t = timeit("iface.ReadTagV('speaker', 0, 200e3)", setup, number=n)/n
    print(200e3*4/t/2**20, "MB/sec")

if __name__ == '__main__':
    # print "Testing win32com"
    # iface = win_iface
    # test_iface(iface)
    # print "Testing comtypes"
    # iface = com_iface
    # test_iface(iface)
    print("Testing modified win32com")
    iface = mod_iface
    test_iface(iface)
