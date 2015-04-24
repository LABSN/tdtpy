# -*- coding: utf-8 -*-
# Created by makepy.py version 0.5.00
# By python version 2.5.4 (r254:67916, Dec 23 2008, 15:10:54) [MSC v.1310 32 bit (Intel)]
# From type library 'PA5x.ocx'
# On Thu Aug 27 14:11:40 2009
"""PA5x ActiveX Control module"""
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

CLSID = IID('{73B7CFAB-7D2C-487A-81EC-E6A15FB9E84A}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 10
LCID = 0x0

from win32com.client import DispatchBaseClass
class _DPA5x(DispatchBaseClass):
	"""Dispatch interface for PA5x Control"""
	CLSID = IID('{9792C25C-198C-4AC3-B915-246CB15BB30C}')
	coclass_clsid = IID('{EC05FCDE-300D-4CE3-9774-A4C377507BD7}')

	def Connect(self, Interface=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), ((3, 0), (3, 0)),Interface
			, DevNum)

	def ConnectPA5(self, IntName=defaultNamedNotOptArg, DevNum=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (3, 0), ((8, 0), (3, 0)),IntName
			, DevNum)

	def Display(self, Text=defaultNamedNotOptArg, Position=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (11, 0), ((8, 0), (3, 0)),Text
			, Position)

	def GetAtten(self):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (4, 0), (),)

	def GetError(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(6, LCID, 1, (8, 0), (),)

	def Reset(self):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (11, 0), (),)

	def SetAtten(self, AttVal=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (11, 0), ((4, 0),),AttVal
			)

	def SetUser(self, ParCode=defaultNamedNotOptArg, Val=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(5, LCID, 1, (11, 0), ((3, 0), (4, 0)),ParCode
			, Val)

	_prop_map_get_ = {
	}
	_prop_map_put_ = {
	}

class _DPA5xEvents:
	"""Event interface for PA5x Control"""
	CLSID = CLSID_Sink = IID('{06D79585-4000-4243-BD17-499FA2F46DDB}')
	coclass_clsid = IID('{EC05FCDE-300D-4CE3-9774-A4C377507BD7}')
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
# This CoClass is known by the name 'PA5.X'
class PA5x(CoClassBaseClass): # A CoClass
	# PA5x Control
	CLSID = IID('{EC05FCDE-300D-4CE3-9774-A4C377507BD7}')
	coclass_sources = [
		_DPA5xEvents,
	]
	default_source = _DPA5xEvents
	coclass_interfaces = [
		_DPA5x,
	]
	default_interface = _DPA5x

RecordMap = {
}

CLSIDToClassMap = {
	'{EC05FCDE-300D-4CE3-9774-A4C377507BD7}' : PA5x,
	'{9792C25C-198C-4AC3-B915-246CB15BB30C}' : _DPA5x,
	'{06D79585-4000-4243-BD17-499FA2F46DDB}' : _DPA5xEvents,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
}


NamesToIIDMap = {
	'_DPA5xEvents' : '{06D79585-4000-4243-BD17-499FA2F46DDB}',
	'_DPA5x' : '{9792C25C-198C-4AC3-B915-246CB15BB30C}',
}


