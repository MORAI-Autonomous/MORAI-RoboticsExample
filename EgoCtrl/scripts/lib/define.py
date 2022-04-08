#!/usr/bin/env python
# -*- Encoding: utf-8 -*-
# from lib.read_text import * 
from enum import Enum

class Platform:    
    LUANCHER = '0x01'
    SIMULATOR = '0x02'

class Stage:   
    BEFORE_LOGIN = '0x01'      
    AFTER_LOGIN = '0x02'    
    LOBBY = '0x01'
    PLAY = '0x02'

class Status:
    HOLDING = '0x0001'

    VER_SELECTED = '0x0001'
    VER_NOT_SELECTED = '0X0002'
    NEED_INSTALL = '0x0003'
    ASSET_DOWNLOADING = '0x0004'
    SIM_DOWNLOADING = '0x0005'
    LOGIN_COMPLETE = '0x0006'
    QUIT_SIM_SUCCESS = '0x0007'

    HOLDING = '0x0001'
    MAP_VEHICLE_NOT_SELECTED = '0x0002'
    LOADING = '0x0003'

    PLAYING = '0x0001'
    PAUSE = '0x0002'
    LOADING = '0x0003'
    QUITTING = '0x0004'
    MAP_OK = '0x0005'  

    WAIT = '0x1000'

class Result:
    NONE = '0x00'    
    SUCCESS = '0x01'    
    INVALID_PALTFORM = '0x11'
    INVALID_STAGE = '0x12'
    ERROR_ID = '0x23'
    ERROR_PW = '0x24'
    ERROR_VERSION = '0x25'
    NOT_INSTALL = '0x26'
    INVALID_MAP = '0X31'
    INVALID_VEHICLE = '0x32'
    ERROR_NET_LOAD = '0x33'
    ERROR_NET_LOAD = '0x34'
    ERROR_SEN_LOAD = '0x35'
    ERROR_SEN_LOAD = '0x36'
    ERROR_SCEN_LOAD = '0x37'
 
class cmd:
    LOGIN = '0x0001'
    SELECT_VER = '0x0002'
    INSTALL_SIM = '0x0003'
    EXECUTE_SIM = '0x0004'
    QUIT_LAUNCHER = '0x1000'     
    LOGOUT = '0x1001'

    MAP_VEHICLE_SELECT = '0x0001'
    SIM_PAUSE = '0x0002'
    SIM_PLAY = '0x0003'
    NET_SETTING = '0x0011'
    NET_SAVE = '0x0016'

    SEN_SETTING = '0x0012'
    SEN_SAVE = '0x0015'

    SCEN_SETTING = '0x0013'
    SCEN_SAVE = '0x0014'
    QUIT_SIM = '0X1000'

class Command : 
    LOGIN = 'LOGIN'
    SELECT_VER = 'SELECT_VER'
    INSTALL_SIM = 'INSTALL_SIM'
    EXECUTE_SIM = 'EXECUTE_SIM'
    QUIT_LAUNCHER = 'QUIT_LAUNCHER'     
    LOGOUT = 'LOGOUT'

    MAP_VEHICLE_SELECT = 'MAP_VEHICLE_SELECT'
    SIM_PAUSE = 'SIM_PAUSE'
    SIM_PLAY = 'SIM_PLAY'
    NET_SETTING = 'NET_SETTING'
    NET_SAVE = 'NET_SAVE'
    SEN_SETTING = 'SEN_SETTING'
    SEN_SAVE = 'SEN_SAVE'
    SCEN_SETTING = 'SCEN_SETTING'
    SCEN_SAVE = 'SCEN_SAVE'
    QUIT_SIM = 'QUIT_SIM'

class Command_list(Enum):
    LOGIN           = (Platform.LUANCHER, cmd.LOGIN         , "")
    SELECT_VER      = (Platform.LUANCHER, cmd.SELECT_VER    , "")
    INSTALL_SIM     = (Platform.LUANCHER, cmd.INSTALL_SIM   , "")
    EXECUTE_SIM     = (Platform.LUANCHER, cmd.EXECUTE_SIM   , "")
    QUIT_LAUNCHER   = (Platform.LUANCHER, cmd.QUIT_LAUNCHER , "")
    LOGOUT          = (Platform.LUANCHER, cmd.LOGOUT        , "")
    MAP_VEHICLE_SELECT      = (Platform.SIMULATOR, cmd.MAP_VEHICLE_SELECT   , "")
    SIM_PAUSE               = (Platform.SIMULATOR, cmd.SIM_PAUSE            , "")
    SIM_PLAY                = (Platform.SIMULATOR, cmd.SIM_PLAY             , "")
    NET_SETTING             = (Platform.SIMULATOR, cmd.NET_SETTING          , "")
    NET_SAVE                = (Platform.SIMULATOR, cmd.NET_SAVE             , "")
    SEN_SETTING             = (Platform.SIMULATOR, cmd.SEN_SETTING          , "")
    SEN_SAVE                = (Platform.SIMULATOR, cmd.SEN_SAVE             , "")
    SCEN_SETTING            = (Platform.SIMULATOR, cmd.SCEN_SETTING         , "")
    SCEN_SAVE               = (Platform.SIMULATOR, cmd.SCEN_SAVE            , "")
    QUIT_SIM                = (Platform.SIMULATOR, cmd.QUIT_SIM             , "")   