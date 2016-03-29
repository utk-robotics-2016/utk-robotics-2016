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
logger = logging.getLogger(__name__)

with get_spine() as s:
    
    ultrasonic_go_to_position(s, front=26, unit='cm', rot=-.055)
    time.sleep(1)
    
    ultrasonic_go_to_position(s, front=50, unit='cm', rot=-.02)
    time.sleep(1)

    trapezoid(s.move_pid, (0, -175, .02), (.6, -175, .02), (0, -175, .02), 1.2)
    time.sleep(1)

    trapezoid(s.move_pid, (0, 0, .01), (.6, 0, .01), (0, 0, .01), 2.0)
    time.sleep(1)

    ultrasonic_go_to_position(s, front=26, unit='cm', rot=.01)
    time.sleep(1)
     
    ultrasonic_go_to_position(s, front=5, unit='cm')

#    ultrasonic_go_to_position(s, left=12, unit='cm')
#    time.sleep(1)
    #ultrasonic_go_to_position(s, front=88, unit='cm', rot=-.025)
    '''
    time.sleep(1)
    ultrasonic_go_to_position(s, front=65, unit='cm')
    time.sleep(1)
    ultrasonic_go_to_position(s, front=36, unit='cm')
    time.sleep(1)
    ultrasonic_go_to_position(s, front=11, unit='cm')
    '''
