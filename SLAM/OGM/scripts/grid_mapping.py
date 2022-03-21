#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from math import pi
import rospy
import rospkg
from morai_msgs.msg import EgoVehicleStatus
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid, Path
from geometry_msgs.msg import PoseStamped
from lib.utils import l2p, p2l, quarternion_to_yaw
import tf
import atexit
import os

class GridMappingROS:
    def __init__(self):
        rospy.init_node('RosGridMapping', anonymous=True)
        
        self.is_gridmapping_initialized = False
        self.map_last_publish = rospy.Time()
        self.prev_robot_x = -99999999
        self.prev_robot_y = -99999999

        self.sensor_model_p_occ   = rospy.get_param('~sensor/sensor_model_p_occ', 0.75)
        self.sensor_model_p_free  = rospy.get_param('~sensor/sensor_model_p_free', 0.45)
        self.sensor_model_p_prior = rospy.get_param('~sensor/sensor_model_p_prior', 0.5)
        self.robot_frame          = rospy.get_param('~frame/robot_frame', 'base_link')
        self.map_frame            = rospy.get_param('~frame/map_frame', 'map')
        self.map_size_x           = rospy.get_param('~mapping/map_size_x', 50.0)
        self.map_size_y           = rospy.get_param('~mapping/map_size_y', 50.0)
        self.map_resolution       = rospy.get_param('~mapping/map_resolution', 0.1)
        self.map_publish_freq     = rospy.get_param('~mapping/map_publish_freq', 1.0)
        self.update_movement      = rospy.get_param('~mapping/update_movement', 0.1)
        self.file_name            = rospy.get_param('~file_name', 'test')

        # Creata a OccupancyGrid message template
        self.map_msg = OccupancyGrid()
        self.map_msg.header.frame_id = self.map_frame
        self.map_msg.info.resolution = self.map_resolution
        self.map_msg.info.width = int(self.map_size_x / self.map_resolution)
        self.map_msg.info.height = int(self.map_size_y / self.map_resolution)

        status_msg=rospy.wait_for_message('/Ego_topic', EgoVehicleStatus)

        self.map_center_x = status_msg.position.x - self.map_size_x/2 
        self.map_center_y = status_msg.position.y - self.map_size_y/2
        self.map_msg.info.origin.position.x = self.map_center_x
        self.map_msg.info.origin.position.y = self.map_center_y

        self.laser_sub = rospy.Subscriber("/lidar2D", LaserScan, self.laserscan_callback, queue_size=2)
        self.laser_pub = rospy.Publisher('/lidar2D_pub', LaserScan, queue_size=2)

        self.map_pub = rospy.Publisher('/map', OccupancyGrid, queue_size=2)
        self.tf_sub = tf.TransformListener()

        self.path = Path()
        self.path.header.frame_id = 'map'
        self.path_pub = rospy.Publisher('/odom',Path,queue_size=1)

        atexit.register(self.save_map)

    def init_gridmapping(self, laser_min_angle, laser_max_angle, laser_resolution, laser_max_dist):       
        self.gridmapping = GridMapping(self.map_center_x, self.map_center_y, self.map_size_x, self.map_size_y, self.map_resolution, laser_min_angle, laser_max_angle, laser_resolution, laser_max_dist, self.sensor_model_p_occ, self.sensor_model_p_free, self.sensor_model_p_prior)
        self.is_gridmapping_initialized = True
        print("initialized!")

    def publish_occupancygrid(self, gridmap, stamp):
        gridmap_p = l2p(gridmap)
        gridmap_int8 = (gridmap_p*100).astype(dtype=np.int8)
        
        # Publish map
        self.map_msg.data = gridmap_int8
        self.map_msg.header.stamp = stamp
        self.map_pub.publish(self.map_msg)
        rospy.loginfo_once("Published map!")

    def laserscan_callback(self, data):
        if not self.is_gridmapping_initialized:
            self.init_gridmapping(0, 2*pi, data.angle_increment, data.range_max)
        
        scan_repub = data
        scan_repub.header.frame_id = 'base_link'
        scan_repub.angle_min = 0
        scan_repub.angle_max = 2*pi
        self.laser_pub.publish(scan_repub)

        self.tf_sub.waitForTransform(self.map_frame, self.robot_frame, data.header.stamp, rospy.Duration(1.0))
        try:
            (x, y, _),(qx, qy, qz, qw) = self.tf_sub.lookupTransform(self.map_frame, self.robot_frame, data.header.stamp)
            theta = quarternion_to_yaw(qx, qy, qz, qw)

            if ( (x-self.prev_robot_x)**2 + (y-self.prev_robot_y)**2 >= self.update_movement**2 ):
                gridmap = self.gridmapping.update(x, y, theta, data.ranges).flatten() # update map
                self.prev_robot_x = x
                self.prev_robot_y = y

                pose = PoseStamped()
                pose.header.frame_id = 'map'
                pose.pose.position.x = x
                pose.pose.position.y = y
                pose.pose.orientation.w = 1.0
                pose.header.seq = self.path.header.seq + 1
                self.path.header.stamp = rospy.Time.now()
                pose.header.stamp = self.path.header.stamp
                self.path.poses.append(pose)
                self.path_pub.publish(self.path)

                if (self.map_last_publish.to_sec() + 1.0/self.map_publish_freq < rospy.Time.now().to_sec() ):
                    self.map_last_publish = rospy.Time.now()
                    self.publish_occupancygrid(gridmap, data.header.stamp)

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
            rospy.logerr(e)

    def save_map(self):
        rospack=rospkg.RosPack()
        
        pkg_name = 'ogm'
        file_path=rospack.get_path(pkg_name)
        file_name = self.file_name + '.txt'
        file_folder = file_path+'/map'
        if not os.path.isfile(file_folder):
            os.makedirs(file_folder)
        
        full_path=file_path+'/map/'+file_name
        print(full_path)
        f=open(full_path,'w')
        data=''
        for pixel in self.map_msg.data :
                data+='{0} '.format(pixel)
        f.write(data) 
        f.close()

