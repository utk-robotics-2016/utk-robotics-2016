# Python modules
import time
import logging
import itertools
import cv2

# Local modules
from head.spine.core import get_spine
from head.spine.arm import get_arm
from head.spine.rail_sorting import RailSorter
from head.spine.loader import Loader
from head.spine.control import trapezoid
from head.spine.Vec3d import Vec3d
from head.spine.ultrasonic import ultrasonic_go_to_position
# from head.spine.ultrasonic import ultrasonic_rotate_square
from head.spine.ourlogging import setup_logging
from head.imaging.railorder import railorder

setup_logging(__file__)
logger = logging.getLogger(__name__)


with get_spine() as s:
    with get_arm(s) as arm:
        class Robot:

            def __init__(self):
                # Determine which course layout
                if s.read_switches()['course_mirror'] == 1:
                    # tunnel on left
                    self.course = 'B'
                    self.dir_mod = 1
                else:
                    # tunnel on right
                    self.course = 'A'
                    self.dir_mod = -1
                logging.info("Using course id '%s' and dir_mod '%d'." % (self.course, self.dir_mod))

            def arm_to_vertical(self):
                arm.move_to(Vec3d(11, -4, 10), 1.3, 180)
                if self.course == 'A':
                    arm.move_to(Vec3d(-11, -4, 10), 1.3, 180)
                time.sleep(1)
                
            def park_arm(self):
                arm.move_to(Vec3d(11, -4, 10), 1.3, 180)
                arm.park()

            def start(self):
                self.arm_to_vertical()
                binStuff = railorder(self.course)
                bin_order = binStuff.get_rail_order(self.course)
                print(bin_order)
                self.park_arm()
                

        bot = Robot()

        bot.start()
