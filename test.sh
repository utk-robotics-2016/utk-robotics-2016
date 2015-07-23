#!/usr/bin/env bash

find . -not -path '*/.eggs/*' -name '*.py' | xargs flake8
