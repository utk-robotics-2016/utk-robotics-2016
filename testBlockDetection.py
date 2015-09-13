
# Python modules
import logging

from head.BlockDetection import BlockDetection
import csv
import numpy as np
import cv2
from matplotlib import pyplot as plt

bd = BlockDetection(0)
success = 0.0
failure = 0.0


with open('../Image_Training/DataSet.csv','rU') as csvfile:
    reader = csv.reader(csvfile, dialect='excel',delimiter=',')
    for row in reader:

        i = row[0]
        print "Left %s"%i
        bd.loadLeftFrame("../Image_Training/DataSet/left%s.png"%i)
        bd.loadRightFrame("../Image_Training/DataSet/right%s.png"%i)
        test = bd.getBlocks(1)
        test = test.strip()
        print "Test: "+test
        actual = ' '.join(row[1:])
        actual = actual.strip()
        print "Actual: "+actual

        if test == actual:
            print "SUCCESS\n"
            success = success + 1.0
        else:
            print "FAILURE\n"
            failure = failure + 1.0

            left = cv2.cvtColor(bd.left_frame,cv2.COLOR_BGR2RGB)
            fig = plt.figure() 
            fig.canvas.set_window_title("%s"%i) 
            plt.subplot(2,2,1),plt.imshow(left)
            plt.title('Left %s'%i)
            plt.subplot(2,2,2),plt.imshow(bd.left_laplacian,cmap="gray")
            plt.title('Left Laplacian %s'%i)
            right = cv2.cvtColor(bd.right_frame,cv2.COLOR_BGR2RGB)
            plt.subplot(2,2,3),plt.imshow(right)
            plt.title('Right %s'%i)

            plt.subplot(2,2,4),plt.imshow(bd.right_laplacian,cmap="gray")
            plt.title('Right Laplacian %s'%i)

            plt.show()
        
        #break
print "Successes: %d\nFailures: %d\nSuccess Rate: % 3.2f%%"%(success,failure,success/(success+failure)*100)