# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.00
# By python version 2.6.6 |EPD 6.3-1 (32-bit)| (r266:84292, Sep 20 2010, 11:26:16) [MSC v.1500 32 bit (Intel)]
# From type library 'TDevAccX.ocx'
# On Mon Nov 22 10:28:02 2010
"""TDevAccX ActiveX Control module"""
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

CLSID = IID('{735FF2F5-CC9A-4D67-BFC1-FD5FA6742027}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 10
LCID = 0x0

from win32com.client import DispatchBaseClass
class _DTDevAccX(DispatchBaseClass):
	"""Dispatch interface for TDevAccX Control"""
	CLSID = IID('{F04FC131-D33B-45B7-BC22-CF58B06CA5CB}')
	coclass_clsid = IID('{09EFA19D-3AD0-49A8-8232-18D6F7512CE8}')

	def AboutBox(self):
		return self._oleobj_.InvokeTypes(-552, LCID, 1, (24, 0), (),)

	def CheckServerConnection(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (3, 0), (),)

	def CloseConnection(self):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), (),)

	def ConnectServer(self, ServerName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (3, 0), ((8, 0),),ServerName
			)

	def GetDeviceName(self, Index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(17, LCID, 1, (8, 0), ((3, 0),),Index
			)

	def GetDeviceRCO(self, DeviceName=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(19, LCID, 1, (8, 0), ((8, 0),),DeviceName
			)

	def GetDeviceSF(self, Target=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (4, 0), ((8, 0),),Target
			)

	def GetDeviceStatus(self, Target=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(14, LCID, 1, (3, 0), ((8, 0),),Target
			)

	def GetDeviceType(self, DeviceName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(18, LCID, 1, (3, 0), ((8, 0),),DeviceName
			)

	def GetNextTag(self, DeviceName=defaultNamedNotOptArg, ReqType=defaultNamedNotOptArg, DoFirst=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(20, LCID, 1, (8, 0), ((8, 0), (3, 0), (3, 0)),DeviceName
			, ReqType, DoFirst)

	def GetSysMode(self):
		return self._oleobj_.InvokeTypes(16, LCID, 1, (3, 0), (),)

	def GetTankName(self):
		"""method GetTankName"""
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(23, LCID, 1, (8, 0), (),)

	def GetTargetClass(self, Target=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (3, 0), ((8, 0),),Target
			)

	def GetTargetSize(self, Target=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(11, LCID, 1, (3, 0), ((8, 0),),Target
			)

	def GetTargetType(self, Target=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(15, LCID, 1, (3, 0), ((8, 0),),Target
			)

	def GetTargetVal(self, Target=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(12, LCID, 1, (5, 0), ((8, 0),),Target
			)

	def ReadTarget(self, Target=defaultNamedNotOptArg, nOS=defaultNamedNotOptArg, nWords=defaultNamedNotOptArg, pData=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (3, 0), ((8, 0), (3, 0), (3, 0), (16388, 0)),Target
			, nOS, nWords, pData)

	def ReadTargetV(self, Target=defaultNamedNotOptArg, nOS=defaultNamedNotOptArg, nWords=defaultNamedNotOptArg):
		return self._ApplyTypes_(7, 1, (12, 0), ((8, 0), (3, 0), (3, 0)), u'ReadTargetV', None,Target
			, nOS, nWords)

	def ReadTargetVEX(self, Target=defaultNamedNotOptArg, nOS=defaultNamedNotOptArg, nWords=defaultNamedNotOptArg, SrcType=defaultNamedNotOptArg
			, DstType=defaultNamedNotOptArg):
		return self._ApplyTypes_(24, 1, (12, 0), ((8, 0), (3, 0), (3, 0), (8, 0), (8, 0)), u'ReadTargetVEX', None,Target
			, nOS, nWords, SrcType, DstType)

	def SetSysMode(self, NewMode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (3, 0), ((3, 0),),NewMode
			)

	def SetTankName(self, TankName=defaultNamedNotOptArg):
		"""method SetTankName"""
		return self._oleobj_.InvokeTypes(22, LCID, 1, (3, 0), ((8, 0),),TankName
			)

	def SetTargetVal(self, Target=defaultNamedNotOptArg, Val=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (3, 0), ((8, 0), (5, 0)),Target
			, Val)

	def WriteTarget(self, Target=defaultNamedNotOptArg, nOS=defaultNamedNotOptArg, nWords=defaultNamedNotOptArg, pData=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (3, 0), ((8, 0), (3, 0), (3, 0), (16388, 0)),Target
			, nOS, nWords, pData)

	def WriteTargetV(self, Target=defaultNamedNotOptArg, nOS=defaultNamedNotOptArg, vData=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(5, LCID, 1, (3, 0), ((8, 0), (3, 0), (12, 0)),Target
			, nOS, vData)

	def WriteTargetVEX(self, Target=defaultNamedNotOptArg, nOS=defaultNamedNotOptArg, DstType=defaultNamedNotOptArg, Buf=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(25, LCID, 1, (3, 0), ((8, 0), (3, 0), (8, 0), (12, 0)),Target
			, nOS, DstType, Buf)

	def ZeroTarget(self, Target=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (24, 0), ((8, 0),),Target
			)

	_prop_map_get_ = {
	}
	_prop_map_put_ = {
	}

class _DTDevAccXEvents:
	"""Event interface for TDevAccX Control"""
	CLSID = CLSID_Sink = IID('{64E8C018-79F7-4C72-9244-6CAE7315BA4F}')
	coclass_clsid = IID('{09EFA19D-3AD0-49A8-8232-18D6F7512CE8}')
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
# This CoClass is known by the name 'TDevAcc.X'
class TDevAccX(CoClassBaseClass): # A CoClass
	# TDevAccX Control
	CLSID = IID('{09EFA19D-3AD0-49A8-8232-18D6F7512CE8}')
	coclass_sources = [
		_DTDevAccXEvents,
	]
	default_source = _DTDevAccXEvents
	coclass_interfaces = [
		_DTDevAccX,
	]
	default_interface = _DTDevAccX

RecordMap = {
}

CLSIDToClassMap = {
	'{F04FC131-D33B-45B7-BC22-CF58B06CA5CB}' : _DTDevAccX,
	'{64E8C018-79F7-4C72-9244-6CAE7315BA4F}' : _DTDevAccXEvents,
	'{09EFA19D-3AD0-49A8-8232-18D6F7512CE8}' : TDevAccX,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
}


NamesToIIDMap = {
	'_DTDevAccXEvents' : '{64E8C018-79F7-4C72-9244-6CAE7315BA4F}',
	'_DTDevAccX' : '{F04FC131-D33B-45B7-BC22-CF58B06CA5CB}',
}


