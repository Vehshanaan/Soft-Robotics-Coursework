'''
Author: “Vehshanaan” 1959180242@qq.com
Date: 2023-04-04 23:12:27
LastEditors: “Vehshanaan” 1959180242@qq.com
LastEditTime: 2023-04-04 23:21:11
FilePath: \Soft-Robotics-Coursework\codes\test.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
import numpy as np

a = np.array([3,2,1])
b = np.array([5,6,7])

res = np.dstack((a,b))[0]

sorted_res = np.argsort(res[:,1])

res=res[sorted_res]

print(res)