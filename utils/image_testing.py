import numpy as np
from datetime import datetime
import cv2
from head.imaging.color_point import color_point

SAVE_LOC = '/var/log/spine/imaging'

image = cv2.imread(SAVE_LOC + "/2016-03-30 00:23:03.489804_left_rotated.jpg")
#image = cv2.GaussianBlur(image, (51, 51), 0)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

red1 = cv2.inRange(hsv, (0, 0, 0), (15, 255, 255))
red2 = cv2.inRange(hsv, (165, 0, 0), (179, 255, 255))
red = cv2.bitwise_or(red1, red2)

blue = cv2.inRange(hsv, (96, 0, 0), (145, 255, 255))
green = cv2.inRange(hsv, (33, 0, 0), (95, 255, 255))
yellow = cv2.inRange(hsv, (16, 0, 0), (32, 255, 255))

cv2.imwrite(SAVE_LOC + "/test_image.jpg", image)
cv2.imwrite(SAVE_LOC + "/red.jpg", red)
cv2.imwrite(SAVE_LOC + "/yellow.jpg", yellow)
cv2.imwrite(SAVE_LOC + "/blue.jpg", blue)
cv2.imwrite(SAVE_LOC + "/green.jpg", green)
cp = color_point((80, 160), image, hsv)
print ("H: %d Color: %c") % (cp.get_h(), cp.get_hsv_color())
