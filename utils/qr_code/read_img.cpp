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
    ImageScanner scanner;
    Magick::Blob blob;
    Magick::Image magick( filename.c_str() );

    /* create a scanner and configure it */
    scanner.set_config( ZBAR_NONE, ZBAR_CFG_ENABLE, 1 );

    /* get image data from ImageMagick */
    int width = magick.columns();
    int height = magick.rows();

    /* extract the raw data */
    magick.modifyImage();
    magick.write( &blob, "GRAY", 8 );
    const void *raw = blob.data();

    /* wrap image data */
    Image image( width, height, "Y800", raw, width * height );

    /* scan the image for QR codes / barcodes */
    int n = scanner.scan( image );

    /* get the results for each recognized code */
    for( Image::SymbolIterator symbol = image.symbol_begin();
         symbol != image.symbol_end();
         ++symbol )
    {
        results.push_back( symbol->get_data() );
    }

    /* clean up */
    image.set_data(NULL, 0);
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
