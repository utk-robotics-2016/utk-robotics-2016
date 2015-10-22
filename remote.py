#!/usr/bin/env python

# Python Modules
import time
import random
import logging
import json
from subprocess import Popen, PIPE

# Local Modules
from head.spine.core import get_spine
from head.spine.arm import get_arm
from head.spine.Vec3d import Vec3d

# Pin and Web Socket Servers
pin = random.randint(0, 99999)
wsServerRead = Popen(['wsServer', '9002'], stdout=PIPE, stdin=PIPE)
wsServerWrite = Popen(['wsServer', '9003'], stdout=PIPE, stdin=PIPE)

# Print pin to screen
print "Pin Code: %05d" % (pin,)
user = None

# Accept input until Pin is entered
while user is None:
    # Read in the line and split it up
    line = wsServerRead.stdout.readline().rstrip()
    line = line.split(':', 1)
    tmpUser = line[0]

    # Received ping to keep connection open
    if line[1] == ".":
        continue

    # Print line received
    print line

    # Get the pin from the line
    uPin = int(line[1])

    # If the pin entered by the user is correct
    if uPin == pin:
        # Then the pin is verified
        user = tmpUser
        wsServerWrite.stdin.write(str(user) + ":Pin Verified\n")
        print "Pin Verified"
    else:
        # Else wait 3 seconds to prevent spamming
        time.sleep(3)

# Setup logging for the robot
fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

# Initliatize robot
with get_spine() as s:
    with get_arm(s) as arm:
        open = True

        # Tell the user they have control
        wsServerWrite.stdin.write(str(user) + ":You have control\n")
        print user, "has control"

        # Loop while the connection is open
        while open:
            # Read in line and split it up
            line = wsServerRead.stdout.readline().rstrip()
            line = line.split(':', 1)
            tmpUser = line[0]

            # Received ping to keep connection open
            if line[1] == ".":
                continue

            # Print line received
            print line

            # If another user tries to enter anything, do nothing
            if tmpUser != user:
                print "User not authorized"
                continue

            # If the user sends close, shutdown the remote
            if line[1] == "close":
                print "closing"
                open = False
                continue

            # Read input as json
            obj = json.loads(line[1])

            if "arm" in obj:
                # If command is arm, move arm to requested location
                try:
                    arm.move_to(Vec3d(obj.get("arm")[0], obj.get("arm")[1], obj.get("arm")[2]), obj.get("arm")[3] * 3.14, 0)
                except ValueError:
                    # If a ValueError exception is thrown, nothing is done.
                    print "Out of reach"
                except AssertionError:
                    # If a AssertionError exception is thrown, then turn remote off
                    print "Out of reach, closing remote"
                    wsServerRead.terminate()
                    wsServerWrite.terminate()

            elif "suction" in obj:
                # If command is suction, either turn the suction on or off
                if obj.get("suction"):
                    s.set_release_suction(False)
                    s.set_suction(True)
                else:
                    s.set_suction(False)
                    s.set_release_suction(True)

            elif "move" in obj:
                # If command is move, move the robot in the desired direction
                # Assume max velocity
                s.move(obj.get("move")[0], obj.get("move")[1], obj.get("arm")[2], True)

            #elif "turn" in obj:
                # deal with turn commands
                # give it a velocity of 0


            else:
                print "invalid command", obj

                

# Close the wsServers
wsServerRead.terminate()
wsServerWrite.terminate()
