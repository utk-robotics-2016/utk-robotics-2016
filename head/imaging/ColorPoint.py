#!/usr/bin/env python
import cv2
import numpy as np
import math

class ColorPoint:
    """ Class that stores the color information of a pixel in an image"""

    def __init__(self, point, rgb_image, hsv_image, blur=2):
        self.p = point
        count = 0.0
        r = 0.0
        g = 0.0
        b = 0.0
        h = 0.0
        s = 0.0
        v = 0.0
        for i in range(point[1]-blur*10,point[1]+blur*10+1,20):
            if i < 0 or i > hsv_image.shape[0]:
                continue
            for j in range(point[0]-blur*10,point[0]+blur*10+1,20):
                if j < 0 or j > hsv_image.shape[1]:
                    continue
                count = count + 1
                r = r + rgb_image[point[1],point[0]][2]
                g = g + rgb_image[point[1],point[0]][1]
                b = b + rgb_image[point[1],point[0]][0]
                h = h + hsv_image[point[1],point[0]][0]
                s = s + hsv_image[point[1],point[0]][1]
                v = v + hsv_image[point[1],point[0]][2]
        self.hsv = (math.floor(h/count),math.floor(s/count),math.floor(v/count))
        self.rgb = (math.floor(r/count),math.floor(g/count),math.floor(b/count))

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

    def setS(self, newS):
        self.hsv[1] = newS

    def getV(self):
        return self.hsv[2]

    def setV(self, newV):
        self.hsv[2] = newV

    def getRGB(self):
        return self.rgb

    def setRGB(self,newRGB):
        self.rgb = newRGB

    def setRGB(self, newR, newG, newB):
        self.rgb = (newR,newG,newB)

    def getR(self):
        return self.rgb[0]

    def setR(self, newR):
        self.rgb[0] = newR

    def getG(self):
        return self.rgb[1]

    def setG(self, newG):
        self.rgb[1] = newG

    def getB(self):
        return self.rgb[2]

    def setB(self, newB):
        self.rgb[2] = newB

    def colorDistance(self,color1,color2):
        return math.sqrt(math.pow(color2[0]-color1[0],2)+math.pow(color2[1]-color1[1],2)+math.pow(color2[2]-color1[2],2))

    def getRGBColor(self):
        rDistance = self.colorDistance(self.rgb,(255,0,0))
        gDistance = self.colorDistance(self.rgb,(0,255,0))
        bDistance = self.colorDistance(self.rgb,(0,0,255))
        yDistance = self.colorDistance(self.rgb,(255,255,0))


        
        if rDistance < gDistance and rDistance < bDistance and rDistance < yDistance:
            return 'R'
        elif gDistance < bDistance and gDistance < yDistance:
            return 'G'
        elif bDistance < yDistance:
            return 'B'
        else:
            return 'Y'

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
