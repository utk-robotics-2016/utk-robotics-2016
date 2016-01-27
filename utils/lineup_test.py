# Python modules
# import time
import logging

# Local modules
from head.spine.core import get_spine
# from head.spine.control import keyframe
# from head.spine.ultrasonic import strafe_at_distance
# from head.spine.ultrasonic import ultrasonic_go_to_position
# from head.spine.control import trapezoid
from head.spine.loader import Loader
fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.WARNING, datefmt='%I:%M:%S')
# logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    loader = Loader(s)
    while 1:
        print s.read_ultrasonics("right", "cm")
#    ultrasonic_go_to_position(s, left=26, unit='cm', right_left_dir=85)
#    s.stop()
#    ultrasonic_go_to_position(s,left=36,unit="cm",right_left_dir=85)
