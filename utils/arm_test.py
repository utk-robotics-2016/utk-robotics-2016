# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine
from head.spine.arm import get_arm
from head.spine.Vec3d import Vec3d

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

SPEED = 1
FULL_BLOCK_FORWARD = 11
HEIGHT_TO_CLEAR_LOADER = 12
RIGHT_DROP_XY = (16,0)
BOTTOM_LEVEL_HEIGHT = -1 # height of the top surface of the bottom level

with get_spine() as s:
    with get_arm(s) as arm:
        class Robot:

            def __init__(self):
                pass

            def pick_block(self):
                # lateral, forward, height
                arm.move_to(Vec3d(-6, FULL_BLOCK_FORWARD, BOTTOM_LEVEL_HEIGHT+4), 0, 180, SPEED)
                s.set_suction(True)
                arm.move_to(Vec3d(-6, FULL_BLOCK_FORWARD, BOTTOM_LEVEL_HEIGHT-1), 0, 180, SPEED)
                time.sleep(0.5)
                arm.move_to(Vec3d(-6, FULL_BLOCK_FORWARD, HEIGHT_TO_CLEAR_LOADER), 0, 180, SPEED)

            def drop_block_right(self):
                arm.move_to(Vec3d(RIGHT_DROP_XY[0], RIGHT_DROP_XY[1], HEIGHT_TO_CLEAR_LOADER), 0, 180, SPEED)
                s.set_suction(False)
                s.set_release_suction(True)
                time.sleep(0.5)
                s.set_release_suction(False)

            def start(self):
                self.pick_block()
                self.drop_block_right()
                logger.info("Done!")

        bot = Robot()
        bot.start()
