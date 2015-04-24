# -*- coding: utf-8 -*-
# Created by makepy.py version 0.5.00
# By python version 2.6.6 |EPD 6.3-2 (32-bit)| (r266:84292, Sep 20 2010, 11:26:16) [MSC v.1500 32 bit (Intel)]
# From type library 'TTankInterfaces.ocx'
# On Thu Dec 02 21:00:50 2010
"""TTankInterfaces"""
makepy_version = '0.5.00'
python_version = 0x20606f0

import win32com.client.CLSIDToClass, pythoncom, pywintypes
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{831D8AF7-7E2B-426B-A430-18E670F56C12}')
MajorVersion = 10
MinorVersion = 9
LibraryFlags = 10
LCID = 0x0

from win32com.client import DispatchBaseClass
class _BlockSelect(DispatchBaseClass):
	CLSID = IID('{C2F42E9B-86B7-4F21-889D-8B854B019640}')
	coclass_clsid = IID('{CB81F5AF-7625-4F83-B629-54C37B55A203}')

	def Refresh(self):
		return self._oleobj_.InvokeTypes(1610809385, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"ActiveBlock": (1745027109, 2, (8, 0), (), "ActiveBlock", None),
		"AllowDragDrop": (1745027114, 2, (11, 0), (), "AllowDragDrop", None),
		"AllowPopup": (1745027115, 2, (11, 0), (), "AllowPopup", None),
		"HideDetails": (1745027110, 2, (11, 0), (), "HideDetails", None),
		"ShowDate": (1745027106, 2, (11, 0), (), "ShowDate", None),
		"ShowDuration": (1745027103, 2, (11, 0), (), "ShowDuration", None),
		"ShowMemo": (1745027101, 2, (11, 0), (), "ShowMemo", None),
		"ShowOwner": (1745027102, 2, (11, 0), (), "ShowOwner", None),
		"ShowServer": (1745027108, 2, (11, 0), (), "ShowServer", None),
		"ShowStart": (1745027105, 2, (11, 0), (), "ShowStart", None),
		"ShowStop": (1745027104, 2, (11, 0), (), "ShowStop", None),
		"ShowTank": (1745027107, 2, (11, 0), (), "ShowTank", None),
		"SingleClickSelect": (1745027100, 2, (11, 0), (), "SingleClickSelect", None),
		"UseServer": (1745027112, 2, (8, 0), (), "UseServer", None),
		"UseTank": (1745027111, 2, (8, 0), (), "UseTank", None),
	}
	_prop_map_put_ = {
		"ActiveBlock": ((1745027109, LCID, 4, 0),()),
		"AllowDragDrop": ((1745027114, LCID, 4, 0),()),
		"AllowPopup": ((1745027115, LCID, 4, 0),()),
		"HideDetails": ((1745027110, LCID, 4, 0),()),
		"ShowDate": ((1745027106, LCID, 4, 0),()),
		"ShowDuration": ((1745027103, LCID, 4, 0),()),
		"ShowMemo": ((1745027101, LCID, 4, 0),()),
		"ShowOwner": ((1745027102, LCID, 4, 0),()),
		"ShowServer": ((1745027108, LCID, 4, 0),()),
		"ShowStart": ((1745027105, LCID, 4, 0),()),
		"ShowStop": ((1745027104, LCID, 4, 0),()),
		"ShowTank": ((1745027107, LCID, 4, 0),()),
		"SingleClickSelect": ((1745027100, LCID, 4, 0),()),
		"UseServer": ((1745027112, LCID, 4, 0),()),
		"UseTank": ((1745027111, LCID, 4, 0),()),
	}

