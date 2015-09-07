# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine
from head.spine.loader import Loader
from head.spine.arm import get_arm
from head.spine.voltage import get_battery_voltage
from head.spine.Vec3d import Vec3d

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.WARNING, datefmt='%I:%M:%S')
# logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    with get_arm(s) as arm:
        def test(f, prompt):
            while True:
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
                while ans not in ['y','n','rerun']:
                    ans = raw_input("%s (y/n/rerun) " % (prompt))
                if ans == 'y':
                    return False
                if ans == 'n':
                    return False

        def arm_move_then_park():
            # right/left, forward, height
            # right side
            arm.move_to(Vec3d(0, 10, 0), 0, 180)
            time.sleep(3)
            arm.move_to(Vec3d(0, 10, 0), 3.14/6, 180)
            arm.move_to(Vec3d(0, 10, 0), -3.14/6, 180)
            arm.move_to(Vec3d(0, 10, 0), 0, 0)
            arm.move_to(Vec3d(0, 10, 0), 0, 180)
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

        def line_sensors():
            starttime = time.time()
            while (time.time() - starttime) < 5:
                print s.read_line_sensors()
        test(line_sensors, "Did the line sensors appear to work?")

        def limit_switches():
            starttime = time.time()
            while (time.time() - starttime) < 7:
                print s.read_limit_switches(), s.read_arm_limit()
        test(limit_switches, "Did the limit switches appear to work?")

        def vacuum():
            s.set_suction(True)
            time.sleep(5)
            s.set_suction(False)
            s.set_release_suction(True)
            time.sleep(5)
            s.set_release_suction(False)
        test(vacuum, "Did the suction and release_suction appear to work?")

        def voltage_adc():
            for i in range(5):
                print get_battery_voltage()
        test(voltage_adc, "Does the voltage ADC reading line up with the actual voltage?")

        logger.info("Passed!")
