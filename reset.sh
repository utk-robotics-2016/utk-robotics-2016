#!/bin/bash

read -p "Should we lift first for 3 seconds? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    python utils/loader_control.py --lift=3
fi
python utils/loader_control.py --compress=4
python utils/loader_control.py --retract=2 --power=130