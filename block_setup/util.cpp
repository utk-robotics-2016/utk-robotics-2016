/*****************************************************************************
 * UTK IEEE Robotics 2015-2016
 * File: util.cpp
 * Author: Parker Mitchell
 *
 * Description: Provides utility functions.
 ****************************************************************************/

#include "util.h"

/*----------------------------------------------------------------------------
 Ouptuts a debugging message if DEBUG is enabled
----------------------------------------------------------------------------*/
void dbg_msg( const char* format, ... )
{
    va_list arglist;

    if( DEBUG )
    {
        printf( "DBG: " );
        va_start( arglist, format );
        vprintf( format, arglist );
        va_end( arglist );
        printf( "\n" );
    }
}

/*----------------------------------------------------------------------------
 Ouputs an error message and exists if fatal
----------------------------------------------------------------------------*/
void error( string error_message, bool fatal )
{
    printf(
          "%s: %s\n",
          ( fatal ) ? "fatal error" : "error",
          error_message.c_str()
          );

    if( fatal ) exit( 1 );
}
