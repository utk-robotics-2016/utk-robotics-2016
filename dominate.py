# Python modules
import time
import logging
import operator

# Local modules
from head.spine.core import get_spine
from head.spine.loader import Loader

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)


def keyframe(f, middleargs, seconds, startargs, endargs):
    ramptime = 1
    if seconds < ramptime * 2:
        ramptime = float(seconds) / 2
    start_time = time.time()
    start_difference = map(operator.sub, middleargs, startargs)
    end_difference = map(operator.sub, endargs, middleargs)
    curr_time = time.time()
    iters = 0
    while (curr_time - start_time) < seconds:
        elapsed = curr_time - start_time
        if elapsed < ramptime:
            fraction = elapsed / ramptime
            toadd = [v * fraction for v in start_difference]
            currargs = map(operator.add, startargs, toadd)
        elif elapsed > (seconds - ramptime):
            fraction = (elapsed - (seconds - ramptime)) / ramptime
            toadd = [v * fraction for v in end_difference]
            currargs = map(operator.add, middleargs, toadd)
        else:
            currargs = middleargs
        f(*currargs)
        curr_time = time.time()
        iters += 1
    logger.info("Keyframe iterations: %d", iters)
    f(*endargs)

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

        def move_pid(self, speed, dir, angle):
            s.move_pid(speed, self.dir_mod * dir, self.dir_mod * angle)

        # moves with respect to the course layout
        def move(self, speed, dir, angle):
            s.move(speed, self.dir_mod * dir, self.dir_mod * angle)

        def move_to_corner(self):
            keyframe(self.move_pid, (1, 0, 0), 6, (0, 0, 0), (1, 0, 0))
            self.move(1, 75, 0)
            time.sleep(.375)

        def strafe_until_white(self):
            # move until we get to the white line
            logger.info("Looking for white")
            self.move_pid(1, -90, 0)
            if self.course == "B":
                while s.read_line_sensors()['left'] > self.qtr_threshold:
                    # do nothing
                    time.sleep(0.01)
            else:
                while s.read_line_sensors()['right'] > self.qtr_threshold:
                    time.sleep(0.01)
            # stop after we detect the line
            logger.info("Found white")
            self.white_square = self.white_square + 1
            s.stop()

        def strafe_until_black(self):
            self.move_pid(1, -90, 0)
            if self.course == "B":
                while s.read_line_sensors()['left'] < self.qtr_threshold:
                    time.sleep(0.01)
            else:
                while s.read_line_sensors()['right'] < self.qtr_threshold:
                    time.sleep(0.01)
            s.stop()

        def wait_until_arm_limit_pressed(self):
            while not s.read_arm_limit():
                pass

        def start(self):
            self.move_to_corner()
            logger.info("Done!")

    bot = Robot()

    #    bot.wait_until_arm_limit_pressed()
    time.sleep(0.5)
    bot.start()

    bot.move_pid(1, -135, -.1)
    time.sleep(0.25)

    for i in range(2):
        bot.strafe_until_white()
        bot.strafe_until_black()
    bot.strafe_until_white()

    keyframe(bot.move_pid, (1, -180, 0), 4, (0, -180, 0), (0, -180, 0))
    bot.move_pid(0, 0, 1)
    time.sleep(2)
    s.stop()
    keyframe(bot.move_pid, (.5, 0, 0), 3, (0, 0, 0), (0, 0, 0))
    s.stop()
