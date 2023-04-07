'''
Author: “Vehshanaan” 1959180242@qq.com
Date: 2023-04-05 09:51:00
LastEditors: “Vehshanaan” 1959180242@qq.com
LastEditTime: 2023-04-07 12:00:59
FilePath: \Soft-Robotics-Coursework\codes\逐帧处理.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
import cv2
import numpy as np
import datetime


def remap(img):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thres = cv2.threshold(
        grey, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thres, cv2.MORPH_OPEN, kernel, iterations=4)

    contours, hierarchy = cv2.findContours(
        opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    points = []
    # 遍历所有多边形，找到四个角点
    for cnt in contours:
        M = cv2.moments(cnt)

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        points.append((cx, cy))

    corners = np.zeros((4, 2), dtype=np.int32)

    x_init = points[0][0]
    y_init = points[0][1]
    x_plus_y_max = x_init+y_init
    x_plus_y_min = x_init+y_init
    x_minus_y_max = x_init-y_init
    x_minus_y_min = x_init-y_init

    # 右下
    for point in points:
        x = point[0]
        y = point[1]
        if((x+y) >= x_plus_y_max):
            x_plus_y_max = (x+y)
            corners[3] = [x, y]
    # 左上
        if((x+y) <= x_plus_y_min):
            x_plus_y_min = (x+y)
            corners[0] = [x, y]
    # 右上
        if((x-y) >= x_minus_y_max):
            x_minus_y_max = (x-y)
            corners[1] = [x, y]
    # 左下
        if((x-y) <= x_minus_y_min):
            x_minus_y_min = (x-y)
            corners[2] = [x, y]

    size = img.shape
    width = 1000#size[1]
    height = 1000#size[0]

    dst = np.float32([[0, 0], [height, 0],
                      [0, width], [height, width]])
    temp = np.float32(corners)
    M = cv2.getPerspectiveTransform(temp, dst)

    stretched_img = cv2.warpPerspective(img, M, (width, height))

    return stretched_img


def strain_cal(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 100, 100])
    upper_red = np.array([50, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    close_kernel = np.ones((10, 10), np.uint8)

    closing = cv2.morphologyEx(
        mask, cv2.MORPH_CLOSE, close_kernel, iterations=10)

    # 查找轮廓
    contours, hierarchy = cv2.findContours(
        closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    xs = []
    ys = []

    # 遍历轮廓
    for contour in contours:
        # 计算轮廓的面积
        area = cv2.contourArea(contour)
        # 如果面积小于一定值，忽略
        if area < 100:
            # continue
            pass

        # 计算轮廓的中心点
        M = cv2.moments(contour)
        if(M['m00'] == 0):
            continue
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        xs.append(cx)
        ys.append(cy)

    if(len(xs) != 3 | len(ys) != 3):
        print("没看着三个点!")
        return [0, 0], img
    for i in range(len(ys)):
        for j in range(i+1, len(ys)):
            if abs(ys[i]-ys[j]) < 100:
                print("虽然有三个点，但是有两个点纵向离得太近了！")
                return [0, 0], img

    else:

        ys = np.array(ys)
        xs = np.array(xs)

        # 寻找中间： 根据y轴数值寻找，y轴数值中不溜的就是
        mid = np.where(ys == np.median(ys))

        mid_x = xs[mid]  # [0]

        ys = np.delete(ys, mid)
        xs = np.delete(xs, mid)

        points = np.dstack((xs, ys))[0]

        sorted_points = np.argsort(points[:, 1])

        points = points[sorted_points]

        results = []
        # 取剩下的两个点
        for point in points:  # point是一行两列的东西
            results.append(point[0]-mid_x)

            # if (point[0]-mid_x) > 300 :
            cv2.circle(img, point, 30, (255, 0, 0), -1)
            cv2.putText(img, str(point), point,
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0,), 2)

        return results, img
        # 结果先图像上再下（坐标y从小到大），具体方向参照那张纸


path = r"A:\OneDrive\MScRobotics\SR (Soft Robotics)\Soft-Robotics-Coursework\videos\90du.mp4"

video = cv2.VideoCapture(path)

save = []
data_prev = np.array([-100, -100])

while True:
    ret, frame = video.read()

    if not ret:
        print("结束")
        break

    # 处理 here
    frame = remap(frame)

    data, frame = strain_cal(frame)

    if(data[0] and data[1]):
        if (data[0]-data_prev[0] > 0) or (data[1]-data_prev[1] > 0):
            # print(data)
            data_prev = data
            save.append(data)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == ord("q"):
        break


video.release()
cv2.destroyAllWindows()

# print(save[428][1]) #save[某一时刻][0=第一个数（上面的形变），1=第二个数（下面的形变）]
# 用最小值把这玩意儿整体搬到数轴正半轴
min = np.min(save, axis=0)
save += abs(min)
# print(save)
print(np.shape(save))

# 保存实验数据
now = datetime.datetime.now()

save_path = "data_{}.npy".format(now.strftime("%d-%H-%M-%S"))

save_path = "A:\OneDrive\MScRobotics\SR (Soft Robotics)\Soft-Robotics-Coursework\datas\\" + save_path

#np.save(save_path, save)
