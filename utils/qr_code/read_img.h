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
#include "util.h"

using namespace std;
using namespace zbar;

/* reads the data from qr codes into the results vector */
void get_codes_from_image( vector <string> &results, string filename );
