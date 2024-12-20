from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    launch_description = LaunchDescription()
    package_name = 'solar_ros'

    lidar_read = Node(
        package = package_name,
        executable = 'lidar_read.py',
        name = 'lidar'
    )
    
    # robot = Node(
    #     package = package_name,
    #     executable = 'robot_control.py',
    #     name = 'robot'
    # )

    robot = Node(
        package = package_name,
        executable = 'drive.py',
        name = 'robot'
    )

    mqtt = Node(
        package = package_name,
        executable = 'mqtt2ros.py',
        name = 'mqtt'
    )

    lidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory("sllidar_ros2"),
                    "launch",
                    "view_sllidar_c1_launch.py"
                )
            ]
        )
    )
    
    launch_description.add_action(lidar)
    launch_description.add_action(lidar_read)
    launch_description.add_action(robot)
    launch_description.add_action(mqtt)

    return launch_description