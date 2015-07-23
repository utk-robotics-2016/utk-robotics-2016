# Most of this taken from http://www.chiefdelphi.com/media/papers/2390
# See Mecanum Programming - Single and double joystick

# For project specific research information, see the mecanum_research
# folder in the head directory.

import math

kf = 1.0
ks = 1.0
kt = 1.0
#wmax = 1 + math.sqrt(2)
wmax = kt + math.sqrt(2) * max(kf, ks)


def w(x, y, z):
    return [
        kf * y + ks * x + kt * z,
        kf * y - ks * x - kt * z,
        kf * y - ks * x + kt * z,
        kf * y + ks * x - kt * z
    ]


def w_from_vectors(speed, direction, angular):
    x = speed * math.cos((90 - direction) * 0.0174532925)
    y = speed * math.sin((90 - direction) * 0.0174532925)
    z = angular
    return w(x, y, z)


def move(speed, direction, angular):
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
