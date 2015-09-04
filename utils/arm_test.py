# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine
from head.spine.arm import get_arm
from head.spine.Vec3d import Vec3d

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

SPEED = 1
FULL_BLOCK_FORWARD = 11
HEIGHT_TO_CLEAR_LOADER = 12
RIGHT_DROP_XY = (16, 0)
# height of the top surface of the bottom level
BOTTOM_LEVEL_HEIGHT = -1
BLOCK_WIDTH_IN_CM = 1.5 * 2.54
# height of the top surface of the top level
TOP_LEVEL_HEIGHT = BOTTOM_LEVEL_HEIGHT + BLOCK_WIDTH_IN_CM

with get_spine() as s:
    with get_arm(s) as arm:
        class Robot:

            def __init__(self):
                pass

            def pick_block(self, col, level):
                # lateral, forward, height
                def get_lateral(thecol):
                    far_left_lateral = 11.145  # col index 0
                    far_right_lateral = -13.858  # col index 7
                    lateral_inc = (far_right_lateral - far_left_lateral) / 7
                    return far_left_lateral + lateral_inc * thecol
                lateral = get_lateral(col)
                logging.info(lateral)
                if level == 'bottom':
                    level_height = BOTTOM_LEVEL_HEIGHT
                elif level == 'top':
                    level_height = TOP_LEVEL_HEIGHT
                else:
                    raise ValueError
                arm.move_to(Vec3d(lateral, FULL_BLOCK_FORWARD,
                            level_height + 4), 0, 180, SPEED)
                s.set_suction(True)
                arm.move_to(Vec3d(lateral, FULL_BLOCK_FORWARD,
                            level_height - 1), 0, 180, SPEED)
                time.sleep(0.5)
                if col == 7:
                    lateral = get_lateral(col - 1)
                    logging.info(lateral)
                    arm.move_to(Vec3d(lateral, FULL_BLOCK_FORWARD,
                                level_height + 4), 0, 180, SPEED)
                    logging.info(lateral)
                arm.move_to(Vec3d(lateral, FULL_BLOCK_FORWARD,
                            HEIGHT_TO_CLEAR_LOADER), 0, 180, SPEED)

            def drop_block_right(self):
                arm.move_to(Vec3d(RIGHT_DROP_XY[0], RIGHT_DROP_XY[1],
                            HEIGHT_TO_CLEAR_LOADER), 0, 180, SPEED)
                s.set_suction(False)
                s.set_release_suction(True)
                time.sleep(0.5)
                s.set_release_suction(False)

            def start(self):
                for level in ['top', 'bottom']:
                    for col in range(8):
                        self.pick_block(col, level)
                        self.drop_block_right()
                logger.info("Done!")

        bot = Robot()
        bot.start()
