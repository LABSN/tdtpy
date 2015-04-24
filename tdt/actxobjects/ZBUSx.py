# -*- coding: utf-8 -*-
# Created by makepy.py version 0.5.00
# By python version 2.5.4 (r254:67916, Dec 23 2008, 15:10:54) [MSC v.1310 32 bit (Intel)]
# From type library 'zBUSx.ocx'
# On Thu Aug 27 14:12:16 2009
"""zBUSx ActiveX Control module"""
makepy_version = '0.5.00'
python_version = 0x20504f0

import win32com.client.CLSIDToClass, pythoncom, pywintypes
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{10055D3E-3938-4652-B6A2-6A6A4184D18D}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 10
LCID = 0x0

from win32com.client import DispatchBaseClass
class _DZBUSx(DispatchBaseClass):
	"""Dispatch interface for ZBUSx Control"""
	CLSID = IID('{9F05A891-D2B9-41AF-8C8E-3F4245261483}')
	coclass_clsid = IID('{79734A6C-8E6E-4998-B834-3E4E481232B0}')

	def AboutBox(self):
		return self._oleobj_.InvokeTypes(-552, LCID, 1, (24, 0), (),)

	def Connect(self, Interface=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (3, 0), ((3, 0),),Interface
			)

	def ConnectZBUS(self, IntName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(12, LCID, 1, (3, 0), ((8, 0),),IntName
			)

	def FlushIO(self, RackNum=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(5, LCID, 1, (3, 0), ((3, 0),),RackNum
			)

	def GetDeviceAddr(self, DevType=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (3, 0), ((3, 0), (3, 0)),DevType
			, DevNum)

	def GetDeviceAt(self, RackNum=defaultNamedNotOptArg, PosNum=defaultNamedNotOptArg, DevID=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(11, LCID, 1, (8, 0), ((3, 0), (3, 0), (16387, 0), (16387, 0)),RackNum
			, PosNum, DevID, DevNum)

	def GetDeviceVersion(self, DevType=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (3, 0), ((3, 0), (3, 0)),DevType
			, DevNum)

	def GetError(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(10, LCID, 1, (8, 0), (),)

	def HardwareReset(self, RackNum=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (3, 0), ((3, 0),),RackNum
			)

	def KillCode(self, DevType=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg, MagicCode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (3, 0), ((3, 0), (3, 0), (3, 0)),DevType
			, DevNum, MagicCode)

	def zBusSync(self, RackMask=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (3, 0), ((3, 0),),RackMask
			)

	def zBusTrigA(self, RackNum=defaultNamedNotOptArg, zTrgMode=defaultNamedNotOptArg, Delay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (3, 0), ((3, 0), (3, 0), (3, 0)),RackNum
			, zTrgMode, Delay)

	def zBusTrigB(self, RackNum=defaultNamedNotOptArg, zTrgMode=defaultNamedNotOptArg, Delay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (3, 0), ((3, 0), (3, 0), (3, 0)),RackNum
			, zTrgMode, Delay)

	_prop_map_get_ = {
	}
	_prop_map_put_ = {
	}

class _DZBUSxEvents:
	"""Event interface for ZBUSx Control"""
	CLSID = CLSID_Sink = IID('{575833D5-0B5E-4759-B370-40FA23D409E5}')
	coclass_clsid = IID('{79734A6C-8E6E-4998-B834-3E4E481232B0}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
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


from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'ZBUS.X'
class ZBUSx(CoClassBaseClass): # A CoClass
	# ZBUSx Control
	CLSID = IID('{79734A6C-8E6E-4998-B834-3E4E481232B0}')
	coclass_sources = [
		_DZBUSxEvents,
	]
	default_source = _DZBUSxEvents
	coclass_interfaces = [
		_DZBUSx,
	]
	default_interface = _DZBUSx

RecordMap = {
}

CLSIDToClassMap = {
	'{575833D5-0B5E-4759-B370-40FA23D409E5}' : _DZBUSxEvents,
	'{79734A6C-8E6E-4998-B834-3E4E481232B0}' : ZBUSx,
	'{9F05A891-D2B9-41AF-8C8E-3F4245261483}' : _DZBUSx,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
}


NamesToIIDMap = {
	'_DZBUSx' : '{9F05A891-D2B9-41AF-8C8E-3F4245261483}',
	'_DZBUSxEvents' : '{575833D5-0B5E-4759-B370-40FA23D409E5}',
}