class _EventSelect(DispatchBaseClass):
	CLSID = IID('{CBA421AC-7EB7-40BA-AA2C-81CC652B2EEF}')
	coclass_clsid = IID('{01B10737-93FA-4FB2-B1F1-0C59793EBCAA}')

	def ClearChecks(self, CheckState=defaultNamedNotOptArg):
		return self._ApplyTypes_(1610809454, 1, (24, 0), ((16395, 3),), u'ClearChecks', None,CheckState
			)

	def GetChecked(self, EvName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610809451, LCID, 1, (11, 0), ((8, 1),),EvName
			)

	def GetEvName(self, Index=defaultNamedNotOptArg):
		return self._ApplyTypes_(1610809453, 1, (8, 0), ((16387, 3),), u'GetEvName', None,Index
			)

	def Refresh(self):
		return self._oleobj_.InvokeTypes(1610809449, LCID, 1, (24, 0), (),)

	def SetChecked(self, EvName=defaultNamedNotOptArg, CheckState=defaultNamedNotOptArg):
		return self._ApplyTypes_(1610809452, 1, (24, 0), ((8, 1), (16395, 3)), u'SetChecked', None,EvName
			, CheckState)

	_prop_map_get_ = {
		"ActiveEvent": (1745027145, 2, (8, 0), (), "ActiveEvent", None),
		"AllowActive": (1745027143, 2, (11, 0), (), "AllowActive", None),
		"AllowDragDrop": (1745027142, 2, (11, 0), (), "AllowDragDrop", None),
		"HideDetails": (1745027158, 2, (11, 0), (), "HideDetails", None),
		"ShowBlock": (1745027148, 2, (11, 0), (), "ShowBlock", None),
		"ShowChecks": (1745027146, 2, (11, 0), (), "ShowChecks", None),
		"ShowDataFormat": (1745027153, 2, (11, 0), (), "ShowDataFormat", None),
		"ShowDefaultEvent": (1745027183, 2, (11, 0), (), "ShowDefaultEvent", None),
		"ShowFirstTime": (1745027151, 2, (11, 0), (), "ShowFirstTime", None),
		"ShowSampleFreq": (1745027152, 2, (11, 0), (), "ShowSampleFreq", None),
		"ShowServer": (1745027150, 2, (11, 0), (), "ShowServer", None),
		"ShowSize": (1745027147, 2, (11, 0), (), "ShowSize", None),
		"ShowStrbOff": (1745027184, 2, (11, 0), (), "ShowStrbOff", None),
		"ShowTank": (1745027149, 2, (11, 0), (), "ShowTank", None),
		"ShowType": (1745027154, 2, (11, 0), (), "ShowType", None),
		"SingleClickSelect": (1745027144, 2, (11, 0), (), "SingleClickSelect", None),
		"UseBlock": (1745027155, 2, (8, 0), (), "UseBlock", None),
		"UseServer": (1745027157, 2, (8, 0), (), "UseServer", None),
		"UseTank": (1745027156, 2, (8, 0), (), "UseTank", None),
	}
	_prop_map_put_ = {
		"ActiveEvent": ((1745027145, LCID, 4, 0),()),
		"AllowActive": ((1745027143, LCID, 4, 0),()),
		"AllowDragDrop": ((1745027142, LCID, 4, 0),()),
		"HideDetails": ((1745027158, LCID, 4, 0),()),
		"ShowBlock": ((1745027148, LCID, 4, 0),()),
		"ShowChecks": ((1745027146, LCID, 4, 0),()),
		"ShowDataFormat": ((1745027153, LCID, 4, 0),()),
		"ShowDefaultEvent": ((1745027183, LCID, 4, 0),()),
		"ShowFirstTime": ((1745027151, LCID, 4, 0),()),
		"ShowSampleFreq": ((1745027152, LCID, 4, 0),()),
		"ShowServer": ((1745027150, LCID, 4, 0),()),
		"ShowSize": ((1745027147, LCID, 4, 0),()),
		"ShowStrbOff": ((1745027184, LCID, 4, 0),()),
		"ShowTank": ((1745027149, LCID, 4, 0),()),
		"ShowType": ((1745027154, LCID, 4, 0),()),
		"SingleClickSelect": ((1745027144, LCID, 4, 0),()),
		"UseBlock": ((1745027155, LCID, 4, 0),()),
		"UseServer": ((1745027157, LCID, 4, 0),()),
		"UseTank": ((1745027156, LCID, 4, 0),()),
	}

class _ServSelProps(DispatchBaseClass):
	CLSID = IID('{91124062-FA58-4A43-962A-A3E90676DEC0}')
	coclass_clsid = IID('{42EDA46E-842E-4131-9C40-1E47D6B8ABB1}')

	_prop_map_get_ = {
	}
	_prop_map_put_ = {
	}

