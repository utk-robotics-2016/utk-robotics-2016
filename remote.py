#!/usr/bin/env python

import random
from subprocess import Popen, PIPE

pin = random.randint(0, 9999)
wsServer = Popen(['wsServer', '9002'], stdout=PIPE, stdin=PIPE)

print "Pin Code: %04d" % (pin,)
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

open = True
wsServer.stdin.write("You have control\n")
print "You have control"

while open:
    line = wsServer.stdout.readline().rstrip()
    line = line.split(':', 1)
    tmpUser = line[0]
    if line[1] == ".":
        continue
    print line
    if tmpUser != user:
        print "Stop it, play nice"
        continue
    if line[1] == "close":
        print "closing"
        open = False

wsServer.terminate()
