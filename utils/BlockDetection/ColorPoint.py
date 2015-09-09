#!/usr/bin/env python
import cv2
import numpy as np
import math

class ColorPoint:
    """ Class that stores the color information of a pixel in an image"""

    def __init__(self, point, hsv_image, blur=3):
        self.p = point
        count = 0
        h = 0
        s = 0
        v = 0
        for i in range(point[1]-blur,point[1]+blur+1):
            if i < 0 or i > hsv_image.shape[0]:
                continue
            for j in range(point[0]-blur,point[0]+blur+1):
                if j < 0 or j > hsv_image.shape[1]:
                    continue
                count = count + 1
                h = h + hsv_image[point[1],point[0]][0]
                s = s + hsv_image[point[1],point[0]][1]
                v = v + hsv_image[point[1],point[0]][2]
        self.hsv = (h/count,s/count,v/count)


    def getXY(self):
        return self.p

    def setXY(new_p):
        self.p = new_p

    def setXY(new_x, new_y):
        self.p = (new_x,new_y)

    def getX(self):
        return self.p[0]

    def setX(self,new_x):
       self.p[0] = new_x

    def getY(self):
       return self.p[1]

    def setY(self, new_y):
        self.p = (self.p[0],new_y)

    def getHSV(self):
        return self.hsv

    def setHSV(self,newHSV):
        self.hsv = newHSV

    def setHSV(self, newH, newS, newV):
        self.hsv = (newH,newS,newV)

    def getH(self):
        return self.hsv[0]

    def setH(self, newH):
        self.hsv[0] = newH

    def getS(self):
        return self.hsv[1]

    def setS(self):
        self.hsv[1] = newS

    def getV(self):
        return self.hsv[2]

    def setV(self, newV):
        self.hsv[2] = newV

    def getHSVColor(self):
        h = self.hsv[0]
        s = self.hsv[1]
        if s < 20:
            return 'B'
        if h < 15 or h > 165:
            if h == 0 and self.hsv[1] == 0 and self.hsv[2] == 0:
                return '?'
            return 'R'
        elif h < 32:
            return 'Y'
        elif h < 90:
            return 'G'
        elif h < 145:
            return 'B'
        else:
            return '?'
