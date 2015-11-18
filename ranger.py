import cv2
import numpy as np

mode = "Results"

lower = np.array([0,0,0])
upper = np.array([180,255,255])

red = [np.array([160, 128, 0]), np.array([180, 255, 255])]
green = [np.array([70, 128, 0]), np.array([100, 255, 120])]
blue = [np.array([100, 128, 100]), np.array([105, 255, 150])]
yellow = [np.array([20, 150, 220]), np.array([30, 255, 255])]

camera = cv2.VideoCapture(0)
retval, img = camera.read()
#img = cv2.imread("tmp.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower, upper)
res = cv2.bitwise_and(img, img, mask=mask)

def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        #print hsv[y, x]
        print x, y

cv2.namedWindow('image')
cv2.setMouseCallback('image', click)

def remask(x):
    global lower, upper, mask, res
    lower = np.array([cv2.getTrackbarPos('Lower H', 'image'), cv2.getTrackbarPos('Lower S', 'image'), cv2.getTrackbarPos('Lower V', 'image')])
    upper = np.array([cv2.getTrackbarPos('Upper H', 'image'), cv2.getTrackbarPos('Upper S', 'image'), cv2.getTrackbarPos('Upper V', 'image')])
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(img, img, mask= mask)

def findCenterOfBiggestMass(mask):
    contours, hierarchy = cv2.findContours(mask, 1, 2)
    biggestArea = -1
    biggestIndex = -1
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > biggestArea:
            biggestArea = area
            biggestIndex = i
    M = cv2.moments(contours[biggestIndex])
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return (cx, cy)
    return (-1, -1)

def reimg(pos):
    global mask, res
    
    if (pos == 0):
        res = img
    elif (pos == 1):
        mask = cv2.inRange(hsv, red[0], red[1])
        center = findCenterOfBiggestMass(mask)
        res = cv2.bitwise_and(img, img, mask= mask)
        cv2.circle(res, center, 5, (0, 0, 255), 9)
    elif (pos == 2):
        mask = cv2.inRange(hsv, green[0], green[1])
        center = findCenterOfBiggestMass(mask)
        res = cv2.bitwise_and(img, img, mask= mask)
        cv2.circle(res, center, 5, (0, 255, 0), 9)
    elif (pos == 3):
        mask = cv2.inRange(hsv, blue[0], blue[1])
        center = findCenterOfBiggestMass(mask)
        res = cv2.bitwise_and(img, img, mask= mask)
        cv2.circle(res, center, 5, (255, 0, 0), 9)
    elif (pos == 4):
        mask = cv2.inRange(hsv, yellow[0], yellow[1])
        center = findCenterOfBiggestMass(mask)
        res = cv2.bitwise_and(img, img, mask= mask)
        cv2.circle(res, center, 5, (0, 255, 255), 9)
    elif (pos == 5):
        r = cv2.inRange(hsv, red[0], red[1])
        g = cv2.inRange(hsv, green[0], green[1])
        b = cv2.inRange(hsv, blue[0], blue[1])
        y = cv2.inRange(hsv, yellow[0], yellow[1])
        cr = findCenterOfBiggestMass(r)
        cg = findCenterOfBiggestMass(g)
        cb = findCenterOfBiggestMass(b)
        cy = findCenterOfBiggestMass(y)
        resmask = cv2.bitwise_or(r, g)
        resmask = cv2.bitwise_or(resmask, b)
        resmask = cv2.bitwise_or(resmask, y)
        res = cv2.bitwise_and(img, img, mask=resmask)
        cv2.circle(res, cr, 5, (0, 0, 255), 9)
        cv2.circle(res, cg, 5, (0, 255, 0), 9)
        cv2.circle(res, cb, 5, (255, 0, 0), 9)
        cv2.circle(res, cy, 5, (0, 255, 255), 9)

#function to get position of cart
def get_color(color):
    global mask
    mask = cv2.inRange(hsv, color[0], color[1])
    c = findCenterOfBiggestMass(mask)  #considering just returning the value of findCenterOfBiggestMass
    return c

def get_rail_zone_order():
    cr = ('red', get_color(red))
    cb = ('blue', get_color(blue))
    cg = ('green', get_color(green))
    cy = ('yellow', get_color(yellow))
    bins = [cr, cb, cg, cy]
    bins = sorted(bins, key=lambda color: color[1][0])
    #if there's an error, the coords will be (-1, -1) and the missing bin will be sorted into bins[0] 
    width = img.shape[1]    #get the width of the img to calculate the midpoint
    avg = np.mean([bins[1][0], bins[2][0], bins[3][0]])
    if (avg > width/2): #hard coding in the bin locations, I'm sure there's a better way
        bin_colors = [bins[1][0], bins[2][0], bins[3][0], bins[0][0]]
    else:
        bin_colors = [bins[0][0], bins[1][0], bins[2][0], bins[3][0]]
    return bin_colors
    

if mode == "Ranger":
    cv2.createTrackbar('Lower H','image',0,180,remask)
    cv2.createTrackbar('Lower S','image',0,255,remask)
    cv2.createTrackbar('Lower V','image',0,255,remask)
    cv2.createTrackbar('Upper H','image',180,180,remask)
    cv2.createTrackbar('Upper S','image',255,255,remask)
    cv2.createTrackbar('Upper V','image',255,255,remask)
elif mode == "Results":
    cv2.createTrackbar('Color','image',0,5,reimg)

while True:
    cv2.imshow("image", res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
