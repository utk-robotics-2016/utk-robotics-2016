import cv2
import numpy as np
import sys


class railorder:

    def __init__(self, course):
        self.red = [np.array([0, 160, 155]), np.array([180, 215, 200])]
        self.green = [np.array([50, 50, 60]), np.array([80, 160, 180])]
        self.blue = [np.array([90, 80, 0]), np.array([120, 255, 255])]
        self.yellow = [np.array([0, 200, 210]), np.array([40, 255, 255])]

        if course == 'A':
            self.y1 = 150
            self.y2 = 300
            self.x1 = 0
            self.x2 = 380
        else: 
            self.y1 = 200
            self.y2 = 300
            self.x1 = 260
            self.x2 = 640

        self.w = self.x2 - self.x1
        self.h = self.y2 - self.y1

        self.massThreshold = 2000

        camera = cv2.VideoCapture(0)
        retval, self.origImg = camera.read()
        camera.release()

        cv2.imwrite("/home/kevin/utk-robotics-2016/tmp.jpeg", self.origImg)

    def findCenterOfBiggestMass(self, mask):
        _,contours, hierarchy = cv2.findContours(mask, 1, 2)
        biggestArea = -1
        biggestIndex = -1
        for i, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if area > self.massThreshold and area > biggestArea:
                biggestArea = area
                biggestIndex = i
        if biggestIndex < 0:
            return (-1, -1)
        M = cv2.moments(contours[biggestIndex])
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            return (cx, cy)
        return (-1, -1)

    def get_rail_order(self, course):
        tmphsv = cv2.cvtColor(self.origImg[self.y1:self.y2, self.x1:self.x2], cv2.COLOR_BGR2HSV)
        rr = cv2.inRange(tmphsv, self.red[0], self.red[1])
        rg = cv2.inRange(tmphsv, self.green[0], self.green[1])
        rb = cv2.inRange(tmphsv, self.blue[0], self.blue[1])
        ry = cv2.inRange(tmphsv, self.yellow[0], self.yellow[1])
        cr = self.findCenterOfBiggestMass(rr)
        cg = self.findCenterOfBiggestMass(rg)
        cb = self.findCenterOfBiggestMass(rb)
        cy = self.findCenterOfBiggestMass(ry)
        points = [cr, cg, cb, cy]
        colors = ['red', 'green', 'blue', 'yellow']
        # assume that only one of the bins is not viewable from the camera
        railorder = sorted(zip(points, colors), key=lambda coord: coord[0][0])
        # if less than 3 bins are visible throw an error
        # if railorder[1][0] the x of the second lowest value is -1
        if railorder[1][0] == -1: 
            sys.stderr.write("not all bins were visible. Readjust the camera\n")
        if course == 'B':
            # set the leftmost color's x coord to 1000 and resort, putting it on the right
            railorder[0][0] = 1000
            return [c for (p, c) in sorted(zip(points, colors), key=lambda coord: coord[0][0])]
        else:
            return [c for (p, c) in railorder]
