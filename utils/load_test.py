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
    ldr = Loader(s)

    # Open flaps and extend left
    ldr.open_flaps()
    ldr.widen(4.5)
    ldr.extend(6, 'left')
    time.sleep(1)

    # Strafe right to compress left side
    # s.move_pid(.5, -90, 0)
    thedir = -85
    keyframe(s.move_pid, (0.5, thedir, 0), 2.15, (0, thedir, 0), (0, thedir, 0))
    time.sleep(1)
    s.stop()

    # Compress blocks
    ldr.extend(6, 'right')
    ldr.widen(1)
    ldr.widen(1.6)

    # Bring home the bacon
    s.move(1, 0, 0)
    time.sleep(0.5)
    ldr.close_flaps()
    time.sleep(1)  # Wait for servos to close
    ldr.widen(1)
    s.stop()
    # '''
    ldr.extend(0, 'both')

    # ldr.widen(0)
    # Allow servos time to move:
    time.sleep(2)
    # '''
    s.detach_loader_servos()
    # ldr.lift(0.3)
    # raw_input("continue...")
    # ldr.lift(0)
