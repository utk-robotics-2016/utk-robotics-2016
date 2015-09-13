#!/usr/bin/env python
import ColorPoint
import numpy as np
import cv2


class BlockDetection:
    def __init__(self,live=1):
        self.live = live
        if live:
            self.camera = cv2.VideoCapture(0)

    # Loads the frame from camera for the right side of the loader        
    def grabRightFrame(self):
        retval, image = self.camera.read()
        rows,cols = image.shape[:2]
        M = cv2.getRotationMatrix2D((cols/2,rows/2),-18,1)
        self.right_frame = cv2.warpAffine(image,M,(cols,rows))
        self.right_hsv, self.right_gray, self.right_laplacian= self.processFrame(self.right_frame)

    # Loads the frame from camera for the left side of the loader
    def grabLeftFrame(self):
        retval, image = self.camera.read()
        rows,cols = image.shape[:2]
        M = cv2.getRotationMatrix2D((cols/2,rows/2),29,1)
        image = cv2.warpAffine(image,M,(cols,rows))
        self.left_hsv, self.left_gray, self.left_laplacian = self.processFrame(self.left_frame)

    # Loads the frame from file for the right side of the loader
    def loadRightFrame(self,filename):
        image = cv2.imread(filename)
        rows,cols = image.shape[:2]
        M = cv2.getRotationMatrix2D((cols/2,rows/2),-18,1)
        self.right_frame = cv2.warpAffine(image,M,(cols,rows))
        self.right_hsv, self.right_gray, self.right_laplacian= self.processFrame(self.right_frame)

    # Loads the frame from file for the left side of the loader
    def loadLeftFrame(self,filename):
        image = cv2.imread(filename)
        rows,cols = image.shape[:2]
        M = cv2.getRotationMatrix2D((cols/2,rows/2),29,1)
        self.left_frame = cv2.warpAffine(image,M,(cols,rows))
        self.left_hsv, self.left_gray, self.left_laplacian = self.processFrame(self.left_frame)

    # Processes the frame with horizontal edge detection
    def processFrame(self,image):
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        #Grabs the horizontal edges
        sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)
        sobely = np.absolute(sobely)
        sobely = np.uint8(sobely)
        ret, sobely = cv2.threshold(sobely,40,255,cv2.THRESH_BINARY_INV)
        #contours, hierarchy = cv2.findContours(sobely,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #sobely = np.zeros((480, 640),np.uint8)
        #for contour in contours:
        #    if cv2.contourArea(contour) > 1000:
        #        cv2.drawContours(sobely,contour,-1,255)
        return hsv, gray, sobely

    # Add mouse callback so that image will have mouse and color information displayed
    def displayData(self,windowname, image, left):
        cv2.imshow(windowname,image)
        if left:
            cv2.setMouseCallback(windowname,self.left_mouseEvent,0)
        else:
            cv2.setMouseCallback(windowname,self.right_mouseEvent,0)

    def right_mouseEvent(self,evt,x,y,flags,params):
        temp = self.right_frame.copy()
        cp = ColorPoint.ColorPoint((x,y),self.right_frame,self.right_hsv)
        text = "x=%d, y=%d"%(cp.getX(),cp.getY())
        cv2.putText(temp,text,(5,15),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))
        text = "H=%d, S=%d, V=%d"%(cp.getH(),cp.getS(),cp.getV())
        cv2.putText(temp,text,(5,30),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))
        if cp.getHSVColor() == 'R':
            text = "Red"
        elif cp.getHSVColor() == 'Y':
            text = "Yellow"
        elif cp.getHSVColor() == 'G':
            text = "Green"
        elif cp.getHSVColor() == 'B':
            text = "Blue"
        else:
            text = "Da Fuck...?"
        cv2.putText(temp,text,(5,45),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))
        cv2.imshow("mouse",temp)

    def left_mouseEvent(self,evt,x,y,flags,params):
        temp = self.left_frame.copy()
        cp = ColorPoint.ColorPoint((x,y),self.left_frame,self.left_hsv)
        text = "x=%d, y=%d"%(cp.getX(),cp.getY())
        cv2.putText(temp,text,(5,15),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))
        text = "H=%d, S=%d, V=%d"%(cp.getH(),cp.getS(),cp.getV())
        cv2.putText(temp,text,(5,30),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))
        if cp.getHSVColor() == 'R':
            text = "Red"
        elif cp.getHSVColor() == 'Y':
            text = "Yellow"
        elif cp.getHSVColor() == 'G':
            text = "Green"
        elif cp.getHSVColor() == 'B':
            text = "Blue"
        else:
            text = "Da Fuck...?"
        cv2.putText(temp,text,(5,45),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))
        cv2.imshow("mouse",temp)
    
    # Checks if a slot is 2 half blocks or a full length block
    def checkHalfBlock(self,top,bottom,leftBlocks):
        if( top.getHSVColor() != bottom.getHSVColor()):
            return True
        left = top.getX()-20
        right = top.getX()+20
        line = []
        for i in range(bottom.getY()-top.getY()):
            line.append(0)
            for j in range(right-left):
                if leftBlocks:
                    if self.left_laplacian[top.getY()+i,left+j] == 255:
                        line[-1] = line[-1] + 1
                else:
                    if self.right_laplacian[top.getY()+i,left+j] == 255:
                        line[-1] = line[-1] + 1
            if line[-1] < 10:
                return True
        return False

    #marks point on an image
    def markPoint(self,cp, leftBlocks):
        if leftBlocks:
            cv2.rectangle(self.left_frame,(cp.getX()-40,cp.getY()-40),(cp.getX()+40,cp.getY()+40),(255,0,0))
        else:
            cv2.rectangle(self.right_frame,(cp.getX()-40,cp.getY()-40),(cp.getX()+40,cp.getY()+40),(255,0,0))


        if leftBlocks:
            cv2.circle(self.left_frame,(cp.getX(),cp.getY()),3,(0,255,0),2)
        else:
            cv2.circle(self.right_frame,(cp.getX(),cp.getY()),3,(0,255,0),2)
        
        text = "x=%d, y=%d"%(cp.getX(),cp.getY())
        print text
        if leftBlocks:
            cv2.putText(self.left_frame,text,(cp.getX()-60,cp.getY()+25),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))
        else:
            cv2.putText(self.right_frame,text,(cp.getX()-60,cp.getY()+25),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))    
        
        text = "H=%d, S=%d, V=%d"%(cp.getH(),cp.getS(),cp.getV())
        print text
        if leftBlocks:
            cv2.putText(self.left_frame,text,(cp.getX()-60,cp.getY()+40),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))
        else:
            cv2.putText(self.right_frame,text,(cp.getX()-60,cp.getY()+40),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))        
        
        if cp.getHSVColor() == 'R':
            text = "Red"
        elif cp.getHSVColor() == 'Y':
            text = "Yellow"
        elif cp.getHSVColor() == 'G':
            text = "Green"
        elif cp.getHSVColor() == 'B':
            text = "Blue"
        else:
            text = "Da Fuck...?"
        print text
        if leftBlocks:
            cv2.putText(self.left_frame,text,(cp.getX()-60,cp.getY()+55),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))
        else:
            cv2.putText(self.right_frame,text,(cp.getX()-60,cp.getY()+55),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))
        
        text = "R=%d, G=%d, B=%d"%(cp.getR(),cp.getG(),cp.getB())
        print text
        if leftBlocks:
            cv2.putText(self.left_frame,text,(cp.getX()-60,cp.getY()+70),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))
        else:
            cv2.putText(self.right_frame,text,(cp.getX()-60,cp.getY()+70),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))        
        
        if cp.getRGBColor() == 'R':
            text = "Red"
        elif cp.getRGBColor() == 'Y':
            text = "Yellow"
        elif cp.getRGBColor() == 'G':
            text = "Green"
        elif cp.getRGBColor() == 'B':
            text = "Blue"
        else:
            text = "Da Fuck...?"
        print text
        if leftBlocks:
            cv2.putText(self.left_frame,text,(cp.getX()-60,cp.getY()+85),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))
        else:
            cv2.putText(self.right_frame,text,(cp.getX()-60,cp.getY()+85),cv2.FONT_HERSHEY_PLAIN,1.0,(0,255,0))
        print '\n'
    #Determine the block colors and whether they are a full or half block. 
    #This goes from the top left to the bottom right.
    def getBlocks(self,display):
        rv = ""
        #The first 4 block slots use the left image
        #First block slot
        cpTop = ColorPoint.ColorPoint((124,187),self.left_frame, self.left_hsv)
        cpBottom = ColorPoint.ColorPoint((124,382),self.left_frame,self.left_hsv)
        if self.checkHalfBlock(cpTop,cpBottom,1):
            rv = rv + cpTop.getHSVColor()+"H "+cpBottom.getHSVColor()+"H "
            if display:
                self.markPoint(cpTop,1)
                self.markPoint(cpBottom,1)
        else:
            rv = rv + cpTop.getHSVColor()+"L "
            if display:
                cpTop.setY((cpTop.getY()+cpBottom.getY())/2)
                self.markPoint(cpTop,1)

        #Second block slot
        cpTop = ColorPoint.ColorPoint((257,187),self.left_frame,self.left_hsv)
        cpBottom = ColorPoint.ColorPoint((257,382),self.left_frame,self.left_hsv)
        if self.checkHalfBlock(cpTop,cpBottom,1):
            rv = rv + cpTop.getHSVColor()+"H "+cpBottom.getHSVColor()+"H "
            if display:
                self.markPoint(cpTop,1)
                self.markPoint(cpBottom,1)
        else:
            rv = rv + cpTop.getHSVColor()+"L "
            if display:
                cpTop.setY((cpTop.getY()+cpBottom.getY())/2)
                self.markPoint(cpTop,1)

        #Third block slot
        cpTop = ColorPoint.ColorPoint((398,187),self.left_frame,self.left_hsv)
        cpBottom = ColorPoint.ColorPoint((398,382),self.left_frame,self.left_hsv)
        if self.checkHalfBlock(cpTop,cpBottom,1):
            rv = rv + cpTop.getHSVColor()+"H "+cpBottom.getHSVColor()+"H "
            if display:
                self.markPoint(cpTop,1)
                self.markPoint(cpBottom,1)
        else:
            rv = rv + cpTop.getHSVColor()+"L "
            if display:
                cpTop.setY((cpTop.getY()+cpBottom.getY())/2)
                self.markPoint(cpTop,1)
        #Fourth block slot
        cpTop = ColorPoint.ColorPoint((521,187),self.left_frame,self.left_hsv)
        cpBottom = ColorPoint.ColorPoint((521,372),self.left_frame,self.left_hsv)
        if self.checkHalfBlock(cpTop,cpBottom,1):
            rv = rv + cpTop.getHSVColor()+"H "+cpBottom.getHSVColor()+"H "
            if display:
                self.markPoint(cpTop,1)
                self.markPoint(cpBottom,1)
        else:
            rv = rv + cpTop.getHSVColor()+"L "
            if display:
                cpTop.setY((cpTop.getY()+cpBottom.getY())/2)
                self.markPoint(cpTop,1)
        
        #The second 4 block slots use the right image
        #Fifth block slot
        cpTop = ColorPoint.ColorPoint((107,100),self.right_frame,self.right_hsv)
        cpBottom = ColorPoint.ColorPoint((107,325),self.right_frame,self.right_hsv)
        if self.checkHalfBlock(cpTop,cpBottom,0):
            rv = rv + cpTop.getHSVColor()+"H "+cpBottom.getHSVColor()+"H "
            if display:
                self.markPoint(cpTop,0)
                self.markPoint(cpBottom,0)
        else:
            rv = rv + cpTop.getHSVColor()+"L "
            if display:
                cpTop.setY((cpTop.getY()+cpBottom.getY())/2)
                self.markPoint(cpTop,0)

        #Sixth block slot
        cpTop = ColorPoint.ColorPoint((250,100),self.right_frame,self.right_hsv)
        cpBottom = ColorPoint.ColorPoint((250,325),self.right_frame,self.right_hsv)
        if self.checkHalfBlock(cpTop,cpBottom,0):
            rv = rv + cpTop.getHSVColor()+"H "+cpBottom.getHSVColor()+"H "
            if display:
                self.markPoint(cpTop,0)
                self.markPoint(cpBottom,0)
        else:
            rv = rv + cpTop.getHSVColor()+"L "
            if display:
                cpTop.setY((cpTop.getY()+cpBottom.getY())/2)
                self.markPoint(cpTop,0)

        #Seventh block slot
        cpTop = ColorPoint.ColorPoint((390,100),self.right_frame,self.right_hsv)
        cpBottom = ColorPoint.ColorPoint((390,325),self.right_frame,self.right_hsv)
        if self.checkHalfBlock(cpTop,cpBottom,0):
            rv = rv + cpTop.getHSVColor()+"H "+cpBottom.getHSVColor()+"H "
            if display:
                self.markPoint(cpTop,0)
                self.markPoint(cpBottom,0)
        else:
            rv = rv + cpTop.getHSVColor()+"L "
            if display:
                cpTop.setY((cpTop.getY()+cpBottom.getY())/2)
                self.markPoint(cpTop,0)

        #Eighth block slot
        cpTop = ColorPoint.ColorPoint((520,100),self.right_frame,self.right_hsv)
        cpBottom = ColorPoint.ColorPoint((520,325),self.right_frame,self.right_hsv)
        if self.checkHalfBlock(cpTop,cpBottom,0):
            rv = rv + cpTop.getHSVColor()+"H "+cpBottom.getHSVColor()+"H"
            if display:
                self.markPoint(cpTop,0)
                self.markPoint(cpBottom,0)
        else:
            rv = rv + cpTop.getHSVColor()+"L"
            if display:
                cpTop.setY((cpTop.getY()+cpBottom.getY())/2)
                self.markPoint(cpTop,0)
        return rv
