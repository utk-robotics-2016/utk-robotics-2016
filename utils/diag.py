# Python modules
import time
import logging
import cv2
import os

# Local modules
from head.spine.core import get_spine
from head.spine.loader import Loader
from head.spine.arm import get_arm
from head.spine.voltage import get_battery_voltage
from head.spine.Vec3d import Vec3d
from head.spine.ourlogging import setup_logging

setup_logging(__file__)
logger = logging.getLogger(__name__)

with get_spine() as s:
    with get_arm(s) as arm:
        ldr = Loader(s)

        def test(f, prompt):
            while True:
                print ''
                print '----------------------------'
                print ''
                print("Starting the '%s' test." % (f.__name__))
                print("Prompt will be '%s'." % prompt)
                ans = ''
                while ans not in ['y', 'n']:
                    ans = raw_input("Should we run the '%s' test? (y/n) " % (f.__name__))

                if ans == 'n':
                    return False

                f()
                ans = ''
                while ans not in ['y', 'n', 'rerun']:
                    ans = raw_input("%s (y/n/rerun) " % (prompt))
                if ans == 'y':
                    return False
                if ans == 'n':
                    return False

        def ultrasonics():
            starttime = time.time()
            while (time.time() - starttime) < 15:
                us = {}
                for pos in ['front_left', 'front_right', 'left', 'right']:
                    try:
                        us[pos] = int(round(s.read_ultrasonics(pos, 'cm')))
                    except:
                        us[pos] = -99
                print us
        test(ultrasonics, "Did the ultrasonic sensors appear to work?")

        def loader_flaps():
            ldr.open_flaps()
            time.sleep(2)
            ldr.close_flaps()
            time.sleep(2)
            s.detach_loader_servos()
        test(loader_flaps, "Did the loader flaps open then close?")

        def widen_unwiden():
            ldr.widen(3)
            ldr.widen(1.5)
        test(widen_unwiden, "Did the wings widen and then unwiden?")

        def wings_extend_retract():
            power = 100
            s.set_loader_motor(0, power, 'fw')
            s.set_loader_motor(1, int(power * 3 / 4), 'fw')
            time.sleep(2)
            s.stop_loader_motor(0)
            s.stop_loader_motor(1)
            time.sleep(1)
            s.set_loader_motor(0, int(power * 3 / 4), 'bw')
            s.set_loader_motor(1, power, 'bw')
            time.sleep(4)
            s.stop_loader_motor(0)
            s.stop_loader_motor(1)
        test(wings_extend_retract, "Did the wings extend forward then retract?")

        def arm_move_then_park():
            # right/left, forward, height
            # right side
            arm.move_to(Vec3d(11, -1, 10), 0, 180)
            arm.move_to(Vec3d(0, 10, 10), 0, 180)
            time.sleep(3)
            arm.move_to(Vec3d(0, 10, 10), 3.14 / 6, 180)
            arm.move_to(Vec3d(0, 10, 10), -3.14 / 6, 180)
            arm.move_to(Vec3d(0, 10, 10), 0, 0)
            arm.move_to(Vec3d(0, 10, 10), 0, 180)
            arm.move_to(Vec3d(11, -1, 10), 0, 180)
            arm.park()
        test(arm_move_then_park, "Did the arm move?")

        WHEEL_MOVE_TIME = 2

        def move_fw_bw():
            s.move(0.6, 0, 0)
            time.sleep(WHEEL_MOVE_TIME)
            s.move(0.6, -180, 0)
            time.sleep(WHEEL_MOVE_TIME)
            s.stop()
        test(move_fw_bw, "Did the robot move forward and backward for 4 seconds?")

        def strafe_right_left():
            s.move(0.6, -90, 0)
            time.sleep(WHEEL_MOVE_TIME)
            s.move(0.6, 90, 0)
            time.sleep(WHEEL_MOVE_TIME)
            s.stop()
        test(strafe_right_left, "Did the robot strafe right then left for 4 seconds?")

        def rotate_right_left():
            s.move(0, 0, 0.5)
            time.sleep(WHEEL_MOVE_TIME)
            s.move(0, 0, -0.5)
            time.sleep(WHEEL_MOVE_TIME)
            s.stop()
        test(rotate_right_left, "Did the robot rotate right then left for 4 seconds?")

        def strafe_right_left_pid():
            s.move_pid(0.6, -90, 0)
            time.sleep(WHEEL_MOVE_TIME)
            s.move_pid(0.6, 90, 0)
            time.sleep(WHEEL_MOVE_TIME)
            s.stop()
        test(strafe_right_left_pid, "Did the robot strafe right then left for 4 seconds?")

        def rotate_right_pid():
            s.move_pid(0, 0, 0.5)
            time.sleep(WHEEL_MOVE_TIME)
            s.move_pid(0, 0, -0.5)
            time.sleep(WHEEL_MOVE_TIME)
            s.stop()
        test(rotate_right_pid, "Did the robot rotate right then left for 4 seconds?")

        def line_sensors():
            starttime = time.time()
            while (time.time() - starttime) < 10:
                print s.read_line_sensors()
        test(line_sensors, "Did the line sensors appear to work?")

        def limit_switches():
            starttime = time.time()
            while (time.time() - starttime) < 7:
                print s.read_switches(), s.read_arm_limit()
        test(limit_switches, "Did the limit switches appear to work (fronts are currently off)?")

        def vacuum():
            s.set_suction(True)
            time.sleep(5)
            s.set_suction(False)
            s.set_release_suction(True)
            time.sleep(2)
            s.set_release_suction(False)
        test(vacuum, "Did the suction and release_suction appear to work?")

        def lift_up_down():
            s.set_lift_motor(255, 'ccw')
            time.sleep(1)
            s.set_lift_motor(255, 'cw')
            time.sleep(1)
            s.stop_lift_motor()
        test(lift_up_down, "Did the lift go up and down?")

        def voltage_adc():
            for i in range(5):
                print get_battery_voltage()
        test(voltage_adc, "Does the voltage ADC reading line up with the actual voltage?")

        def disk_usage():
            os.system('df -h | grep -P "Filesystem|rootfs"')
        test(disk_usage, "Does the disk usage look good?")

        def camera():
            camera = cv2.VideoCapture(0)
            retval, img = camera.read()
            if (retval):
                print("Camera is good")
            else:
                print("Camera did not respond, try unplugging and replugging the cable on the camera.")
        test(camera, "Did the camera work?")

        logger.info("Passed!")
