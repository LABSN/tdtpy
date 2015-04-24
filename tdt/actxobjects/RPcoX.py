# -*- coding: utf-8 -*-
# Created by makepy.py version 0.4.97
# By python version 2.5.2 (r252:60911, Feb 21 2008, 13:11:45) [MSC v.1310 32 bit (Intel)]
# From type library 'RPcoX.ocx'
# On Thu Aug 20 14:23:15 2009
"""RPcoX ActiveX Control module"""
makepy_version = '0.4.97'
python_version = 0x20502f0

import win32com.client.CLSIDToClass, pythoncom
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{D323A622-1D13-11D4-8858-444553540000}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 10
LCID = 0x0

from win32com.client import DispatchBaseClass
class _DRPcoX(DispatchBaseClass):
    """Dispatch interface for RPcoX Control"""
    CLSID = IID('{D323A623-1D13-11D4-8858-444553540000}')
    coclass_clsid = IID('{D323A625-1D13-11D4-8858-444553540000}')

    def AboutBox(self):
        return self._oleobj_.InvokeTypes(-552, LCID, 1, (24, 0), (),)

    def ClearCOF(self):
        return self._oleobj_.InvokeTypes(28, LCID, 1, (3, 0), (),)

    def Connect(self, Interface=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(2, LCID, 1, (3, 0), ((3, 0), (3, 0)),Interface
            , DevNum)

    def ConnectRA16(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(24, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRL2(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(23, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRM1(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        """method ConnectRM1"""
        return self._oleobj_.InvokeTypes(38, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRM2(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        """method ConnectRM2"""
        return self._oleobj_.InvokeTypes(39, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRP2(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(22, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRV8(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(32, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRX5(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        """method ConnectRX5"""
        return self._oleobj_.InvokeTypes(40, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRX6(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        """method ConnectRX6"""
        return self._oleobj_.InvokeTypes(41, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRX7(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        """method ConnectRX7"""
        return self._oleobj_.InvokeTypes(42, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRX8(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        """method ConnectRX8"""
        return self._oleobj_.InvokeTypes(43, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRX9(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        """method ConnectRX9"""
        return self._oleobj_.InvokeTypes(44, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRZ2(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        """method ConnectRZ2"""
        return self._oleobj_.InvokeTypes(45, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRZ3(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        """method ConnectRZ3"""
        return self._oleobj_.InvokeTypes(46, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRZ4(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        """method ConnectRZ4"""
        return self._oleobj_.InvokeTypes(47, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRZ5(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        """method ConnectRZ5"""
        return self._oleobj_.InvokeTypes(48, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def ConnectRZ6(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
        """method ConnectRZ6"""
        return self._oleobj_.InvokeTypes(49, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
            , DevNum)

    def DefStatus(self, DefID=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(36, LCID, 1, (3, 0), ((3, 0),),DefID
            )

    def GetCycUse(self):
        return self._oleobj_.InvokeTypes(27, LCID, 1, (3, 0), (),)

    def GetDefData(self, DefID=defaultNamedNotOptArg):
        return self._ApplyTypes_(37, 1, (12, 0), ((3, 0),), u'GetDefData', None,DefID
            )

    def GetDevCfg(self, Addr=defaultNamedNotOptArg, Width32=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(33, LCID, 1, (3, 0), ((3, 0), (3, 0)),Addr
            , Width32)

    def GetError(self):
        # Result is a Unicode object - return as-is for this version of Python
        return self._oleobj_.InvokeTypes(1, LCID, 1, (8, 0), (),)

    def GetNameOf(self, ObjTypeName=defaultNamedNotOptArg, Index=defaultNamedNotOptArg):
        # Result is a Unicode object - return as-is for this version of Python
        return self._oleobj_.InvokeTypes(20, LCID, 1, (8, 0), ((8, 0), (3, 0)),ObjTypeName
            , Index)

    def GetNames(self, NameList=defaultNamedNotOptArg, MaxNames=defaultNamedNotOptArg, ObjType=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(13, LCID, 1, (3, 0), ((8, 0), (3, 0), (3, 0)),NameList
            , MaxNames, ObjType)

    def GetNumOf(self, ObjTypeName=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(19, LCID, 1, (3, 0), ((8, 0),),ObjTypeName
            )

    def GetSFreq(self):
        return self._oleobj_.InvokeTypes(31, LCID, 1, (4, 0), (),)

    def GetStatus(self):
        return self._oleobj_.InvokeTypes(26, LCID, 1, (3, 0), (),)

    def GetTagSize(self, Name=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(16, LCID, 1, (3, 0), ((8, 0),),Name
            )

    def GetTagType(self, Name=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(17, LCID, 1, (3, 0), ((8, 0),),Name
            )

    def GetTagVal(self, Name=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(8, LCID, 1, (4, 0), ((8, 0),),Name
            )

    def Halt(self):
        return self._oleobj_.InvokeTypes(6, LCID, 1, (3, 0), (),)

    def LoadCOF(self, FileName=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(4, LCID, 1, (3, 0), ((8, 0),),FileName
            )

    def LoadCOFsf(self, FileName=defaultNamedNotOptArg, SampFreq=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(35, LCID, 1, (3, 0), ((8, 0), (4, 0)),FileName
            , SampFreq)

    def ReadCOF(self, FileName=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(21, LCID, 1, (3, 0), ((8, 0),),FileName
            )

    def ReadTag(self, Name=defaultNamedNotOptArg, pBuf=defaultNamedNotOptArg, nOS=defaultNamedNotOptArg, nWords=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(9, LCID, 1, (3, 0), ((8, 0), (16388, 0), (3, 0), (3, 0)),Name
            , pBuf, nOS, nWords)
         # Hex tag is 0x44?  We want it to be of type VTS_PR4

    # For ReadTagV and ReadTagVEX, the default output of makepy is to use
    # _ApplyTypes_ to pass the data through _get_good_object_.  This function
    # slows down the I/O significantly, so we just call InvokeTypes directly.
    #
    # This is a hand-edited version of the makepy output.

    def ReadTagV(self, Name=defaultNamedNotOptArg, nOS=defaultNamedNotOptArg, nWords=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(14, 0, 1, (12, 0), ((8, 0), (3, 0), (3, 0)), Name , nOS, nWords)

    def ReadTagVEX(self, Name=defaultNamedNotOptArg, nOS=defaultNamedNotOptArg, nWords=defaultNamedNotOptArg, SrcType=defaultNamedNotOptArg
            , DstType=defaultNamedNotOptArg, nChans=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(25, 0, 1, (12, 0), ((8, 0), (3, 0), (3, 0), (8, 0), (8, 0), (3, 0)), Name
            , nOS, nWords, SrcType, DstType, nChans
            )

    def Run(self):
        return self._oleobj_.InvokeTypes(5, LCID, 1, (3, 0), (),)

    def SendParTable(self, Name=defaultNamedNotOptArg, IndexID=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(11, LCID, 1, (3, 0), ((8, 0), (4, 0)),Name
            , IndexID)

    def SendSrcFile(self, Name=defaultNamedNotOptArg, SeekOS=defaultNamedNotOptArg, nWords=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(12, LCID, 1, (3, 0), ((8, 0), (3, 0), (3, 0)),Name
            , SeekOS, nWords)

    def SetDevCfg(self, Addr=defaultNamedNotOptArg, Val=defaultNamedNotOptArg, Width32=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(34, LCID, 1, (3, 0), ((3, 0), (3, 0), (3, 0)),Addr
            , Val, Width32)

    def SetSrcFileName(self, Name=defaultNamedNotOptArg, FileName=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(18, LCID, 1, (3, 0), ((8, 0), (8, 0)),Name
            , FileName)

    def SetTagVal(self, Name=defaultNamedNotOptArg, Val=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(3, LCID, 1, (3, 0), ((8, 0), (4, 0)),Name
            , Val)

    def SoftTrg(self, Trg_Bitn=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(7, LCID, 1, (3, 0), ((3, 0),),Trg_Bitn
            )

    def WriteTag(self, Name=defaultNamedNotOptArg, pBuf=defaultNamedNotOptArg, nOS=defaultNamedNotOptArg, nWords=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(10, LCID, 1, (3, 0), ((8, 0), (16388, 0), (3, 0), (3, 0)),Name
            , pBuf, nOS, nWords)

    def WriteTagV(self, Name=defaultNamedNotOptArg, nOS=defaultNamedNotOptArg, Buf=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(15, LCID, 1, (3, 0), ((8, 0), (3, 0), (0x2005, 0)),Name
            , nOS, Buf)

    def WriteTagVEX(self, Name=defaultNamedNotOptArg, nOS=defaultNamedNotOptArg, DstType=defaultNamedNotOptArg, Buf=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(29, LCID, 1, (3, 0), ((8, 0), (3, 0), (8, 0), (0x2005, 0)),Name
            , nOS, DstType, Buf)

    def ZeroTag(self, Name=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(30, LCID, 1, (3, 0), ((8, 0),),Name
            )

    _prop_map_get_ = {
    }
    _prop_map_put_ = {
    }

class _DRPcoXEvents:
    """Event interface for RPcoX Control"""
    CLSID = CLSID_Sink = IID('{D323A624-1D13-11D4-8858-444553540000}')
    coclass_clsid = IID('{D323A625-1D13-11D4-8858-444553540000}')
    _public_methods_ = [] # For COM Server support
    _dispid_to_func_ = {
                1 : "OnDefComplete",
        }

    def __init__(self, oobj = None):
        if oobj is None:
            self._olecp = None
        else:
            import win32com.server.util
            from win32com.server.policy import EventHandlerPolicy
            cpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
            cp=cpc.FindConnectionPoint(self.CLSID_Sink)
            cookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
            self._olecp,self._olecp_cookie = cp,cookie
    def __del__(self):
        try:
            self.close()
        except pythoncom.com_error:
            pass
    def close(self):
        if self._olecp is not None:
            cp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None
            cp.Unadvise(cookie)
    def _query_interface_(self, iid):
        import win32com.server.util
        if iid==self.CLSID_Sink: return win32com.server.util.wrap(self)

    # Event Handlers
    # If you create handlers, they should have the following prototypes:
#   def OnDefComplete(self, DefID=defaultNamedNotOptArg):


from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'RPCO.X'
class RPcoX(CoClassBaseClass): # A CoClass
    # RPcoX Control
    CLSID = IID('{D323A625-1D13-11D4-8858-444553540000}')
    coclass_sources = [
        _DRPcoXEvents,
    ]
    default_source = _DRPcoXEvents
    coclass_interfaces = [
        _DRPcoX,
    ]
    default_interface = _DRPcoX

RecordMap = {
}

CLSIDToClassMap = {
    '{D323A623-1D13-11D4-8858-444553540000}' : _DRPcoX,
    '{D323A624-1D13-11D4-8858-444553540000}' : _DRPcoXEvents,
    '{D323A625-1D13-11D4-8858-444553540000}' : RPcoX,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
}


NamesToIIDMap = {
    '_DRPcoX' : '{D323A623-1D13-11D4-8858-444553540000}',
    '_DRPcoXEvents' : '{D323A624-1D13-11D4-8858-444553540000}',
}


