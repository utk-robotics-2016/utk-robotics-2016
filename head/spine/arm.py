from inverse_kinematics import revkin, shoulderToElbow, elbowToWrist, shoulderPos
from Vec3d import Vec3d
from math import pi

wristToCup = 7 # Distance in centimeters from wrist center to cup tip

# Servo configuration
BASECENTER = 86 # more positive moves to the right
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

# CENTER is defined as 0 radians

# Wrist is the amount of up rotation, from straight down, in radians
# cuppos assumes that wrist is set to 0 radians
def to_location(cuppos, wrist, wristrotate):
    wristpos = cuppos + Vec3d(0,0,wristToCup)
    rot = revkin(wristpos)
    wrist += -pi/2
    # If positive wrist flexes up, positive shoulder and elbow rotations will
    # add directly to wrist
    wrist+= rot[1] + rot[2]
    servo = [base_r2p(rot[0]), shoulder_r2p(rot[1]), elbow_r2p(rot[2]),
             wrist_r2p(wrist), wristrotate]
    servo = [int(round(p)) for p in servo]
    print servo

to_location(shoulderPos+Vec3d(0,elbowToWrist,shoulderToElbow-wristToCup),0,0)
to_location(shoulderPos+Vec3d(0,elbowToWrist+3,shoulderToElbow-wristToCup),0,0)
to_location(shoulderPos+Vec3d(3,elbowToWrist,shoulderToElbow-wristToCup),0,0)
to_location(shoulderPos+Vec3d(3,elbowToWrist,shoulderToElbow-wristToCup),pi/16,0)
#to_location(shoulderPos+Vec3d(300,elbowToWrist,shoulderToElbow-wristToCup),0,0)
