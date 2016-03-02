#!/usr/bin/env bash

#ino build -m mega2560
hashes=$(sha1sum `find src/ -type f` | tr '\n' ',' | tr ' ' '-')
#echo $hashes
ino build --cppflags="-D __USER__=`whoami` -D __DIR__=`pwd` -D __GIT_HASH__=`git rev-parse HEAD`"
