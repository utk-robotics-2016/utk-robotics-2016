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

        def move_to_corner(self):
            logger.info("Moving out from corner")
            keyframe(s.move_no_mec, (40, 200), 2.5, (0, 0), (200, 30))
            keyframe(s.move_no_mec, (200, 30), 1, (200, 30), (0, 0))
            keyframe(s.move_no_mec, (100, 100), 3, (0, 0), (0, 0))
            # keyframe(s.move_no_mec, (100, 100), 1, (0,0), (0,0))
            # s.move_no_mec(40, 200)
            # time.sleep(1)
            # s.move_no_mec(100, 100)
            # time.sleep(1)
            s.stop()

            '''
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
            '''

        def start(self):
            self.move_to_corner()

            logger.info("Done!")

    bot = Robot()
    bot.start()
