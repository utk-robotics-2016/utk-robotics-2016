# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine
# from head.spine.loader import Loader
from head.spine.arm import get_arm
from head.spine.voltage import get_battery_voltage
from head.spine.Vec3d import Vec3d
from head.spine.loader import Loader
from head.spine.control import keyframe

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.WARNING, datefmt='%I:%M:%S')
# logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    s.move_pid(1,-85,0)
    ir = s.read_ir_a()['left']
    while ir < 600:
        print ir
        ir = s.read_ir_a()['left']
    s.stop()
