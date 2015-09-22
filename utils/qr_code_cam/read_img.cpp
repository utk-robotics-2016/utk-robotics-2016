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
 Extracts QR code data from an image
----------------------------------------------------------------------------*/
void get_codes( vector<string> &results, void *raw_data, int width, int height )
{
    zbar::ImageScanner scanner; /* Zbar image scanner object    */
    zbar::Image *image;         /* Zbar image object            */

    /* configure the Zbar scanner */
    scanner.set_config( zbar::ZBAR_QRCODE, zbar::ZBAR_CFG_ENABLE, 1 );
    scanner.set_config( zbar::ZBAR_QRCODE, zbar::ZBAR_CFG_X_DENSITY, 8 );
    scanner.set_config( zbar::ZBAR_QRCODE, zbar::ZBAR_CFG_Y_DENSITY, 8 );

    /* drop image data into Zbar image object */
    image = new zbar::Image( width, height, "Y800", raw_data, width * height );

    /* scan the image for QR codes / barcodes */
    scanner.scan( *image );

    /* get the results for each recognized code */
    for( zbar::Image::SymbolIterator symbol = image->symbol_begin(); symbol != image->symbol_end(); ++symbol )
    {
        results.push_back( symbol->get_data() );
    }

    /* report if codes were found */
    dbg_msg( "%d codes found", results.size() );

    /* clean up */
    delete image;
}

/*----------------------------------------------------------------------------
 Captures an image from the webcam - gets raw image data + dimensions
----------------------------------------------------------------------------*/
void get_cam_img( void *&raw_data, int &width, int &height )
{
    VideoCapture cam( 0 );  /* OpenCV Video Capture         */
    Mat frame;              /* image captured from webcam   */
    Mat grayscale;          /* image converted to grayscale */

    if( !cam.isOpened() )
    {
        error( TRUE, "Cannot open webcam" );
    }

    /* get dimensions */
    width = cam.get( CV_CAP_PROP_FRAME_WIDTH );
    height = cam.get( CV_CAP_PROP_FRAME_HEIGHT );

    /* check if we could get a capture */
    if( !cam.read( frame ) )
    {
        dbg_msg( "Could not read from webcam" );
        raw_data = NULL;
        return;
    }

    /* convert to greysale */
    cvtColor( frame, grayscale, CV_BGR2GRAY );

    /* get the raw image data */
    raw_data = malloc( sizeof( char ) * grayscale.rows * grayscale.cols );
    memcpy( raw_data, grayscale.data, sizeof( char ) * grayscale.rows * grayscale.cols );
    cam.release();
}

int main ( int argc, char **argv )
{
    int i;                      /* loop iterator            */
    int height, width;          /* image dimensions         */
    string param;               /* passed parameter         */
    void *raw_data;             /* raw image data           */
    vector <string> qr_data;    /* decoded qr codes         */

    /* obtain the image from the webcam */
    dbg_msg( "Attempting to get data from webcam using OpenCV" );
    get_cam_img( raw_data, width, height );

    /* process the qr codes */
    if( raw_data == NULL )
    {
        error( TRUE, "Could not read image data" );
    }
    get_codes( qr_data, raw_data, width, height );

    /* output all of the recognized codes */
    for( i = 0; i < qr_data.size(); i++ )
    {
        printf( "%s\n", qr_data[ i ].c_str() );
    }

    free( raw_data );

    return 0;
}
