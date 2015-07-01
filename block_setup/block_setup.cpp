/*****************************************************************************
 * UTK IEEE Robotics 2015-2016
 * File: block_setup.cpp
 * Author: Parker Mitchell
 *
 * Description: Implements a basic block position randomization program
 * which allows for different course setups for each run.
 ****************************************************************************/

#include "block_setup.h"

/*----------------------------------------------------------------------------
 Boolean constants
----------------------------------------------------------------------------*/
#define TRUE  ( 1 )
#define FALSE ( 0 )

/*----------------------------------------------------------------------------
 Columns in each zone to generate
----------------------------------------------------------------------------*/
#define ZONE_B_COLS ( 7 )
#define ZONE_C_COLS ( 6 )

/*----------------------------------------------------------------------------
 Error Messages
----------------------------------------------------------------------------*/
#define UNREC_COLOR "unrecognized block color"
#define UNREC_SIZE "unrecognized block size"

/*----------------------------------------------------------------------------
 Keep track of number of blocks
----------------------------------------------------------------------------*/
unsigned int small_blocks;
unsigned int large_blocks;

/*----------------------------------------------------------------------------
 Output all of the blocks in the blocks vector if DEBUG is enabled
----------------------------------------------------------------------------*/
void dbg_print_blocks( vector <block *> &blocks )
{
    if( DEBUG )
    {
        for( int i = 0; i < blocks.size(); i++ )
        {
            dbg_msg
                (
                "Block %d - color: %c size: %s",
                blocks[i]->id,
                blocks[i]->color,
                ( blocks[i]->size ) ? "large" : "small"
                );
        }
    }
}

/*----------------------------------------------------------------------------
 Adds a new block to the blocks vector
----------------------------------------------------------------------------*/
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

    if( i_size == 1 )
    {
        large_blocks++;
    }
    else
    {
        small_blocks++;
    }
}

/*----------------------------------------------------------------------------
 Loads the available blocks from an input file into the blocks vector
----------------------------------------------------------------------------*/
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

/*----------------------------------------------------------------------------
 Removes a random block from avaiable and returns a pointer to it
----------------------------------------------------------------------------*/
block * get_block( vector <block *> &blocks )
{
    int r_num; /* random number */
    block *b;

    if( blocks.size() == 0 )
    {
        error( "Out of blocks", TRUE );
        return NULL;
    }

    r_num = rand() % blocks.size();
    b = blocks[r_num];

    if( b->size == 1 )
    {
        large_blocks--;
    }
    else
    {
        small_blocks--;
    }

    blocks.erase( blocks.begin() + r_num );

    return b;
}

/*----------------------------------------------------------------------------
 Same as get_block except it ensures the block is a large block
----------------------------------------------------------------------------*/
block * get_large_block( vector <block *> &blocks )
{
    int r_num; /* random number */
    block *b;

    if( large_blocks == 0 ) {
        error( "Out of large blocks", TRUE );
        return NULL;
    }

    do
    {
        r_num = rand() % blocks.size();
        b = blocks[r_num];
    }
    while( b->size == 0 );

    large_blocks--;
    blocks.erase( blocks.begin() + r_num );

    return b;
}

/*----------------------------------------------------------------------------
 Same as get_block except it ensure the block is a small block
----------------------------------------------------------------------------*/
block * get_small_block( vector <block *> &blocks )
{
    int r_num; /* random number */
    block *b;

    if( small_blocks == 0 )
    {
        error( "Out of small blocks", TRUE );
        return NULL;
    }

    do
    {
        r_num =  rand() % blocks.size();
        b = blocks[r_num];
    }
    while( b->size == 1 );

    small_blocks--;
    blocks.erase( blocks.begin() + r_num );

    return b;
}

/*----------------------------------------------------------------------------
 Generates the block set up based on the available blocks and given seed
----------------------------------------------------------------------------*/
void generate_setup(
                   vector <block *> &blocks,
                   vector <block_col *> &zone_b,
                   vector <block_col *> &zone_c,
                   int seed
                   )
{
    int i; /* iterator */
    int r_num; /* random number */
    block *b;
    block_col *bc;

    /* Seed the random number generator */
    srand( seed );

    dbg_msg( "Generating setup" );

    /* generate zone c first to use large blocks */
    for( i = 0; i < ZONE_C_COLS; i++ )
    {
        bc = new block_col;
        bc->top[0] = get_large_block( blocks );
        bc->bottom[0] = get_large_block( blocks );
        zone_c.push_back( bc );
    }

    /* generate zone b */
    for( i = 0; i < ZONE_B_COLS; i++ )
    {
        bc = new block_col;

        bc->top[0] = get_block( blocks );
        if( bc->top[0]->size == 0 )
        {
            bc->top[1] = get_small_block( blocks );
        }

        bc->bottom[0] = get_block( blocks );
        if( bc->bottom[0]->size == 0 )
        {
            bc->bottom[1] = get_small_block( blocks );
        }

        zone_b.push_back( bc );
    }
}

/*----------------------------------------------------------------------------
 Prints a column of blocks
----------------------------------------------------------------------------*/
void print_col( block_col *bc )
{
    block *b;

    if( bc == NULL )
    {
        error( "NULL block column", TRUE );
    }

    if( bc->top[0] == NULL || bc->bottom[0] == NULL )
    {
        error( "NULL block in column", TRUE );
    }

    printf("\t");

    printf( "Top: %c ", bc->top[0]->color );
    if( bc->top[0]->size == 0 )
    {
        printf( "%c ", bc->top[1]->color );
    }
    else
    {
        printf( "  " );
    }

    printf( "Bottom: %c", bc->bottom[0]->color );
    if( bc->bottom[0]->size == 0 )
    {
        printf( " %c", bc->bottom[1]->color );
    }
    printf("\n");
}

/*----------------------------------------------------------------------------
 Provides text output for the generated block configuration
----------------------------------------------------------------------------*/
void print_output( vector <block_col *> &zone_b, vector <block_col *> &zone_c )
{
    int i;

    printf("Zone B:\n");
    for( i = 0; i < zone_b.size(); i++ )
    {
        print_col( zone_b[i] );
    }

    printf("Zone C:\n");
    for( i = 0; i < zone_c.size(); i++ )
    {
        print_col( zone_c[i] );
    }

}

int main ( int argc, char **argv )
{
    int seed;
    string input_file;

    /* use a vector to represent each set of blocks */
    vector <block *> blocks;

    /* use a vector to represent each zone */
    vector <block_col *> zone_b;
    vector <block_col *> zone_c;

    /* Allow for specifying the seed as a command line parameter */
    if( argc == 1 )
    {
        seed = time( 0 );
    }
    else if( argc == 2 )
    {
        seed = atoi( argv[1] );
    }

    large_blocks = 0;
    small_blocks = 0;

    /* default input file for now - TODO: add as a command line parameter */
    input_file = "input.txt";

    /* read in the available blocks */
    load_blocks( input_file, blocks );
    /* TODO: generate the layout of blocks in each zone */
    generate_setup( blocks, zone_b, zone_c, seed );
    /* TODO: output the results */
    //dbg_print_blocks( blocks );
    dbg_msg( "Small Blocks left: %d | Large Blocks left: %d | Blocks left: %d", small_blocks, large_blocks, blocks.size() );
    print_output( zone_b, zone_c );

    return( 0 );
}
