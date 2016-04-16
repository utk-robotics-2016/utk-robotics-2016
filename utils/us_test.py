# Python modules
# import time
import logging
# import cv2
# import os

# Local modules
from head.spine.core import get_spine
from head.spine.loader import Loader
from head.spine.arm import get_arm
# from head.spine.voltage import get_battery_voltage
# from head.spine.Vec3d import Vec3d
from head.spine.ourlogging import setup_logging

setup_logging(__file__)
logger = logging.getLogger(__name__)

with get_spine() as s:
    with get_arm(s) as arm:
        ldr = Loader(s)

        us = {'right': 0}
        s.move_pid(0.6, 90, 0)
        while us['right'] < 88:
            for pos in ['front_left', 'front_right', 'left', 'right']:
                try:
                    us[pos] = int(round(s.read_ultrasonics(pos, 'cm')))
                except:
                    us[pos] = -99
            print us
        s.stop()
