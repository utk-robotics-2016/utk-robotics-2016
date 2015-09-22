#!/usr/bin/env python
import sys
import logging
import cv2
import zbar
import Image
import numpy as np

from color_point import color_point

# Requires: python-zbar, python-imaging

logger = logging.getLogger(__name__)

class rail_detector:

    def __init__(self):
        logger.info("Created rail detector")
        self.codes = []
        # do something

    # connect to webcam and grab a frame
    def grab_frame(self):
        logger.info("Connecting to camera")
        self.camera = cv2.VideoCapture(0)
        logger.info("Grabbing a frame")
        retval, image = self.camera.read()
        logger.info("Disconnecting from camera")
        self.camera.release()

        # get the image dimensions
        self.height, self.width = image.shape[:2]
        self.hsv, self.gray = self.process_frame(image)

    # Processes the frame into HSV and grayscale color spaces
    def process_frame(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        return hsv, gray

    # Determines the color of the rail cars
    def get_rails(self):
        # get a frame from the webcam
        self.grab_frame()

        # scan the frame for a QR code
        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')
        raw = Image.fromarray(self.gray).tostring()
        image = zbar.Image(self.width, self.height, 'Y800', raw)
        scanner.scan(image)
        for symbol in image:
            self.codes.append(symbol.data)

        print self.codes

        # TODO: fall back to HSV color detection if QR isn't read
