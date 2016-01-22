# Python modules
import logging

# Local modules
from head.spine.core import get_spine
# from head.spine.loader import Loader
from head.spine.loader import Loader
from head.spine.arm import get_arm
from head.spine.Vec3d import Vec3d

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.WARNING, datefmt='%I:%M:%S')
# logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    with get_arm(s) as arm:
        ldr = Loader(s)
        # Initialize before button press
        ldr.initial_zero_lift()
        ldr.lift(1.9)
        import IPython; IPython.embed()
        # arm.move_to(Vec3d(11, -1, 10), 0, 180)
        # ldr.widen(0.1)
        # arm.park()

        # raw_input('press enter')

        '''
        # Before colliding with barge
        ldr.widen(1)
        ldr.lift(0.2)
        raw_input('press enter')

        # After lining up
        # arm.move_to(Vec3d(11, -1, 10), 0, 180)
        # ldr.widen(0.1)
        ldr.lift(1.8)
        raw_input('press enter')
        # arm.park()
        '''
