# Python modules
import logging

# Local modules
from head.spine.core import get_spine
# from head.spine.loader import Loader
from head.spine.loader import Loader
from head.spine.arm import get_arm
from head.spine.Vec3d import Vec3d
from head.spine.ourlogging import setup_logging

setup_logging(__file__)
logger = logging.getLogger(__name__)

with get_spine() as s:
    with get_arm(s) as arm:
        ldr = Loader(s)
        # Initialize before button press
        ldr.initial_zero_lift()
        ldr.lift(1.9)
        import IPython
        IPython.embed()
        arm.move_to(Vec3d(11, -1, 10), 0, 180)
        ldr.widen(0.1)
        arm.park()

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
