#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class LidarReadNode(Node):
    def __init__(self):
        super().__init__('lidar_read_node')

        #subscription
        self.create_subscription(LaserScan, "/scan", self.lidar_callback, 10)

        #variable
        self.stack_pos = []


    def cal_something(self,msg:LaserScan):
        self.stack_pos = []
        for i in range(len(msg)):
            self.stack_pos.append(round(msg[i],2))
        print(self.stack_pos, len(self.stack_pos))
        
        
            
    def lidar_callback(self, msg:LaserScan):
        range = msg.ranges
        self.cal_something(range)

   



def main(args=None):
    rclpy.init(args=args)
    node = LidarReadNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
