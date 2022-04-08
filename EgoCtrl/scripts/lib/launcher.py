#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, signal
import yaml

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.normpath(os.path.join(current_path, './')))
sys.path.append(os.path.normpath(os.path.join(current_path, '../')))

from lib.define import *
from lib.controller import *

with open('example_config.yaml') as f:
    config = yaml.safe_load(f)
sensor_file = config['setting']['sensor']
user_id = config['setting']['user_id']
user_pw = config['setting']['user_pw']
version = config['setting']['version']
_map = config['setting']['map']
_vehicle = config['setting']['vehicle']

class launcher_start(controller):
        
    def __init__(self):                
        self.controller = controller()
        self.is_first = True
        self.is_wait=0
        signal.signal(signal.SIGINT, self.signal_handler) #handle ctrl-c
    def launcher_start(self):
        
        while True:
            
            if self.controller.update():             
                self.controller.is_waitting() #status_wait 
                self.controller.is_downloading() #check_is_download_status                       

                if self.controller.is_befor_login():
                    self.controller.commander(Command.LOGIN,user_id+'/'+user_pw) # Login

                if self.controller.is_after_login() or self.controller.is_after_sim_quit_to_launcher():  

                    self.controller.commander(Command.SELECT_VER,version) # select the version

                if self.controller.is_not_find_version(): # version check
                    print(f"cannot find {version}. Try another version you have.")
                    break
                    
                if self.controller.is_can_execute_sim():                                                                     
                    self.controller.commander(Command.EXECUTE_SIM,'') #Simulator excute                      

                                            
                if self.controller.is_sim_not_install():
                    print(f"{version} is not installed. Wait a few minutes.\n Installing....................")                                
                    self.controller.commander(Command.INSTALL_SIM,'') #Simulator install                     


                if self.controller.is_sim_lobby():                    
                    self.controller.commander(Command.MAP_VEHICLE_SELECT, _map+'/'+ _vehicle) # select the map and the vehicle
                    self.is_first = False

                if self.controller.is_sim_playing():
                    
                    if (self.is_first):
                        self.controller.commander(Command.MAP_VEHICLE_SELECT, _map+'/'+_vehicle) # select the map and the vehicle 
                        self.is_first = False
                    else:
                        self.controller.commander(Command.SEN_SETTING,sensor_file) #Sensor setting
                        time.sleep(2)     
                        while True:
                            
                            rostopic_list_cmd = os.popen('rostopic list')
                            rostopic_list_res = rostopic_list_cmd.read()
                            
                            if('/lidar2D' in rostopic_list_res):
                                print('\033[92m'+'Network Connection Success'+'\033[0m')
                                break
                            else:
                                print('\033[91m'+'Network Connection Failed Wait..'+'\033[0m')                        
                                self.controller.commander(Command.SEN_SETTING,sensor_file) #Sensor setting
                                time.sleep(2)
                        
                        print("done")
                        break

            else :
                print("[NO Simulator Control Data]")
                time.sleep(1)
        exit(0)
    def signal_handler(self, signal, frame):
        sys.exit(0) 

if __name__ == '__main__':
    ego_init =launcher_start()
    ego_init.launcher_start()