class _ServerSelect(DispatchBaseClass):
	CLSID = IID('{7BE3D05E-A964-4EF6-A8E6-1E07AB181A98}')
	coclass_clsid = IID('{A16140DD-AAA9-46C3-9565-6F1E8815D90A}')

	def AddServer(self, ServName=defaultNamedNotOptArg, IPAddr=defaultNamedNotOptArg, Username=defaultNamedNotOptArg, Domain=defaultNamedNotOptArg
			, Password=defaultNamedNotOptArg):
		return self._ApplyTypes_(1610809405, 1, (11, 0), ((16392, 3), (16392, 3), (16392, 3), (16392, 3), (16392, 3)), u'AddServer', None,ServName
			, IPAddr, Username, Domain, Password)

	def DeleteServer(self, ServerName=defaultNamedNotOptArg):
		return self._ApplyTypes_(1610809407, 1, (11, 0), ((16392, 3),), u'DeleteServer', None,ServerName
			)

	def ModifyServer(self, ServName=defaultNamedNotOptArg, IPAddr=defaultNamedNotOptArg, Username=defaultNamedNotOptArg, Domain=defaultNamedNotOptArg
			, Password=defaultNamedNotOptArg):
		return self._ApplyTypes_(1610809406, 1, (11, 0), ((16392, 3), (16392, 3), (16392, 3), (16392, 3), (16392, 3)), u'ModifyServer', None,ServName
			, IPAddr, Username, Domain, Password)

	def Refresh(self):
		return self._oleobj_.InvokeTypes(1610809419, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"ActiveServer": (1745027118, 2, (8, 0), (), "ActiveServer", None),
		"AllowDragDrop": (1745027148, 2, (11, 0), (), "AllowDragDrop", None),
		"AllowEdit": (1745027119, 2, (11, 0), (), "AllowEdit", None),
		"HideDetails": (1745027136, 2, (11, 0), (), "HideDetails", None),
	}
	_prop_map_put_ = {
		"ActiveServer": ((1745027118, LCID, 4, 0),()),
		"AllowDragDrop": ((1745027148, LCID, 4, 0),()),
		"AllowEdit": ((1745027119, LCID, 4, 0),()),
		"HideDetails": ((1745027136, LCID, 4, 0),()),
	}

class _TankSelect(DispatchBaseClass):
	CLSID = IID('{2303C7E3-BC00-4B81-A550-D258167DC1C0}')
	coclass_clsid = IID('{6BCC8D27-0166-441E-9441-8F55DB2779FB}')

	def AddTank(self, path=defaultNamedNotOptArg, name=defaultNamedNotOptArg, quite=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1610809446, LCID, 1, (11, 0), ((8, 1), (8, 1), (11, 1)),path
			, name, quite)

	def Refresh(self):
		return self._oleobj_.InvokeTypes(1610809417, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"ActiveTank": (1745027119, 2, (8, 0), (), "ActiveTank", None),
		"AllowDragDrop": (1745027146, 2, (11, 0), (), "AllowDragDrop", None),
		"AllowPopup": (1745027124, 2, (11, 0), (), "AllowPopup", None),
		"FileDialogInitPath": (1745027149, 2, (8, 0), (), "FileDialogInitPath", None),
		"HideDetails": (1745027121, 2, (11, 0), (), "HideDetails", None),
		"ShowOnlyPathString": (1745027147, 2, (8, 0), (), "ShowOnlyPathString", None),
		"ShowServer": (1745027122, 2, (11, 0), (), "ShowServer", None),
		"ShowSpecPathOnly": (1745027148, 2, (11, 0), (), "ShowSpecPathOnly", None),
		"ShowTankNew": (1745027175, 2, (11, 0), (), "ShowTankNew", None),
		"SingleClickSelect": (1745027120, 2, (11, 0), (), "SingleClickSelect", None),
		"UseServer": (1745027123, 2, (8, 0), (), "UseServer", None),
	}
	_prop_map_put_ = {
		"ActiveTank": ((1745027119, LCID, 4, 0),()),
		"AllowDragDrop": ((1745027146, LCID, 4, 0),()),
		"AllowPopup": ((1745027124, LCID, 4, 0),()),
		"FileDialogInitPath": ((1745027149, LCID, 4, 0),()),
		"HideDetails": ((1745027121, LCID, 4, 0),()),
		"ShowOnlyPathString": ((1745027147, LCID, 4, 0),()),
		"ShowServer": ((1745027122, LCID, 4, 0),()),
		"ShowSpecPathOnly": ((1745027148, LCID, 4, 0),()),
		"ShowTankNew": ((1745027175, LCID, 4, 0),()),
		"SingleClickSelect": ((1745027120, LCID, 4, 0),()),
		"UseServer": ((1745027123, LCID, 4, 0),()),
	}

