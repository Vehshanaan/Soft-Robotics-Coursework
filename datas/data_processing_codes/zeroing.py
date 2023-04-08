import numpy as np

path = r"A:\OneDrive\MScRobotics\SR (Soft Robotics)\Soft-Robotics-Coursework\datas\normals\5.npy"

data = np.load(path)

min = np.min(data,axis=0)

data-=min

np.save(path,data)