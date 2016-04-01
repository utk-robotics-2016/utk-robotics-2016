import numpy
import cv2
import argparse
import sys
import os.path

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])
clone = image.copy()
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

def mouse_events(event, x, y, flags, param):
    global image, hsv
    image = clone.copy()
    cv2.circle(image, (x, y), 3, (0, 255, 0), 2)
    cv2.putText(image, "H: %d S: %d V: %d" % (hsv[y, x][0], hsv[y, x][1], hsv[y, x][2]), (x,y+20), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
    cv2.imshow("image", image)

cv2.namedWindow("image")
cv2.imshow("image", image)
cv2.setMouseCallback("image", mouse_events)
while True:
    key = cv2.waitKey(1) & 0xFF

    # if the 'c' key is pressed, break from the loop
    if key == ord("c"):
        break
# close all open windows
cv2.destroyAllWindows()
