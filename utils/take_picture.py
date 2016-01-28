import cv2

camera = cv2.VideoCapture(0)
retval, image = camera.read()
cv2.imwrite("test.jpg",image)
