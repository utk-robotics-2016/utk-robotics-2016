#!/usr/bin/env bash

#ino serial -p /dev/teensy -b 115200 -- --echo
picocom /dev/teensy -b 115200 --echo
