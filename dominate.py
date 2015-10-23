# Python modules
import time
import logging
import operator

# Local modules
from head.spine.core import get_spine
from head.spine.arm import get_arm
from head.spine.block_picking import BlockPicker
from head.spine.loader import Loader

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
# logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logging.basicConfig(format=fmt, level=logging.INFO, datefmt='%I:%M:%S')
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
    with get_arm(s) as arm:
        class Robot:

            def __init__(self):
                self.ldr = Loader(s)
                self.bp = BlockPicker(s, arm)

                # set a threshold for white vs black values from the QTR sensor
                self.qtr_threshold = 800

                # Determine which course layout
                if s.read_switches()['course_mirror'] == 1:
                    # tunnel on left
                    self.course = 'B'
                    # dir_mod stands for direction modifier
                    self.dir_mod = 1
                else:
                    # tunnel on right
                    self.course = 'A'
                    self.dir_mod = -1

            def move_pid(self, speed, dir, angle):
                s.move_pid(speed, self.dir_mod * dir, self.dir_mod * angle)

            # moves with respect to the course layout
            def move(self, speed, dir, angle):
                s.move(speed, self.dir_mod * dir, self.dir_mod * angle)

            def move_to_corner(self):
                keyframe(self.move_pid, (1, 0, 0), 6, (0, 0, 0), (1, 0, 0))
                # move back a smidgen
                self.move(.75, 180, 0)
                time.sleep(.1)
                self.move(1, 75, 0)
                time.sleep(.375)

            def bump_forward(self, bumptime=0.2):
                self.move(1, 0, 0)
                time.sleep(bumptime)
                s.stop()

            # These two functions could be combined into one. Code duplication
            def strafe_until_white(self):
                self.move_pid(1, -85, 0)
                if self.course == "B":
                    while s.read_line_sensors()['left'] > self.qtr_threshold:
                        time.sleep(0.01)
                else:
                    while s.read_line_sensors()['right'] > self.qtr_threshold:
                        time.sleep(0.01)
                # This function does not stop the movement after returning!!

            def strafe_until_black(self):
                self.move_pid(1, -85, 0)
                if self.course == "B":
                    while s.read_line_sensors()['left'] < self.qtr_threshold:
                        time.sleep(0.01)
                else:
                    while s.read_line_sensors()['right'] < self.qtr_threshold:
                        time.sleep(0.01)
                # This function does not stop the movement after returning!!

            def wait_until_arm_limit_pressed(self):
                logging.info("Waiting for arm limit press.")
                while not s.read_arm_limit():
                    pass

            def move_to_rail_zone(self, currzone, destzone, method='deadreckon'):
                if method == 'manual':
                    raw_input('Move me to zone %d' % (destzone))
                elif method == 'deadreckon':
                    if currzone == 3 and destzone == 0:
                        # Bump up against barge
                        s.move_for(5, 0.8, 0, 0.08)
                        # Bump against railroad
                        s.move_for(1, 0.6, -70, 0)
                        # Move away from railroad
                        s.move_for(1, 0.6, 70, 0)
                    elif currzone != -1:
                        keyframe(self.move_pid, (0.5, 180, 0), 2.8, (0, 180, 0), (0, 180, 0))
                        s.stop()
                else:
                    raise ValueError

            def detect_blocks(self, level):
                # logger.info(arm.detect_blocks('top'))
                # '''
                blocks = []
                if level == 'bottom':
                    # Far right
                    blocks.append([{'color': 'blue', 'type': 'full'}])
                    blocks.append([{'color': 'red', 'type': 'full'}])
                    blocks.append([{'color': 'yellow', 'type': 'full'}])
                    blocks.append([{'color': 'green', 'type': 'full'}])
                    blocks.append([{'color': 'red', 'type': 'full'}])
                    blocks.append([{'color': 'blue', 'type': 'full'}])
                    blocks.append([{'color': 'green', 'type': 'full'}])
                    blocks.append([{'color': 'green', 'type': 'full'}])
                    # Far left
                elif level == 'top':
                    # Far right
                    blocks.append([{'color': 'green', 'type': 'full'}])
                    blocks.append([{'color': 'yellow', 'type': 'full'}])
                    blocks.append([{'color': 'yellow', 'type': 'full'}])
                    blocks.append([{'color': 'blue', 'type': 'full'}])
                    blocks.append([{'color': 'blue', 'type': 'full'}])
                    blocks.append([{'color': 'red', 'type': 'full'}])
                    blocks.append([{'color': 'yellow', 'type': 'full'}])
                    blocks.append([{'color': 'red', 'type': 'full'}])
                    # Far left
                else:
                    raise ValueError
                # '''
                return blocks

            def get_rail_zone_color(self, zid):
                return ['yellow', 'blue', 'red', 'green'][zid]

            def unload_rail(self):
                lastzid = -1
                # for level in ['top', 'bottom']:
                for level in ['top']:
                    blocks = self.detect_blocks(level)
                    for b in blocks:
                        assert b[0]['type'] == 'full'
                    for zid in range(4):
                        self.move_to_rail_zone(lastzid, zid)
                        color = self.get_rail_zone_color(zid)
                        indices = []
                        for i, b in enumerate(blocks):
                            if b[0]['color'] == color:
                                indices.append(i)
                        logging.info('%s blocks at %s.' % (color, indices))
                        for i in indices:
                            self.bp.pick_block(i, level, 'full')
                            side = {'B': 'right', 'A': 'left'}[self.course]
                            self.bp.drop_block(rail=True, side=side)
                        lastzid = zid

            def start(self):
                # '''
                self.move_to_corner()
                logger.info("Done!")

                # self.move_pid(1, -135, -.1)
                # time.sleep(0.15)

                # LOAD SEA BLOCKS
                self.strafe_until_white()
                s.stop()
                self.bump_forward()
                self.wait_until_arm_limit_pressed()

                # UNLOAD SEA BLOCKS
                self.strafe_until_black()
                self.strafe_until_white()
                self.strafe_until_black()
                self.strafe_until_white()
                s.stop()
                time.sleep(0.5)
                # back away from the rail zone
                self.move(1, 80, 0)
                time.sleep(0.275)
                s.stop()
                # Move to sea zone
                keyframe(self.move_pid, (1, -180, 0), 4, (0, -180, 0), (0, -180, 0))
                self.move_pid(0, 0, 1)
                time.sleep(2.1)
                s.stop()
                keyframe(self.move_pid, (.5, 0, 0), 3, (0, 0, 0), (0, 0, 0))
                s.stop()
                self.wait_until_arm_limit_pressed()

                # LOAD RAIL BLOCKS
                # Move from sea zone
                keyframe(self.move_pid, (1, -180, 0), 4, (0, -180, 0), (0, -180, 0))
                self.move_pid(0, 0, 1)
                time.sleep(2.1)
                s.stop()
                keyframe(self.move_pid, (.7, 0, 0), 3, (0, 0, 0), (0, 0, 0))
                # self.bump_forward(bumptime=0.375)
                s.stop()
                # Move closer to rail zone
                self.move(1, -80, 0)
                time.sleep(0.31)
                s.stop()
                self.wait_until_arm_limit_pressed()
                time.sleep(1)
                # '''

                # UNLOAD RAIL BLOCKS
                self.unload_rail()

        bot = Robot()

        bot.wait_until_arm_limit_pressed()
        time.sleep(0.5)
        bot.start()
