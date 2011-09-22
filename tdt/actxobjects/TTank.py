# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.00
# By python version 2.6.6 |EPD 6.3-1 (32-bit)| (r266:84292, Sep 20 2010, 11:26:16) [MSC v.1500 32 bit (Intel)]
# From type library 'TTankEng.exe'
# On Mon Nov 22 10:28:59 2010
"""TTankEng 1.0 Type Library"""
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

CLSID = IID('{BBA11881-D2C7-4FDB-873D-A474560D7394}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'TTankEng.TankServer.1'
class TankServer(CoClassBaseClass): # A CoClass
	# TankServer Class
	CLSID = IID('{23ADF218-986A-4FE1-8C7E-0CBB5D8EF70F}')
	coclass_sources = [
	]
	coclass_interfaces = [
	]

ITankServer_vtables_dispatch_ = 0
ITankServer_vtables_ = [
	(( u'AddClient' , u'ClientName' , ), 1610678272, (1610678272, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 12 , (3, 0, None, None) , 0 , )),
	(( u'AddTank' , u'TankName' , u'FilePath' , ), 1610678273, (1610678273, (), [ (8, 1, None, None) , 
			(8, 1, None, None) , ], 1 , 1 , 4 , 0 , 16 , (3, 0, None, None) , 0 , )),
	(( u'CloseTank' , u'CID' , ), 1610678274, (1610678274, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 20 , (3, 0, None, None) , 0 , )),
	(( u'DeleteClient' , u'CID' , ), 1610678275, (1610678275, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( u'RemoveTank' , u'TankName' , ), 1610678276, (1610678276, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 28 , (3, 0, None, None) , 0 , )),
	(( u'GetBlockInfo' , u'CID' , u'Name' , u'Owner' , u'Memo' , 
			u'StartTime' , u'StopTime' , u'Notes' , ), 1610678277, (1610678277, (), [ (3, 1, None, None) , 
			(16392, 2, None, None) , (16392, 2, None, None) , (16392, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , 
			(16392, 2, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( u'GetError' , u'CID' , u'ErrMess' , ), 1610678278, (1610678278, (), [ (3, 1, None, None) , 
			(16392, 2, None, None) , ], 1 , 1 , 4 , 0 , 36 , (3, 0, None, None) , 0 , )),
	(( u'GetEvents' , u'CID' , u'pvEV' , u'MaxEv' , u'CodeID' , 
			u'ChanNo' , u'SortCode' , u'T1' , u'T2' , u'Options' , 
			), 1610678279, (1610678279, (), [ (3, 1, None, None) , (16396, 2, None, None) , (3, 1, None, None) , (3, 1, None, None) , 
			(3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( u'GetStatus' , u'CID' , u'StatCode' , ), 1610678280, (1610678280, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 1 , 4 , 0 , 44 , (3, 0, None, None) , 0 , )),
	(( u'InitializeTank' , u'TankName' , ), 1610678281, (1610678281, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( u'OpenTank' , u'CID' , u'TankName' , u'Mode' , ), 1610678282, (1610678282, (), [ 
			(3, 1, None, None) , (8, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 52 , (3, 0, None, None) , 0 , )),
	(( u'SaveEvents' , u'CID' , u'pvEV' , ), 1610678283, (1610678283, (), [ (3, 1, None, None) , 
			(16396, 1, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'SelectBlock' , u'CID' , u'Name' , ), 1610678284, (1610678284, (), [ (3, 1, None, None) , 
			(8, 1, None, None) , ], 1 , 1 , 4 , 0 , 60 , (3, 0, None, None) , 0 , )),
	(( u'SetReadOffset' , u'CID' , u'OSTime' , ), 1610678285, (1610678285, (), [ (3, 1, None, None) , 
			(5, 1, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'StartRecord' , u'CID' , u'BlockName' , ), 1610678286, (1610678286, (), [ (3, 1, None, None) , 
			(8, 1, None, None) , ], 1 , 1 , 4 , 0 , 68 , (3, 0, None, None) , 0 , )),
	(( u'StopRecord' , u'CID' , ), 1610678287, (1610678287, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'GetSeqEvents' , u'pvEV' , u'MaxRead' , u'Reset' , ), 1610678288, (1610678288, (), [ 
			(16396, 2, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 76 , (3, 0, None, None) , 0 , )),
	(( u'SetOSTime' , u'CID' , u'OSTime' , ), 1610678289, (1610678289, (), [ (3, 1, None, None) , 
			(5, 1, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'QueryBlockName' , u'CID' , u'n' , u'pName' , ), 1610678290, (1610678290, (), [ 
			(3, 1, None, None) , (3, 1, None, None) , (16392, 2, None, None) , ], 1 , 1 , 4 , 0 , 84 , (3, 0, None, None) , 0 , )),
	(( u'GetEventCodes' , u'CID' , u'pvCL' , u'evtype' , ), 1610678291, (1610678291, (), [ 
			(3, 1, None, None) , (16396, 2, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'ResetTank' , u'TankName' , ), 1610678292, (1610678292, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 92 , (3, 0, None, None) , 0 , )),
	(( u'CheckTank' , u'TankName' , ), 1610678293, (1610678293, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'GetEnumTank' , u'nTank' , u'TankName' , ), 1610678294, (1610678294, (), [ (3, 1, None, None) , 
			(16392, 2, None, None) , ], 1 , 1 , 4 , 0 , 100 , (3, 0, None, None) , 0 , )),
	(( u'GetTankDebug' , u'TankName' , u'DebugMess' , ), 1610678295, (1610678295, (), [ (8, 1, None, None) , 
			(16392, 2, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( u'EnabTankDebug' , u'TankName' , u'enab' , ), 1610678296, (1610678296, (), [ (8, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 1 , 4 , 0 , 108 , (3, 0, None, None) , 0 , )),
	(( u'GetTankItem' , u'Name' , u'ItemCode' , u'RetVal' , ), 1610678297, (1610678297, (), [ 
			(8, 1, None, None) , (8, 1, None, None) , (16392, 2, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( u'RemoveEvents' , u'CID' , u'BlockName' , u'RelTime1' , u'RelTime2' , 
			), 1610678298, (1610678298, (), [ (3, 1, None, None) , (8, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , ], 1 , 1 , 4 , 0 , 116 , (3, 0, None, None) , 0 , )),
	(( u'GetHotBlock' , u'CID' , u'pName' , ), 1610678299, (1610678299, (), [ (3, 1, None, None) , 
			(16392, 2, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( u'GetNumOf' , u'CID' , u'ItemCode' , ), 1610678300, (1610678300, (), [ (3, 1, None, None) , 
			(8, 1, None, None) , ], 1 , 1 , 4 , 0 , 124 , (3, 0, None, None) , 0 , )),
	(( u'GetEpocCodes' , u'CID' , u'pvCL' , ), 1610678301, (1610678301, (), [ (3, 1, None, None) , 
			(16396, 2, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( u'GetEpocs' , u'CID' , u'pvEP' , u'TankCode' , u'T1' , 
			u'T2' , u'MaxEpocs' , ), 1610678302, (1610678302, (), [ (3, 1, None, None) , (16396, 2, None, None) , 
			(3, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 132 , (3, 0, None, None) , 0 , )),
	(( u'SetFilter' , u'CID' , u'TankCode' , u'TestCode' , u'V1' , 
			u'V2' , ), 1610678303, (1610678303, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , 
			(5, 1, None, None) , (5, 1, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( u'QryEpocAt' , u'CID' , u'TankCode' , u'rTime' , u'ReqItem' , 
			u'pRV' , ), 1610678304, (1610678304, (), [ (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , 
			(3, 1, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 140 , (3, 0, None, None) , 0 , )),
	(( u'CreateEpocIndexing' , u'CID' , ), 1610678305, (1610678305, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( u'ClearIndexing' , u'CID' , ), 1610678306, (1610678306, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 148 , (3, 0, None, None) , 0 , )),
	(( u'IndexEvent' , u'CID' , u'TankCode' , u'Channel' , u'SortCode' , 
			), 1610678307, (1610678307, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( u'SetBlockInfo' , u'CID' , u'BlockName' , u'ItemCode' , u'sVal' , 
			), 1610678308, (1610678308, (), [ (3, 1, None, None) , (8, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 156 , (3, 0, None, None) , 0 , )),
	(( u'QryEpocAtIdx' , u'CID' , u'TankCode' , u'Idx' , u'ReqItem' , 
			u'pRV' , ), 1610678309, (1610678309, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , 
			(3, 1, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( u'LosenFactor' , u'CID' , u'pVal' , ), 1610678310, (1610678310, (), [ (3, 0, None, None) , 
			(16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 164 , (3, 0, None, None) , 0 , )),
	(( u'LosenFactor' , u'CID' , u'pVal' , ), 1610678310, (1610678310, (), [ (3, 0, None, None) , 
			(5, 1, None, None) , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( u'SetFilterEx' , u'CID' , u'TankCode' , u'TestCode' , u'V1' , 
			u'V2' , u'dimension' , u'filterIdx' , ), 1610678312, (1610678312, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 1 , 4 , 0 , 172 , (3, 0, None, None) , 0 , )),
	(( u'CacheDalay' , u'CID' , u'pVal' , ), 1610678313, (1610678313, (), [ (3, 1, None, None) , 
			(16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( u'CacheDalay' , u'CID' , u'pVal' , ), 1610678313, (1610678313, (), [ (3, 1, None, None) , 
			(5, 1, None, None) , ], 1 , 4 , 4 , 0 , 180 , (3, 0, None, None) , 0 , )),
	(( u'SetQueryCondition' , u'CID' , u'strQuery' , u'RespectDuration' , ), 1610678315, (1610678315, (), [ 
			(3, 1, None, None) , (8, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( u'SetFilterWithDimension' , u'CID' , u'dimension' , u'ID' , u'strQuery' , 
			u'IsExclusive' , u'RecpectDuration' , ), 1610678316, (1610678316, (), [ (3, 1, None, None) , (3, 1, None, None) , 
			(3, 1, None, None) , (8, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 188 , (3, 0, None, None) , 0 , )),
	(( u'SetEpocTimeFilter' , u'CID' , u'EpocCode' , u'T1' , u'T2' , 
			u'RefOnset' , ), 1610678317, (1610678317, (), [ (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , 
			(5, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( u'SetTimeRefEpoc' , u'CID' , u'EpocCode' , u'RefOnset' , ), 1610678318, (1610678318, (), [ 
			(3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 196 , (3, 0, None, None) , 0 , )),
	(( u'GetEpocsEx' , u'CID' , u'pvEP' , u'TankCode' , u'T1' , 
			u'T2' , u'MaxEpocs' , u'Mode' , ), 1610678319, (1610678319, (), [ (3, 1, None, None) , 
			(16396, 2, None, None) , (3, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( u'GetValidTimeRanges' , u'CID' , u'pvEP' , u'T1' , u'T2' , 
			u'MaxRanges' , ), 1610678320, (1610678320, (), [ (3, 1, None, None) , (16396, 2, None, None) , (5, 1, None, None) , 
			(5, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 204 , (3, 0, None, None) , 0 , )),
	(( u'QryEpocAtEx' , u'CID' , u'pvEP' , u'TankCode' , u'rTime' , 
			u'RespectDuration' , ), 1610678321, (1610678321, (), [ (3, 1, None, None) , (16396, 2, None, None) , (3, 1, None, None) , 
			(5, 1, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( u'StartRecordEx' , u'CID' , u'BlockName' , u'SupplementString' , ), 1610678322, (1610678322, (), [ 
			(3, 1, None, None) , (8, 1, None, None) , (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 212 , (3, 0, None, None) , 0 , )),
	(( u'SetUseSortName' , u'CID' , u'SortName' , u'option' , ), 1610678323, (1610678323, (), [ 
			(3, 1, None, None) , (8, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( u'SaveSortCode' , u'CID' , u'codeName' , u'idxChan' , u'SortName' , 
			u'sortCodeArray' , u'sortCondition' , u'option' , ), 1610678324, (1610678324, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , (12, 1, None, None) , (8, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 1 , 4 , 0 , 220 , (3, 0, None, None) , 0 , )),
	(( u'GetSortInfoList' , u'CID' , u'codeName' , u'option1' , u'option2' , 
			u'pInfoArray' , ), 1610678325, (1610678325, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , 
			(3, 1, None, None) , (16396, 2, None, None) , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( u'GetSortCondition' , u'CID' , u'codeName' , u'idxChan' , u'SortName' , 
			u'option' , u'pSortCondition' , ), 1610678326, (1610678326, (), [ (3, 1, None, None) , (3, 1, None, None) , 
			(3, 1, None, None) , (8, 1, None, None) , (3, 1, None, None) , (16392, 2, None, None) , ], 1 , 1 , 4 , 0 , 228 , (3, 0, None, None) , 0 , )),
	(( u'DeleteSortCode' , u'CID' , u'codeName' , u'idxChan' , u'SortName' , 
			u'option' , ), 1610678327, (1610678327, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , 
			(8, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( u'GetSortChanMap' , u'CID' , u'codeName' , u'SortName' , u'option' , 
			u'pChanMap' , ), 1610678328, (1610678328, (), [ (3, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , 
			(3, 1, None, None) , (16392, 2, None, None) , ], 1 , 1 , 4 , 0 , 236 , (3, 0, None, None) , 0 , )),
	(( u'SetRecordOption' , u'CID' , u'refTime' , u'option' , u'bufOption' , 
			), 1610678329, (1610678329, (), [ (3, 1, None, None) , (5, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
	'{23ADF218-986A-4FE1-8C7E-0CBB5D8EF70F}' : TankServer,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{3E7319F1-2220-41D1-A76A-0A30C45AA03F}' : 'ITankServer',
}


NamesToIIDMap = {
	'ITankServer' : '{3E7319F1-2220-41D1-A76A-0A30C45AA03F}',
}


