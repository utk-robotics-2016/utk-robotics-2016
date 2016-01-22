# Global modules
import logging
import time
from math import pi

# Local modules
from head.spine.Vec3d import Vec3d

# SPEED = 0.75
SPEED = 1
FULL_BLOCK_FORWARD = 11
NEAR_HALF_BLOCK_FORWARD = FULL_BLOCK_FORWARD - 2
FAR_HALF_BLOCK_FORWARD = FULL_BLOCK_FORWARD + 3
HEIGHT_TO_CLEAR_LOADER = 13
DROP_XY = {'right': (16, 0), 'left': (-16, -4)}
# height of the top surface of the bottom level
BOTTOM_LEVEL_HEIGHT = -2
BLOCK_WIDTH_IN_CM = 1.5 * 2.54
# height of the top surface of the top level
TOP_LEVEL_HEIGHT = BOTTOM_LEVEL_HEIGHT + BLOCK_WIDTH_IN_CM
RAIL_DROP_XY = {'right': (16 + 5, -5), 'left': (-(16 + 5), -4)}
HEIGHT_TO_DROP_RAIL = HEIGHT_TO_CLEAR_LOADER - 11


class BlockPicker:
    def __init__(self, s, arm):
        self.s = s
        self.arm = arm

    def pick_block(self, col, level, desc='full'):
        # lateral, forward, height
        def get_lateral(thecol):
            far_left_lateral = 11.645+1  # col index 0
            far_right_lateral = -11.645+1  # col index 7
            lateral_inc = (far_right_lateral - far_left_lateral) / 7
            return far_left_lateral + lateral_inc * thecol
        lateral = get_lateral(col)
        # Special case!
        if col == 0 and desc == 'far_half':
            lateral += 1
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
        # Special case!
        if col == 0 and desc == 'full':
            forward -= 2
        self.arm.move_to(Vec3d(lateral, forward,
                         level_height + 4), 0, 180, SPEED)
        self.s.set_suction(True)
        self.arm.move_to(Vec3d(lateral, forward,
                         level_height - 1), -pi / 20, 180, SPEED)
        time.sleep(0.5)
        # Special case!
        # To avoid the math domain errors on retract
        if (col in [0, 7] and desc == 'far_half'):
            forward = FULL_BLOCK_FORWARD
        self.arm.move_to(Vec3d(lateral, forward,
                         HEIGHT_TO_CLEAR_LOADER), 0, 180, SPEED)

    def drop_block(self, **kwargs):
        rail_drop = kwargs.get('rail', False)
        side = kwargs.get('side', 'right')
        extend_wrist = rail_drop
        if extend_wrist:
            wrist = pi / 2
        else:
            wrist = 0
        self.arm.move_to(Vec3d(DROP_XY[side][0], DROP_XY[side][1],
                         HEIGHT_TO_CLEAR_LOADER), wrist, 180, SPEED)
        if rail_drop:
            self.arm.move_to(Vec3d(RAIL_DROP_XY[side][0], RAIL_DROP_XY[side][1],
                             HEIGHT_TO_DROP_RAIL), wrist, 180, SPEED)
        self.s.set_suction(False)
        self.s.set_release_suction(True)
        time.sleep(0.5)
        self.s.set_release_suction(False)
        # To clear rails before returning
        if rail_drop:
            self.arm.move_to(Vec3d(DROP_XY[side][0], DROP_XY[side][1],
                             HEIGHT_TO_CLEAR_LOADER), wrist, 180, SPEED)
