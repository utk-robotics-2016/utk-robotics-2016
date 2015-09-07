# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine
from head.spine.loader import Loader
from head.spine.arm import get_arm
from head.spine.Vec3d import Vec3d

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
# logging.basicConfig(format=fmt, level=logging.WARNING, datefmt='%I:%M:%S')
logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    with get_arm(s) as arm:
        def test(f, prompt):
            print ''
            print '----------------------------'
            print ''
            print("Starting the '%s' test." % (f.__name__))
            print("Prompt will be '%s'." % prompt)
            ans = ''
            while ans not in ['y','n']:
                ans = raw_input("Should we run the '%s' test? (y/n) " % (f.__name__))

            if ans == 'n':
                return False

            f()
            ans = ''
            while ans not in ['y','n']:
                ans = raw_input("%s (y/n) " % (prompt))
            if ans == 'y':
                return False
            return False

        def arm_move_then_park():
            # right/left, forward, height
            # right side
            arm.move_to(Vec3d(3, 10, 14), 0, 180)
            time.sleep(5)
            # arm.move_to(Vec3d(0, 15, 3), -20, 180)
            # time.sleep(2)
            # arm.move_to(Vec3d(0, 15, 3), -20, 180)
            # time.sleep(2)
            # arm.move_to(Vec3d(0, 15, 3), -20, 180)
            # time.sleep(2)
            # arm.move_to(Vec3d(0, 10, 3), -20, 180)
            # time.sleep(2)
            # arm.move_to(Vec3d(0, 5, 3), -20, 180)
            # time.sleep(2)
            arm.park()
        test(arm_move_then_park, "Did the arm move?")

        def move_forward():
            s.move(0.6, 0, 0)
            time.sleep(5)
            s.stop()
        test(move_forward, "Did the robot move forward for 5 seconds?")

        def move_backward():
            s.move(0.6, -180, 0)
            time.sleep(5)
            s.stop()
        test(move_backward, "Did the robot move backward for 5 seconds?")

        logger.info("Passed!")
