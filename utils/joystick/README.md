This utility allows remote control of the robot's arm and movement through an Xbox 360 controller.

## Quickstart

On the Beaglebone:

    cory@beaglebone:~/code/utk-robotics-2016/utils/joystick$ python joyserver.py
    The object's uri is: PYRO:obj_39cb775c1bc84e87851b2901d1f44217@0.0.0.0:9091
    The object's remote uri is: PYRO:obj_39cb775c1bc84e87851b2901d1f44217@ieeebeagle.nomads.utk.edu:9091

Take note of the remote uri. You will use it in joyclient.py to run remote `spine` commands on the BBB.

On a Linux computer with pygame installed:

    unbuffer python joyclient.py

or just

    python joyclient.py

Currently this depends on Pygame but soon we will switch to David's Xbox interface to remove this dependency.
