# solar cleaner ROS
โปรแกรม ROS สำหรับควบคุมหุ่นยนต์ Solar cleaner

## LIDAR
LIDAR C1 package from https://github.com/Slamtec/sllidar_ros2.git

ขั้นตอนการใช้งาน
1. Create udev rules for rplidar
```bash
sudo chmod 777 /dev/ttyUSB0
```
หรือ
```bash
cd src/rpldiar_ros/
source scripts/create_udev_rules.sh
```
2. Run Slidar ROS2
```bash
ros2 launch sllidar_ros2 view_sllidar_c1_launch.py
```
3. Read LIDAR data
```bash
ros2 run solar lidar_read.py
```
