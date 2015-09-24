#!/usr/bin/env python

import time
import random
import logging
import json
from subprocess import Popen, PIPE

from head.spine.core import get_spine
from head.spine.arm import get_arm
from head.spine.Vec3d import Vec3d

pin = random.randint(0, 99999)
wsServer = Popen(['wsServer', '9002'], stdout=PIPE, stdin=PIPE)

print "Pin Code: %05d" % (pin,)
user = None

while user is None:
    line = wsServer.stdout.readline().rstrip()
    line = line.split(':', 1)
    tmpUser = line[0]
    if line[1] == ".":
        continue
    print line
    uPin = int(line[1])
    if uPin == pin:
        user = tmpUser
        wsServer.stdin.write("Pin Verified\n")
        print "Pin Verified"
    else:
        time.sleep(3)

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    with get_arm(s) as arm:
        open = True
        wsServer.stdin.write("You have control\n")
        print user, "has control"

        while open:
            line = wsServer.stdout.readline().rstrip()
            line = line.split(':', 1)
            tmpUser = line[0]
            if line[1] == ".":
                continue
            print line
            if tmpUser != user:
                print "User not authorized"
                continue
            if line[1] == "close":
                print "closing"
                open = False
                continue

            obj = json.loads(line[1])

            if obj.has_key("arm"):
                print "Moving arm to", obj.get("arm")[0], obj.get("arm")[1], obj.get("arm")[2], 0.08 * 3.14, 180
                arm.move_to(Vec3d(obj.get("arm")[0], obj.get("arm")[1], obj.get("arm")[2]), 0.08 * 3.14, 180)
                print "Done moving arm"
            else:
                print "obj does not have arm"

        arm.park()

wsServer.terminate()
