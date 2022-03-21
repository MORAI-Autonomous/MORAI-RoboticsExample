#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import tf
from morai_msgs.msg import EgoVehicleStatus
from math import pi
import numpy as np

class tf_listener():
    def __init__(self):
        rospy.init_node('status_listener', anonymous=True)
        rospy.Subscriber('/Ego_topic',EgoVehicleStatus, self.statusCB)
        self.status_msg=EgoVehicleStatus()
  
        rate = rospy.Rate(30)

        while not rospy.is_shutdown():
            rate.sleep()

    def statusCB(self,data): 
        self.status_msg=data
        print("tf broad cast")
        br = tf.TransformBroadcaster()
        br.sendTransform((self.status_msg.position.x, self.status_msg.position.y , self.status_msg.position.z),
                        tf.transformations.quaternion_from_euler(0, 0, self.status_msg.heading/180 *pi),
                        data.header.stamp,
                        "base_link",
                        "map")

    
if __name__ == '__main__':
    try:
        tl=tf_listener()
    except rospy.ROSInterruptException:
        pass