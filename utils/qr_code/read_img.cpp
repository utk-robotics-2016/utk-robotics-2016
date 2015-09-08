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
 Extracts QR code data from an image file and returns the data in a vector
----------------------------------------------------------------------------*/
void get_codes_from_image( vector <string> &results, string filename )
{
    ImageScanner scanner;   /* Zbar image scanner object    */
    Magick::Blob blob;      /* image data from Magick       */
    const void *raw;        /* raw image data               */
    int width, height;      /* image dimensions             */
    Magick::Image *magick;  /* ImageMagick object           */
    Image *image;           /* Zbar image object            */

    /* create the Image Magick object based on filename */
    magick = new Magick::Image( filename.c_str() );

    /* create a scanner and configure it */
    scanner.set_config( ZBAR_NONE, ZBAR_CFG_ENABLE, 1 );

    /* get image dimensions from ImageMagick */
    width = magick->columns();
    height = magick->rows();

    /* extract the raw data - convert to greyscale, 8-bit depth */
    magick->modifyImage();
    magick->write( &blob, "GRAY", 8 );
    raw = blob.data();

    /* drop image data into Zbar image object */
    image = new Image( width, height, "Y800", raw, width * height );

    /* scan the image for QR codes / barcodes */
    scanner.scan( *image );

    /* get the results for each recognized code */
    for( Image::SymbolIterator symbol = image->symbol_begin();
         symbol != image->symbol_end();
         ++symbol )
    {
        results.push_back( symbol->get_data() );
    }

    /* clean up */
    delete image;
    delete magick;
}

int main (int argc, char **argv)
{
    int i;
    vector <string> qr_data;

    /* Check that a file was passed - provide usage statement if not */
    if( argc != 2 )
    {
        error( TRUE, "Usage: read_img imagefile" );
    }

    /* initalize image magick c++ library */
    Magick::InitializeMagick( NULL );

    /* process the image and extract the codes */
    get_codes_from_image( qr_data, argv[ 1 ] );

    /* output all of the recognized codes */
    for( i = 0; i < qr_data.size(); i++ )
    {
        printf( "symbol %d - data: %s\n", i, qr_data[ i ].c_str() );
    }

    return 0;
}
