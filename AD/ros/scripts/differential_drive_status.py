#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rospy

from morai_msgs.msg  import EgoDdVehicleStatus



class StatusSubscriber :

    def __init__(self):
        rospy.init_node('Controller', anonymous=True)

        rospy.Subscriber("/EgoDdVehicleStatus",EgoDdVehicleStatus, self.status_callback)
        rospy.spin()

    

    def status_callback(self,msg):
        print("Wheel speed(rpm)")
        for index,wheel in enumerate(msg.wheel_speed) :
            print("[{}] : {}".format(index,wheel))
        print("heading(deg) {} ".format(msg.heading))
        print("position(m)\n{} ".format(msg.position))
        print("angular_velocity(rad/s)\n{} ".format(msg.angular_velocity))
        print("acceleration(m/s^2)\n{} ".format(msg.acceleration))

        # print("eastOffset {}".format(data.eastOffset))
        # print("northOffset {}".format(data.northOffset))


if __name__ == '__main__':
    try:
        test=StatusSubscriber()
    except rospy.ROSInterruptException:
        pass

