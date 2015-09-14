/*****************************************************************************
 * UTK IEEE Robotics 2015-2016
 * File: util.h
 * Author: Parker Mitchell
 *
 * Description: Header file for util.cpp
 ****************************************************************************/

#include <cstdlib>
#include <cstdio>
#include <cstdarg>
#include <cstring>
#include <string>

using namespace std;

/*----------------------------------------------------------------------------
 Boolean constants
----------------------------------------------------------------------------*/
#define TRUE  ( 1 )
#define FALSE ( 0 )

/*----------------------------------------------------------------------------
 Debugging flag - enable by setting to TRUE - enables debugging output
----------------------------------------------------------------------------*/
#define DEBUG TRUE

/*----------------------------------------------------------------------------
 Utility procedures
----------------------------------------------------------------------------*/
void dbg_msg( const char *format, ... );
void error( bool fatal, const char *format, ... );
