# Makefile for Block Setup Utility
CC = g++
CFLAGS = -g
EXECTUABLES: block_setup

all: $(EXECUTABLES)

.SUFFIXES: .cpp .o
.cpp .o:
	$(CC) $(CFLAGS) -c $*.cpp

block_setup: block_setup.o block_setup.h
	$(CC) $(CFLAGS) -o block_setup block_setup.o

clean:
	rm $(EXECUTABLES) *.o
