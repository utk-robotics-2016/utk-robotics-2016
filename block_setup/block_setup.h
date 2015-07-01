/*****************************************************************************
 * UTK IEEE Robotics 2015-2016
 * File: block_setup.h
 * Author: Parker Mitchell
 *
 * Description: Header file for block_setup.cpp
 ****************************************************************************/

#include <ctime>
#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include "util.h"

using namespace std;

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

/*****************************************************************************
 * Represents each column of blocks
 * Each column can support 2 half length blocks at the bottom or the top
 * or 1 full length block at the bottom or the top
 ****************************************************************************/
struct block_col
{
    int id;
    struct block *top[2];
    struct block *bottom[2];
};

void dbg_print_blocks( vector <block *> &blocks );
void add_block( vector <block *> &blocks, string size, string color );
void load_blocks( string filename, vector <block *> &blocks );
block * get_block( vector <block *> &blocks );
block * get_large_block( vector <block *> &blocks );
block * get_small_block( vector <block *> &blocks );
void generate_setup(
                   vector <block *> &blocks,
                   vector <block_col *> &zone_b,
                   vector <block_col *> &zone_c,
                   int seed
               );
void print_col( block_col *bc );
void print_output( vector <block_col *> &zone_b, vector <block_col *> &zone_c );
