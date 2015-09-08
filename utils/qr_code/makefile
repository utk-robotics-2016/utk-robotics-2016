# Makefile for QR Code utility
CC = g++
CFLAGS = -g `Magick++-config --cppflags --cxxflags`
LDFLAGS = `Magic++-config --ldflags` -I/usr/local/include/opencv -I/usr/local/include/opencv2 -L/usr/local/lib/
LIBS = -lzbar `Magick++-config --libs` -lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_ml -lopencv_video -lopencv_features2d -lopencv_calib3d -lopencv_objdetect -lopencv_stitching -lopencv_imgcodecs -lopencv_videoio
EXECTUABLES: read_img

all: $(EXECUTABLES)

.SUFFIXES: .cpp .o
.cpp .o:
	$(CC) $(CFLAGS) $(LDFLAGS) -c $*.cpp

read_img: read_img.o read_img.h util.o util.h
	$(CC) $(CFLAGS) -o read_img read_img.o util.o $(LIBS)

clean:
	rm -f $(EXECUTABLES) *.o
