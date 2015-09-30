# Python modules
# import time
import logging

# Local modules
from head.spine.core import get_spine
from head.spine.arm import get_arm
from head.spine.block_picking import BlockPicker
from head.spine.Vec3d import Vec3d

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    with get_arm(s) as arm:
        class Robot:

            def __init__(self):
                self.bp = BlockPicker(s, arm)

            def start(self):
                arm.move_to(Vec3d(11, -1, 10), 0, 180)
                # arm.move_to(Vec3d(0, 10, 10), 0, 180)
                # self.bp.pick_block(2, 'top', 'near_half')
                # self.bp.drop_block_right()
                # self.bp.pick_block(2, 'top', 'far_half')
                # self.bp.drop_block_right()
                # self.bp.pick_block(3, 'top', 'near_half')
                # self.bp.drop_block_right()
                # self.bp.pick_block(3, 'top', 'far_half')
                # self.bp.drop_block_right()
                # self.bp.pick_block(0, 'top', 'full')
                # self.bp.drop_block_right()
                # self.bp.pick_block(7, 'top', 'far_half')
                # self.bp.drop_block_right()
                # '''
                # for level in ['top']:
                for level in ['top', 'bottom']:
                    for col in range(8):
                        self.bp.pick_block(col, level)
                        self.bp.drop_block_right()
                logger.info("Done!")
                # '''

        bot = Robot()
        bot.start()
