i = [0,1,2,3,4,5,6]
b = []
b = i[0:2]
b = b[:] + i[4:6]
# print(b)
# print(b[0]== 0)
b = [a * -1 for a in [1,1,1,1]]
print(b)

import numpy as np

f_mid_pose = -0.2
b_mid_pose = -0.6
lidar_distance = 0.5

robot_theta = np.arcsin((-f_mid_pose+b_mid_pose)/lidar_distance)

print(np.rad2deg(robot_theta))