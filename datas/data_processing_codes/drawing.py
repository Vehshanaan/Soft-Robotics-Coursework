'''
Author: “Vehshanaan” 1959180242@qq.com
Date: 2023-04-05 16:26:30
LastEditors: “Vehshanaan” 1959180242@qq.com
LastEditTime: 2023-04-08 23:10:49
FilePath: \Soft-Robotics-Coursework\datas\data_processing_codes\drawing.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_filter1d

path = r"A:\OneDrive\MScRobotics\SR (Soft Robotics)\Soft-Robotics-Coursework\datas\45s\1.npy"

raw = np.load(path)


# 原始数据: 若干个二维点。
# [a][b]
# [a]是第几个点
# [b] 0 = 上面坐标，1=下面坐标

# 提取上面点
top = raw[:, 0]

# 提取下面点
bottom = raw[:, 1]

# bottom=bottom[::10]
# top=top[::10]


plt.plot(bottom, top)

plt.xlabel("bottom")
plt.ylabel("top")

plt.xlim(-1, 300)
plt.ylim(-1, 300)

# plt.gca().set_aspect("equal",adjustable="box")

plt.legend()
temp = np.arange(3000)
temp_ = temp
plt.plot(temp,temp_,"r")

plt.show()
