#!/usr/bin/env python
# -*- Encoding: utf-8 -*-

import socket
import threading
import time
import struct
import os,sys
class udp_parser :
    def __init__(self,ip,port,data_type):
        self.data_type=data_type
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # default SOCK_DGRAM
        recv_address = (ip,port)
        self.sock.bind(recv_address)
        self.data_size=65535 
        self.parsed_data=[]
        thread = threading.Thread(target=self.recv_udp_data)
        thread.daemon = True 
        thread.start() 

    
    def recv_udp_data(self):
        while True :
            raw_data, sender = self.sock.recvfrom(self.data_size)
            self.data_parsing(raw_data)


    def data_parsing(self,raw_data) :

        if self.data_type == 'get_sim_status' :                             
            header=raw_data[0:11].decode()            
            data_length=struct.unpack('i',raw_data[11:15])
            aux_data = struct.unpack('5i',raw_data[15:35])            
            
            if header == '#SimStatus$' and data_length[0] == 108:                
                data_platform  = struct.unpack('B',raw_data[35:36]) 
                data_platform = format(data_platform[0],'#04x')               
                
                data_stage = struct.unpack('B',raw_data[36:37])
                data_stage = format(data_stage[0],'#04x')

                data_status = struct.unpack('H',raw_data[37:39])                
                data_status = format(data_status[0],'#06x')
                                
                command_platform = struct.unpack('B',raw_data[39:40])
                command_platform = format(command_platform[0], '#04x')

                command_cmd = struct.unpack('H',raw_data[40:42])
                command_cmd = format(command_cmd[0],'#06x')
                
                command_option = raw_data[42:142].decode()

                             
                command_result = struct.unpack('B',raw_data[142:143])
                command_result = format(command_result[0],'#04x')

                self.parsed_data=[data_platform, data_stage, data_status, command_platform, command_cmd, command_option,command_result] 
                
                

    def get_data(self) :
        return self.parsed_data

    def __del__(self):
        self.sock.close()
        print('del')


class udp_sender :
    def __init__(self,ip,port,data_type):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip=ip
        self.port=port
        self.data_type=data_type

        if self.data_type=='set_sim_status':
            
            header='#SimControl$'.encode()                
            data_length=struct.pack('i',103)
            aux_data=struct.pack('5i',0,0,0,0,0)
            self.upper=header+data_length+aux_data
            self.tail='\r\n'.encode()
            
    

    def send_data(self,data):        
        if self.data_type=='set_sim_status':
            
            packed_platform=struct.pack('B',data[0])
            packed_command=struct.pack('H',data[1])     
            option=data[2]+'$'            
            packed_option=option.encode()
               
            if len(option) < 100:
                check=100-len(option)      
                version,_,_,_,_=sys.version_info
                if version == 3 :
                    packed_padding = bytes(check)                         
                elif version == 2 :
                    packed_padding = bytes(0)*(check)
                
                lower=packed_platform+packed_command+packed_option+packed_padding           
            else:
                lower=packed_platform+packed_command+packed_option                       
            
            send_data=self.upper+lower+self.tail                  
 
        self.sock.sendto(send_data,(self.ip,self.port))