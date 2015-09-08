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
    Magick::Image *magick;  /* ImageMagick object */

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
    zbar::ImageScanner scanner; /* Zbar image scanner object    */
    zbar::Image *image;         /* Zbar image object            */

    /* configure the Zbar scanner */
    scanner.set_config( zbar::ZBAR_NONE, zbar::ZBAR_CFG_ENABLE, 1 );

    /* drop image data into Zbar image object */
    image = new zbar::Image( width, height, "Y800", raw_data, width * height );

    /* scan the image for QR codes / barcodes */
    scanner.scan( *image );

    /* get the results for each recognized code */
    for( zbar::Image::SymbolIterator symbol = image->symbol_begin(); symbol != image->symbol_end(); ++symbol )
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
    //VideoCapture cam(0);
    //Mat frame;
    //Mat greyscale;

    /* get dimensions */
    //width =  cam.get( CV_CAP_PROP_FRAME_WIDTH );
    //height =  cam.get( CV_CAP_PROP_FRAME_HEIGHT );

    /* check if we could get a capture */
    //if( !cam.read( frame ) )
    //{
    //    raw_data = NULL;
    //    return;
    //}

    /* convert to greysale */
    //cvtColor( frame, greyscale, CV_BGR2GRAY );

    /* get the raw image data */
    //raw_data = (char *) greyscale.data;
}

int main ( int argc, char **argv )
{
    int i;                      /* loop iterator        */
    int height, width;          /* image dimensions     */
    void *raw_data;             /* raw image data       */
    Magick::Blob blob;          /* image in blob format */
    vector <string> qr_data;    /* decoded qr codes     */

    /* Check that a file was passed - provide usage statement if not */
    if( argc != 2 )
    {
        error( TRUE, "Usage: read_img imagefile" );
    }

    /* initalize image magick c++ library */
    Magick::InitializeMagick( NULL );

    /* process the image into the raw data */
    read_img( argv[ 1 ], blob, width, height );
    raw_data = (void *) blob.data();

    /* process the qr codes */
    get_codes( qr_data, raw_data, width, height );

    /* output all of the recognized codes */
    for( i = 0; i < qr_data.size(); i++ )
    {
        printf( "symbol %d - data: %s\n", i, qr_data[ i ].c_str() );
    }

    return 0;
}