class _BlockSelect_:
	CLSID = CLSID_Sink = IID('{DC769221-9AD4-4CCD-B51A-FEC47ED63458}')
	coclass_clsid = IID('{CB81F5AF-7625-4F83-B629-54C37B55A203}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		        2 : "OnBeginDrag",
		        1 : "OnBlockChanged",
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
#	def OnBeginDrag(self, TDD=defaultNamedNotOptArg):
#	def OnBlockChanged(self, ActBlock=defaultNamedNotOptArg, ActTank=defaultNamedNotOptArg, ActServer=defaultNamedNotOptArg):


class _EventSelect_:
	CLSID = CLSID_Sink = IID('{3F098EDA-4EFB-4923-9613-373BF08B3F5C}')
	coclass_clsid = IID('{01B10737-93FA-4FB2-B1F1-0C59793EBCAA}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		        2 : "OnBeginDrag",
		        3 : "OnChangeCheck",
		        5 : "OnEventDblClicked",
		        4 : "OnEventClicked",
		        1 : "OnActEventChanged",
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
#	def OnBeginDrag(self, TDD=defaultNamedNotOptArg):
#	def OnChangeCheck(self, EvName=defaultNamedNotOptArg):
#	def OnEventDblClicked(self, EvName=defaultNamedNotOptArg):
#	def OnEventClicked(self, EvName=defaultNamedNotOptArg):
#	def OnActEventChanged(self, NewActEvent=defaultNamedNotOptArg):


class _ServerSelect_:
	CLSID = CLSID_Sink = IID('{75CA8D1D-4078-4EA7-8EC2-E2198C9CFA52}')
	coclass_clsid = IID('{A16140DD-AAA9-46C3-9565-6F1E8815D90A}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		        1 : "OnServerChanged",
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
#	def OnServerChanged(self, NewServer=defaultNamedNotOptArg):


class _TankSelect_:
	CLSID = CLSID_Sink = IID('{58277ACF-7979-45F9-BBE7-0FB5D6B416F4}')
	coclass_clsid = IID('{6BCC8D27-0166-441E-9441-8F55DB2779FB}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		        1 : "OnTankChanged",
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
#	def OnTankChanged(self, ActTank=defaultNamedNotOptArg, ActServer=defaultNamedNotOptArg):


from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'TTankInterfaces.BlockSelect'
class BlockSelect(CoClassBaseClass): # A CoClass
	CLSID = IID('{CB81F5AF-7625-4F83-B629-54C37B55A203}')
	coclass_sources = [
		_BlockSelect_,
	]
	default_source = _BlockSelect_
	coclass_interfaces = [
		_BlockSelect,
	]
	default_interface = _BlockSelect

# This CoClass is known by the name 'TTankInterfaces.EventSelect'
class EventSelect(CoClassBaseClass): # A CoClass
	CLSID = IID('{01B10737-93FA-4FB2-B1F1-0C59793EBCAA}')
	coclass_sources = [
		_EventSelect_,
	]
	default_source = _EventSelect_
	coclass_interfaces = [
		_EventSelect,
	]
	default_interface = _EventSelect

class ServSelProps(CoClassBaseClass): # A CoClass
	CLSID = IID('{42EDA46E-842E-4131-9C40-1E47D6B8ABB1}')
	coclass_sources = [
	]
	coclass_interfaces = [
		_ServSelProps,
	]
	default_interface = _ServSelProps

# This CoClass is known by the name 'TTankInterfaces.ServerSelect'
class ServerSelect(CoClassBaseClass): # A CoClass
	CLSID = IID('{A16140DD-AAA9-46C3-9565-6F1E8815D90A}')
	coclass_sources = [
		_ServerSelect_,
	]
	default_source = _ServerSelect_
	coclass_interfaces = [
		_ServerSelect,
	]
	default_interface = _ServerSelect

# This CoClass is known by the name 'TTankInterfaces.TankSelect'
class TankSelect(CoClassBaseClass): # A CoClass
	CLSID = IID('{6BCC8D27-0166-441E-9441-8F55DB2779FB}')
	coclass_sources = [
		_TankSelect_,
	]
	default_source = _TankSelect_
	coclass_interfaces = [
		_TankSelect,
	]
	default_interface = _TankSelect

_BlockSelect_vtables_dispatch_ = 1
_BlockSelect_vtables_ = [
	(( u'Refresh' , ), 1610809385, (1610809385, (), [ ], 1 , 1 , 4 , 0 , 1956 , (3, 0, None, None) , 0 , )),
	(( u'UseServer' , None , ), 1745027112, (1745027112, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1960 , (3, 0, None, None) , 0 , )),
	(( u'UseServer' , None , ), 1745027112, (1745027112, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1964 , (3, 0, None, None) , 0 , )),
	(( u'UseTank' , None , ), 1745027111, (1745027111, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1968 , (3, 0, None, None) , 0 , )),
	(( u'UseTank' , None , ), 1745027111, (1745027111, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1972 , (3, 0, None, None) , 0 , )),
	(( u'HideDetails' , None , ), 1745027110, (1745027110, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1976 , (3, 0, None, None) , 0 , )),
	(( u'HideDetails' , None , ), 1745027110, (1745027110, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1980 , (3, 0, None, None) , 0 , )),
	(( u'ActiveBlock' , None , ), 1745027109, (1745027109, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1984 , (3, 0, None, None) , 0 , )),
	(( u'ActiveBlock' , None , ), 1745027109, (1745027109, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1988 , (3, 0, None, None) , 0 , )),
	(( u'ShowServer' , None , ), 1745027108, (1745027108, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1992 , (3, 0, None, None) , 0 , )),
	(( u'ShowServer' , None , ), 1745027108, (1745027108, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1996 , (3, 0, None, None) , 0 , )),
	(( u'ShowTank' , None , ), 1745027107, (1745027107, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2000 , (3, 0, None, None) , 0 , )),
	(( u'ShowTank' , None , ), 1745027107, (1745027107, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2004 , (3, 0, None, None) , 0 , )),
	(( u'ShowDate' , None , ), 1745027106, (1745027106, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2008 , (3, 0, None, None) , 0 , )),
	(( u'ShowDate' , None , ), 1745027106, (1745027106, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2012 , (3, 0, None, None) , 0 , )),
	(( u'ShowStart' , None , ), 1745027105, (1745027105, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2016 , (3, 0, None, None) , 0 , )),
	(( u'ShowStart' , None , ), 1745027105, (1745027105, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2020 , (3, 0, None, None) , 0 , )),
	(( u'ShowStop' , None , ), 1745027104, (1745027104, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2024 , (3, 0, None, None) , 0 , )),
	(( u'ShowStop' , None , ), 1745027104, (1745027104, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2028 , (3, 0, None, None) , 0 , )),
	(( u'ShowDuration' , None , ), 1745027103, (1745027103, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2032 , (3, 0, None, None) , 0 , )),
	(( u'ShowDuration' , None , ), 1745027103, (1745027103, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2036 , (3, 0, None, None) , 0 , )),
	(( u'ShowOwner' , None , ), 1745027102, (1745027102, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2040 , (3, 0, None, None) , 0 , )),
	(( u'ShowOwner' , None , ), 1745027102, (1745027102, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2044 , (3, 0, None, None) , 0 , )),
	(( u'ShowMemo' , None , ), 1745027101, (1745027101, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2048 , (3, 0, None, None) , 0 , )),
	(( u'ShowMemo' , None , ), 1745027101, (1745027101, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2052 , (3, 0, None, None) , 0 , )),
	(( u'SingleClickSelect' , None , ), 1745027100, (1745027100, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2056 , (3, 0, None, None) , 0 , )),
	(( u'SingleClickSelect' , None , ), 1745027100, (1745027100, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2060 , (3, 0, None, None) , 0 , )),
	(( u'AllowDragDrop' , None , ), 1745027114, (1745027114, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2064 , (3, 0, None, None) , 0 , )),
	(( u'AllowDragDrop' , None , ), 1745027114, (1745027114, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2068 , (3, 0, None, None) , 0 , )),
	(( u'AllowPopup' , None , ), 1745027115, (1745027115, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2072 , (3, 0, None, None) , 0 , )),
	(( u'AllowPopup' , None , ), 1745027115, (1745027115, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2076 , (3, 0, None, None) , 0 , )),
]

_EventSelect_vtables_dispatch_ = 1
_EventSelect_vtables_ = [
	(( u'HideDetails' , None , ), 1745027158, (1745027158, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1956 , (3, 0, None, None) , 0 , )),
	(( u'HideDetails' , None , ), 1745027158, (1745027158, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1960 , (3, 0, None, None) , 0 , )),
	(( u'UseServer' , None , ), 1745027157, (1745027157, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1964 , (3, 0, None, None) , 0 , )),
	(( u'UseServer' , None , ), 1745027157, (1745027157, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1968 , (3, 0, None, None) , 0 , )),
	(( u'UseTank' , None , ), 1745027156, (1745027156, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1972 , (3, 0, None, None) , 0 , )),
	(( u'UseTank' , None , ), 1745027156, (1745027156, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1976 , (3, 0, None, None) , 0 , )),
	(( u'UseBlock' , None , ), 1745027155, (1745027155, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1980 , (3, 0, None, None) , 0 , )),
	(( u'UseBlock' , None , ), 1745027155, (1745027155, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1984 , (3, 0, None, None) , 0 , )),
	(( u'Refresh' , ), 1610809449, (1610809449, (), [ ], 1 , 1 , 4 , 0 , 1988 , (3, 0, None, None) , 0 , )),
	(( u'ShowType' , None , ), 1745027154, (1745027154, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1992 , (3, 0, None, None) , 0 , )),
	(( u'ShowType' , None , ), 1745027154, (1745027154, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1996 , (3, 0, None, None) , 0 , )),
	(( u'ShowDataFormat' , None , ), 1745027153, (1745027153, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2000 , (3, 0, None, None) , 0 , )),
	(( u'ShowDataFormat' , None , ), 1745027153, (1745027153, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2004 , (3, 0, None, None) , 0 , )),
	(( u'ShowSampleFreq' , None , ), 1745027152, (1745027152, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2008 , (3, 0, None, None) , 0 , )),
	(( u'ShowSampleFreq' , None , ), 1745027152, (1745027152, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2012 , (3, 0, None, None) , 0 , )),
	(( u'ShowFirstTime' , None , ), 1745027151, (1745027151, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2016 , (3, 0, None, None) , 0 , )),
	(( u'ShowFirstTime' , None , ), 1745027151, (1745027151, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2020 , (3, 0, None, None) , 0 , )),
	(( u'ShowServer' , None , ), 1745027150, (1745027150, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2024 , (3, 0, None, None) , 0 , )),
	(( u'ShowServer' , None , ), 1745027150, (1745027150, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2028 , (3, 0, None, None) , 0 , )),
	(( u'ShowTank' , None , ), 1745027149, (1745027149, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2032 , (3, 0, None, None) , 0 , )),
	(( u'ShowTank' , None , ), 1745027149, (1745027149, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2036 , (3, 0, None, None) , 0 , )),
	(( u'ShowBlock' , None , ), 1745027148, (1745027148, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2040 , (3, 0, None, None) , 0 , )),
	(( u'ShowBlock' , None , ), 1745027148, (1745027148, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2044 , (3, 0, None, None) , 0 , )),
	(( u'ShowSize' , None , ), 1745027147, (1745027147, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2048 , (3, 0, None, None) , 0 , )),
	(( u'ShowSize' , None , ), 1745027147, (1745027147, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2052 , (3, 0, None, None) , 0 , )),
	(( u'ShowChecks' , None , ), 1745027146, (1745027146, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2056 , (3, 0, None, None) , 0 , )),
	(( u'ShowChecks' , None , ), 1745027146, (1745027146, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2060 , (3, 0, None, None) , 0 , )),
	(( u'GetChecked' , u'EvName' , None , ), 1610809451, (1610809451, (), [ (8, 1, None, None) , 
			(16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 2064 , (3, 0, None, None) , 0 , )),
	(( u'SetChecked' , u'EvName' , u'CheckState' , ), 1610809452, (1610809452, (), [ (8, 1, None, None) , 
			(16395, 3, None, None) , ], 1 , 1 , 4 , 0 , 2068 , (3, 0, None, None) , 0 , )),
	(( u'GetEvName' , u'Index' , None , ), 1610809453, (1610809453, (), [ (16387, 3, None, None) , 
			(16392, 10, None, None) , ], 1 , 1 , 4 , 0 , 2072 , (3, 0, None, None) , 0 , )),
	(( u'ClearChecks' , u'CheckState' , ), 1610809454, (1610809454, (), [ (16395, 3, None, None) , ], 1 , 1 , 4 , 0 , 2076 , (3, 0, None, None) , 0 , )),
	(( u'ActiveEvent' , None , ), 1745027145, (1745027145, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 2080 , (3, 0, None, None) , 0 , )),
	(( u'ActiveEvent' , None , ), 1745027145, (1745027145, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 2084 , (3, 0, None, None) , 0 , )),
	(( u'SingleClickSelect' , None , ), 1745027144, (1745027144, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2088 , (3, 0, None, None) , 0 , )),
	(( u'SingleClickSelect' , None , ), 1745027144, (1745027144, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2092 , (3, 0, None, None) , 0 , )),
	(( u'AllowActive' , None , ), 1745027143, (1745027143, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2096 , (3, 0, None, None) , 0 , )),
	(( u'AllowActive' , None , ), 1745027143, (1745027143, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2100 , (3, 0, None, None) , 0 , )),
	(( u'AllowDragDrop' , None , ), 1745027142, (1745027142, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2104 , (3, 0, None, None) , 0 , )),
	(( u'AllowDragDrop' , None , ), 1745027142, (1745027142, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2108 , (3, 0, None, None) , 0 , )),
	(( u'ShowDefaultEvent' , None , ), 1745027183, (1745027183, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2112 , (3, 0, None, None) , 0 , )),
	(( u'ShowDefaultEvent' , None , ), 1745027183, (1745027183, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2116 , (3, 0, None, None) , 0 , )),
	(( u'ShowStrbOff' , None , ), 1745027184, (1745027184, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2120 , (3, 0, None, None) , 0 , )),
	(( u'ShowStrbOff' , None , ), 1745027184, (1745027184, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2124 , (3, 0, None, None) , 0 , )),
]

_ServSelProps_vtables_dispatch_ = 1
_ServSelProps_vtables_ = [
]

_ServerSelect_vtables_dispatch_ = 1
_ServerSelect_vtables_ = [
	(( u'AllowEdit' , None , ), 1745027119, (1745027119, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1956 , (3, 0, None, None) , 0 , )),
	(( u'AllowEdit' , None , ), 1745027119, (1745027119, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1960 , (3, 0, None, None) , 0 , )),
	(( u'AddServer' , u'ServName' , u'IPAddr' , u'Username' , u'Domain' , 
			u'Password' , None , ), 1610809405, (1610809405, (), [ (16392, 3, None, None) , (16392, 3, None, None) , 
			(16392, 3, None, None) , (16392, 3, None, None) , (16392, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 1964 , (3, 0, None, None) , 0 , )),
	(( u'ModifyServer' , u'ServName' , u'IPAddr' , u'Username' , u'Domain' , 
			u'Password' , None , ), 1610809406, (1610809406, (), [ (16392, 3, None, None) , (16392, 3, None, None) , 
			(16392, 3, None, None) , (16392, 3, None, None) , (16392, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 1968 , (3, 0, None, None) , 0 , )),
	(( u'DeleteServer' , u'ServerName' , None , ), 1610809407, (1610809407, (), [ (16392, 3, None, None) , 
			(16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 1972 , (3, 0, None, None) , 0 , )),
	(( u'ActiveServer' , None , ), 1745027118, (1745027118, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1976 , (3, 0, None, None) , 0 , )),
	(( u'ActiveServer' , None , ), 1745027118, (1745027118, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1980 , (3, 0, None, None) , 0 , )),
	(( u'HideDetails' , None , ), 1745027136, (1745027136, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1984 , (3, 0, None, None) , 0 , )),
	(( u'HideDetails' , None , ), 1745027136, (1745027136, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1988 , (3, 0, None, None) , 0 , )),
	(( u'Refresh' , ), 1610809419, (1610809419, (), [ ], 1 , 1 , 4 , 0 , 1992 , (3, 0, None, None) , 0 , )),
	(( u'AllowDragDrop' , None , ), 1745027148, (1745027148, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1996 , (3, 0, None, None) , 0 , )),
	(( u'AllowDragDrop' , None , ), 1745027148, (1745027148, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2000 , (3, 0, None, None) , 0 , )),
]

_TankSelect_vtables_dispatch_ = 1
_TankSelect_vtables_ = [
	(( u'Refresh' , ), 1610809417, (1610809417, (), [ ], 1 , 1 , 4 , 0 , 1956 , (3, 0, None, None) , 0 , )),
	(( u'AllowPopup' , None , ), 1745027124, (1745027124, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1960 , (3, 0, None, None) , 0 , )),
	(( u'AllowPopup' , None , ), 1745027124, (1745027124, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1964 , (3, 0, None, None) , 0 , )),
	(( u'UseServer' , None , ), 1745027123, (1745027123, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 1968 , (3, 0, None, None) , 0 , )),
	(( u'UseServer' , None , ), 1745027123, (1745027123, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 1972 , (3, 0, None, None) , 0 , )),
	(( u'ShowServer' , None , ), 1745027122, (1745027122, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1976 , (3, 0, None, None) , 0 , )),
	(( u'ShowServer' , None , ), 1745027122, (1745027122, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1980 , (3, 0, None, None) , 0 , )),
	(( u'HideDetails' , None , ), 1745027121, (1745027121, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1984 , (3, 0, None, None) , 0 , )),
	(( u'HideDetails' , None , ), 1745027121, (1745027121, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1988 , (3, 0, None, None) , 0 , )),
	(( u'SingleClickSelect' , None , ), 1745027120, (1745027120, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 1992 , (3, 0, None, None) , 0 , )),
	(( u'SingleClickSelect' , None , ), 1745027120, (1745027120, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 1996 , (3, 0, None, None) , 0 , )),
	(( u'ActiveTank' , None , ), 1745027119, (1745027119, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 2000 , (3, 0, None, None) , 0 , )),
	(( u'ActiveTank' , None , ), 1745027119, (1745027119, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 2004 , (3, 0, None, None) , 0 , )),
	(( u'AllowDragDrop' , None , ), 1745027146, (1745027146, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2008 , (3, 0, None, None) , 0 , )),
	(( u'AllowDragDrop' , None , ), 1745027146, (1745027146, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2012 , (3, 0, None, None) , 0 , )),
	(( u'ShowOnlyPathString' , None , ), 1745027147, (1745027147, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 2016 , (3, 0, None, None) , 0 , )),
	(( u'ShowOnlyPathString' , None , ), 1745027147, (1745027147, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 2020 , (3, 0, None, None) , 0 , )),
	(( u'ShowSpecPathOnly' , None , ), 1745027148, (1745027148, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2024 , (3, 0, None, None) , 0 , )),
	(( u'ShowSpecPathOnly' , None , ), 1745027148, (1745027148, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2028 , (3, 0, None, None) , 0 , )),
	(( u'FileDialogInitPath' , None , ), 1745027149, (1745027149, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 2032 , (3, 0, None, None) , 0 , )),
	(( u'FileDialogInitPath' , None , ), 1745027149, (1745027149, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 2036 , (3, 0, None, None) , 0 , )),
	(( u'AddTank' , u'path' , u'name' , u'quite' , None , 
			), 1610809446, (1610809446, (), [ (8, 1, None, None) , (8, 1, None, None) , (11, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 2040 , (3, 0, None, None) , 0 , )),
	(( u'ShowTankNew' , None , ), 1745027175, (1745027175, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 2044 , (3, 0, None, None) , 0 , )),
	(( u'ShowTankNew' , None , ), 1745027175, (1745027175, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 2048 , (3, 0, None, None) , 0 , )),
]

RecordMap = {
	u'TankInfo': '{A3EA7E81-5BF7-4FE4-9659-D797A6DD6A13}',
}

CLSIDToClassMap = {
	'{A16140DD-AAA9-46C3-9565-6F1E8815D90A}' : ServerSelect,
	'{C2F42E9B-86B7-4F21-889D-8B854B019640}' : _BlockSelect,
	'{DC769221-9AD4-4CCD-B51A-FEC47ED63458}' : _BlockSelect_,
	'{01B10737-93FA-4FB2-B1F1-0C59793EBCAA}' : EventSelect,
	'{42EDA46E-842E-4131-9C40-1E47D6B8ABB1}' : ServSelProps,
	'{75CA8D1D-4078-4EA7-8EC2-E2198C9CFA52}' : _ServerSelect_,
	'{CBA421AC-7EB7-40BA-AA2C-81CC652B2EEF}' : _EventSelect,
	'{7BE3D05E-A964-4EF6-A8E6-1E07AB181A98}' : _ServerSelect,
	'{91124062-FA58-4A43-962A-A3E90676DEC0}' : _ServSelProps,
	'{58277ACF-7979-45F9-BBE7-0FB5D6B416F4}' : _TankSelect_,
	'{3F098EDA-4EFB-4923-9613-373BF08B3F5C}' : _EventSelect_,
	'{6BCC8D27-0166-441E-9441-8F55DB2779FB}' : TankSelect,
	'{2303C7E3-BC00-4B81-A550-D258167DC1C0}' : _TankSelect,
	'{CB81F5AF-7625-4F83-B629-54C37B55A203}' : BlockSelect,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{CBA421AC-7EB7-40BA-AA2C-81CC652B2EEF}' : '_EventSelect',
	'{91124062-FA58-4A43-962A-A3E90676DEC0}' : '_ServSelProps',
	'{7BE3D05E-A964-4EF6-A8E6-1E07AB181A98}' : '_ServerSelect',
	'{2303C7E3-BC00-4B81-A550-D258167DC1C0}' : '_TankSelect',
	'{C2F42E9B-86B7-4F21-889D-8B854B019640}' : '_BlockSelect',
}


NamesToIIDMap = {
	'_BlockSelect_' : '{DC769221-9AD4-4CCD-B51A-FEC47ED63458}',
	'_EventSelect' : '{CBA421AC-7EB7-40BA-AA2C-81CC652B2EEF}',
	'_BlockSelect' : '{C2F42E9B-86B7-4F21-889D-8B854B019640}',
	'_ServSelProps' : '{91124062-FA58-4A43-962A-A3E90676DEC0}',
	'_ServerSelect_' : '{75CA8D1D-4078-4EA7-8EC2-E2198C9CFA52}',
	'_EventSelect_' : '{3F098EDA-4EFB-4923-9613-373BF08B3F5C}',
	'_TankSelect' : '{2303C7E3-BC00-4B81-A550-D258167DC1C0}',
	'_ServerSelect' : '{7BE3D05E-A964-4EF6-A8E6-1E07AB181A98}',
	'_TankSelect_' : '{58277ACF-7979-45F9-BBE7-0FB5D6B416F4}',
}


