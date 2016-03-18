import time
import math
import logging
from control import keyframe

logger = logging.getLogger(__name__)

# TO BE TESTED
def strafe_at_distance(s, dist, unit, dir, total_time, rampUp=1.0, rampDown=1.0):
    assert dir in ['left', 'right']
    assert unit in ['inch', 'cm']

    middle_time = total_time - rampUp - rampDown
    assert middle_time > 0

    unit_mult = 1.0
    if unit == 'cm':
        unit_mult = 2.54

    if dir == 'left':
        angle = -90
    else:
        angle = 90

    if rampUp:
        keyframe(s.move_pid, (0, angle, 0), (1.0, angle, 0), rampUp)
    else:
        s.move_pid(1.0, angle, 0)

    last_angle = angle

    start_time = time.time()
    current_time = start_time
    while current_time - start_time < middle_time:
        current_dist = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
        delta_dist = dist - current_dist
        if dir == 'left':
            if delta_dist > 1.0 * unit_mult:
                current_angle = angle - 10
            elif delta_dist < 1.0 * unit_mult:
                current_angle = angle + 10
            else:
                current_angle = angle
        else:
            if delta_dist > 1.0 * unit_mult:
                current_angle = angle + 10
            elif delta_dist < 1.0 * unit_mult:
                current_angle = angle - 10
            else:
                current_angle = angle

        if current_angle != last_angle:
            s.move_pid(1.0, current_angle, 0.0)
            last_angle = current_angle

    if rampDown:
        keyframe(s.move_pid, (0.0, angle, 0), (0.0, angle, 0), rampDown)

    s.stop()


# read a sensor some number of times and return the average
def ultrasonic_read_avg(s, sensor, units='cm', readings=5):
    min = 99999
    max = -1
    avg = 0

    # this function is pointless for less than three readings
    assert (readings >= 3)

    # get the readings and determine the average while recording the outliers
    for x in range(readings):
        read = s.read_ultrasonics(sensor, units)
        if read < min:
            min = read
        if read > max:
            max = read
        avg += read

    # return the average without the min/max being included
    return (avg - max - min) / (readings - 2)


# correct rotation using the front left and front right ultraonsic sensors
def ultrasonic_rotate_square(s, tolerance=2.5, again=1):
    # constants
    num_read = 9

    # get averages & difference between sensors
    fl_avg = ultrasonic_read_avg(s, 'front_left', 'cm', num_read)
    fr_avg = ultrasonic_read_avg(s, 'front_right', 'cm', num_read)
    diff = abs(fl_avg - fr_avg)

    print(fl_avg)
    print(fr_avg)
    print(diff)

    while diff > tolerance:
        # robot is angled right
        if fl_avg > fr_avg:
            s.move_pid(0, 0, 0.2)
        # robot is angled left
        else:
            s.move_pid(0, 0, -0.2)

        # get new readings
        fl_avg = ultrasonic_read_avg(s, 'front_left', 'cm', num_read)
        fr_avg = ultrasonic_read_avg(s, 'front_right', 'cm', num_read)
        diff = abs(fl_avg - fr_avg)

        print(fl_avg)
        print(fr_avg)
        print(diff)

    # stop when done
    s.stop()

    if again == 1:
        ultrasonic_rotate_square(s, 1.5, 0)


