#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import paho.mqtt.client as mqtt

# Define the MQTT settings
BROKER = "broker.mqtt-dashboard.com"
PORT = 1883
CLIENT_ID = "ros2-mqtt-bridge"
TOPIC_SUBSCRIBE = "test/topic/solar/fibo"
MQTT_USERNAME = ""  # Replace with actual username
MQTT_PASSWORD = ""  # Replace with actual password

class mqtt2ros(Node):
    def __init__(self):
        super().__init__("mqtt2ros")
        self.publisher_ = self.create_publisher(Float32MultiArray, "/cmd_vel", 10)
        self.get_logger().info("ROS 2 Node initialized, setting up MQTT client...")

        # Initialize MQTT client
        self.mqtt_client = mqtt.Client(client_id=CLIENT_ID)
        self.mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

        # Connect to the MQTT broker
        try:
            self.mqtt_client.connect(BROKER, PORT, 60)
            self.get_logger().info(f"Connected to MQTT broker at {BROKER}:{PORT}")
            self.mqtt_client.loop_start()  # Start MQTT loop in a separate thread
        except Exception as e:
            self.get_logger().error(f"Failed to connect to MQTT broker: {e}")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.get_logger().info(f"Connected to MQTT broker, subscribing to '{TOPIC_SUBSCRIBE}'")
            self.mqtt_client.subscribe(TOPIC_SUBSCRIBE)
        else:
            self.get_logger().error(f"Failed to connect to MQTT broker, return code {rc}")

    def on_message(self, client, userdata, msg):
        mqtt_message = msg.payload.decode()
        self.get_logger().info(f"Received MQTT message: '{mqtt_message}' on topic '{msg.topic}'")

        # Publish the message to the ROS 2 topic
        split_msg = mqtt_message.split()
        ros_message = Float32MultiArray()
        ros_message.data = [float(split_msg[0]), float(split_msg[1])]
        self.publisher_.publish(ros_message)
        self.get_logger().info(f"Republished to ROS topic: 'ros_topic'")

def main(args=None):
    rclpy.init(args=args)
    node = mqtt2ros()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down node.")
    finally:
        node.mqtt_client.loop_stop()  # Stop the MQTT loop
        node.mqtt_client.disconnect()  # Disconnect from MQTT broker
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
