'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2023-04-04 10:49:10
LastEditors: “Vehshanaan” 1959180242@qq.com
LastEditTime: 2023-04-04 17:09:12
FilePath: \Soft-Robotics-Coursework\codes\图片的四角识别与拉伸.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
import cv2 as cv
import numpy as np
import math

'''
description: 输入所有点的坐标,找到位于四角上的点
param {*} points 所有点 
return {*} result 四角的点的坐标数组,处理为方便透视变换使用的格式.
'''
def find_corner_points(points):
    

    # 左上：x+y最小
    # 右上：x-y最大
    # 左下: y-x最大
    # 右下: x+y最大

    result = np.zeros((4,2),dtype=np.int)

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
            result[3] = [x,y]
    # 左上
        if((x+y)<=x_plus_y_min):
            x_plus_y_min = (x+y)
            result[0]=[x,y]
    # 右上
        if((x-y)>=x_minus_y_max):
            x_minus_y_max = (x-y)
            result[1]=[x,y]
    # 左下
        if((x-y)<=x_minus_y_min):
            x_minus_y_min = (x-y)
            result[2]=[x,y]
            print((x,y))
    return result
    

'''
description: 透视变换把四角拉伸到四角
param {*} corners 四个脚垫,内容参考上面的函数
param {*} img 待拉伸的原图像
return {*} 拉伸后的图像
'''
def stretch_image(corners,img):
    size = img.shape
    width = size[1]
    height=size[0]

    dst = np.float32([[0,0], [height, 0],
                      [0, width], [height, width]])
    temp = np.float32(corners)
    M = cv.getPerspectiveTransform(temp, dst)

    stretched_img = cv.warpPerspective(img, M, (width,height))

    return stretched_img
    


img_path = "A:\OneDrive\MScRobotics\SR (Soft Robotics)\Soft-Robotics-Coursework\codes\corner_4dots.jpg"

img = cv.imread(img_path)

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
    # 在图像上绘制中心点
    ##cv.circle(img, (x, y), 5, (0, 0, 255), -1)

corners = find_corner_points(points)

#for _ in corners: cv.circle(img, _, 5, (0, 0, 255), -1)

stretched = stretch_image(corners, img)


cv.imshow("null",stretched)
cv.waitKey(-1)