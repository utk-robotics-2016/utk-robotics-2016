# Python modules
import time
# Local modules
from head.spine import spine, arm
from head.spine.arm import shoulderPos, elbowToWrist, shoulderToElbow, wristToCup
from head.spine.Vec3d import Vec3d
import math

# Change this port if not on LINUX
s = spine.Spine(spine.DEF_LINUX_PORT)
s.startup()
a = arm.Arm(s)

class Robot:
    def __init__(self):
        pass

    def start(self):
        s.set_suction(0)
        a.set_pos(shoulderPos+Vec3d(0,elbowToWrist,shoulderToElbow-wristToCup),0,0)
        a.move_to(shoulderPos+Vec3d(0,elbowToWrist,shoulderToElbow-wristToCup-7.7),-math.pi/16,0,1)
        s.set_suction(180)
        time.sleep(1)
        a.move_to(shoulderPos+Vec3d(0,elbowToWrist,shoulderToElbow-wristToCup),0,0,1)
        #set_arm_pos(s, shoulderPos+Vec3d(0,elbowToWrist,shoulderToElbow-wristToCup-3),0,0)
        #time.sleep(1)
        #set_arm_pos(s, shoulderPos+Vec3d(0,elbowToWrist,shoulderToElbow-wristToCup-6),0,0)
        #time.sleep(1)
        #set_arm_pos(s, shoulderPos+Vec3d(0,elbowToWrist,shoulderToElbow-wristToCup-7.7),-math.pi/16,0)
        #time.sleep(1)
        #s.set_suction(180)
        #time.sleep(5)
        #set_arm_pos(s, shoulderPos+Vec3d(0,elbowToWrist,shoulderToElbow-wristToCup-3),0,0)
        time.sleep(100)
        print "Done!"

bot = Robot()
bot.start()

s.close()