class GridMapping:
    def __init__(self, map_center_x, map_center_y, map_size_x, map_size_y, map_resolution, laser_min_angle, laser_max_angle, laser_resolution, laser_max_dist, sensor_model_p_occ, sensor_model_p_free, sensor_model_p_prior):
        self.map_center_x = map_center_x          #meter
        self.map_center_y = map_center_y          #meter
        self.map_size_x = map_size_x              #meter
        self.map_size_y = map_size_y              #meter
        self.map_resolution = map_resolution      #meter/cell
        self.laser_min_angle = laser_min_angle    #radian
        self.laser_max_angle = laser_max_angle    #radian
        self.laser_resolution = laser_resolution  #radian
        self.laser_max_dist = laser_max_dist      #meter
        self.sensor_model_l_occ = p2l(sensor_model_p_occ)
        self.sensor_model_l_free = p2l(sensor_model_p_free)
        self.sensor_model_l_prior = p2l(sensor_model_p_prior)

        map_rows = int(map_size_y / map_resolution)
        map_cols = int(map_size_x / map_resolution)
        self.gridmap = self.sensor_model_l_prior * np.ones((map_rows, map_cols))

    def to_xy (self, i, j):
        x = j * self.map_resolution + self.map_center_x
        y = i * self.map_resolution + self.map_center_y
        return x, y

    def to_ij (self, x, y):
        i = (y-self.map_center_y) / self.map_resolution
        j = (x-self.map_center_x) / self.map_resolution
        return i, j

    def is_inside (self, i, j):
        return i<self.gridmap.shape[0] and j<self.gridmap.shape[1] and i>=0 and j>=0

    def raycast_update(self, x0, y0, theta, d):
        if np.isnan(d):
            d = self.laser_max_dist

        x1 = x0 + d*np.cos(theta)
        y1 = y0 + d*np.sin(theta)
        i0, j0 = self.to_ij(x0, y0)
        i1, j1 = self.to_ij(x1, y1)
        d_cells = d / self.map_resolution
        ip, jp, is_hit = self.bresenham(i0, j0, i1, j1, d_cells)
        if not np.isnan(d) and d != self.laser_max_dist:
            # Hit
            self.gridmap[int(ip),int(jp)] += self.sensor_model_l_occ - self.sensor_model_l_prior
        return
    
    #bresenham method is used to plot the lines
    def bresenham (self, i0, j0, i1, j1, d):   
        dx = np.absolute(j1-j0)
        dy = -1 * np.absolute(i1-i0)
        sx = -1
        if j0<j1:
            sx = 1
        sy = -1
        if i0<i1:
            sy = 1
        jp, ip = j0, i0
        err = dx+dy                     
        while True:                     
            if (jp == j1 and ip == i1) or (np.sqrt((jp-j0)**2+(ip-i0)**2) >= d) or not self.is_inside(ip, jp):
                return ip, jp, False
            elif self.gridmap[int(ip),int(jp)]>100:
                return ip, jp, True

            if self.is_inside(ip, jp):
                # miss
                self.gridmap[int(ip),int(jp)] += self.sensor_model_l_free - self.sensor_model_l_prior

            e2 = 2*err
            if e2 >= dy:                
                err += dy
                jp += sx
            if e2 <= dx:                
                err += dx
                ip += sy

    def update(self, x, y, theta, scan):

        for i, z in enumerate(scan):
            self.raycast_update(x, y, (theta + self.laser_min_angle + i*self.laser_resolution), z)
        return self.gridmap

gm = GridMappingROS()
while not rospy.is_shutdown():
    rospy.spin()

