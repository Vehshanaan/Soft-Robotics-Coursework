'''
Author: “Vehshanaan” 1959180242@qq.com
Date: 2023-04-04 18:38:55
LastEditors: “Vehshanaan” 1959180242@qq.com
LastEditTime: 2023-04-05 11:52:48
FilePath: \Soft-Robotics-Coursework\codes\色块的识别和定位.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
import cv2 as cv
import numpy as np

path = "A:\OneDrive\MScRobotics\SR (Soft Robotics)\Soft-Robotics-Coursework\codes\ActuatorWithRedBlobs.jpg"


## 根据图片中的四个黑色角点正畸的函数
def remap(img):
    grey = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    ret, thres = cv.threshold(grey, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)

    kernel = np.ones((3,3),np.uint8)
    opening = cv.morphologyEx(thres, cv.MORPH_OPEN,kernel,iterations=4)


    contours, hierarchy = cv.findContours(opening, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    points=[]
    # 遍历所有多边形，找到四个角点
    for cnt in contours:
        M = cv.moments(cnt)

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        points.append((cx,cy))
    
    corners = np.zeros((4,2),dtype=np.int32)

    x_init = points[0][0]
    y_init = points[0][1]
    x_plus_y_max=x_init+y_init
    x_plus_y_min=x_init+y_init
    x_minus_y_max=x_init-y_init
    x_minus_y_min=x_init-y_init
    
        # 右下
    for point in points:
        x = point[0]
        y=point[1]
        if((x+y)>=x_plus_y_max):
            x_plus_y_max = (x+y)
            corners[3] = [x,y]
    # 左上
        if((x+y)<=x_plus_y_min):
            x_plus_y_min = (x+y)
            corners[0]=[x,y]
    # 右上
        if((x-y)>=x_minus_y_max):
            x_minus_y_max = (x-y)
            corners[1]=[x,y]
    # 左下
        if((x-y)<=x_minus_y_min):
            x_minus_y_min = (x-y)
            corners[2]=[x,y]
    
    size = img.shape
    width = size[1]
    height=size[0]

    dst = np.float32([[0,0], [height, 0],
                      [0, width], [height, width]])
    temp = np.float32(corners)
    M = cv.getPerspectiveTransform(temp, dst)

    stretched_img = cv.warpPerspective(img, M, (width,height))

    return stretched_img






"""
hsv = cv.cvtColor(stretched,cv.COLOR_BGR2HSV)

lower_red = np.array([0,100,100])
upper_red = np.array([10,255,255])

mask = cv.inRange(hsv,lower_red,upper_red)

close_kernel = np.ones((10,10),np.uint8)


closing = cv.morphologyEx(mask, cv.MORPH_CLOSE,close_kernel,iterations=10)


# 查找轮廓
contours, hierarchy = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

xs=[]
ys=[]

# 遍历轮廓
for contour in contours:
    # 计算轮廓的面积
    area = cv.contourArea(contour)
    # 如果面积小于一定值，忽略
    if area < 1000:
        continue

    # 计算轮廓的中心点
    M = cv.moments(contour)

    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

    xs.append(cx)
    ys.append(cy)

    # 绘制中心点
    cv.circle(stretched, (cx, cy), 20, (0, 255, 0), -1)

ys=np.array(ys)
xs=np.array(xs)

if(len(xs)!=3|len(ys)!=3):
    print("Error!")
else:
    # 寻找中间和两个变量：
    
    points = np.column_stack((xs,ys))

    # 寻找中间： 根据y轴数值寻找，y轴数值中不溜的就是
    mid = np.where(ys==np.median(ys))


    results = []  

    mid_y = ys[mid][0]

    # 取剩下的两个点
    for point in points: # point是一行两列的东西
        point_y = point[1]
        if (point_y==mid_y): continue
    
        results.append(point[0]-xs[mid][0])

        # 结果先上再下，上下对应的是什么方向参见那张纸。

"""

'''
description: 计算两端相对于中间的纵向位移
param {*} img 四角已经被拽过的彩图
return {*} 画面中两个末端点离中心点的横向位移。顺序为[画面上方，画面下方]
'''
def strain_cal(img):

    hsv = cv.cvtColor(stretched,cv.COLOR_BGR2HSV)

    lower_red = np.array([0,100,100])
    upper_red = np.array([10,255,255])

    mask = cv.inRange(hsv,lower_red,upper_red)

    close_kernel = np.ones((10,10),np.uint8)


    closing = cv.morphologyEx(mask, cv.MORPH_CLOSE,close_kernel,iterations=10)


    # 查找轮廓
    contours, hierarchy = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    xs=[]
    ys=[]

    # 遍历轮廓
    for contour in contours:
        # 计算轮廓的面积
        area = cv.contourArea(contour)
        # 如果面积小于一定值，忽略
        if area < 1000:
            continue

        # 计算轮廓的中心点
        M = cv.moments(contour)

        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        xs.append(cx)
        ys.append(cy)
    
    if(len(xs)!=3|len(ys)!=3):
        print("Error!")
    else:

        ys=np.array(ys)
        xs=np.array(xs)


        # 寻找中间： 根据y轴数值寻找，y轴数值中不溜的就是
        mid = np.where(ys==np.median(ys))

        mid_x = xs[mid][0]

        ys = np.delete(ys, mid)
        xs = np.delete(xs, mid)


        points = np.dstack((xs,ys))[0]
        
        sorted_points = np.argsort(points[:,1])

        points = points[sorted_points]


        results = []  
        # 取剩下的两个点
        for point in points: # point是一行两列的东西        
            results.append(point[0]-mid_x)

            # if (point[0]-mid_x) > 300 :
            #     cv.circle(stretched, point, 30, (255,0,0),-1)
            


        return results
        # 结果先图像上再下（坐标y从小到大），具体方向参照那张纸

img = cv.imread(path)

stretched = remap(img)

results = strain_cal(stretched)

print(results)

cv.imshow("_",stretched)

cv.waitKey(0)
