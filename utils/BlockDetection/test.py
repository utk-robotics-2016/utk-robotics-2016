import cv2
import numpy as np

mask_pts = np.array([[150,0],[245,0],[640,145],[640,240],[535,480],[180,480],[0,380],[0,230]])
mask = np.zeros((480,640),np.uint8)
cv2.fillConvexPoly(mask, mask_pts, 1)

image = cv2.imread("DataSet/left3.png")
cv2.imshow("image",image)
image = cv2.bitwise_and(image,image,mask = mask)

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray,(5,5),0)
laplacian = cv2.Laplacian(gray,cv2.CV_64F, ksize = 3)
laplacian = np.absolute(laplacian)
laplacian = np.uint8(laplacian)
ret, laplacian = cv2.threshold(laplacian,5,255,cv2.THRESH_BINARY)
laplacian = cv2.medianBlur(laplacian,3)
laplacian = cv2.medianBlur(laplacian,3)
laplacian = cv2.medianBlur(laplacian,3)
laplacian = cv2.dilate(laplacian,(5,5),iterations = 1)
laplacian = cv2.erode(laplacian,(3,3),iterations = 1)

contours, hierarchy = cv2.findContours(laplacian,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(laplacian, contours, -1, (255,255,255), 3)

newContours = []
for contour in contours:
    if cv2.contourArea(contour) > 10000:
        newContours.append(contour)
    else:
        cv2.fillConvexPoly(laplacian, contour, 1)

cv2.drawContours(laplacian, newContours, -1, (255,255,255), 3)
cv2.imshow("Laplacian",laplacian)

    

cv2.waitKey(0)