# TO BE TESTED
# Update December 14 - This function is used in dominate.py. Is that tested
# enough? If not, please test what needs to be tested.
def ultrasonic_go_to_position(s, front=float('inf'), left=float('inf'), right=float('inf'), unit='inch', **kwargs):
    assert unit in ['inch', 'cm']

    # This allows us to strafe at e.g. 85 and -85 rather than 90 and -90 to
    # stay brushed up against a barge for example. Probably a hacky solution,
    # but it works. Andrew, you can fix this up if you would like.
    right_left_dir = kwargs.get('right_left_dir', 90)

    def one_sensor(s, side, target, dir_pos, dir_neg, unit):
        unit_mult = 1.0
        if unit == 'cm':
            unit_mult = 2.54
        threshold = 1.0 * unit_mult
        current = float('inf')
        if(side == 'front'):
            current = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
        else:
            current = s.read_ultrasonics(side, unit)
        while current == float('inf'):
            if(side == 'front'):
                current = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
            else:
                current = s.read_ultrasonics(side, unit)

        delta = (current - target)

        if abs(delta / unit_mult) > 16:
            speed = 1.0 * delta / abs(delta)
        else:
            speed = 0.5 * delta / abs(delta)

        dir = dir_pos
        if speed < 0.0:
            speed = -1.0 * speed
            dir = dir_neg
        if speed > 1.0:
            speed = 1.0

        s.move_pid(speed, dir, 0)
        last_speed = speed

        while(abs(delta) > threshold):
            if(side == 'front'):
                current = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
            else:
                current = s.read_ultrasonics(side, unit)
            while current == float('inf'):
                if(side == 'front'):
                    current = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
                else:
                    current = s.read_ultrasonics(side, unit)
            delta = (current - target)
            logger.debug("Delta: %s Current: %s Target: %s" % (delta, current, target))
            if abs(delta / unit_mult) > 16:
                speed = 1.0 * delta / abs(delta)
            else:
                speed = 0.5 * delta / abs(delta)

            dir = dir_pos
            if speed < 0.0:
                speed = -1.0 * speed
                dir = dir_neg
            if speed > 1.0:
                speed = 1.0
            if speed != last_speed:
                s.move_pid(speed, dir, 0)
                last_speed = speed
        s.stop()

    # TODO: update speed based on distance once values have been tuned in the the one sensor version
    def two_sensors(s, front_target, side, side_target, unit):
        assert side in ['left', 'right']
        unit_mult = 1.0
        if unit == 'cm':
            unit_mult = 2.54
        threshold = 1.0 * unit_mult


        current_front = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
        while current_front == float('inf'):
            current_front = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0

        current_side = s.read_ultrasonics(side, unit)
        while current_side == float('inf')
            current_side = s.read_ultrasonics(side, unit)

        delta_forward = (front_target - current_front)
        delta_side = (side_target - current_side)

        angle = math.degrees(math.atan2(delta_forward, delta_side))
        if(side == 'left'):
            angle = angle + 90.0
        else:
            angle = angle + 180.0

        if angle > 180.0:
            angle = angle - 360.0
        if angle < -180:
            angle = angle + 360.0

        # TODO: speed adjusting
        s.move_pid(1.0, angle, 0)
        while abs(delta_forward) > threshold or abs(delta_side) > threshold:

            angle = math.degrees(math.atan2(delta_forward, delta_side))
            if(side == 'left'):
                angle = angle + 90.0
            else:
                angle = angle + 180.0

            if angle > 180.0:
                angle = angle - 360.0
            if angle < -180:
                angle = angle + 360.0

            # TODO: speed adjusting
            s.move_pid(1.0, angle, 0)
            
            current_front = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
            while current_front == float('inf'):
                current_front = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0

            current_side = s.read_ultrasonics(side, unit)
            while current_side == float('inf')
                current_side = s.read_ultrasonics(side, unit)

            delta_forward = front_target - current_front
            delta_side = side_target - current_side
        s.stop

    # front sensor
    if front != float('inf') and left == float('inf') and right == float('inf'):
        one_sensor(s, 'front', front, 0, 180, unit)

    # front and left sensors
    elif front != float('inf') and left != float('inf') and right == float('inf'):
        two_sensors(s, front, 'left', left, unit)

    # front and right sensors
    elif front != float('inf') and left == float('inf') and right != float('inf'):
        two_sensors(s, front, 'right', right, unit)

    # right sensor
    elif front == float('inf') and left == float('inf') and right != float('inf'):
        one_sensor(s, 'right', right, -right_left_dir, right_left_dir, unit)

    # left sensor
    elif front == float('inf') and left != float('inf') and right == float('inf'):
        one_sensor(s, 'left', left, right_left_dir, -right_left_dir, unit)
