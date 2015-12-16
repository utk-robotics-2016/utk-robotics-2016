# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine
# from head.spine.control import keyframe
# from head.spine.ultrasonic import strafe_at_distance
from head.spine.ultrasonic import ultrasonic_go_to_position
from head.spine.control import trapezoid
fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.WARNING, datefmt='%I:%M:%S')
# logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    trapezoid(s.move_pid, (0, 0, 0), (1, 0, 0), (1, 0, 0), 3.1)
    ultrasonic_go_to_position(s, 7, float('inf'), float('inf'), 'cm', 0.2)
    s.move_pid(.75, 45, 0)
    time.sleep(.3)
    s.stop()
