from comtypes import client
from numpy import random, equal, ones
from array import array
from win32com import client as wclient
from actxobjects import RPcoX

com_iface = client.CreateObject('RPco.X')
win_iface = wclient.Dispatch('RPco.X')
#mod_iface = RPcoX()

data = random.normal(size=100e3)
from timeit import timeit
setup = "from __main__ import iface, data, array"
n = 4

for iface in (com_iface, win_iface):
    print 'Testing', iface
    iface.ConnectRZ6('GB', 1)
    iface.LoadCOF('components/test_physiology_RZ6.rcx')
    iface.Run()

    try:
        print "ndarray\t", iface.WriteTagV('speaker', 0, data)
    except:
        print "error"
    print "list\t", iface.WriteTagV('speaker', 0, data.tolist())
    print "array\t", iface.WriteTagV('speaker', 0, array('d', data))

    print "Testing speed of calling WriteTagV"
    try:
        t = timeit("iface.WriteTagV('speaker', 0, data)", setup, number=4)/4
        print "ndarray\t", t
    except:
        print "error"
    t = timeit("iface.WriteTagV('speaker', 0, data.tolist())", setup, number=4)/4
    print "list\t", t
    t = timeit("iface.WriteTagV('speaker', 0, array('d', data))", setup, number=4)/4
    print "array\t", t

    print "Testing speed of calling ReadTagV"
    t = timeit("iface.ReadTagV('speaker', 0, 200e3)", setup, number=4)/4
    print t
