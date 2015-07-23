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
void error( bool fatal, const char *format, ... )
{
    va_list arglist;

    printf("%s: ", ( fatal ) ? "fatal error" : "error" );

    va_start( arglist, format );
    vprintf( format, arglist );
    va_end( arglist );
    printf( "\n" );

    if( fatal ) exit( 1 );
}
