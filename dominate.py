# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine
from head.spine.arm import get_arm
from head.spine.rail_sorting import RailSorter
from head.spine.loader import Loader
from head.spine.control import trapezoid
from head.spine.Vec3d import Vec3d
from head.spine.ultrasonic import ultrasonic_go_to_position, ultrasonic_rotate_square
from head.spine.ourlogging import setup_logging
from head.imaging.railorder import railorder

setup_logging(__file__)
logger = logging.getLogger(__name__)


with get_spine() as s:
    with get_arm(s) as arm:
        class Robot:

            def __init__(self):
                self.ldr = Loader(s)
                self.rs = RailSorter(s, arm)

                # flag to determine if the loader is enabled
                # this allows for a pure navigational run when set to False
                self.use_loader = True

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
                self.ldr.initial_zero_lift()
                self.ldr.lift(1.9)
                arm.move_to(Vec3d(11, -1, 10), 0, 180)
                self.ldr.widen(0.1)
                arm.park()

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

            def detect_line(self, color, sensor):
                if color == 'black':
                    return s.read_line_sensors()[sensor] < self.qtr_threshold
                elif color == 'white':
                    return s.read_line_sensors()[sensor] > self.qtr_threshold
                else:
                    raise ValueError

            def strafe_until_line_abs(self, color, dir, sensor):
                # determine movement and sensor
                if dir == 'left':
                    angle = 90
                elif dir == 'right':
                    angle = -90
                else:
                    raise ValueError

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
                    time.sleep(0.1)

            # Procedure to navigate from the start area through the tunnel to near Zone A
            def move_to_corner(self):
                # advance through the tunnel
                trapezoid(s.move_pid, (0, -5, 0), (1, -5, 0), (1, -5, 0), 3.0)

                # open loader flaps before impacting the barge
                self.ldr.open_flaps()

                # approach the barge
                trapezoid(s.move_pid, (1, -5, 0), (1, -5, 0), (0, -5, 0), 3.0)

            def align_zone_b(self):

                # back up from the white squares
                trapezoid(s.move_pid, (0, 180, 0), (1, 180, 0), (0, 0, 0), 1.75)

                # strafe to the center white line
                self.strafe_until_line("white", "right", "left")

                # move forward to the barge
                trapezoid(s.move_pid, (0, 0, 0), (1, 0, 0), (0, 0, 0), 3.0)

                # ultrasonic alignment prior to calling the load function
                dist = 88.0
                if self.course == 'A':
                    ultrasonic_go_to_position(s, left=dist, unit='cm')
                else:
                    ultrasonic_go_to_position(s, right=dist, unit='cm')

                s.move_pid(1, 0, 0)
                time.sleep(1)
                s.move_pid(1, 0, .3)
                time.sleep(1)
                s.move_pid(1, 0, -.3)
                time.sleep(1)
                s.stop()
                # trapezoid(s.move, (0, 0, 0), (1, 0, 0), (0, 0, 0), 1.5)
                # trapezoid(s.move, (0, 180, 0), (.65, 180, 0), (0, 180, 0), 0.5)
                # trapezoid(s.move, (0, 0, 0), (1, 0, 0), (0, 0, 0), 3)

            def arm_to_vertical(self):
                arm.move_to(Vec3d(11, -4, 10), 1.3, 180)
                if self.course == 'A':
                    arm.move_to(Vec3d(-11, -4, 10), 1.3, 180)
                time.sleep(1)

            def go_to_rail_cars(self):

                # back up from the barge zone
                trapezoid(s.move_pid, (0, 180, 0), (1, 180, 0), (0, 0, 0), 1.75)

                dist = 18.0
                if self.course == 'A':
                    ultrasonic_go_to_position(s, left=dist, unit='cm')
                else:
                    ultrasonic_go_to_position(s, right=dist, unit='cm')

                # move forward to the barge to square up
                trapezoid(s.move_pid, (0, 0, 0), (1, 0, 0), (0, 0, 0), 4.0)

                # back up slightly
                trapezoid(s.move_pid, (0, 180, 0), (.6, 180, 0), (0, 180, 0), 0.3)

                self.ldr.initial_zero_lift()

            def start(self):
                # Moves from start square to corner near Zone A
                self.move_to_corner()
                logger.info("In corner")

                self.arm_to_vertical()
                logger.info( "Attempting to determine bin order" )
                binStuff = railorder(self.course)
                bin_order = binStuff.get_rail_order(self.course)
                print( bin_order )
                # Give the rail sorter the bins in the correct order
                self.rs.set_rail_zone_bins( list( reversed( bin_order ) ) )
                arm.park()

                # Move to Zone B from the corner
                self.align_zone_b()
                logger.info("At zone B")

                # Set proper lift height
                self.ldr.lift(4.8)

                # Load the blocks from zone B
                if self.use_loader is True:
                    self.ldr.load(strafe_dir={'B': 'right', 'A': 'left'}[self.course])

                self.go_to_rail_cars()
                # I took a picture of everything that happens up to this point

                self.rs.unload_rail(self.course)

                # Load at Zone B
                # if self.use_loader is True:
                #    self.ldr.load(strafe_dir={'B': 'right', 'A': 'left'}[self.course])

                # LOAD SEA BLOCKS
                # self.align_zone_a()
                # logger.info("At zone A")
                # note: the life is already set to the correct height for Zone A (1.9)
                # if self.use_loader is True:
                #    self.ldr.load(strafe_dir={'B': 'right', 'A': 'left'}[self.course])

                # move from zone A to the sea zone
                # self.zone_a_to_sea_zone()

                # unload blocks
                # logging.info("Unloading at sea zone")
                # if self.use_loader is True:
                #    self.ldr.dump_blocks()

                # move from the sea zone to zone B
                # self.sea_zone_to_zone_b()

                # pick up the blocks in zone b
                # logging.info("Picking up zone B blocks")
                # Lift to proper loading height for rail blocks.
                # self.ldr.lift(4.875)
                # if self.use_loader is True:
                #    self.ldr.load(strafe_dir={'B': 'right', 'A': 'left'}[self.course])

                # move to the rail zone
                # logging.info("Moving to rail zone")
                # self.zone_b_to_rail_zone()

                # sort and unload blocks into bins in rail zone
                # TODO #
                # logging.info("At rail zone")

        bot = Robot()

        bot.wait_until_arm_limit_pressed()
        time.sleep(0.5)
        bot.start()
