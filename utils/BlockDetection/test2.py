import cv2
import numpy as np

rect_width = 20
rect_height = 100
#mask_pts = np.array([[150,0],[245,0],[640,145],[640,240],[535,480],[180,480],[0,380],[0,230]])
#mask = np.zeros((480,640),np.uint8)
#cv2.fillConvexPoly(mask, mask_pts, 1)
image = cv2.imread("DataSet/left12.png")
rows,cols = image.shape[:2]
M = cv2.getRotationMatrix2D((cols/2,rows/2),29,1)
image = cv2.warpAffine(image,M,(cols,rows))
cv2.imshow("Rotated",image)
background_mask = np.zeros((480,640),np.uint8)
cv2.fillConvexPoly(background_mask, np.array([[80,285-392/2],[640,90],[640,480],[80,480]]), 1)
image = cv2.bitwise_and(image,image,mask=background_mask)
hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
background_mask = np.zeros((480,640),np.uint8)
cv2.fillConvexPoly(background_mask, np.array([[149-119/2,285-392/2],[640,285-392/2],[640,285+392/2],[149-119/2,285+392/2]]), 1)
image = cv2.bitwise_and(image,image,mask=background_mask)
blue_mask = cv2.inRange(hsv,(90,0,0),(134,255,255))
#cv2.imshow("Blue Mask",blue_mask)
red_mask = cv2.bitwise_or(cv2.inRange(hsv,(0,1,1),(14,255,255)),cv2.inRange(hsv,(165,0,0),(180,255,255)))
#cv2.imshow("Red Mask",red_mask)
green_mask = cv2.inRange(hsv,(35,0,0),(89,255,255))
#cv2.imshow("Green Mask",green_mask)
yellow_mask = cv2.inRange(hsv,(15,0,0),(34,255,255))
#cv2.imshow("Yellow Mask",yellow_mask)
blocks = []

