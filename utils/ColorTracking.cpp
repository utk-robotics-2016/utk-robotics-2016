#include <sstream>
#include <string>
#include <iostream>
#include <vector>

#include "Block.h"

// initial min and max HSV filter values
int H_MIN = 0;
int H_MAX = 256;
int S_MIN = 0;
int S_MAX = 256;
int V_MIN = 0;
int V_MAX = 256;
int brightness = 256;

// default capture width and height
const int FRAME_WIDTH = 640;
const int FRAME_HEIGHT = 480;

// max number of objects to be detected in frame
const int MAX_NUM_OBJECTS = 50;

// minimum and maximum object area
const int MIX_OBJECT_AREA = 20*20;
const int MAX_OBJECT_AREA = FRAME_HEIGHT*FRAME_WIDTH/1.5;

// names that will appear at the top of each window
const string windowName = "Original Image";
const string windowName1 = "HSV Image";
const string windowName2 = "Thresholded Image";
const string windowName3 = "After Morphological Operations";
const string trackbarWindowName = "Trackbars";

// The following for canny edge detection
Mat dst, detected_edges;
Mat src, src_gray;
int edgeThresh = 1;
int lowThreshold;
int const max_lowThreshold = 100;
int ratio = 3;
int kernel_size = 3;
const string window_name = "Edge Map";

// Gets called when the trackbar position is changed
void on_trackbar(int, void*){}


string intToString(int number)
{
    std::stringstream ss;
    ss << number;
    return ss.str();
}

void createTrackbars()
{
    // create window for trackbars
    namedWindow(trackbarWindowName,0);

    createTrackbar("H_MIN", trackbarWindowName, &H_MIN, H_MAX, on_trackbar);
    createTrackbar("H_MAX", trackbarWindowName, &H_MAX, H_MAX, on_trackbar);
    createTrackbar("S_MIN", trackbarWindowName, &S_MIN, S_MAX, on_trackbar);
    createTrackbar("S_MAX", trackbarWindowName, &S_MAX, S_MAX, on_trackbar);
    createTrackbar("V_MIN", trackbarWindowName, &V_MIN, V_MAX, on_trackbar);
    createTrackbar("V_MAX", trackbarWindowName, &V_MAX, V_MAX, on_trackbar);
    createTrackbar("Brightness",trackbarWindowName,&brightness,512, on_trackbar);
}

void morphOps(Mat &thresh)
{
    Mat erodeElement = getStructuringElement(MORPH_RECT,Size(3,3));
    Mat dilateElement = getStructuringElement(MORPH_RECT,Size(8,8));

    erode(thresh, thresh, erodeElement);
    erode(thresh, thresh, erodeElement);

    dilate(thresh, thresh, dilateElement);
    dilate(thresh, thresh, dilateElement);
}


int main(int argc, char** argv)
{
    // for calibrating filter values
    bool calibrationMode = false;

    Mat hsv;
    Mat threshold;

    Block* blue = new Block("blue", Scalar(92,90,0),Scalar(124,256,256),Scalar(255,0,0));
    printf("Blue:\n\tMin: %d, %d, %d\n\tMax: %d, %d, %d\n\n", (int)blue->getHSVmin()[0], (int)blue->getHSVmin()[1], (int)blue->getHSVmin()[2], (int)blue->getHSVmax()[0],(int)blue->getHSVmax()[1], (int)blue->getHSVmax()[2]);

    if(calibrationMode)
    {
        //create slider bars for HSV filtering
        createTrackbars();
    }

    Mat srcOrig = imread(argv[1]);
    src = imread(argv[1]);

    while(1)
    {
        // Check for invalid input
        if(! src.data )
        {
            cout <<  "Could not open or find the image: "<<argv[1] << std::endl;
            return -1;
        }

        if(calibrationMode)
        {
        src = srcOrig + Scalar(brightness-256,brightness-256,brightness-256);
        }

        cvtColor(src,hsv,COLOR_BGR2HSV);
        if(calibrationMode)
        {
             printf("Threshold Value\n\tBrightness: %d\n\tH_MIN: %d\n\tH_MAX: %d\n\tS_MIN: %d\n\tS_MAX: %d\n\tV_MIN: %d\n\tV_MAX: %d\n\n",brightness,H_MIN,H_MAX,S_MIN,S_MAX,V_MIN,V_MAX);
            inRange(hsv, Scalar(H_MIN,S_MIN,V_MIN),Scalar(H_MAX,S_MAX,V_MAX),threshold);
        }
        else
        {
            inRange(hsv,blue->getHSVmin(),blue->getHSVmax(),threshold);
            morphOps(threshold);
        }
        
        namedWindow(windowName, CV_WINDOW_AUTOSIZE);
        imshow(windowName,src);
        namedWindow(windowName2,CV_WINDOW_AUTOSIZE);
        imshow(windowName2,threshold);
        
        waitKey(1);
    }
}
