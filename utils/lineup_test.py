# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine
from head.spine.control import trapezoid
# from head.spine.ultrasonic import strafe_at_distance
from head.spine.ultrasonic import ultrasonic_go_to_position
from head.spine.ultrasonic import ultrasonic_rotate_square
# from head.spine.control import trapezoid
from head.spine.loader import Loader
fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.WARNING, datefmt='%I:%M:%S')
# logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
from head.spine.ourlogging import setup_logging

setup_logging(__file__)
logger = logging.getLogger(__name__)

with get_spine() as s:
    
    ultrasonic_go_to_position(s, right=88, unit='cm')
    time.sleep(1)
    
