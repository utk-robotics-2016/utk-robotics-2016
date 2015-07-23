#!/usr/bin/env bash

find . -not -path '*/optics/*' -not -path '*/new_optics/*' -not -path '*/.eggs/*' -name '*.py' | xargs flake8
