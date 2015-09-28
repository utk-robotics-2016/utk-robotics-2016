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

            # keep track of what white square we are on
            self.white_square = 0

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
            s.move_pid(1, 0, 0)
            time.sleep(5)
            self.move(1, 75, 0)
            time.sleep(.25)

        def strafe_until_white(self):
            # move until we get to the white line
            logger.info("Looking for white")
            self.move(1, -78, 0)
            while s.read_line_sensors()['left'] > self.qtr_threshold:
                # do nothing
                time.sleep(0.01)

            # stop after we detect the line
            logger.info("Found white")
            self.white_square = self.white_square + 1
            s.stop()

        def wait_until_arm_limit_pressed(self):
            while not s.read_arm_limit():
                pass

        def start(self):
            self.move_to_corner()
            logger.info("Done!")

    bot = Robot()
    bot.wait_until_arm_limit_pressed()
    time.sleep(0.5)
    bot.start()
'''
    bot.start()
    while bot.white_square < 3:
        bot.strafe_until_white()
        logger.info("Found the white square #" + str(bot.white_square))
        time.sleep(1)
        if bot.white_square < 3:
            bot.move(1, -78, 0)
            time.sleep(3)
'''
