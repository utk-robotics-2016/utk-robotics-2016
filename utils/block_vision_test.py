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
                logger.info(arm.detect_blocks())

        bot = Robot()
        bot.start()
