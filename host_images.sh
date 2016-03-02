#!/bin/bash

echo "Browse to: http://ieeebeagle.nomads.utk.edu:1337/"
cd /var/log/spine/imaging/
python -m SimpleHTTPServer 1337
