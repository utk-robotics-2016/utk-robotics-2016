import time
import math
from control import keyframe


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


# TO BE TESTED
def ultrasonic_go_to_position(s, front, left, right, unit='inch', p=.1):
    assert unit in ['inch', 'cm']

    def one_sensor(s, side, target, dir_pos, dir_neg, unit):
        unit_mult = 1.0
        if unit == 'cm':
            unit_mult = 2.54
        threshold = 1.0 * unit_mult
        if(side == 'front'):
            current = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
        else:
            current = s.read_ultrasonics(side, unit)

        delta = target - current

        if abs(delta/unit_mult) > 16:
            speed = 1.0 * delta / abs(delta)
        elif abs(delta/unit_mult) > 6:
            speed = 0.5 * delta / abs(delta)
        else:
            speed = 0.25 * delta / abs(delta)
        dir = dir_pos
        if speed < 0.0:
            speed = -1.0*speed
            dir = dir_neg
        if speed > 1.0:
            speed = 1.0

        s.move_pid(speed, dir, 0)
        last_speed = speed

        while(abs(delta) > threshold):
            if(side == 'front'):
                current = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
            else:
                current = s.read_ultrasonics('side', unit)
            delta = target - current
            if abs(delta/unit_mult) > 16:
                speed = 1.0 * delta / abs(delta)
            elif abs(delta/unit_mult) > 6:
                speed = 0.5 * delta / abs(delta)
            else:
                speed = 0.25 * delta / abs(delta)
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

    #TODO: update speed based on distance once values have been tuned in the the one sensor version
    def two_sensors(s, front_target, side, side_target, unit):
        assert side in ['left', 'right']
        unit_mult = 1.0
        if unit == 'cm':
            unit_mult = 2.54
        threshold = 1.0 * unit_mult
        current_front = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
        current_side = s.read_ultrasonics(side, unit)

        delta_forward = front - current_front
        delta_side = side_target - current_side

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
            current_side = s.read_ultrasonics(side, unit)

            delta_forward = front - current_front
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
        one_sensor(s, 'right', right, 90, -90, unit)

    # left sensor
    elif front == float('inf') and left != float('inf') and right == float('inf'):
        one_sensor(s, 'left', left, -90, 90, unit)
