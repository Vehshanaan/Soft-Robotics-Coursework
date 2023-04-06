'''
Author: “Vehshanaan” 1959180242@qq.com
Date: 2023-04-05 16:26:30
LastEditors: “Vehshanaan” 1959180242@qq.com
LastEditTime: 2023-04-06 17:57:54
FilePath: \Soft-Robotics-Coursework\datas\drawing.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
import numpy as np
import matplotlib.pyplot as plt

path = r"A:\OneDrive\MScRobotics\SR (Soft Robotics)\Soft-Robotics-Coursework\datas\90du.npy"

raw = np.load(path)


# 原始数据: 若干个二维点。
#[a][b]
#[a]是第几个点
# [b] 0 = 上面坐标，1=下面坐标

# 提取上面点
top = raw[:,0]

# 提取下面点
bottom = raw[:,1]

plt.plot(bottom,top)

plt.xlabel("bottom")
plt.ylabel("top")

plt.legend

plt.show()