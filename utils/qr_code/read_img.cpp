/*****************************************************************************
 * UTK IEEE Robotics 2015-2016
 * File: read_img.cpp
 * Author: Parker Mitchell
 *
 * Description: Modification of provided Zbar example code. Reads a QR code
 * from an input image file.
 ****************************************************************************/
#include "read_img.h"

/*----------------------------------------------------------------------------
 Reads image data from a file into the raw data with dimensions
----------------------------------------------------------------------------*/
void read_img( string filename, Magick::Blob &blob, int &width, int &height )
{
    Magick::Image *magick;  /* ImageMagick object           */

    /* load the file into an ImageMagick object */
    magick = new Magick::Image( filename.c_str() );

    /* get image dimensions from ImageMagick */
    width = magick->columns();
    height = magick->rows();

    /* convert image to grayscale, 8-bit depth and get raw data */
    magick->modifyImage();
    magick->write( &blob, "GRAY", 8 );

    /* enough magick for now */
    delete magick;
}

/*----------------------------------------------------------------------------
 Extracts QR code data from an image
----------------------------------------------------------------------------*/
void get_codes( vector<string> &results, void *raw_data, int width, int height )
{
    ImageScanner scanner;   /* Zbar image scanner object    */
    Image *image;           /* Zbar image object            */

    /* configure the Zbar scanner */
    scanner.set_config( ZBAR_NONE, ZBAR_CFG_ENABLE, 1 );

    /* drop image data into Zbar image object */
    image = new Image( width, height, "Y800", raw_data, width * height );

    /* scan the image for QR codes / barcodes */
    scanner.scan( *image );

    /* get the results for each recognized code */
    for( Image::SymbolIterator symbol = image->symbol_begin();
         symbol != image->symbol_end();
         ++symbol )
    {
        results.push_back( symbol->get_data() );
    }

    delete image;
}

/*----------------------------------------------------------------------------
 Captures an image from the webcam - gets raw image data + dimensions
----------------------------------------------------------------------------*/
void get_cam_img( void *raw_data, int &width, int &height )
{
    return;
}

int main (int argc, char **argv)
{
    int i;
    vector <string> qr_data;
    void *raw_data;
    int height, width;
    Magick::Blob blob;

    /* Check that a file was passed - provide usage statement if not */
    if( argc != 2 )
    {
        error( TRUE, "Usage: read_img imagefile" );
    }

    /* initalize image magick c++ library */
    Magick::InitializeMagick( NULL );

    /* process the image and extract the codes */
    read_img( argv[ 1 ], blob, width, height );
    get_codes( qr_data, (void *) blob.data(), width, height );

    /* output all of the recognized codes */
    for( i = 0; i < qr_data.size(); i++ )
    {
        printf( "symbol %d - data: %s\n", i, qr_data[ i ].c_str() );
    }

    return 0;
}
