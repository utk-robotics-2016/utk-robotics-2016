#!/usr/bin/env python
# import cv2
# import numpy as np
import math


class color_point:
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
        for i in range(point[1] - blur * 10, point[1] + blur * 10 + 1, blur * 10):
            if i < 0 or i > hsv_image.shape[0]:
                continue
            for j in range(point[0] - blur * 10, point[0] + blur * 10 + 1, blur * 10):
                if j < 0 or j > hsv_image.shape[1]:
                    continue
                count = count + 1
                r = r + rgb_image[point[1], point[0]][2]
                g = g + rgb_image[point[1], point[0]][1]
                b = b + rgb_image[point[1], point[0]][0]
                h = h + hsv_image[point[1], point[0]][0]
                s = s + hsv_image[point[1], point[0]][1]
                v = v + hsv_image[point[1], point[0]][2]
        self.hsv = (math.floor(h / count),
                    math.floor(s / count), math.floor(v / count))
        self.rgb = (math.floor(r / count),
                    math.floor(g / count), math.floor(b / count))

    def get_xy(self):
        return self.p

    def set_xy(self, new_p):
        self.p = new_p

    '''
    def set_xy(self, new_x, new_y):
        self.p = (new_x, new_y)
    '''

    def get_x(self):
        return self.p[0]

    def set_x(self, new_x):
        self.p[0] = new_x

    def get_y(self):
        return self.p[1]

    def set_y(self, new_y):
        self.p = (self.p[0], new_y)

    def get_hsv(self):
        return self.hsv

    def set_hsv(self, new_hsv):
        self.hsv = new_hsv

    '''
    def set_hsv(self, new_h, new_s, new_v):
        self.hsv = (new_h, new_s, new_v)
    '''

    def get_h(self):
        return self.hsv[0]

    def set_h(self, new_h):
        self.hsv[0] = new_h

    def get_s(self):
        return self.hsv[1]

    def setS(self, new_s):
        self.hsv[1] = new_s

    def get_v(self):
        return self.hsv[2]

    def setV(self, new_v):
        self.hsv[2] = new_v

    def get_rGB(self):
        return self.rgb

    def setRGB(self, new_rgb):
        self.rgb = new_rgb

    '''
    def setRGB(self, newR, newG, newB):
        self.rgb = (newR, newG, newB)
    '''

    def get_r(self):
        return self.rgb[0]

    def setR(self, new_r):
        self.rgb[0] = new_r

    def get_g(self):
        return self.rgb[1]

    def setG(self, new_g):
        self.rgb[1] = new_g

    def get_b(self):
        return self.rgb[2]

    def setB(self, new_b):
        self.rgb[2] = new_b

    def color_distance(self, color1, color2):
        return math.sqrt(math.pow(color2[0] - color1[0], 2) + math.pow(color2[1] - color1[1], 2) + math.pow(color2[2] - color1[2], 2))

    def get_rgb_color(self):
        rDistance = self.color_distance(self.rgb, (255, 0, 0))
        gDistance = self.color_distance(self.rgb, (0, 255, 0))
        bDistance = self.color_distance(self.rgb, (0, 0, 255))
        yDistance = self.color_distance(self.rgb, (255, 255, 0))

        if rDistance < gDistance and rDistance < bDistance and rDistance < yDistance:
            return 'R'
        elif gDistance < bDistance and gDistance < yDistance:
            return 'G'
        elif bDistance < yDistance:
            return 'B'
        else:
            return 'Y'

    def get_hsv_color(self):
        h = self.hsv[0]
        s = self.hsv[1]
        if s < 20:
            return 'B'
        if h <= 15 or h >= 165:
            if h == 0 and self.hsv[1] == 0 and self.hsv[2] == 0:
                return '?'
            return 'R'
        elif h <= 32:
            return 'Y'
        elif h <= 95:
            return 'G'
        elif h <= 145:
            return 'B'
        else:
            return '?'
