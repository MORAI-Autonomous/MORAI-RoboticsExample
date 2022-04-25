#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

# path = os.path.abspath(os.path.join(os.path.dirname(__file__),'/../../'))
path = '/root/catkin_ws/src/MORAI-RoboticsExample/AD/'
sys.path.append(path)

from network.ros_manager import RosManager
from autonomous_driving.autonomous_driving import AutonomousDriving

def main():
    autonomous_driving = AutonomousDriving()
    ros_manager = RosManager(autonomous_driving)
    ros_manager.execute()


if __name__ == '__main__':
    main()
