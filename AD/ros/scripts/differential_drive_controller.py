#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import rospy
from morai_msgs.msg  import DdCtrlCmd


class Controller :

    def __init__(self):
        rospy.init_node('Controller', anonymous=True)


        self.ctrl_pub= rospy.Publisher('/DdCtrlCmd',DdCtrlCmd, queue_size=1)
        self.ctrl_msg=DdCtrlCmd()
        self.ctrl_msg.cmd_type=1
        self.control_loop()
        


    def go_staright(self):
        self.ctrl_msg.right_track_speed = 5
        self.ctrl_msg.left_track_speed = 5
        print('Go Straight Func')

    def stop(self):
        self.ctrl_msg.right_track_speed = 0
        self.ctrl_msg.left_track_speed = 0
        print('STOP Func')

    def go_back(self):
        self.ctrl_msg.right_track_speed = -5
        self.ctrl_msg.left_track_speed = -5
        print('Go Back Func')

    def turn_left(self):
        self.ctrl_msg.right_track_speed = 5
        self.ctrl_msg.left_track_speed = 2.5
        print('Turn Left Func')


    def turn_right(self):
        self.ctrl_msg.right_track_speed = 2.5
        self.ctrl_msg.left_track_speed = 5
        print('Turn Right Func')

    def control_loop(self):
        rate=rospy.Rate(30)

        while not rospy.is_shutdown():

            self.go_staright()
            # self.stop()
            # self.go_back()
            # self.turn_left()
            # self.turn_right()
            self.ctrl_pub.publish(self.ctrl_msg)
            rate.sleep()    

    


if __name__ == '__main__':
    try:
        test=Controller()
    except rospy.ROSInterruptException:
        pass

