# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine
from head.spine.loader import Loader

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    ldr = Loader(s)
    ldr.open_flap()
    time.sleep(2)
    # ldr.extend(6.5)
    ldr.extend(5.2)
    time.sleep(2)
    ldr.close_flap()
    time.sleep(2)
    ldr.extend(0)
    time.sleep(2)
    ldr.open_flap()
    time.sleep(2)
