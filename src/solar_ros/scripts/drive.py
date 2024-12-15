#!/usr/bin/python3

from solar_ros.dummy_module import dummy_function, dummy_var
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

import odrive
from odrive.enums import *
from odrive.enums import AXIS_STATE_UNDEFINED, AXIS_STATE_CLOSED_LOOP_CONTROL
import time


class OdriveNode(Node):
    def __init__(self):
        super().__init__('odrive_node')
        self.initial_odrive()
        self.create_timer(0.01, self.odrive_loop)
        self.create_subscription(Float32MultiArray, "/cmd_vel", self.velo_callback, 10)
        self.left_speed = 0
        self.right_speed = 0
    
    def Odrive_VelControl(self):
        self.odrv_L.axis0.controller.config.control_mode = ControlMode.VELOCITY_CONTROL
        self.odrv_L.axis0.controller.config.vel_ramp_rate = 20
        self.odrv_L.axis0.controller.config.input_mode = InputMode.VEL_RAMP

        self.odrv_R.axis0.controller.config.control_mode = ControlMode.VELOCITY_CONTROL
        self.odrv_R.axis0.controller.config.vel_ramp_rate = 20
        self.odrv_R.axis0.controller.config.input_mode = InputMode.VEL_RAMP
    
    def Odrive_TorqueControl(self):
        self.odrv_L.axis0.controller.config.control_mode = ControlMode.TORQUE_CONTROL
        # odrv.axis0.controller.config.torque_ramp_rate = 40
        self.odrv_L.axis0.controller.config.input_mode = InputMode.PASSTHROUGH

        self.odrv_R.axis0.controller.config.control_mode = ControlMode.TORQUE_CONTROL
        self.odrv_R.axis0.controller.config.input_mode = InputMode.PASSTHROUGH
        
    def initial_odrive(self):
        # self.odrv = odrive.find_any()
        self.odrv_L = odrive.find_any(serial_number="3680336A3432") #left
        self.odrv_R = odrive.find_any(serial_number="367D335A3432") #right
        
        while self.odrv_L.axis0.current_state == AXIS_STATE_UNDEFINED or self.odrv_R.axis0.current_state == AXIS_STATE_UNDEFINED:
            time.sleep(0.01)

        while self.odrv_L.axis0.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            self.odrv_L.clear_errors()
            self.odrv_L.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
            time.sleep(0.01)

        while self.odrv_R.axis0.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            self.odrv_R.clear_errors()
            self.odrv_R.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
            time.sleep(0.01)    
        
        time.sleep(1)
        self.Odrive_VelControl()
        # self.Odrive_TorqueControl()

        print("Finished setup Odrive")
        time.sleep(1)
        
    def odrive_loop(self):
        # self.vx_speed = self.accl_vel/(2.0*math.pi) # rps
        # self.odrv.axis0.controller.config.control_mode = ControlMode.VELOCITY_CONTROL
        self.odrv_L.axis0.controller.input_vel = self.left_speed
        self.odrv_R.axis0.controller.input_vel = -self.right_speed
        print(odrive.utils.dump_errors(self.odrv_L))
        print(odrive.utils.dump_errors(self.odrv_R))

    def velo_callback(self, msg:Float32MultiArray):
        self.left_speed = msg.data[0]
        self.right_speed = msg.data[1]


def main(args=None):
    rclpy.init(args=args)
    node = OdriveNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
