#!/usr/bin/env python
# -*- Encoding: utf-8 -*-
from lib.udp_parser import udp_parser, udp_sender

receive_user_ip = '127.0.0.1'
receive_user_port = 10329
request_dst_ip = '127.0.0.1'
request_dst_port = 10509

class msc_socket:
    def __init__(self):
        self.get_status = udp_parser(receive_user_ip, receive_user_port,'get_sim_status')        
        self.set_status = udp_sender(request_dst_ip, request_dst_port,'set_sim_status') 
        print("socket")

    def connect(self):
        return self.get_status, self.set_status
