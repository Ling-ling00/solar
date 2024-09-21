#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import numpy as np


class LidarReadNode(Node):
    def __init__(self):
        super().__init__('lidar_read_node')

        self.lim_pos_publisher = self.create_publisher(LaserScan, '/scan2', 10)

        #subscription
        self.create_subscription(LaserScan, "/scan", self.lidar_callback, 10)

        #variable
        self.stack_pos = []
        self.deg = [320, 45]
        self.dh = [0.30, 0.25]

    def publish_lidar_data(self, msg:LaserScan, deg):
        scan = msg
        scan.header.stamp = self.get_clock().now().to_msg()
        scan.angle_min = np.deg2rad(deg[0])
        scan.angle_max = np.deg2rad(deg[1])
        scan.ranges = self.lim_deg
        self.lim_pos_publisher.publish(scan)
        self.get_logger().info('Publishing LIDAR data')

    def cal_something(self,msg:LaserScan):
        self.stack_pos = []
        self.dx = []
        self.dy = []
        for i in range(len(msg)):
            self.stack_pos.append(round(msg[i],2))
            self.dx.append(round(np.sin(np.deg2rad(i*0.5))*msg[i],2))
            self.dy.append(round(np.cos(np.deg2rad(i*0.5))*msg[i],2))
        
    def lim_deg_pos(self, first, last):
        self.lim_deg = []
        self.lim_dx = []
        self.lim_dy = []
        if first < last:
            self.lim_deg = self.stack_pos[first*2:last*2]
            self.lim_dx = self.dx[first*2:last*2]
            self.lim_dy = self.dy[first*2:last*2]
        else:
            self.lim_deg = self.stack_pos[first*2:720]
            self.lim_deg = self.lim_deg[:] + self.stack_pos[0:last*2]
            self.lim_dx = self.dx[first*2:720]
            self.lim_dx = self.lim_dx[:] + self.dx[0:last*2]
            self.lim_dy = self.dy[first*2:720]
            self.lim_dy = self.lim_dy[:] + self.dy[0:last*2]
        print('----')
        print(self.lim_dy)
        print('--')
        print(self.lim_dx)

    def distance_check(self, dy, dx, dh):
        distance = [0,0]
        for i in range(len(dy)):
            if abs(dy[i] - dh[0]) < 0.05:
                if distance[0] == 0:
                    distance[0] = dx[i]
            if abs(dy[len(dy)-1-i]- dh[1]) < 0.05:
                if distance[1] == 0:
                    distance[1] = dx[len(dy)-1-i]
            if distance[0] != 0 and distance[1] != 0:
                break
        return distance
            
    def lidar_callback(self, msg:LaserScan):
        range = msg.ranges
        self.cal_something(range)
        self.lim_deg_pos(self.deg[0],self.deg[1])
        print('distance')
        print(self.distance_check(self.lim_dy, self.lim_dx, self.dh))
        self.publish_lidar_data(msg, self.deg)

def main(args=None):
    rclpy.init(args=args)
    node = LidarReadNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
