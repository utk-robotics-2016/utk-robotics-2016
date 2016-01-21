import cv2
import numpy as np
import time

red = [np.array([0, 160, 155]), np.array([180, 215, 200])]
green = [np.array([50, 50, 60]), np.array([80, 160, 180])]
blue = [np.array([90, 80, 0]), np.array([120, 255, 255])]
yellow = [np.array([0, 200, 210]), np.array([40, 255, 255])]

#numImg = 24
#r = 6
#c = 4

#y1 = 200
#y2 = 300
#x1 = 260
#x2 = 640
#w = x2 - x1
#h = y2 - y1

massThreshold = 2000

#origImg = []
#for i in range(1, numImg + 1):
origImg = (cv2.imread(str(i) + ".jpg"))

def findCenterOfBiggestMass(mask):
    contours, hierarchy = cv2.findContours(mask, 1, 2)
    biggestArea = -1
    biggestIndex = -1
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > massThreshold and area > biggestArea:
            biggestArea = area
            biggestIndex = i
    if biggestIndex < 0:
        return (-1, -1)
    M = cv2.moments(contours[biggestIndex])
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return (cx, cy)
    return (-1, -1)

#img = np.empty([r * h, c * w, 3], dtype=np.uint8)
#res = np.empty([r * h, c * w, 3], dtype=np.uint8)
#points = []

def get_rail_order(course):
    tmpimg = np.empty([h, w, 3], dtype=np.uint8)
    tmphsv = cv2.cvtColor(origImg[i][y1:y2, x1:x2], cv2.COLOR_BGR2HSV)
    rr = cv2.inRange(tmphsv, red[0], red[1])
    rg = cv2.inRange(tmphsv, green[0], green[1])
    rb = cv2.inRange(tmphsv, blue[0], blue[1])
    ry = cv2.inRange(tmphsv, yellow[0], yellow[1])
    cr = findCenterOfBiggestMass(rr)
    cg = findCenterOfBiggestMass(rg)
    cb = findCenterOfBiggestMass(rb)
    cy = findCenterOfBiggestMass(ry)
    points = [cr, cg, cb, cy]
    colors = ['red', 'green', 'blue', 'yellow']
#assume that only one of the bins is not viewable from the camera
    railorder = sorted(zip(points, colors), key=lambda coord: coord[0][0])
    if course = 'B':
        #set the 
        railorder[0][0] = 1000
        return c for (p, c) in sorted(zip(points, colors), key=lambda coord: coord[0][0])
    else:
        return c for (p, c) in railorder