blue = cv2.bitwise_and(image,image,mask=blue_mask)
contours, hierarchies = cv2.findContours(blue_mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
newContours = []
for contour in contours:
	if cv2.contourArea(contour) > 10000:
		newContours.append(contour)
	else:
		cv2.fillConvexPoly(blue, contour, 1)
cv2.drawContours(blue, newContours, -1, (0,255,0), 3)
for contour in newContours:
    m = cv2.moments(contour)
    cx = int(m['m10']/m['m00'])
    cy = int(m['m01']/m['m00'])
    cv2.circle(blue,(cx,cy),3,(0,0,255),2)
    cv2.circle(blue,(cx-rect_width,cy-rect_height),3,(0,0,255),2)
    cv2.circle(blue,(cx+rect_width,cy-rect_height),3,(0,0,255),2)
    cv2.circle(blue,(cx-rect_width,cy+rect_height),3,(0,0,255),2)
    cv2.circle(blue,(cx+rect_width,cy+rect_height),3,(0,0,255),2)
    x,y,w,h = cv2.boundingRect(contour)
    cv2.rectangle(blue,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.rectangle(blue,(cx-rect_width,cy-rect_height),(cx+rect_width,cy+rect_height),(0,0,255),2)
    print "Width: %d"%w
    print "Height: %d"%h
    blocks.append((cx,cy,w,h,contour))
#cv2.imshow("Blue Mask",blue)


red = cv2.bitwise_and(image,image,mask=red_mask)
contours, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
newContours = []
for contour in contours:
	if cv2.contourArea(contour) > 10000:
		newContours.append(contour)
	else:
		cv2.fillConvexPoly(red, contour, 1)
cv2.drawContours(red, newContours, -1, (0,255,0), 3)
for contour in newContours:
    m = cv2.moments(contour)
    cx = int(m['m10']/m['m00'])
    cy = int(m['m01']/m['m00'])
    cv2.circle(red,(cx,cy),3,(0,0,255),2)
    cv2.circle(red,(cx-rect_width,cy-rect_height),3,(0,0,255),2)
    cv2.circle(red,(cx+rect_width,cy-rect_height),3,(0,0,255),2)
    cv2.circle(red,(cx-rect_width,cy+rect_height),3,(0,0,255),2)
    cv2.circle(red,(cx+rect_width,cy+rect_height),3,(0,0,255),2)
    x,y,w,h = cv2.boundingRect(contour)
    cv2.rectangle(red,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.rectangle(red,(cx-rect_width,cy-rect_height),(cx+rect_width,cy+rect_height),(0,0,255),2)
    print "Width: %d"%w
    print "Height: %d"%h
    blocks.append((cx,cy,w,h,contour))
#cv2.imshow("Red Mask",red)

green = cv2.bitwise_and(image,image,mask=green_mask)
contours, hierarchies = cv2.findContours(green_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
newContours = []
for contour in contours:
	if cv2.contourArea(contour) > 10000:
		newContours.append(contour)
	else:
		cv2.fillConvexPoly(green, contour, 1)
cv2.drawContours(green, newContours, -1, (0,255,0), 3)
for contour in newContours:
    m = cv2.moments(contour)
    cx = int(m['m10']/m['m00'])
    cy = int(m['m01']/m['m00'])
    cv2.circle(green,(cx,cy),3,(0,0,255),2)
    cv2.circle(green,(cx-rect_width,cy-rect_height),3,(0,0,255),2)
    cv2.circle(green,(cx+rect_width,cy-rect_height),3,(0,0,255),2)
    cv2.circle(green,(cx-rect_width,cy+rect_height),3,(0,0,255),2)
    cv2.circle(green,(cx+rect_width,cy+rect_height),3,(0,0,255),2)
    x,y,w,h = cv2.boundingRect(contour)
    cv2.rectangle(green,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.rectangle(green,(cx-rect_width,cy-rect_height),(cx+rect_width,cy+rect_height),(0,0,255),2)
    print "Width: %d"%w
    print "Height: %d"%h
    blocks.append((cx,cy,w,h,contour))
#cv2.imshow("Green Mask",green)

yellow = cv2.bitwise_and(image,image,mask=yellow_mask)
contours, hierarchy = cv2.findContours(yellow_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
newContours = []
for contour in contours:
	if cv2.contourArea(contour) > 10000:
		newContours.append(contour)
	else:
		cv2.fillConvexPoly(yellow, contour, 1)
cv2.drawContours(yellow, newContours, -1, (0,255,0), 3)
for contour in newContours:
    m = cv2.moments(contour)
    cx = int(m['m10']/m['m00'])
    cy = int(m['m01']/m['m00'])
    cv2.circle(yellow,(cx,cy),3,(0,0,255),2)
    cv2.circle(yellow,(cx-rect_width,cy-rect_height),3,(0,0,255),2)
    cv2.circle(yellow,(cx+rect_width,cy-rect_height),3,(0,0,255),2)
    cv2.circle(yellow,(cx-rect_width,cy+rect_height),3,(0,0,255),2)
    cv2.circle(yellow,(cx+rect_width,cy+rect_height),3,(0,0,255),2)
    x,y,w,h = cv2.boundingRect(contour)
    cv2.rectangle(yellow,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.rectangle(yellow,(cx-rect_width,cy-rect_height),(cx+rect_width,cy+rect_height),(0,0,255),2)
    print "Width: %d"%w
    print "Height: %d"%h
    blocks.append((cx,cy,w,h,contour))
#cv2.imshow("Yellow Mask",yellow)

final = cv2.bitwise_or(blue,red)
final = cv2.bitwise_or(final,yellow)
final = cv2.bitwise_or(final,green)
blocks = sorted(blocks, key=lambda block: block[0])
print blocks
numBlocks = 0
newBlocks = []
for block in blocks:
    if len(newBlocks) > 0:
        if abs(newBlocks[-1][0]-block[0]) > 10:
            numBlocks = numBlocks + 1
    if numBlocks < 4:
        newBlocks.append(block)
    else:
        cv2.fillConvexPoly(final,block[4],(0,0,0))

cv2.imshow("Final",final)

#image = cv2.bitwise_and(image,image,mask = mask)
'''
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray,(5,5),0)
laplacian = cv2.Laplacian(gray,cv2.CV_64F, ksize = 3)
laplacian = np.absolute(laplacian)
laplacian = np.uint8(laplacian)
ret, laplacian = cv2.threshold(laplacian,5,255,cv2.THRESH_BINARY_INV)
laplacian = cv2.medianBlur(laplacian,3)
laplacian = cv2.medianBlur(laplacian,3)
laplacian = cv2.medianBlur(laplacian,3)
laplacian = cv2.dilate(laplacian,(5,5),iterations = 1)
laplacian = cv2.erode(laplacian,(3,3),iterations = 1)
cv2.imshow("Laplacian",laplacian)
'''
cv2.waitKey(0)