from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():

    launch_description = LaunchDescription()
    package_name = 'solar_ros'

    lidar_read = Node(
        package = package_name,
        executable = 'lidar_read.py',
        name = 'lidar'
    )
    
    robot = Node(
        package = package_name,
        executable = 'robot_control.py',
        name = 'robot'
    )

    mqtt = Node(
        package = package_name,
        executable = 'mqtt2ros.py',
        name = 'mqtt'
    )
    
    launch_description.add_action(lidar_read)
    launch_description.add_action(robot)
    launch_description.add_action(mqtt)

    return launch_description