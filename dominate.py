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
            # set a threshold for white vs black values from the QTR sensor
            self.qtr_threshold = 800
            # Determine which course layout
            if s.read_switches()['course_mirror'] == 1:
                self.course = 'B'
                # dir_mod stands for direction modifier
                self.dir_mod = 1
            else:
                self.course = 'A'
                self.dir_mod = -1

        # moves with respect to the course layout
        def move(self, speed, dir, angle):
            s.move(speed, self.dir_mod * dir, angle)

        def move_to_corner(self):
            if self.course == 'B':
                logger.info("Moving out from corner")
                self.move(1, -90, 0)
                time.sleep(0.25)

                logger.info("Move through tunnel and open flap")
                self.move(1, 5, 0)
                time.sleep(2.5)
                self.move(1, 0, 0)
                # self.ldr.open_flap()
                time.sleep(2.5)
                self.move(0.5, 20, 0)
                time.sleep(0.5)
            else:
                logger.info("Move straight ahead")
                self.move(1, 0, 0)
                time.sleep(6)

            logger.info("Align to corner")
            self.move(1, 90, 0)
            time.sleep(.5)
            self.move(1, 0, 0)
            time.sleep(.5)
            self.move(1, 90, 0)
            time.sleep(.5)
            self.move(1, 0, 0)
            time.sleep(.5)
            '''
            logger.info("Moving back for space")
            self.move(1, 180, 0)
            time.sleep(0.2)

            logger.info("Move to front of blocks")
            self.move(1, -90, 0)
            time.sleep(1.2)

            logger.info("Align to wall")
            self.move(1, 0, 0)
            time.sleep(1)
            '''

            s.stop()
            # self.ldr.load()

            logger.info("Resetting to start state")

        def strafe_until_white(self):
            while read_line_sensors()['left'] > self.qtr_threshold:
                self.move(1, -90, 0)

        def start(self):
            self.move_to_corner()

            logger.info("Done!")

    bot = Robot()
    bot.start()
