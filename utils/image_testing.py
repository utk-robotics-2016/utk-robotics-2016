# import numpy
import cv2
import argparse
import sys
import os.path

refPt = []
processing = False
selecting = False

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-f", "--file", default="image_testing/output.csv", help="Path to the output file")
args = vars(ap.parse_args())
newFile = False
if not os.path.exists(args["file"]):
    newFile = True
f = open(args["file"], "a+")
if newFile:
    f.write('r,g,b,h,s,v,correct_color,andrew_color\n')

image = cv2.imread(args["image"])
clone = image.copy()
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


def mouse_events(event, x, y, flags, param):
    global refPt, processing, selecting, image

    if processing:
        return

    if event == cv2.EVENT_LBUTTONDOWN and not selecting:
        refPt = [(x, y)]
        selecting = True

    elif event == cv2.EVENT_LBUTTONUP:
        selecting = False
        refPt.append((x, y))

        # cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        # cv2.imshow("image", image)
    elif selecting:
        image = clone.copy()
        cv2.rectangle(image, refPt[0], (x, y), (0, 255, 0), 2)
        cv2.imshow("image", image)


cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_events)

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # if the 'c' key is pressed, break from the loop
    if key == ord("c"):
        break

    if len(refPt) == 2:
        processing = True
        response = raw_input("Color (G, B, Y, R)?\n>")
        if response.lower() == 'r' or response.lower() == 'red':
            color = 'r'
        elif response.lower() == 'g' or response.lower() == 'green':
            color = 'g'
        elif response.lower() == 'b' or response.lower() == 'blue':
            color = 'b'
        elif response.lower() == 'y' or response.lower() == 'yellow':
            color = 'y'

        blur = 20
        pixelCount = 0
        for x in range(refPt[0][0], refPt[1][0]):
                for y in range(refPt[0][1], refPt[1][1]):
                    if pixelCount != 5:
                        pixelCount = pixelCount + 1
                        continue
                    pixelCount = 0
                    count = 0
                    r = 0
                    g = 0
                    b = 0
                    h = 0
                    s = 0
                    v = 0
                    for i in range(y - blur, y + blur):
                        if i < 0 or i > hsv.shape[0]:
                            continue
                        for j in range(x - blur, x + blur):
                            if j < 0 or j > hsv.shape[1]:
                                continue
                            count = count + 1
                            r = r + clone[i, j][2]
                            g = g + clone[i, j][1]
                            b = b + clone[i, j][0]
                            h = h + hsv[i, j][0]
                            s = s + hsv[i, j][1]
                            v = v + hsv[i, j][2]

                    r = r / count
                    g = g / count
                    b = b / count
                    h = h / count
                    s = s / count
                    v = v / count

                    if s < 20:
                        myColor = 'b'
                    if h <= 15 or h >= 165:
                        if h == 0 and self.hsv[1] == 0 and self.hsv[2] == 0:
                            myColor = '?'
                        myColor = 'r'
                    elif h <= 32:
                        myColor = 'y'
                    elif h <= 95:
                        myColor = 'g'
                    elif h <= 145:
                        myColor = 'b'
                    else:
                        myColor = '?'

                    f.write('%d,%d,%d,%d,%d,%d,%c,%c\n' % (r, g, b, h, s, v, color, myColor))
        image = clone.copy()
        cv2.imshow("image", image)
        refPt = []
        processing = False
        response = raw_input("Would you like to add another section?\n>")
        if response.lower() == 'n' or response.lower() == 'no':
            sys.exit()
# close all open windows
cv2.destroyAllWindows()
