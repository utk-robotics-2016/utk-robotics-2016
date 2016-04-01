import argparse
import numpy as np
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
blur = 101
image = cv2.GaussianBlur(image, (blur, blur), 0)

cv2.imshow("image", image)

print image[235, 100][0], image[235, 100][1], image[235, 100][0]

raw_input("")