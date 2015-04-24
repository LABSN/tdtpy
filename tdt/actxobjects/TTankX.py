# -*- coding: utf-8 -*-
# Created by makepy.py version 0.5.00
# By python version 2.6.6 |EPD 6.3-2 (32-bit)| (r266:84292, Sep 20 2010, 11:26:16) [MSC v.1500 32 bit (Intel)]
# From type library 'TTankX.ocx'
# On Thu Dec 02 21:01:19 2010
"""TTankX ActiveX Control module"""
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

CLSID = IID('{3EABA0EF-2FBA-41F8-A970-3F238A4BAB01}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 10
LCID = 0x0

from win32com.client import DispatchBaseClass
class _DTTankX(DispatchBaseClass):
	"""Dispatch interface for TTankX Control"""
	CLSID = IID('{BE6CAD3F-28F1-4EAC-B210-9CAA5CA8B5B8}')
	coclass_clsid = IID('{670490CE-57D2-4176-8E74-80C4C6A47D88}')

	def AboutBox(self):
		return self._oleobj_.InvokeTypes(-552, LCID, 1, (24, 0), (),)

	def AddClient(self, ClientName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (3, 0), ((8, 0),),ClientName
			)

	def AddServer(self, ServerName=defaultNamedNotOptArg, IPAddress=defaultNamedNotOptArg, Username=defaultNamedNotOptArg, Domain=defaultNamedNotOptArg
			, Password=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(48, LCID, 1, (3, 0), ((8, 0), (8, 0), (8, 0), (8, 0), (8, 0)),ServerName
			, IPAddress, Username, Domain, Password)

	def AddTank(self, TankName=defaultNamedNotOptArg, FilePath=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (3, 0), ((8, 0), (8, 0)),TankName
			, FilePath)

	def BuildEpocEv(self, Index=defaultNamedNotOptArg, TankCode=defaultNamedNotOptArg, TimeStamp=defaultNamedNotOptArg, Value=defaultNamedNotOptArg
			, BuddyEpoc=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(69, LCID, 1, (3, 0), ((3, 0), (8, 0), (5, 0), (5, 0), (8, 0)),Index
			, TankCode, TimeStamp, Value, BuddyEpoc)

	def BuildFilterDesc(self, TankCode=defaultNamedNotOptArg, TestCode=defaultNamedNotOptArg, V1=defaultNamedNotOptArg, V2=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(81, LCID, 1, (8, 0), ((3, 0), (3, 0), (5, 0), (5, 0)),TankCode
			, TestCode, V1, V2)

	def BuildScalar(self, Index=defaultNamedNotOptArg, TankCode=defaultNamedNotOptArg, SortChan=defaultNamedNotOptArg, TimeStamp=defaultNamedNotOptArg
			, Value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(68, LCID, 1, (3, 0), ((3, 0), (8, 0), (3, 0), (5, 0), (5, 0)),Index
			, TankCode, SortChan, TimeStamp, Value)

	def BuildSnipEv(self, Index=defaultNamedNotOptArg, SortChan=defaultNamedNotOptArg, TimeStamp=defaultNamedNotOptArg, HasSort=defaultNamedNotOptArg
			, pData=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(71, LCID, 1, (3, 0), ((3, 0), (3, 0), (5, 0), (3, 0), (16388, 0)),Index
			, SortChan, TimeStamp, HasSort, pData)

	def BuildSnipEvV(self, Index=defaultNamedNotOptArg, SortChan=defaultNamedNotOptArg, TimeStamp=defaultNamedNotOptArg, HasSort=defaultNamedNotOptArg
			, vData=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(73, LCID, 1, (3, 0), ((3, 0), (3, 0), (5, 0), (3, 0), (16396, 0)),Index
			, SortChan, TimeStamp, HasSort, vData)

	def BuildStreamEv(self, Index=defaultNamedNotOptArg, SortChan=defaultNamedNotOptArg, TimeStamp=defaultNamedNotOptArg, pData=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(72, LCID, 1, (3, 0), ((3, 0), (3, 0), (5, 0), (16388, 0)),Index
			, SortChan, TimeStamp, pData)

	def BuildStreamEvV(self, Index=defaultNamedNotOptArg, SortChan=defaultNamedNotOptArg, TimeStamp=defaultNamedNotOptArg, vData=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(74, LCID, 1, (3, 0), ((3, 0), (3, 0), (5, 0), (12, 0)),Index
			, SortChan, TimeStamp, vData)

	def CheckTank(self, TankName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (3, 0), ((8, 0),),TankName
			)

	def ClearEpocIndexing(self):
		return self._oleobj_.InvokeTypes(85, LCID, 1, (24, 0), (),)

	def CloseTank(self):
		return self._oleobj_.InvokeTypes(22, LCID, 1, (24, 0), (),)

	def CodeToString(self, EvCode=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(23, LCID, 1, (8, 0), ((3, 0),),EvCode
			)

	def ConnectServer(self, ServerName=defaultNamedNotOptArg, ClientName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(18, LCID, 1, (3, 0), ((8, 0), (8, 0)),ServerName
			, ClientName)

	def CreateEpocIndexing(self):
		return self._oleobj_.InvokeTypes(84, LCID, 1, (3, 0), (),)

	def DFromToString(self, DFormCode=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(27, LCID, 1, (8, 0), ((3, 0),),DFormCode
			)

	def DeleteClient(self, ClientName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(24, LCID, 1, (24, 0), ((8, 0),),ClientName
			)

	def DeleteSortCode(self, sortName=defaultNamedNotOptArg, snipName=defaultNamedNotOptArg, idxChan=defaultNamedNotOptArg):
		"""method DeleteSortCode"""
		return self._oleobj_.InvokeTypes(125, LCID, 1, (3, 0), ((8, 0), (8, 0), (3, 0)),sortName
			, snipName, idxChan)

	def DisableTankDebug(self, TankName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(34, LCID, 1, (24, 0), ((8, 0),),TankName
			)

	def EnableTankDebug(self, TankName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(33, LCID, 1, (24, 0), ((8, 0),),TankName
			)

	def EvTypeToString(self, evTypeCode=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(26, LCID, 1, (8, 0), ((3, 0),),evTypeCode
			)

	def FancyTime(self, Time=defaultNamedNotOptArg, Format=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(44, LCID, 1, (8, 0), ((5, 0), (8, 0)),Time
			, Format)

	def FromTTD(self, TTD=defaultNamedNotOptArg, FieldCode=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(54, LCID, 1, (8, 0), ((8, 0), (8, 0)),TTD
			, FieldCode)

	def GetClientID(self, ClientName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(35, LCID, 1, (3, 0), ((8, 0),),ClientName
			)

	def GetCodeSpecs(self, EvCode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(36, LCID, 1, (3, 0), ((3, 0),),EvCode
			)

	def GetCodeSpecsLazy(self, EvCode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(111, LCID, 1, (3, 0), ((3, 0),),EvCode
			)

	def GetDebug(self, TankName=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(28, LCID, 1, (8, 0), ((8, 0),),TankName
			)

	def GetEnumServer(self, Index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(51, LCID, 1, (8, 0), ((3, 0),),Index
			)

	def GetEnumTank(self, Index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(47, LCID, 1, (8, 0), ((3, 0),),Index
			)

	def GetEpocCode(self, Index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(58, LCID, 1, (8, 0), ((3, 0),),Index
			)

	def GetEpocs(self, pEPs=defaultNamedNotOptArg, TankCode=defaultNamedNotOptArg, T1=defaultNamedNotOptArg, T2=defaultNamedNotOptArg
			, MaxRet=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(60, LCID, 1, (3, 0), ((16389, 0), (3, 0), (5, 0), (5, 0), (3, 0)),pEPs
			, TankCode, T1, T2, MaxRet)

	def GetEpocsEx(self, pEPs=defaultNamedNotOptArg, TankCode=defaultNamedNotOptArg, MaxReturn=defaultNamedNotOptArg, Mode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(94, LCID, 1, (3, 0), ((16389, 0), (3, 0), (3, 0), (3, 0)),pEPs
			, TankCode, MaxReturn, Mode)

	def GetEpocsExV(self, TankCode=defaultNamedNotOptArg, Mode=defaultNamedNotOptArg):
		return self._ApplyTypes_(95, 1, (12, 0), ((8, 0), (3, 0)), u'GetEpocsExV', None,TankCode
			, Mode)

	def GetEpocsV(self, TankCode=defaultNamedNotOptArg, T1=defaultNamedNotOptArg, T2=defaultNamedNotOptArg, MaxEpocs=defaultNamedNotOptArg):
		return self._ApplyTypes_(57, 1, (12, 0), ((8, 0), (5, 0), (5, 0), (3, 0)), u'GetEpocsV', None,TankCode
			, T1, T2, MaxEpocs)

	def GetError(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(29, LCID, 1, (8, 0), (),)

	def GetEvTsqIdx(self):
		"""method GetEvTsqIdx"""
		return self._ApplyTypes_(122, 1, (12, 0), (), u'GetEvTsqIdx', None,)

	def GetEventCodes(self, EvType=defaultNamedNotOptArg):
		return self._ApplyTypes_(38, 1, (12, 0), ((3, 0),), u'GetEventCodes', None,EvType
			)

	def GetFilterTolerance(self):
		return self._oleobj_.InvokeTypes(87, LCID, 1, (5, 0), (),)

	def GetGlobal(self, code=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(106, LCID, 1, (5, 0), ((3, 0),),code
			)

	def GetGlobalB(self, name=defaultNamedNotOptArg):
		"""method GetGlobalB"""
		return self._oleobj_.InvokeTypes(119, LCID, 1, (5, 0), ((8, 0),),name
			)

	def GetGlobalStringB(self, name=defaultNamedNotOptArg):
		"""method GetGlobalStringB"""
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(120, LCID, 1, (8, 0), ((8, 0),),name
			)

	def GetGlobalStringV(self, name=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(108, LCID, 1, (8, 0), ((31, 0),),name
			)

	def GetGlobalV(self, name=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(107, LCID, 1, (5, 0), ((31, 0),),name
			)

	def GetHotBlock(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(66, LCID, 1, (8, 0), (),)

	def GetNPer(self, DForm=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(59, LCID, 1, (3, 0), ((3, 0),),DForm
			)

	def GetServerItem(self, ServerName=defaultNamedNotOptArg, ItemCode=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(50, LCID, 1, (8, 0), ((8, 0), (8, 0)),ServerName
			, ItemCode)

	def GetSortChanMap(self, sortName=defaultNamedNotOptArg, snipName=defaultNamedNotOptArg):
		"""method GetSortChanMap"""
		return self._ApplyTypes_(126, 1, (12, 0), ((8, 0), (8, 0)), u'GetSortChanMap', None,sortName
			, snipName)

	def GetSortCondition(self, sortName=defaultNamedNotOptArg, snipName=defaultNamedNotOptArg, idxChan=defaultNamedNotOptArg):
		"""method GetSortCondition"""
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(124, LCID, 1, (8, 0), ((8, 0), (8, 0), (3, 0)),sortName
			, snipName, idxChan)

	def GetSortName(self, EventName=defaultNamedNotOptArg, idxSortID=defaultNamedNotOptArg):
		"""method GetSortName"""
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(113, LCID, 1, (8, 0), ((8, 0), (3, 0)),EventName
			, idxSortID)

	def GetStatus(self, StatCode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(39, LCID, 1, (3, 0), ((3, 0),),StatCode
			)

	def GetTankItem(self, TankName=defaultNamedNotOptArg, ItemCode=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(52, LCID, 1, (8, 0), ((8, 0), (8, 0)),TankName
			, ItemCode)

	def GetValidTimeRanges(self, pRanges=defaultNamedNotOptArg, MaxReturn=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(99, LCID, 1, (3, 0), ((16389, 0), (3, 0)),pRanges
			, MaxReturn)

	def GetValidTimeRangesV(self):
		return self._ApplyTypes_(100, 1, (12, 0), (), u'GetValidTimeRangesV', None,)

	def IndexEvent(self, TankCode=defaultNamedNotOptArg, Channel=defaultNamedNotOptArg, SortCode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(83, LCID, 1, (3, 0), ((3, 0), (3, 0), (3, 0)),TankCode
			, Channel, SortCode)

	def InitializeTank(self, TankName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(40, LCID, 1, (3, 0), ((8, 0),),TankName
			)

	def OpenTank(self, TankName=defaultNamedNotOptArg, AccessMode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(30, LCID, 1, (3, 0), ((8, 0), (8, 0)),TankName
			, AccessMode)

	def ParseEv(self, RecIndex=defaultNamedNotOptArg, TimeStamp=defaultNamedNotOptArg, Channel=defaultNamedNotOptArg, SortCode=defaultNamedNotOptArg
			, Npts=defaultNamedNotOptArg, pData=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(75, LCID, 1, (3, 0), ((3, 0), (16389, 0), (16387, 0), (16387, 0), (16387, 0), (16388, 0)),RecIndex
			, TimeStamp, Channel, SortCode, Npts, pData
			)

	def ParseEvInfoV(self, RecIndex=defaultNamedNotOptArg, nRecs=defaultNamedNotOptArg, nItem=defaultNamedNotOptArg):
		return self._ApplyTypes_(77, 1, (12, 0), ((3, 0), (3, 0), (3, 0)), u'ParseEvInfoV', None,RecIndex
			, nRecs, nItem)

	def ParseEvV(self, RecIndex=defaultNamedNotOptArg, nRecs=defaultNamedNotOptArg):
		return self._ApplyTypes_(76, 1, (12, 0), ((3, 0), (3, 0)), u'ParseEvV', None,RecIndex
			, nRecs)

	def ParseFilterDesc(self, FiltDesc=defaultNamedNotOptArg, TankCode=defaultNamedNotOptArg, TestCode=defaultNamedNotOptArg, V1=defaultNamedNotOptArg
			, V2=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(80, LCID, 1, (3, 0), ((8, 0), (16387, 0), (16387, 0), (16389, 0), (16389, 0)),FiltDesc
			, TankCode, TestCode, V1, V2)

	def QryEpocAt(self, TankCode=defaultNamedNotOptArg, rTime=defaultNamedNotOptArg, ReqItem=defaultNamedNotOptArg, RetVal=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(64, LCID, 1, (3, 0), ((3, 0), (5, 0), (3, 0), (16389, 0)),TankCode
			, rTime, ReqItem, RetVal)

	def QryEpocAtV(self, TankCode=defaultNamedNotOptArg, rTime=defaultNamedNotOptArg, ReqItem=defaultNamedNotOptArg):
		return self._ApplyTypes_(65, 1, (12, 0), ((8, 0), (5, 0), (3, 0)), u'QryEpocAtV', None,TankCode
			, rTime, ReqItem)

	def QueryBlockName(self, BlockNumber=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(41, LCID, 1, (8, 0), ((3, 0),),BlockNumber
			)

	def ReadEvents(self, MaxRet=defaultNamedNotOptArg, TankCode=defaultNamedNotOptArg, Channel=defaultNamedNotOptArg, SortCode=defaultNamedNotOptArg
			, T1=defaultNamedNotOptArg, T2=defaultNamedNotOptArg, Options=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(62, LCID, 1, (3, 0), ((3, 0), (3, 0), (3, 0), (3, 0), (5, 0), (5, 0), (3, 0)),MaxRet
			, TankCode, Channel, SortCode, T1, T2
			, Options)

	def ReadEventsSimple(self, EventName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(96, LCID, 1, (3, 0), ((8, 0),),EventName
			)

	def ReadEventsV(self, MaxRet=defaultNamedNotOptArg, TankCode=defaultNamedNotOptArg, Channel=defaultNamedNotOptArg, SortCode=defaultNamedNotOptArg
			, T1=defaultNamedNotOptArg, T2=defaultNamedNotOptArg, Options=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(63, LCID, 1, (3, 0), ((3, 0), (8, 0), (3, 0), (3, 0), (5, 0), (5, 0), (8, 0)),MaxRet
			, TankCode, Channel, SortCode, T1, T2
			, Options)

	def ReadWaves(self, TankCode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(97, LCID, 1, (3, 0), ((3, 0),),TankCode
			)

	def ReadWavesOnTimeRange(self, TankCode=defaultNamedNotOptArg, Channel=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(101, LCID, 1, (3, 0), ((3, 0), (3, 0)),TankCode
			, Channel)

	def ReadWavesOnTimeRangeB(self, TankCode=defaultNamedNotOptArg, Channel=defaultNamedNotOptArg):
		"""method ReadWavesOnTimeRangeB"""
		return self._ApplyTypes_(116, 1, (12, 0), ((8, 0), (3, 0)), u'ReadWavesOnTimeRangeB', None,TankCode
			, Channel)

	def ReadWavesOnTimeRangeV(self, TankCode=defaultNamedNotOptArg, Channel=defaultNamedNotOptArg):
		return self._ApplyTypes_(102, 1, (12, 0), ((31, 0), (3, 0)), u'ReadWavesOnTimeRangeV', None,TankCode
			, Channel)

	def ReadWavesV(self, TankCode=defaultNamedNotOptArg):
		return self._ApplyTypes_(98, 1, (12, 0), ((8, 0),), u'ReadWavesV', None,TankCode
			)

	def ReleaseServer(self):
		return self._oleobj_.InvokeTypes(42, LCID, 1, (24, 0), (),)

	def RemoveBlock(self, BlockName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(56, LCID, 1, (3, 0), ((8, 0),),BlockName
			)

	def RemoveEvents(self, BlockName=defaultNamedNotOptArg, RelTime1=defaultNamedNotOptArg, RelTime2=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(55, LCID, 1, (3, 0), ((8, 0), (5, 0), (5, 0)),BlockName
			, RelTime1, RelTime2)

	def RemoveServer(self, ServerName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(49, LCID, 1, (3, 0), ((8, 0),),ServerName
			)

	def RemoveTank(self, TankName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(25, LCID, 1, (3, 0), ((8, 0),),TankName
			)

	def ResetFilters(self):
		return self._oleobj_.InvokeTypes(82, LCID, 1, (24, 0), (),)

	def ResetGlobals(self):
		return self._oleobj_.InvokeTypes(110, LCID, 1, (24, 0), (),)

	def ResetTank(self, TankName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(43, LCID, 1, (3, 0), ((8, 0),),TankName
			)

	def SaveSortCodes(self, sortName=defaultNamedNotOptArg, snipName=defaultNamedNotOptArg, idxChan=defaultNamedNotOptArg, sortCondition=defaultNamedNotOptArg
			, sortCodeArray=defaultNamedNotOptArg):
		"""method SaveSortCodes"""
		return self._oleobj_.InvokeTypes(123, LCID, 1, (3, 0), ((8, 0), (8, 0), (3, 0), (8, 0), (12, 0)),sortName
			, snipName, idxChan, sortCondition, sortCodeArray)

	def SelectBlock(self, BlockName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(32, LCID, 1, (3, 0), ((8, 0),),BlockName
			)

	def SetBuildHead(self, TankCode=defaultNamedNotOptArg, DataForm=defaultNamedNotOptArg, SampFreq=defaultNamedNotOptArg, nNet=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(70, LCID, 1, (24, 0), ((8, 0), (3, 0), (5, 0), (3, 0)),TankCode
			, DataForm, SampFreq, nNet)

	def SetEpocTimeFilter(self, EpocCode=defaultNamedNotOptArg, Offset=defaultNamedNotOptArg, Dur=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(90, LCID, 1, (3, 0), ((3, 0), (5, 0), (5, 0)),EpocCode
			, Offset, Dur)

	def SetEpocTimeFilterB(self, EpocCode=defaultNamedNotOptArg, Offset=defaultNamedNotOptArg, Dur=defaultNamedNotOptArg):
		"""method SetEpocTimeFilterB"""
		return self._oleobj_.InvokeTypes(114, LCID, 1, (3, 0), ((8, 0), (5, 0), (5, 0)),EpocCode
			, Offset, Dur)

	def SetEpocTimeFilterV(self, EpocCode=defaultNamedNotOptArg, Offset=defaultNamedNotOptArg, Dur=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(91, LCID, 1, (3, 0), ((31, 0), (5, 0), (5, 0)),EpocCode
			, Offset, Dur)

	def SetFilter(self, TankCode=defaultNamedNotOptArg, TestCode=defaultNamedNotOptArg, V1=defaultNamedNotOptArg, V2=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(78, LCID, 1, (3, 0), ((3, 0), (3, 0), (5, 0), (5, 0)),TankCode
			, TestCode, V1, V2)

	def SetFilterArray(self, Dim=defaultNamedNotOptArg, ID=defaultNamedNotOptArg, Filter=defaultNamedNotOptArg, Exclusive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(89, LCID, 1, (3, 0), ((3, 0), (3, 0), (8, 0), (3, 0)),Dim
			, ID, Filter, Exclusive)

	def SetFilterTolerance(self, loosenFactor=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(86, LCID, 1, (3, 0), ((5, 0),),loosenFactor
			)

	def SetFilterWithDesc(self, FiltDesc=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(79, LCID, 1, (3, 0), ((8, 0),),FiltDesc
			)

	def SetFilterWithDescEx(self, Filter=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(88, LCID, 1, (3, 0), ((8, 0),),Filter
			)

	def SetGlobal(self, code=defaultNamedNotOptArg, Value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(103, LCID, 1, (3, 0), ((3, 0), (5, 0)),code
			, Value)

	def SetGlobalB(self, name=defaultNamedNotOptArg, Value=defaultNamedNotOptArg):
		"""method SetGlobalB"""
		return self._oleobj_.InvokeTypes(117, LCID, 1, (3, 0), ((8, 0), (5, 0)),name
			, Value)

	def SetGlobalStringB(self, name=defaultNamedNotOptArg, strvalue=defaultNamedNotOptArg):
		"""method SetGlobalStringB"""
		return self._oleobj_.InvokeTypes(118, LCID, 1, (3, 0), ((8, 0), (8, 0)),name
			, strvalue)

	def SetGlobalStringV(self, name=defaultNamedNotOptArg, strvalue=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(105, LCID, 1, (3, 0), ((31, 0), (31, 0)),name
			, strvalue)

	def SetGlobalV(self, name=defaultNamedNotOptArg, Value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(104, LCID, 1, (3, 0), ((31, 0), (5, 0)),name
			, Value)

	def SetGlobals(self, str=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(109, LCID, 1, (3, 0), ((31, 0),),str
			)

	def SetGlobalsB(self, str=defaultNamedNotOptArg):
		"""method SetGlobalsB"""
		return self._oleobj_.InvokeTypes(121, LCID, 1, (3, 0), ((8, 0),),str
			)

	def SetRefEpoc(self, EpocCode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(92, LCID, 1, (3, 0), ((3, 0),),EpocCode
			)

	def SetRefEpocB(self, EpocCode=defaultNamedNotOptArg):
		"""method SetRefEpocB"""
		return self._oleobj_.InvokeTypes(115, LCID, 1, (3, 0), ((8, 0),),EpocCode
			)

	def SetRefEpocV(self, EpocCode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(93, LCID, 1, (3, 0), ((31, 0),),EpocCode
			)

	def SetRefTime(self, TimeOS=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(31, LCID, 1, (3, 0), ((5, 0),),TimeOS
			)

	def SetUseSortName(self, sortID=defaultNamedNotOptArg):
		"""method SetUseSortName"""
		return self._oleobj_.InvokeTypes(112, LCID, 1, (3, 0), ((8, 0),),sortID
			)

	def StartRecord(self, BlockName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(45, LCID, 1, (3, 0), ((8, 0),),BlockName
			)

	def StopRecord(self):
		return self._oleobj_.InvokeTypes(46, LCID, 1, (24, 0), (),)

	def StringToEvCode(self, EvCode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(37, LCID, 1, (3, 0), ((8, 0),),EvCode
			)

	def SwitchClient(self, ClientName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(67, LCID, 1, (3, 0), ((8, 0),),ClientName
			)

	def ToTTD(self, ServName=defaultNamedNotOptArg, TankName=defaultNamedNotOptArg, BlockName=defaultNamedNotOptArg, EvName=defaultNamedNotOptArg
			, ChanList=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(53, LCID, 1, (8, 0), ((8, 0), (8, 0), (8, 0), (8, 0), (16387, 0)),ServName
			, TankName, BlockName, EvName, ChanList)

	def WriteEvents(self, NumEv=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(61, LCID, 1, (3, 0), ((3, 0),),NumEv
			)

	_prop_map_get_ = {
		"ClientID": (6, 2, (3, 0), (), "ClientID", None),
		"CurBlockMemo": (3, 2, (8, 0), (), "CurBlockMemo", None),
		"CurBlockName": (1, 2, (8, 0), (), "CurBlockName", None),
		"CurBlockNotes": (17, 2, (8, 0), (), "CurBlockNotes", None),
		"CurBlockOwner": (2, 2, (8, 0), (), "CurBlockOwner", None),
		"CurBlockStartTime": (4, 2, (5, 0), (), "CurBlockStartTime", None),
		"CurBlockStopTime": (5, 2, (5, 0), (), "CurBlockStopTime", None),
		"Domain": (15, 2, (8, 0), (), "Domain", None),
		"EvChannel": (13, 2, (3, 0), (), "EvChannel", None),
		"EvDForm": (10, 2, (3, 0), (), "EvDForm", None),
		"EvDataSize": (8, 2, (3, 0), (), "EvDataSize", None),
		"EvFirstTime": (9, 2, (5, 0), (), "EvFirstTime", None),
		"EvSampFreq": (11, 2, (4, 0), (), "EvSampFreq", None),
		"EvTimeStamp": (12, 2, (5, 0), (), "EvTimeStamp", None),
		"EvType": (7, 2, (3, 0), (), "EvType", None),
		"Password": (16, 2, (8, 0), (), "Password", None),
		"Username": (14, 2, (8, 0), (), "Username", None),
	}
	_prop_map_put_ = {
		"ClientID" : ((6, LCID, 4, 0),()),
		"CurBlockMemo" : ((3, LCID, 4, 0),()),
		"CurBlockName" : ((1, LCID, 4, 0),()),
		"CurBlockNotes" : ((17, LCID, 4, 0),()),
		"CurBlockOwner" : ((2, LCID, 4, 0),()),
		"CurBlockStartTime" : ((4, LCID, 4, 0),()),
		"CurBlockStopTime" : ((5, LCID, 4, 0),()),
		"Domain" : ((15, LCID, 4, 0),()),
		"EvChannel" : ((13, LCID, 4, 0),()),
		"EvDForm" : ((10, LCID, 4, 0),()),
		"EvDataSize" : ((8, LCID, 4, 0),()),
		"EvFirstTime" : ((9, LCID, 4, 0),()),
		"EvSampFreq" : ((11, LCID, 4, 0),()),
		"EvTimeStamp" : ((12, LCID, 4, 0),()),
		"EvType" : ((7, LCID, 4, 0),()),
		"Password" : ((16, LCID, 4, 0),()),
		"Username" : ((14, LCID, 4, 0),()),
	}

class _DTTankXEvents:
	"""Event interface for TTankX Control"""
	CLSID = CLSID_Sink = IID('{9C0BD59B-8842-47DA-8105-DC3E883D72D1}')
	coclass_clsid = IID('{670490CE-57D2-4176-8E74-80C4C6A47D88}')
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
# This CoClass is known by the name 'TTANK.X'
class TTankX(CoClassBaseClass): # A CoClass
	# TTankX Control
	CLSID = IID('{670490CE-57D2-4176-8E74-80C4C6A47D88}')
	coclass_sources = [
		_DTTankXEvents,
	]
	default_source = _DTTankXEvents
	coclass_interfaces = [
		_DTTankX,
	]
	default_interface = _DTTankX

RecordMap = {
}

CLSIDToClassMap = {
	'{670490CE-57D2-4176-8E74-80C4C6A47D88}' : TTankX,
	'{9C0BD59B-8842-47DA-8105-DC3E883D72D1}' : _DTTankXEvents,
	'{BE6CAD3F-28F1-4EAC-B210-9CAA5CA8B5B8}' : _DTTankX,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
}


NamesToIIDMap = {
	'_DTTankX' : '{BE6CAD3F-28F1-4EAC-B210-9CAA5CA8B5B8}',
	'_DTTankXEvents' : '{9C0BD59B-8842-47DA-8105-DC3E883D72D1}',
}


