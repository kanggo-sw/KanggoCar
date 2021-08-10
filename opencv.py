import numpy as np
import cv2
import sys
import math
import copy
import serial


degree = []
def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    if len(img.shape) > 2:
        channel_cnt = img.shape[2]
        ignore_mask_color = (255,) * channel_cnt
    else:
        ignore_mask_color = 255

    cv2.fillPoly(mask, vertices, ignore_mask_color)

    return cv2.bitwise_and(img, mask)

def makeLine(orinImg, img, rho, theta, threshold, min_line_len, max_line_gap):


    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    degree = []
    if type(lines) == type(np.array([])):
        lines = lines.tolist()
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(orinImg, (x1, y1), (x2, y2), [255, 0, 0], 2)
                y1 = src.shape[0] - y1
                y2 = src.shape[0] - y2
                if x1 != x2:
                    degree.append(math.degrees(math.atan((y2 - y1) / (x2 - x1))))

capture = cv2.VideoCapture(1)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#ser = serial.Serial("COM3", 115200, timeout=1)

while cv2.waitKey(33) < 0:
    ret, src = capture.read()
    #src = cv2.imread('blackBox.jpg')

    if src is None:
        print('Image load failed!')
        sys.exit()
    imgray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # -----

    src_hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

    dst1 = cv2.inRange(src, (0, 0, 0), (50, 50, 50))

    # -----

    kernel = np.ones((5, 5)) / 10
    imgray = cv2.filter2D(imgray, -1, kernel)

    edge = cv2.Canny(imgray, 100, 200)

    # ------
    # 결과물에서 제외
    imshape = src.shape

    vertices = np.array([[(850, 100), (850, 600), (0, 700), (0, 50)]], dtype=np.int32)

    masked_src = region_of_interest(src, vertices)
    cv2.imshow('cx', masked_src)

    # -----

    imshape = edge.shape

    vertices = np.array([[(850, 100), (850, 600), (0, 700), (0, 50)]], dtype=np.int32)

    masked_edge = region_of_interest(edge, vertices)



    rho = 1
    theta = np.pi / 180
    threshold = 160
    min_line_len = 120
    max_line_gap = 150
    makeLine(src, masked_edge, rho, theta, threshold, min_line_len, max_line_gap)

    # ------
    for n, i in zip(range(len(degree)), degree):
        if i < 0:
            degree[n] += 180
    temp = []

    for i in degree:
        if i > 20:
            temp.append(i)
    degree = copy.deepcopy(temp)
    if len(degree) != 0:
        s = sum(degree) / len(degree)
        d1 = []
        d2 = []
        for i in degree:
            if i < s:
                d1.append(i)
            else:
                d2.append(i)
        d1 = sum(d1) / len(d1)
        d2 = sum(d2) / len(d2)
    else:
        d1 = 90
        d2 = 90
    
    #시리얼 통신
    op = str((d1 + d2) / 2)
    #ser.write(op.encode())

    #cv2.imshow('range', masked_src)
    cv2.imshow('imgray', imgray)
    cv2.imshow('edge', edge)
    # cv2.imshow('masked_edge', masked_edge)
    cv2.imshow('src', src)

src.release()
cv2.waitKey()
cv2.destroyAllWindows()
