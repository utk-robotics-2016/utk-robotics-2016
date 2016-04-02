#!/usr/bin/env python
import logging
import numpy as np
import time
from datetime import datetime
import cv2

from color_point import color_point

logger = logging.getLogger(__name__)

SAVE_LOC = '/var/log/spine/imaging'


class block_detector:

    def __init__(self, s):

        self.s = s
        self.top_points = ((60, 160), (60, 350),
                           (200, 160), (200, 350),
                           (375, 160), (375, 350),
                           (560, 160), (560, 350),
                           (80, 100), (80, 325),
                           (225, 100), (225, 325),
                           (400, 100), (400, 325),
                           (570, 120), (570, 325))

        self.bottom_points = ((104, 187), (104, 382),
                              (232, 187), (232, 382),
                              (378, 187), (378, 382),
                              (526, 187), (526, 372),
                              (100, 200), (100, 375),
                              (240, 200), (240, 395),
                              (390, 200), (390, 395),
                              (530, 200), (530, 395))

    # Loads the frame from camera for the right side of the loader
    def grab_right_frame(self, saveImage=True):
        retval = False
        # loop until we get an image -- sleep to let the camera come online
        while( retval == False ):
            logger.info("Connecting to camera")
            self.camera = cv2.VideoCapture(0)
            time.sleep(1.0)
            logger.info("Grabbing right frame")
            retval, image = self.camera.read()
            logging.info(("Camera init return - block_detect", retval, type(image)))
            logger.info("Disconnecting from camera")
            self.camera.release()
        logging.info("Camera grab success")

        if saveImage:
            cv2.imwrite(SAVE_LOC + "/%s_right.jpg" % datetime.now(), image)
        rows, cols = image.shape[:2]
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -18, 1)
        self.right_frame = cv2.warpAffine(image, M, (cols, rows))
        if saveImage:
            cv2.imwrite(SAVE_LOC + "/%s_right_rotated.jpg" % datetime.now(), self.right_frame)
        self.right_hsv, self.right_gray, self.right_laplacian = self.process_frame(
            self.right_frame)
        cv2.imwrite(SAVE_LOC + "/%s_right_laplacian.jpg" % datetime.now(), self.right_laplacian)

    # Loads the frame from camera for the left side of the loader
    def grab_left_frame(self, saveImage=True):
        retval = False
        # loop until we get an image -- sleep to let the camera come online
        while( retval == False ):
            logger.info("Connecting to camera")
            self.camera = cv2.VideoCapture(0)
            time.sleep(1.0)
            logger.info("Grabbing left frame")
            retval, image = self.camera.read()
            logging.info(("Camera init return - block_detect", retval, type(image)))
            logger.info("Disconnecting from camera")
            self.camera.release()
        logging.info("Camera grab success")

        if saveImage:
            cv2.imwrite(SAVE_LOC + "/%s_left.jpg" % datetime.now(), image)
        rows, cols = image.shape[:2]
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 24, 1)
        self.left_frame = cv2.warpAffine(image, M, (cols, rows))
        if saveImage:
            cv2.imwrite(SAVE_LOC + "/%s_left_rotated.jpg" % datetime.now(), self.left_frame)
        self.left_hsv, self.left_gray, self.left_laplacian = self.process_frame(
            self.left_frame)
        cv2.imwrite(SAVE_LOC + "/%s_left_laplacian.jpg" % datetime.now(), self.left_laplacian)

    # Loads the frame from file for the right side of the loader
    def load_right_frame(self, filename):
        image = cv2.imread(filename)
        rows, cols = image.shape[:2]
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -18, 1)
        self.right_frame = cv2.warpAffine(image, M, (cols, rows))
        self.right_hsv, self.right_gray, self.right_laplacian = self.process_frame(
            self.right_frame)

    # Loads the frame from file for the left side of the loader
    def load_left_frame(self, filename):
        image = cv2.imread(filename)
        rows, cols = image.shape[:2]
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 24, 1)
        self.left_frame = cv2.warpAffine(image, M, (cols, rows))
        self.left_hsv, self.left_gray, self.left_laplacian = self.process_frame(
            self.left_frame)

    # Processes the frame with horizontal edge detection
    def process_frame(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        #blur = 51
        #hsv = cv2.GaussianBlur(hsv, (blur, blur), 0)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Grabs the horizontal edges
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobely = np.absolute(sobely)
        sobely = np.uint8(sobely)
        ret, sobely = cv2.threshold(sobely, 40, 255, cv2.THRESH_BINARY_INV)
        return hsv, gray, sobely

    # Add mouse callback so that image will have mouse and color information
    # displayed
    def display_data(self, windowname, image, left):
        cv2.imshow(windowname, image)
        if left:
            cv2.setMouseCallback(windowname, self.left_mouse_event, 0)
        else:
            cv2.setMouseCallback(windowname, self.right_mouse_event, 0)

    def right_mouse_event(self, evt, x, y, flags, params):
        temp = self.right_frame.copy()
        cp = color_point((x, y), self.right_frame, self.right_hsv)
        text = "x=%d, y=%d" % (cp.get_x(), cp.get_y())
        cv2.putText(temp, text, (5, 15),
                    cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
        text = "H=%d, S=%d, V=%d" % (cp.get_h(), cp.get_s(), cp.get_v())
        cv2.putText(temp, text, (5, 30),
                    cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
        if cp.get_color_improved() == 'R':
            text = "Red"
        elif cp.get_color_improved() == 'Y':
            text = "Yellow"
        elif cp.get_color_improved() == 'G':
            text = "Green"
        elif cp.get_color_improved() == 'B':
            text = "Blue"
        else:
            text = "Da Fuck...?"
        cv2.putText(temp, text, (5, 45),
                    cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
        cv2.imshow("mouse", temp)

    def left_mouse_event(self, evt, x, y, flags, params):
        temp = self.left_frame.copy()
        cp = color_point((x, y), self.left_frame, self.left_hsv)
        text = "x=%d, y=%d" % (cp.get_x(), cp.get_y())
        cv2.putText(temp, text, (5, 15),
                    cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
        text = "H=%d, S=%d, V=%d" % (cp.get_h(), cp.get_s(), cp.get_v())
        cv2.putText(temp, text, (5, 30),
                    cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
        if cp.get_color_improved() == 'R':
            text = "Red"
        elif cp.get_color_improved() == 'Y':
            text = "Yellow"
        elif cp.get_color_improved() == 'G':
            text = "Green"
        elif cp.get_color_improved() == 'B':
            text = "Blue"
        else:
            text = "Da Fuck...?"
        cv2.putText(temp, text, (5, 45),
                    cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
        cv2.imshow("mouse", temp)

    # Checks if a slot is 2 half blocks or a full length block
    def check_half_block(self, top, bottom, left_blocks):
        if(top.get_color_improved() != bottom.get_color_improved()):
            return True
        left = top.get_x() - 20
        right = top.get_x() + 20
        line = []
        for i in range(bottom.get_y() - top.get_y()):
            line.append(0)
            for j in range(right - left):
                if left_blocks:
                    if self.left_laplacian[top.get_y() + i, left + j] == 255:
                        line[-1] = line[-1] + 1
                else:
                    if self.right_laplacian[top.get_y() + i, left + j] == 255:
                        line[-1] = line[-1] + 1
            if line[-1] < 10:
                return True
        return False

    # marks point on an image
    def mark_point(self, cp, left_blocks):
        text1 = "x=%d, y=%d" % (cp.get_x(), cp.get_y())
        text2 = "H=%d, S=%d, V=%d" % (cp.get_h(), cp.get_s(), cp.get_v())
        if cp.get_color_improved() == 'R':
            text3 = "Red"
        elif cp.get_color_improved() == 'Y':
            text3 = "Yellow"
        elif cp.get_color_improved() == 'G':
            text3 = "Green"
        elif cp.get_color_improved() == 'B':
            text3 = "Blue"
        else:
            text3 = "Da Fuck...?"
        text4 = "R=%d, G=%d, B=%d" % (cp.get_r(), cp.get_g(), cp.get_b())
        if cp.get_rgb_color() == 'R':
            text5 = "Red"
        elif cp.get_rgb_color() == 'Y':
            text5 = "Yellow"
        elif cp.get_rgb_color() == 'G':
            text5 = "Green"
        elif cp.get_rgb_color() == 'B':
            text5 = "Blue"
        else:
            text5 = "Da Fuck...?"

        if left_blocks:
            cv2.rectangle(self.left_frame, (cp.get_x() - 30, cp.get_y() - 30),
                          (cp.get_x() + 30, cp.get_y() + 30), (255, 0, 0))
            cv2.circle(self.left_frame, (cp.get_x(),
                                         cp.get_y()), 3, (0, 255, 0), 2)
            cv2.putText(self.left_frame, text1, (cp.get_x() - 60,
                                                 cp.get_y() + 25), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
            cv2.putText(self.left_frame, text2, (cp.get_x() - 60,
                                                 cp.get_y() + 40), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
            cv2.putText(self.left_frame, text3, (cp.get_x() - 60,
                                                 cp.get_y() + 55), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
            cv2.putText(self.left_frame, text4, (cp.get_x() - 60,
                                                 cp.get_y() + 70), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
            cv2.putText(self.left_frame, text5, (cp.get_x() - 60,
                                                 cp.get_y() + 85), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
        else:
            cv2.rectangle(self.right_frame, (cp.get_x() - 30, cp.get_y() - 30),
                          (cp.get_x() + 30, cp.get_y() + 30), (255, 0, 0))
            cv2.circle(self.right_frame, (cp.get_x(),
                                          cp.get_y()), 3, (0, 255, 0), 2)
            cv2.putText(self.right_frame, text1, (cp.get_x() - 60,
                                                  cp.get_y() + 25), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
            cv2.putText(self.right_frame, text2, (cp.get_x() - 60,
                                                  cp.get_y() + 40), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
            cv2.putText(self.right_frame, text3, (cp.get_x() - 60,
                                                  cp.get_y() + 55), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
            cv2.putText(self.right_frame, text4, (cp.get_x() - 60,
                                                  cp.get_y() + 70), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))
            cv2.putText(self.right_frame, text5, (cp.get_x() - 60,
                                                  cp.get_y() + 85), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0))

    # Determine the block colors and whether they are a full or half block.
    # This goes from the top left to the bottom right.

    def get_blocks(self, top, saveFile=True, display=False):
        rv = ""
        if top:
            points = self.top_points
        else:
            points = self.bottom_points

        # The first 4 block slots use the left image
        for i in range(4):
            cp_top = color_point(points[i * 2], self.left_frame, self.left_hsv)
            cp_bottom = color_point(
                points[i * 2 + 1], self.left_frame, self.left_hsv)
            if self.check_half_block(cp_top, cp_bottom, 1):
                rv = rv + cp_top.get_color_improved() + "H " + \
                    cp_bottom.get_color_improved() + "H "
                if display or saveFile:
                    self.mark_point(cp_top, 1)
                    self.mark_point(cp_bottom, 1)
            else:
                rv = rv + cp_top.get_color_improved() + "L "
                if display or saveFile:
                    cp_top.set_y((cp_top.get_y() + cp_bottom.get_y()) / 2)
                    self.mark_point(cp_top, 1)

        # The second 4 block slots use the right image
        for i in range(4, 8):
            cp_top = color_point(
                points[i * 2], self.right_frame, self.right_hsv)
            cp_bottom = color_point(
                points[i * 2 + 1], self.right_frame, self.right_hsv)
            if self.check_half_block(cp_top, cp_bottom, 0):
                rv = rv + cp_top.get_color_improved() + "H " + \
                    cp_bottom.get_color_improved() + "H "
                if display or saveFile:
                    self.mark_point(cp_top, 0)
                    self.mark_point(cp_bottom, 0)
            else:
                rv = rv + cp_top.get_color_improved() + "L "
                if display or saveFile:
                    cp_top.set_y((cp_top.get_y() + cp_bottom.get_y()) / 2)
                    self.mark_point(cp_top, 0)

        if saveFile:
            if top:
                cv2.imwrite(SAVE_LOC + "/%s_top_left_marked.jpg" % datetime.now(), self.left_frame)
                cv2.imwrite(SAVE_LOC + "/%s_top_right_marked.jpg" % datetime.now(), self.right_frame)
            else:
                cv2.imwrite(SAVE_LOC + "/%s_bottom_left_marked.jpg" % datetime.now(), self.left_frame)
                cv2.imwrite(SAVE_LOC + "/%s_bottom_right_marked.jpg" % datetime.now(), self.right_frame)

        # self.s.writeWs({"type": "Blocks", "val": rv})
        if display:
            cv2.imshow("Left", self.left_frame)
            cv2.imshow("Right", self.right_frame)
        logger.info("Block Array: %s" % rv)
        with open(SAVE_LOC + '/%s_parsed.txt' % datetime.now(), 'a') as the_file:
            the_file.write(rv)
        return rv
