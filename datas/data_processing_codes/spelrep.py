'''
Author: “Vehshanaan” 1959180242@qq.com
Date: 2023-04-05 16:26:30
LastEditors: “Vehshanaan” 1959180242@qq.com
LastEditTime: 2023-04-09 11:01:03
FilePath: \Soft-Robotics-Coursework\datas\data_processing_codes\spelrep.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression



folder_path = r"A:\OneDrive\MScRobotics\SR (Soft Robotics)\Soft-Robotics-Coursework\datas\normals\\"

offset_path = ["1.npy", "2.npy", "3.npy", "4.npy", "5.npy"]

datas = []


for i in range(len(offset_path)):
    datas.append(np.load(folder_path+offset_path[i]))

ps = []



for data in datas:

    tops = data[:,0]
    bottoms = data[:,1]

    tops = tops.reshape(-1)
    bottoms = bottoms.reshape(-1)
    
    coeff = np.polyfit(tops, bottoms, 5)
    p = np.poly1d(coeff)
    ps.append(p)

results=[]

for i in range(300):
    result = 0
    for p in ps:
        result+=p(i)
    if result: result/=5
    results.append(result)

plt.plot(results,range(300))
temp = np.arange(3000)
temp_ = temp
plt.plot(temp,temp_,"r")
plt.xlim(-1,300)
plt.ylim(-1,300)

plt.ylabel("comparing",fontsize=18)
plt.xlabel("standard",fontsize=18)

plt.title("Polyfit(no tilt)",fontsize=20)
plt.grid() 
plt.show()




