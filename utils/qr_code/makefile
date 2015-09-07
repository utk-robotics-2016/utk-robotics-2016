# Makefile for QR Code utility
CC = g++
CFLAGS = -g `Magick++-config --cppflags --cxxflags`
LDFLAGS = `Magic++-config --ldflags`
LIBS = -lzbar `Magick++-config --libs`
EXECTUABLES: read_img

all: $(EXECUTABLES)

.SUFFIXES: .cpp .o
.cpp .o:
	$(CC) $(CFLAGS) $(LDFLAGS) -c $*.cpp

read_img: read_img.o read_img.h util.o util.h
	$(CC) $(CFLAGS) -o read_img read_img.o util.o $(LIBS)

clean:
	rm -f $(EXECUTABLES) *.o
