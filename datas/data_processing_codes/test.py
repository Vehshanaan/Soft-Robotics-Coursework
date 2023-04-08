'''
Author: “Vehshanaan” 1959180242@qq.com
Date: 2023-04-08 18:57:58
LastEditors: “Vehshanaan” 1959180242@qq.com
LastEditTime: 2023-04-08 19:09:17
FilePath: \Soft-Robotics-Coursework\datas\data_processing_codes\test.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
import numpy as np

c = [[0, 5], [3, 4], [2, 1], [4, 5]]

c = np.array(c)

min = np.min(c, axis=0)

min_0, min_1 = min



if(min_0 > 0):
    c[:, 0] -= min_0
else:
    c[:, 1] += min_0

if(min_1 > 0):
    c[:, 1] -= min_1
else:
    c[:, 1] += min_1


print(c)
