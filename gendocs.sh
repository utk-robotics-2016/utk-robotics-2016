#!/usr/bin/env bash

echo "Removing old files..."
rm -v docs/source/head.*
rm -v docs/source/modules.rst
echo "Done removing old files..."
sphinx-apidoc -o docs/source/ head --separate
sphinx-build -b html docs/source docs/build
