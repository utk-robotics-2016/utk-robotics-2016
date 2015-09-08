/*****************************************************************************
 * UTK IEEE Robotics 2015-2016
 * File: read_img.h
 * Author: Parker Mitchell
 *
 * Description: Header file for read_img.cpp
 ****************************************************************************/

#include <vector>
#include <Magick++.h>
#include <zbar.h>
#include <opencv2/opencv.hpp>
#include "util.h"

using namespace std;
using namespace cv;

/* webcam capture dimensions */
#define WEBCAM_CAPTURE_WIDTH  ( 1280 )
#define WEBCAM_CAPTURE_HEIGHT ( 720  )

/* gets the data from qr codes embeded in the raw image data */
void get_codes( vector<string> &results, void *raw_data, int width, int height );

/* read an image from a file into the raw data with dimensions */
void read_img( string filename, Magick::Blob &blob, int &width, int &height );

/* captures an image from the webcam */
void get_cam_img( void *raw_data, int &width, int &height );
