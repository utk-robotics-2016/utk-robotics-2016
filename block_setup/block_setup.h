/*****************************************************************************
 * File: block_setup.h
 *
 * Description: Header file for block_setup.cpp
 ****************************************************************************/

#include <cstdlib>
#include <cstdio>
#include <cstdarg>
#include <ctime>
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>

/*****************************************************************************
 * Represents each wooden block
 * Size:
 *      0 = small or half length
 *      1 = large or full length
 *
 * Color:
 *      'r' = red
 *      'b' = blue
 *      'g' = green
 *      'y' = yellow
 ****************************************************************************/
struct block
{
    int id;
    int color;
    int size;
};

struct block_col
{
    int id;
    struct block top[2];
    struct block bottom[2];
};
