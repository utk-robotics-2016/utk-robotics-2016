# Python modules
import time
# Local modules
from head.spine import spine
from head.spine.arm import set_arm_pos, shoulderPos, elbowToWrist, shoulderToElbow, wristToCup
from head.spine.Vec3d import Vec3d

# Change this port if not on LINUX
s = spine.Spine(spine.DEF_LINUX_PORT)
s.startup()

class Robot:
    def __init__(self):
        pass

    def start(self):
        set_arm_pos(s, shoulderPos+Vec3d(0,elbowToWrist,shoulderToElbow-wristToCup),0,0)
        time.sleep(100)
        print "Done!"

bot = Robot()
bot.start()

s.close()
