#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from morai_msgs.msg import CtrlCmd, EventInfo
from morai_msgs.srv import MoraiEventCmdSrv 
class EgoInitController:
    def __init__(self):

        ctrl_cmd = CtrlCmd()
        rospy.init_node('ego_ctrl', anonymous=True)
        cmd_pub = rospy.Publisher('/ctrl_cmd', CtrlCmd, queue_size=1)

        rospy.wait_for_service('Service_MoraiEventCmd')
        self.event_mode_srv = rospy.ServiceProxy('Service_MoraiEventCmd', MoraiEventCmdSrv)

        self.event_cmd = EventInfo()
        self.mode = rospy.get_param('~mode', "auto")
                
        rate = rospy.Rate(30)
        ctrl_cmd.longlCmdType = 1
        ctrl_cmd.brake = 1

        for _ in range(10):
            cmd_pub.publish(ctrl_cmd)
            rate.sleep()

    def change_ctrl(self):
        if self.mode=='auto':
            self.event_cmd.option = 1
            self.event_cmd.ctrl_mode = 3 # auto mode
            self.event_cmd.gear = 4 # P
        elif self.mode=='cruise':
            self.event_cmd.option = 1
            self.event_cmd.ctrl_mode = 6 # cruise mode
            self.event_cmd.gear = 4 # P
        else:
            self.event_cmd.option = 1
            self.event_cmd.ctrl_mode = 1 # keyboard mode
            self.event_cmd.gear = 4 # P
        return self.event_mode_srv(self.event_cmd)

if __name__ == '__main__':
    try:
        ego_ctrl =EgoInitController()
        response = ego_ctrl.change_ctrl()
    except rospy.ROSInterruptException:
        pass