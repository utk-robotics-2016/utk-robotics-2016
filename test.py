import cv2
import numpy as np
#from head.imaging.color_point import color_point

camera = cv2.VideoCapture(0)
retval, im = camera.read()
print retval
cv2.imwrite("/home/anthony/tmp.jpg", im)
camera.release()

'''
img = cv2.imread("/home/anthony/tmp.jpg")
shp= img.shape
M = cv2.getRotationMatrix2D((shp[1]/2, shp[0]/2), 180, 1)
dst = cv2.warpAffine(img, M, (shp[1], shp[0]))
dst = dst[shp[1]/2:shp[1], 0:shp[0]]
hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
cv2.imwrite("/home/anthony/hsv.jpg", hsv)
dst = cv2.inRange(hsv, np.array([105, 50, 50],np.uint8), np.array([135, 255, 255],np.uint8))
cv2.imwrite("/home/anthony/bgr.jpg", dst)
'''
#rgb = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
#cv2.imwrite("/home/anthony/rgb.jpg", rgb)

#cp = color_point((shp[0] / 2, shp[1] / 2), rgb, hsv)
#print cp.get_hsv_color()
