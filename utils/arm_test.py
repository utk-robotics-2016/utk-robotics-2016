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

with get_spine() as s:
    with get_arm(s) as arm:
        class Robot:

            def __init__(self):
                pass

            def start(self):
                # raise ValueError()
                #s.move(1, 180, 0)
                arm.move_to(Vec3d(0,10,3),0,180)
                time.sleep(2)
                arm.move_to(Vec3d(0,10,1.5),0,180)
                time.sleep(2)
                arm.move_to(Vec3d(0,10,0),0,180)
                time.sleep(2)
                arm.move_to(Vec3d(0,10,1.5),0,180)
                time.sleep(2)
                arm.move_to(Vec3d(0,10,3),0,180)
                time.sleep(2)
                logger.info("Done!")

        bot = Robot()
        bot.start()
