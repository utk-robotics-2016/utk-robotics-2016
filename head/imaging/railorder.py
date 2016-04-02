import cv2
import numpy as np
from datetime import datetime
import logging
import sys
import time

SAVE_LOC = '/var/log/spine/imaging'


class railorder:

    def __init__(self, course):
        # try:
            self.red = [np.array([0, 140, 100]), np.array([180, 245, 150])]
            self.green = [np.array([45, 40, 30]), np.array([100, 130, 85])]
            self.blue = [np.array([103, 100, 60]), np.array([115, 180, 150])]
            self.yellow = [np.array([25, 130, 155]), np.array([30, 255, 255])]

            self.y1 = 200
            self.y2 = 350

            if course == 'A':
                self.x1 = 0
                self.x2 = 365
            else:
                self.x1 = 275
                self.x2 = 640

            self.w = self.x2 - self.x1
            self.h = self.y2 - self.y1

            self.massThreshold = 2000

            retval = False

            # loop until we get an image -- sleep to let the camera come online
            while( retval == False ):
                camera = cv2.VideoCapture(0)
                time.sleep(1.0)
                retval, self.origImg = camera.read()
                logging.info(("Camera init return - railorder", retval, type(self.origImg)))
                camera.release()

            logging.info("Camera grab success")

            blur = 11
            self.procImg = cv2.GaussianBlur(self.origImg[self.y1:self.y2, self.x1:self.x2], (blur, blur), 0)
            tmphsv = cv2.cvtColor(self.procImg, cv2.COLOR_BGR2HSV)
            rr = cv2.inRange(tmphsv, self.red[0], self.red[1])
            rg = cv2.inRange(tmphsv, self.green[0], self.green[1])
            rb = cv2.inRange(tmphsv, self.blue[0], self.blue[1])
            ry = cv2.inRange(tmphsv, self.yellow[0], self.yellow[1])
            cr = self.findCenterOfBiggestMass(rr)
            cg = self.findCenterOfBiggestMass(rg)
            cb = self.findCenterOfBiggestMass(rb)
            cy = self.findCenterOfBiggestMass(ry)

            mask = cv2.bitwise_or(rr, rg)
            mask = cv2.bitwise_or(mask, rb)
            mask = cv2.bitwise_or(mask, ry)

            self.procImg = self.applyMask(self.procImg, mask)

            cv2.imwrite(SAVE_LOC + "/%s_rail_order.jpg" % datetime.now(), self.origImg)
            cv2.imwrite(SAVE_LOC + "/%s_rail_order_proc.jpg" % datetime.now(), self.procImg)

            self.points = [cr, cg, cb, cy]
            self.colors = ['red', 'green', 'blue', 'yellow']

            self.railorder = sorted(zip(self.points, self.colors), key=lambda coord: coord[0][0])
            self.railorder = [list(i) for i in self.railorder]
            print(self.railorder)
        # except:
        #    sys.stderr.write("Error in init\n")

    def applyMask(self, img, mask):
        rv = np.zeros(img.shape, dtype=np.uint8)
        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                if mask[x][y]:
                    rv[x][y] = img[x][y]
        return rv

    def findCenterOfBiggestMass(self, mask):
        #try:
            _, contours, hierarchy = cv2.findContours(mask, 1, 2)
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
        #except:
            #sys.stderr.write("Error in findCenterOfBiggestMass")

    def get_rail_order(self, course):
        #try:
            # assume that only one of the bins is not viewable from the camera
            # if less than 3 bins are visible throw an error
            # if railorder[1][0] the x of the second lowest value is -1
            if self.railorder[1][0] == -1:
                sys.stderr.write("not all bins were visible. Readjust the camera\n")
            if course == 'B':
                # set the leftmost color's x coord to 1000 and resort, putting it on the right
                return [self.railorder[1][1], self.railorder[2][1], self.railorder[3][1], self.railorder[0][1]]
            else:
                return [c for (p, c) in self.railorder]
        #except:
            #sys.stderr.write("Error in get_rail_order\n")
