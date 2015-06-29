/*****************************************************************************
 * File: block_setup.cpp
 *
 * Description: Implements a basic block position randomization program
 * which allows for different course setups for each run.
 ****************************************************************************/

#include "block_setup.h"

/*****************************************************************************
 * Debugging flag - enable by setting to TRUE - enables debugging output
 ****************************************************************************/
#define DEBUG TRUE

/*****************************************************************************
 * Boolean constants
 ****************************************************************************/
#define TRUE 1
#define FALSE 0

/*****************************************************************************
 * Error Messages
 ****************************************************************************/
#define UNREC_COLOR "unrecognized block color"
#define UNREC_SIZE "unrecognized block size"

using namespace std;

/*****************************************************************************
 * Ouptuts a debugging message if DEBUG is enabled
 ****************************************************************************/
static void dbg_msg( const char* format, ... )
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

/*****************************************************************************
 * Ouputs an error message and exists if fatal
 ****************************************************************************/
static inline void error( string error_message, bool fatal )
{
    printf(
          "%s: %s\n",
          ( fatal ) ? "fatal error" : "error",
          error_message.c_str()
          );

    if( fatal ) exit( 1 );
}

/*****************************************************************************
 * Output all of the blocks in the blocks vector if DEBUG is enabled
 ****************************************************************************/
static inline void dbg_print_blocks( vector <block *> blocks )
{
    if( DEBUG )
    {
        for( int i = 0; i < blocks.size(); i++ )
        {
            dbg_msg( "Block %d - color: %c size: %s", blocks[i]->id, blocks[i]->color, (blocks[i]->size) ? "large" : "small" );
        }
    }
}

/*****************************************************************************
 * Randomly generate a column of blocks
 ****************************************************************************/
void generate_block_col()
{

}

/*****************************************************************************
 * Adds a new block to the blocks vector
 ****************************************************************************/
void add_block( vector <block *> &blocks, string size, string color )
{
    int i_size;
    int i_color;

    i_size = -1;
    i_color = -1;

    /* convert string into integer for block struct */
    if( size == "small" )
    {
        i_size = 0;
    }
    else if( size == "large" )
    {
        i_size = 1;
    }
    else
    {
        error( UNREC_SIZE, TRUE );
    }

    if( color == "red" )
    {
        i_color = 'r';
    }
    else if( color == "green" )
    {
        i_color = 'g';
    }
    else if( color == "blue" )
    {
        i_color = 'b';
    }
    else if( color == "yellow" )
    {
        i_color = 'y';
    }
    else
    {
        error( UNREC_COLOR, TRUE );
    }

    /* Create the block object, add to the vector, and assign its attributes */
    blocks.push_back( new block );
    blocks.back()->id = blocks.size() - 1;
    blocks.back()->size = i_size;
    blocks.back()->color = i_color;

}

/*****************************************************************************
 * Loads the available blocks from an input file into the blocks vector
 ****************************************************************************/
void load_blocks( string filename, vector <block *> &blocks )
{
    fstream input;
    stringstream ss;
    string line;
    string size;
    string color;

    dbg_msg( "Reading the input file %s", filename.c_str() );

    input.open( filename.c_str() );

    /* Process each line of text into a block */
    while( getline( input, line ) )
    {
        ss.clear();
        ss.str(line);

        ss >> size >> color;

        add_block( blocks, size, color );
    }
}

/*****************************************************************************
 * Generates the block set up based on the available blocks and given seed
 ****************************************************************************/
void generate_setup(
                   vector <block *> blocks,
                   vector <block_col> zone_a,
                   vector <block_col> zone_b,
                   int seed
                   )
{

    /* Seed the random number generator */
    srand( seed );

    dbg_msg( "Generating setup" );
}

int main ( int argc, char **argv )
{
    int seed;
    string input_file;

    /* use a vector to represent each set of blocks */
    vector <block *> blocks;

    /* use a vector to represent each zone */
    vector <block_col> zone_a;
    vector <block_col> zone_b;

    /* Allow for specifying the seed as a command line parameter */
    if( argc == 1 )
    {
        seed = time( 0 );
    }
    else if( argc == 2 )
    {
        seed = atoi( argv[1] );
    }

    /* default input file for now - TODO: add as a command line parameter */
    input_file = "input.txt";

    /* read in the available blocks */
    load_blocks( input_file, blocks );
    /* TODO: generate the layout of blocks in each zone */
    generate_setup( blocks, zone_a, zone_b, seed );
    /* TODO: output the results */
    dbg_print_blocks( blocks );

    return( 0 );
}
