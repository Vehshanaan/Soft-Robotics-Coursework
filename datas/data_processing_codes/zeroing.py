import numpy as np


path = r"A:\OneDrive\MScRobotics\SR (Soft Robotics)\Soft-Robotics-Coursework\datas\45s\1.npy"


data = np.load(path)


min = np.min(data,axis=0)

min_0,min_1=min


if(min_0 > 0):
    data[:, 0] -= min_0

else:
    data[:, 1] += min_0


if(min_1 > 0):
    data[:, 1] -= min_1

else:
    data[:, 1] += min_1

np.save(path,data)