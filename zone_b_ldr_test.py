# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine
from head.spine.arm import get_arm
from head.spine.block_picking import BlockPicker
from head.spine.loader import Loader
from head.spine.control import trapezoid
from head.spine.Vec3d import Vec3d

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
# logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logging.basicConfig(format=fmt, level=logging.INFO, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)


with get_spine() as s:
    with get_arm(s) as arm:
        class Robot:

            def __init__(self):
                self.ldr = Loader(s)
                self.bp = BlockPicker(s, arm)

                # flag to determine if the loader is enabled
                # this allows for a pure navigational run when set to False
                self.use_loader = False

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
                logging.info("Using course id '%s' and dir_mod '%d'." % (self.course, self.dir_mod))

                # Initialize before button press
                # self.ldr.initial_zero_lift()
                # self.ldr.lift(2)
                # arm.move_to(Vec3d(11, -1, 10), 0, 180)
                # self.ldr.widen(0.1)
                # arm.park()

            def move_pid(self, speed, dir, angle):
                s.move_pid(speed, self.dir_mod * dir, self.dir_mod * angle)

            # moves with respect to the course layout
            def move(self, speed, dir, angle):
                s.move(speed, self.dir_mod * dir, self.dir_mod * angle)

            # rotate the orientation of the robot by 180 degrees
            def rotate_180(self):
                trapezoid(s.move_pid, (0, 0, 0), (0, 0, 1), (0, 0, 0), 1.74, rampuptime=.7, rampdowntime=1)

            # rotate the orientation of the robot by 90 degrees
            def rotate_90(self, dir):
                if dir == 'right':
                    angle = 0.5
                elif dir == 'left':
                    angle = -0.5
                else:
                    raise ValueError

                trapezoid(s.move_pid, (0, 0, 0), (0, 0, angle), (0, 0, 0), 1.74, rampuptime=.7, rampdowntime=1)

            def move_to_corner(self):
                trapezoid(self.move_pid, (0, 0, 0), (1, 0, 0), (1, 0, 0), 3.8)
                self.move(0.9, -10, 0)
                time.sleep(4)
                s.stop()

                # move back a smidgen
                self.move_pid(.75, 180, 0)
                time.sleep(.1)
                self.move(1, 90, 0)
                time.sleep(1)

            def detect_line(self, color, sensor):
                if color == 'black':
                    return s.read_line_sensors()[sensor] < self.qtr_threshold
                elif color == 'white':
                    return s.read_line_sensors()[sensor] > self.qtr_threshold
                else:
                    raise ValueError

            def strafe_until_line_abs(self, color, dir, sensor='auto'):
                # determine movement and sensor
                if dir == 'left':
                    angle = 90
                elif dir == 'right':
                    angle = -90
                else:
                    raise ValueError

                if sensor == 'auto':
                    if self.course == 'B':
                        sensor = 'left'
                    else:
                        sensor = 'right'

                    if self.course == 'A':
                        sensor = 'right'
                    else:
                        sensor = 'left'

                # start moving
                s.move_pid(0.6, angle, 0)

                # read the line sensor and stop when desired color is detected
                while self.detect_line(color, sensor):
                    time.sleep(0.01)
                # This function does not stop the movement after returning!

            def strafe_until_line(self, color, dir, sensor):
                # flip stuff for course A
                if self.course == 'A':
                    if dir == 'left':
                        dir = 'right'
                    elif dir == 'right':
                        dir = 'left'

                    if sensor == 'left':
                        sensor = 'right'
                    elif sensor == 'right':
                        sensor = 'left'

                # call the actual strafe function
                self.strafe_until_line_abs(color, dir, sensor)

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
                        trapezoid(self.move_pid, (0, 180, 0), (0.5, 180, 0), (0, 180, 0), 2.8)
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
                # forward forward and over to the line
                trapezoid(self.move_pid, (0, 0, 0), (0.8, 0, 0), (0, 0, 0), 1.0)
                self.strafe_until_line('white', 'right', 'left')
                s.stop()

                # move forward to zone B
                trapezoid(s.move_pid, (0, -5, 0), (1, -5, 0), (0, -5, 0), 5.6)
                self.ldr.open_flaps()

                # align at zone B
                self.strafe_until_line_abs('black', 'left', 'left')
                trapezoid(s.move_pid, (0, -90, 0), (0.65, -90, 0), (0, -90, 0), 1.15)

                # pick up the blocks in zone b
                # TODO #
                logging.info("Picking up zone B blocks")
                time.sleep(0.5)
                self.ldr.load(strafe_dir={'B': 'right', 'A': 'left'}[self.course])
                


        bot = Robot()

        bot.wait_until_arm_limit_pressed()
        time.sleep(0.5)
        bot.start()
