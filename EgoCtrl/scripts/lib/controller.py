#!/usr/bin/env python
# -*- Encoding: utf-8 -*-

import time,os

from lib.define import *
from lib.msc_socket import msc_socket
from lib.status_data_print import status_parser
import platform
import time
class controller(msc_socket):

    def __init__(self):
        super(controller,self).__init__()    
        self.status_parser = status_parser()    
        self.status_data=None
        self.wait_time = 0.0
        
    def update(self):        
        
        self.status_data = self.get_status.get_data()        
        if len (self.status_data) == 0:
            return False
        else:  
            self.platform, self.stage, self.status, self.cmd_platform, self.cmd, self.cmd_option, self.result = self.status_data                      
            self.clear()
            self.status_parser.print_info(self.status_data)
            return True

    def commander(self,cmd,option):#change_option
        cmd_platform,cmd_command,cmd_option = Command_list[cmd].value       
        if cmd == Command.INSTALL_SIM or cmd == Command.EXECUTE_SIM or cmd == Command.QUIT_LAUNCHER or cmd == Command.LOGOUT or cmd == Command.SIM_PLAY or cmd == Command.SIM_PAUSE or cmd == Command.QUIT_SIM:            
            self.custom_option =''
            
        else:
            self.custom_option = option                    
        self.send_data(cmd_platform,cmd_command,self.custom_option) 
        time.sleep(1)
        self.is_waitting() #cmd_platform,cmd_command,self.custom_option)


    def is_not_find_version(self):        
        if self.result == Result.ERROR_VERSION:
            print("version_error")
            time.sleep(3) 

        return self.result == Result.ERROR_VERSION

    def is_befor_login(self):
        return self.platform == Platform.LUANCHER and self.stage == Stage.BEFORE_LOGIN #Launcher platform에서 로그인 전 상태                    

    def is_after_login(self):
        return self.platform == Platform.LUANCHER and self.stage == Stage.AFTER_LOGIN and self.status == Status.LOGIN_COMPLETE #Launcher platform에서 로그인 후 상태

    def is_sim_not_install(self):
        return self.status == Status.NEED_INSTALL and self.result == Result.NOT_INSTALL

    def is_can_execute_sim(self):
        return self.status == Status.VER_SELECTED and self.result == Result.SUCCESS

    def is_after_sim_quit_to_launcher(self):
        return self.status == Status.QUIT_SIM_SUCCESS 

    def watting_download(self):
        count=0           
        while True:                        
            self.clear()     
            print("downloading"+"."*count)
            if count == 5 :
                count = 0
            count+=1
            self.update()            
            if self.platform == Platform.LUANCHER and self.status == Status.VER_SELECTED:
                break
            time.sleep(1)

    def watting_execute(self):
        count=0        
        while True:        
            self.clear()
            print("exe_loading"+"."*count)
            if count == 5 :
                count = 0
            count+=1            
            self.update()   
            if self.platform == Platform.SIMULATOR and self.status == Status.HOLDING:
                break
            time.sleep(1)

    def is_sim_lobby(self):
        return self.platform == Platform.SIMULATOR and self.stage == Stage.LOBBY and self.status == Status.HOLDING #Simulator platform에서 로비 Stage의 대기상태
    
    

    def watting_loading(self):
        count=0
        while True:            
            self.clear()
            print("map_vehicle_loading"+"."*count)
            if count == 5 :
                count = 0
            count+=1
            self.update()            
            if self.platform == Platform.SIMULATOR and self.stage == Stage.PLAY and self.status == Status.MAP_OK:
                break
            time.sleep(1)

    def is_sim_playing(self):
        self.update()
        return self.platform == Platform.SIMULATOR and self.stage==Stage.PLAY and (self.status==Status.MAP_OK or self.status == Status.HOLDING)#simulator map/vehicle 로딩 완료
    def is_sim_pause(self):
        self.update()
        return self.platform == Platform.SIMULATOR and (self.status==Status.MAP_OK or self.status == Status.PAUSE)#simulator map/vehicle 로딩 완료
    def is_downloading(self):
        
        if self.platform == Platform.LUANCHER and (self.status == Status.SIM_DOWNLOADING or self.status == Status.ASSET_DOWNLOADING):
            count=0
            while True:
                self.clear()
                self.update()
                if self.status == Status.ASSET_DOWNLOADING :
                    print("Asset Downloading"+"."*count)
                elif self.status == Status.SIM_DOWNLOADING :
                    print("Simulator Downloading"+"."*count)                
                elif self.status == Status.VER_SELECTED:
                    self.update()
                    break

                if count == 5 :
                    count = 0
                count+=1
                # time.sleep(1)
            

    def is_waitting(self):
        self.is_wait = '0x1000'
        
        if int(self.is_wait,16) < int(self.status,16):
            self.tmp_status = int(self.status,16)-4096
            self.update()
            count=0
            
            while True:
                print("status : ",self.tmp_status , self.status)
                self.clear()
                self.update()
                print("wait_status"+"."*count)

                # if count == 5:
                #     count = 0
                # count+=1

                if int(self.status,16) == self.tmp_status :
                    break

                if(self.tmp_status == -4095):
                    break

                # # time.sleep(1)
                


    def send_data(self, cmd_platform, cmd_command, cmd_option):

        try:
            print("send>>",cmd_platform,cmd_command,cmd_option)
            cmd_platform=int(cmd_platform,0)
            cmd_command=int(cmd_command,0)
            cmd_option=cmd_option
            self.set_status.send_data([cmd_platform,cmd_command,cmd_option])
            # time.sleep(1)

            self.update()
            
        except ValueError:
            print("Invalid input")    
        


    def clear(self):

        operation = platform.system()
        if operation == "Linux":
            os.system("clear")
        elif operation == "Windows":
            os.system("cls")        