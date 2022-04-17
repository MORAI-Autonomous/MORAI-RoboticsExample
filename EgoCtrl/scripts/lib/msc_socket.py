#!/usr/bin/env python
# -*- Encoding: utf-8 -*-
from lib.udp_parser import udp_parser, udp_sender
import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)

receive_user_ip = config['setting']['host_ip']
receive_user_port = config['setting']['host_port']
request_dst_ip = config['setting']['dst_ip']
request_dst_port = config['setting']['dst_port']

class msc_socket:
    def __init__(self):
        self.get_status = udp_parser(receive_user_ip, receive_user_port,'get_sim_status')        
        self.set_status = udp_sender(request_dst_ip, request_dst_port,'set_sim_status') 
        print("socket")

    def connect(self):
        return self.get_status, self.set_status
