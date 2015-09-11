# Global modules
import logging
import time

# Local modules
from head.spine.Vec3d import Vec3d

SPEED = 1
FULL_BLOCK_FORWARD = 11
NEAR_HALF_BLOCK_FORWARD = 9
FAR_HALF_BLOCK_FORWARD = 14
HEIGHT_TO_CLEAR_LOADER = 12
RIGHT_DROP_XY = (16, 0)
# height of the top surface of the bottom level
BOTTOM_LEVEL_HEIGHT = -1
BLOCK_WIDTH_IN_CM = 1.5 * 2.54
# height of the top surface of the top level
TOP_LEVEL_HEIGHT = BOTTOM_LEVEL_HEIGHT + BLOCK_WIDTH_IN_CM

class BlockPicker:
    def __init__(self, s, arm):
        self.s = s
        self.arm = arm

    def pick_block(self, col, level, desc='full'):
        # lateral, forward, height
        def get_lateral(thecol):
            far_left_lateral = 11.645  # col index 0
            far_right_lateral = -13.258  # col index 7
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
        if desc == 'full':
            forward = FULL_BLOCK_FORWARD
        elif desc == 'near_half':
            forward = NEAR_HALF_BLOCK_FORWARD
        elif desc == 'far_half':
            forward = FAR_HALF_BLOCK_FORWARD
        else:
            raise ValueError
        self.arm.move_to(Vec3d(lateral, forward,
                    level_height + 4), 0, 180, SPEED)
        self.s.set_suction(True)
        self.arm.move_to(Vec3d(lateral, forward,
                    level_height - 1), 0, 180, SPEED)
        time.sleep(0.5)
        if col == 7:
            lateral = get_lateral(col - 1)
            logging.info(lateral)
            self.arm.move_to(Vec3d(lateral, forward,
                        level_height + 4), 0, 180, SPEED)
            logging.info(lateral)
        self.arm.move_to(Vec3d(lateral, forward,
                    HEIGHT_TO_CLEAR_LOADER), 0, 180, SPEED)

    def drop_block_right(self):
        self.arm.move_to(Vec3d(RIGHT_DROP_XY[0], RIGHT_DROP_XY[1],
                    HEIGHT_TO_CLEAR_LOADER), 0, 180, SPEED)
        self.s.set_suction(False)
        self.s.set_release_suction(True)
        time.sleep(0.5)
        self.s.set_release_suction(False)
