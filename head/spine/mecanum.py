# Most of this taken from http://www.chiefdelphi.com/media/papers/2390
# See Mecanum Programming - Single and double joystick

# For project specific research information, see the mecanum_research
# folder in the head directory.

import math

kf = 1.0
ks = 1.0
kt = 1.0
# wmax = 1 + math.sqrt(2)
wmax = kt + math.sqrt(2) * max(kf, ks)


def w(x, y, z):
    '''Internal use function.'''
    return [
        kf * y + ks * x + kt * z,
        kf * y - ks * x - kt * z,
        kf * y - ks * x + kt * z,
        kf * y + ks * x - kt * z
    ]


def w_from_vectors(speed, direction, angular):
    '''Internal use function.'''
    x = speed * math.cos((90 - direction) * 0.0174532925)
    y = speed * math.sin((90 - direction) * 0.0174532925)
    z = angular
    return w(x, y, z)


def move(speed, direction, angular):
    '''For a given speed, direction, and angular rotation, calculate wheel
    speeds.

    :param speed:
        Speed of translational movement. 1 is full speed, 0 is no speed, -1
        is backwards. You should not exceed an absolute value of 1.
    :type speed: ``float``
    :param direction:
        Direction of translational movement, in degrees. 0 is straight ahead.
        You should also be able to provide -180 or 180 to move backwards.
    :type direction: ``float``
    :param angular:
        Continuous value from -1 to 1 where 0 is no angular rotation at all.
        If 0, the robot's heading will not change while moving.
    :type angular: ``float``
    '''

    # Convert speeds to integers 0 - 255 with direction
    w = w_from_vectors(speed, direction, angular)
    normalized = []
    for s in w:
        if s > 0:
            w_dir = "fw"
        else:
            w_dir = "rv"
        w_speed = int(abs(s / wmax) * 255)
        w_speed = min(w_speed, 255)
        normalized.append((w_speed, w_dir))
    return normalized
