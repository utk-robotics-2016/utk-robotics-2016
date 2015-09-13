from head.imaging.BlockDetection import BlockDetection
import cv2

bd = BlockDetection()

bd.grabRightFrame()
#cv2.imwrite("test.jpg",bd.right_frame)

