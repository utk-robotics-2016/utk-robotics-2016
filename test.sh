#!/usr/bin/env bash

find . -not -path '*/optics/*' -not -path '*/new_optics/*' -not -path '*/.eggs/*' -not -name 'Vec3d.py' -name '*.py' | xargs flake8 --max-complexity 10
#vulture --exclude="/new_optics/,/optics/,/Vec3d.py" .
