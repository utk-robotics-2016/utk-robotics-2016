# Python modules
# import time
import logging

# Local modules
from head.spine.core import get_spine
# from head.spine.loader import Loader
from head.spine.loader import Loader

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.WARNING, datefmt='%I:%M:%S')
# logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    ldr = Loader(s)
    # ldr.load(strafe_dir='right')
    # s.set_width_motor(int(100 * 1.5), 'ccw')
    # time.sleep(5)
    raw_input("Please compress the loader fully and rerun...")
    s.stop_width_motor()
    ldr.open_flaps()
    ldr.widen(4.3 - .5)
    raw_input()
    ldr.close_flaps()
    # ldr.load(strafe_dir='left')
