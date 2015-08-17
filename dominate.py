# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine
from head.spine.loader import Loader

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    class Robot:

        def __init__(self):
            self.ldr = Loader(s)

        def move_to_corner(self):
            logger.info("Moving out from corner")
            s.move(1, -90, 0)
            time.sleep(0.25)

            logger.info("Move through tunnel and open flap")
            s.move(1, 0, 0)
            time.sleep(3)
            s.move(1, 20, 0)
            self.ldr.open_flap()
            time.sleep(2)
            s.move(0.5, 20, 0)
            time.sleep(0.5)

            logger.info("Align to corner")
            s.move(1, 90, 0)
            time.sleep(1)

            logger.info("Moving back for space")
            s.move(1, 180, 0)
            time.sleep(0.2)

            logger.info("Move to front of blocks")
            s.move(1, -90, 0)
            time.sleep(1.2)
            
            logger.info("Align to wall")
            s.move(1, 0, 0)
            time.sleep(1)
            
            s.stop()
            self.ldr.load()
            
            logger.info("Resetting to start state")

        def start(self):
            self.move_to_corner()

            logger.info("Done!")

    bot = Robot()
    bot.start()

