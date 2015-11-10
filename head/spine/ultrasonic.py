import math


def ultrasonic_go_to_position(s, front, left, right, unit='inch', p=.1):
    assert unit in ['inch', 'cm']
    if front != float('inf') and left == float('inf') and right == float('inf'):
        threshold = 1.0
        if unit == 'cm':
            threshold = 2.54
        curr_front = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
        delta_front = front - curr_front
        speed = delta_front * p
        dir = 0
        if speed < 0.0:
            speed = -1.0*speed
            dir = 1
        if speed > 1.0:
            speed = 1.0
        s.move_pid(speed, 180*dir, 0)
        while(abs(delta_front) > threshold):
            curr_front = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
            delta_front = front - curr_front
            speed = delta_front*p
            dir = 0
            if speed < 0.0:
                speed = -1.0*speed
                dir = 1
            if speed > 1.0:
                speed = 1.0
            s.move_pid(speed, 180*dir, 0)
        s.stop()

    elif front != float('inf') and left != float('inf') and right == float('inf'):
        curr_front = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
        curr_left = s.read_ultrasonics('left', unit)

        delta_forward = front - curr_front
        delta_left = left - curr_left

        if unit == 'inch':
            threshold = 1.0
        if unit == 'cm':
            threshold = 2.54

        angle = math.degrees(math.atan2(delta_forward, delta_left)) + 90.0
        if angle > 180.0:
            angle = angle - 360.0
        if angle < -180:
            angle = angle + 360.0
        s.move_pid(1.0, angle, 0)

        while abs(delta_forward) > threshold or abs(delta_left) > threshold:
            angle = math.degrees(math.atan2(delta_forward, delta_left)) + 90.0
            if angle > 180.0:
                angle = angle - 360.0
            if angle < -180:
                angle = angle + 360.0
            s.move_pid(1.0, angle, 0)
            curr_front = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
            curr_left = s.read_ultrasonics('left', unit)

            delta_forward = front - curr_front
            delta_left = left - curr_left
        s.stop

    elif front != float('inf') and left == float('inf') and right != float('inf'):
        curr_front = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
        curr_right = s.read_ultrasonics('right', unit)

        delta_forward = front - curr_front
        delta_right = right - curr_right

        if unit == 'inch':
            threshold = 1.0
        if unit == 'cm':
            threshold = 2.54

        angle = math.degrees(math.atan2(delta_forward, delta_right)) + 180.0
        if angle > 180.0:
            angle = angle - 360.0
        if angle < -180:
            angle = angle + 360.0
        s.move_pid(1.0, angle, 0)

        while abs(delta_forward) > threshold or abs(delta_right) > threshold:
            angle = math.degrees(math.atan2(delta_forward, delta_right)) + 180.0
            if angle > 180.0:
                angle = angle - 360.0
            if angle < -180:
                angle = angle + 360.0
            s.move_pid(1.0, angle, 0)
            curr_front = (s.read_ultrasonics('front_left', unit) + s.read_ultrasonics('front_right', unit)) / 2.0
            curr_right = s.read_ultrasonics('right', unit)

            delta_forward = front - curr_front
            delta_right = right - curr_right
        s.stop()

    elif front == float('inf') and left == float('inf') and right != float('inf'):
        threshold = 1.0
        if unit == 'cm':
            threshold = 2.54
        curr_right = s.read_ultrasonics('right', unit)
        delta_right = right - curr_right
        speed = delta_right*p
        dir = 1
        if speed < 0.0:
            speed = -1.0*speed
            dir = -1
        if speed > 1.0:
            speed = 1.0
        s.move_pid(speed, 90*dir, 0)
        while(abs(delta_right) > threshold):
            curr_right = s.read_ultrasonics('right', unit)
            delta_right = right - curr_right
            speed = delta_right*p
            dir = 1
            if speed < 0.0:
                speed = -1.0*speed
                dir = -1
            if speed > 1.0:
                speed = 1.0
            s.move_pid(speed, 90*dir, 0)
        s.stop()

    elif front == float('inf') and left != float('inf') and right == float('inf'):
        threshold = 1.0
        if unit == 'cm':
            threshold = 2.54
        curr_left = s.read_ultrasonics('left', unit)
        delta_left = left - curr_left
        speed = delta_left*p
        dir = 1
        if speed < 0.0:
            speed = -1.0*speed
            dir = -1
        if speed > 1.0:
            speed = 1.0
        s.move_pid(speed, -90*dir, 0)
        while(abs(delta_left) > threshold):
            curr_left = s.read_ultrasonics('left', unit)
            delta_left = left - curr_left
            speed = delta_left*p
            dir = 1
            if speed < 0.0:
                speed = -1.0*speed
                dir = -1
            if speed > 1.0:
                speed = 1.0
            s.move_pid(speed, -90*dir, 0)
        s.stop()
