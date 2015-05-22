# Python modules
import time
# Local modules
from head.spine import spine, arm
from head.spine.arm import shoulderPos, elbowToWrist, shoulderToElbow, wristToCup
from head.spine.Vec3d import Vec3d
from math import pi

# Change this port if not on LINUX
s = spine.Spine(spine.DEF_LINUX_PORT)
s.startup()
a = arm.Arm(s)

class Robot:
    def __init__(self):
        pass

    def start(self):
        '''
        a.move_to(shoulderPos+Vec3d(0,elbowToWrist,shoulderToElbow-wristToCup-7.7),-math.pi/16,0,1)
        s.set_suction(180)
        time.sleep(1)
        a.move_to(shoulderPos+Vec3d(0,elbowToWrist,shoulderToElbow-wristToCup),0,0,1)
        '''
        '''
        s.set_suction(0)
        a.set_pos(shoulderPos+Vec3d(0,elbowToWrist,shoulderToElbow-wristToCup),0,0)
        a.move_to(Vec3d(0,13,4),0,0,1)
        a.move_to(Vec3d(0,13,1.5),-pi/32,0,1)
        s.set_suction(180)
        time.sleep(2)
        #a.move_to(Vec3d(0,10,5),0,0,1)
        a.move_to(Vec3d(0,13,12),pi/16,0,1)
        #a.move_to(Vec3d(0,10,10),math.pi/3,0,1)
        #a.move_to(Vec3d(10,10,5),0,0,1)
        #a.move_to(Vec3d(10,10,-2),0,0,1)
        #s.set_suction(0)
        #time.sleep(2)
        #a.move_to(Vec3d(0,10,10),math.pi/3,0,1)
        '''
        # startup
        s.set_suction(0)
        # move to a high position
        a.move_to(Vec3d(0,13,10),-pi/32,0,3)

        # make contact with green block
        a.move_to(Vec3d(0,13,1.5),-pi/32,0,2)
        s.set_suction(180)
        time.sleep(3)
        # lift block
        a.move_to(Vec3d(0,13,10),pi/10,0,2)
        # hover over destination
        a.move_to(Vec3d(10,13,10),0,0,2)
        # place block
        a.move_to(Vec3d(15,13,-1),0,0,2)
        s.set_suction(0)
        time.sleep(1)
        # move to high position
        a.move_to(Vec3d(10,13,10),0,0,2)

        # hover over red block
        a.move_to(Vec3d(.5,5.5,10),-pi/64,0,2)
        time.sleep(1)
        # make contact with red block
        a.move_to(Vec3d(.5,5,6),-pi/32,0,2)
        s.set_suction(180)
        time.sleep(3)
        # lift red block
        a.move_to(Vec3d(.5,5,10),pi/10,0,2)
        # hover over destination
        a.move_to(Vec3d(10,13,10),0,0,2)
        a.move_to(Vec3d(14,13,5),pi/9,0,2)
        a.move_to(Vec3d(14.5,13,3.5),pi/9,0,2)
        # place block
        s.set_suction(0)
        time.sleep(1)

        # hover over orange block
        a.move_to(Vec3d(.5,4.5,6),0,0,2)
        time.sleep(1)
        a.move_to(Vec3d(.5,4,2),-pi/32,0,2)
        s.set_suction(180)
        time.sleep(3)
        # lift orange block
        a.move_to(Vec3d(.5,5,10),pi/10,0,2)
        # hover over destination
        a.move_to(Vec3d(10,13,10),0,0,2)
        a.move_to(Vec3d(13,12,5),0,0,2)
        a.move_to(Vec3d(12.5,12.5,3),pi/32,0,2)
        # place block
        s.set_suction(0)
        time.sleep(1)

        # shutdown
        # move to a high position
        a.move_to(Vec3d(0,13,10),-pi/32,0,3)
        a.park()
        print "Done!"

bot = Robot()
bot.start()

s.close()
