from __future__ import print_function

from math import pi, exp
import time
import operator
import logging

from head.spine.kinematics import revkin, shoulderToElbow, elbowToWrist, shoulderPos
from head.spine.Vec3d import Vec3d

wristToCup = 10 # Distance in centimeters from wrist center to cup tip

# Servo configuration
BASECENTER = 90 # more positive moves to the right
BASERIGHT = BASECENTER+85
BASELEFT = BASECENTER-85
def base_r2p(r): return BASECENTER + (r/(pi/2))*(BASERIGHT-BASECENTER)
SHOULDERCENTER = 95 # more positive moves backward
SHOULDERDOWN = SHOULDERCENTER-79
def shoulder_r2p(r): return SHOULDERCENTER + (r/(pi/2))*(SHOULDERDOWN-SHOULDERCENTER)
ELBOWCENTER = 126 # more positive moves down
ELBOWUP = ELBOWCENTER-90
def elbow_r2p(r): return ELBOWCENTER - (r/(pi/2))*(ELBOWUP-ELBOWCENTER)
WRISTCENTER = 95 # more positive flexes up
WRISTDOWN = WRISTCENTER-82
def wrist_r2p(r): return WRISTCENTER - (r/(pi/2))*(WRISTDOWN-WRISTCENTER)

# Probably no calibration needed
WRISTROTATECENTER = 90
SUCTIONCENTER = 90

PARKED = [90, 170, 180, 30, 0]

# CENTER is defined as 0 radians

def to_servos(cuppos, wrist, wristrotate):
    wristpos = cuppos + Vec3d(0,0,wristToCup)
    rot = revkin(wristpos)
    wrist += -pi/2
    # If positive wrist flexes up, positive shoulder and elbow rotations will
    # add directly to wrist
    wrist+= rot[1] + rot[2]
    servo = [base_r2p(rot[0]), shoulder_r2p(rot[1]), elbow_r2p(rot[2]),
             wrist_r2p(wrist), wristrotate]
    servo = [max(int(round(p)),0) for p in servo]
    #print servo
    return servo

def interpolate(f, startargs, endargs, seconds, smoothing):
    def linear(x):
        return x
    def rawsigmoid(a, x):
        return 1/(1 + exp(-(x - .5)/a))
    def sigmoid(a, x):
        return (rawsigmoid(a, x) - rawsigmoid(a, 0))/(rawsigmoid(a, 1) - rawsigmoid(a, 0))
    start_time = time.time()
    difference = map(operator.sub, endargs, startargs)
    curr_time = time.time()
    iters = 0
    while (curr_time-start_time) < seconds:
        elapsed = curr_time - start_time
        fraction = elapsed/seconds
        if smoothing == 'linear':
            sfunc = lambda x: linear(x)
        elif smoothing == 'sigmoid':
            sfunc = lambda x: sigmoid(0.13, x)
        toadd = [v*sfunc(fraction) for v in difference]
        currargs = map(operator.add, startargs, toadd)
        f(*currargs)
        curr_time = time.time()
        iters += 1
    print(iters)
    f(*endargs)

class Arm(object):
    def __init__(self, s):
        self.s = s
        self.servos = PARKED

    # Wrist is the amount of up rotation, from straight down, in radians
    # cuppos assumes that wrist is set to 0 radians
    # This is a raw function - use move_to instead
    def set_pos(self, cuppos, wrist, wristrotate):
        self.servos = to_servos(cuppos, wrist, wristrotate)
        self.s.set_arm(self.servos)

    def set_servos(self, *args):
        self.servos = args
        self.s.set_arm(list(args))

    def move_to(self, cuppos, wrist, wristrotate, seconds=1, smoothing='sigmoid'):
        startargs = self.servos
        endargs = to_servos(cuppos, wrist, wristrotate)
        interpolate(lambda *args: self.set_servos(*args), startargs, endargs, seconds, smoothing)
        #interpolate(lambda *args: print(repr(args)), startargs, endargs, seconds, smoothing)

    def move_to_abs(self, servopos, seconds=1, smoothing='sigmoid'):
        startargs = self.servos
        endargs = servopos
        interpolate(lambda *args: self.set_servos(*args), startargs, endargs, seconds, smoothing)

    def park(self, seconds=2):
        self.move_to_abs(PARKED, seconds)
        self.s.detach_servos()


#to_location(shoulderPos+Vec3d(0,elbowToWrist,shoulderToElbow-wristToCup),0,0)
#to_location(shoulderPos+Vec3d(0,elbowToWrist+3,shoulderToElbow-wristToCup),0,0)
#to_location(shoulderPos+Vec3d(3,elbowToWrist,shoulderToElbow-wristToCup),0,0)
#to_location(shoulderPos+Vec3d(3,elbowToWrist,shoulderToElbow-wristToCup),pi/16,0)
#to_location(shoulderPos+Vec3d(300,elbowToWrist,shoulderToElbow-wristToCup),0,0)