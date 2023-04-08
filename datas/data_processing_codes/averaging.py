'''
Author: “Vehshanaan” 1959180242@qq.com
Date: 2023-04-08 12:51:08
LastEditors: “Vehshanaan” 1959180242@qq.com
LastEditTime: 2023-04-08 13:15:05
FilePath: \Soft-Robotics-Coursework\datas\data_processing_codes\averaging.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
import numpy as np

folder_path = r"A:\OneDrive\MScRobotics\SR (Soft Robotics)\Soft-Robotics-Coursework\datas\90s\\"

offset_path = ["1.npy", "2.npy", "3.npy", "4.npy", "5.npy"]

data = []


for i in range(len(offset_path)):
    data.append(np.load(folder_path+offset_path[i]))


result = []


# 对于每一个底部形变值：
for current_bottom in range(0, 400):
    top_sum = 0
    top_count = 0
    # 对于每一个数据：
    for i in range(len(offset_path)):
        # 分裂其顶部和底部
        top = data[i][:,0]
        bottom = data[i][:,1]
        # 根据当前找的底部形变值找到对应的顶部形变值们的索引
        # 记录索引的数量
        # 将顶部形变值加到外层sum中，也记得加计数
    if top_count == 0:continue

    top_average = top_sum/top_count
    result.append([top_average,bottom])

