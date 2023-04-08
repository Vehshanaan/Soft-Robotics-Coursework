'''
Author: “Vehshanaan” 1959180242@qq.com
Date: 2023-04-08 12:51:08
LastEditors: “Vehshanaan” 1959180242@qq.com
LastEditTime: 2023-04-08 17:35:06
FilePath: \Soft-Robotics-Coursework\datas\data_processing_codes\averaging.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
import numpy as np

import matplotlib.pyplot as plt

folder_path = r"A:\OneDrive\MScRobotics\SR (Soft Robotics)\Soft-Robotics-Coursework\datas\90s\\"

offset_path = ["1.npy", "2.npy", "3.npy", "4.npy", "5.npy"]

datas = []


for i in range(len(offset_path)):
    datas.append(np.load(folder_path+offset_path[i]))


result = []

for current_bottom in range(0, 400):

    top_sum = 0
    top_count = 0

    for data in datas:
        top = data[:, 0]
        bottom = data[:, 1]
        for label in range(len(bottom)):
            if bottom[label] == current_bottom:
                top_sum += top[label]
                top_count += 1

    if top_count == 0:
        continue

    top_average = top_sum/top_count

    result.append((current_bottom, top_average))

result = np.array(result)

x = result[:, 0]
y = result[:, 1]

plt.plot(x[::10],y[::10])
plt.show()