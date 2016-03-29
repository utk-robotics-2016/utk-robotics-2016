# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine
# from head.spine.control import keyframe
# from head.spine.ultrasonic import strafe_at_distance
from head.spine.ultrasonic import ultrasonic_go_to_position
from head.spine.ultrasonic import ultrasonic_rotate_square
# from head.spine.control import trapezoid
from head.spine.loader import Loader
fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.WARNING, datefmt='%I:%M:%S')
# logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    #s.move_pid(1.0,0.0,0.0)
    time.sleep(1)
    ultrasonic_go_to_position(s, front=11, unit='cm')
    time.sleep(1)
    ultrasonic_go_to_position(s, left=12, unit='cm')
    time.sleep(1)
    ultrasonic_go_to_position(s, front=36, unit='cm')
    time.sleep(1)
    ultrasonic_go_to_position(s, left=12, unit='cm')
    time.sleep(1)
    ultrasonic_go_to_position(s, front=65, unit='cm')
    time.sleep(1)
    ultrasonic_go_to_position(s, left=12, unit='cm')
    time.sleep(1)
    ultrasonic_go_to_position(s, front=88, unit='cm')
    '''
    time.sleep(1)
    ultrasonic_go_to_position(s, front=65, unit='cm')
    time.sleep(1)
    ultrasonic_go_to_position(s, front=36, unit='cm')
    time.sleep(1)
    ultrasonic_go_to_position(s, front=11, unit='cm')
    '''
