# Global modules
import logging
# import time

# Local modules
# from head.spine.Vec3d import Vec3d
from head.spine.ultrasonic import ultrasonic_go_to_position
from head.spine.block_picking import BlockPicker
from head.spine.control import trapezoid


class RailSorter:
    def __init__(self, s, arm):
        self.s = s
        self.arm = arm
        self.bp = BlockPicker(s, arm)
        self.bin_colors = ['yellow', 'green', 'red', 'blue']

    def move_to_rail_zone(self, currzone, destzone, course, method='deadreckon'):
        if method == 'manual':
            raw_input('Move me to zone %d' % (destzone))
        elif method == 'deadreckon':
            if currzone == 3 and destzone == 0:
                # Bump up against barge
                self.s.move_for(5, 0.8, 0, 0.08)
                # Bump against railroad
                self.s.move_for(1, 0.6, -70, 0)
                # Move away from railroad
                self.s.move_for(1, 0.6, 70, 0)
            elif currzone != -1:
                if currzone < destzone: # moving backward
                    if destzone == 1:
                        ultrasonic_go_to_position(self.s, front=26, unit='cm', rot=-.055)
                    elif destzone == 2:
                        ultrasonic_go_to_position(self.s, front=50, unit='cm', rot=-.02)
                    elif destzone == 3:
                        trapezoid(self.s.move_pid, (0, -175, .02), (.6, -175, .02), (0, -175, .02), 1.2)
                        self.s.stop()
                else:
                   if destzone == 2:
                       trapezoid(self.s.move_pid, (0, 0, .01), (.6, 0, .01), (0, 0, .01), 2.0)
                       self.s.stop()
                   elif destzone == 1:
                       ultrasonic_go_to_position(self.s, front=26, unit='cm', rot=.01)
                   elif destzone == 0:
                       ultrasonic_go_to_position(self.s, front=5, unit='cm')
#                side_dist = 13
#                if course == 'A':
#                    ultrasonic_go_to_position(self.s, left=side_dist, unit='cm')
#                else:
#                    ultrasonic_go_to_position(self.s, right=side_dist, unit='cm')

                '''
                trapezoid(self.s.move_pid, (0, 180, 0), (0.5, 180, 0), (0, 180, 0), 2.0)
                self.s.stop()
                if currzone == 1 and destzone == 2:
                    back_away_time = 1.0
                    if course == 'A':
                        trapezoid(self.s.move_pid, (0, -90, 0), (0.5, -90, 0), (0, -90, 0), back_away_time)
                    else:
                        trapezoid(self.s.move_pid, (0, 90, 0), (0.5, 90, 0), (0, 90, 0), back_away_time)
                '''
                '''
                dist = 18.0
                if course == 'A':
                    ultrasonic_go_to_position(self.s, left=dist, unit='cm')
                else:
                    ultrasonic_go_to_position(self.s, right=dist, unit='cm')
                '''
        else:
            raise ValueError

    def convert_andrew_block_string(self, s):
        raw_blocks = s.split()
        # GL RH BH YL YL YL RL RL BL
        logging.info(raw_blocks)
        blocks = []
        colors = {'G': 'green', 'B': 'blue', 'R': 'red', 'Y': 'yellow'}
        i = 0
        while i < len(raw_blocks):
            if raw_blocks[i][1] == 'L':
                blocks.append([{'color': colors[raw_blocks[i][0]], 'type': 'full'}])
                i += 1
            elif raw_blocks[i][1] == 'H':
                # Assert that the next block is half as well.
                assert raw_blocks[i][1] == 'H'
                blocks.append([
                    {'color': colors[raw_blocks[i][0]], 'type': 'far_half'},
                    {'color': colors[raw_blocks[i + 1][0]], 'type': 'near_half'}
                ])
                i += 2
            else:
                raise ValueError
        blocks = list(reversed(blocks))
        logging.info(blocks)
        return blocks

    def detect_blocks(self, level, method='optical'):
        if method == 'optical':
            raw_blocks = self.arm.detect_blocks(level)
            blocks = self.convert_andrew_block_string(raw_blocks)
        elif method == 'hardcoded':
            blocks = []
            if level == 'bottom':
                # Far right
                blocks.append([{'color': 'blue', 'type': 'full'}])
                blocks.append([{'color': 'red', 'type': 'full'}])
                blocks.append([{'color': 'yellow', 'type': 'full'}])
                blocks.append([{'color': 'green', 'type': 'full'}])
                blocks.append([{'color': 'red', 'type': 'full'}])
                blocks.append([{'color': 'blue', 'type': 'full'}])
                blocks.append([{'color': 'green', 'type': 'full'}])
                blocks.append([{'color': 'green', 'type': 'full'}])
                # Far left
            elif level == 'top':
                # Far right
                blocks.append([{'color': 'green', 'type': 'full'}])
                blocks.append([{'color': 'yellow', 'type': 'full'}])
                blocks.append([{'color': 'yellow', 'type': 'full'}])
                blocks.append([{'color': 'blue', 'type': 'full'}])
                blocks.append([{'color': 'blue', 'type': 'full'}])
                blocks.append([{'color': 'red', 'type': 'full'}])
                blocks.append([{'color': 'yellow', 'type': 'full'}])
                blocks.append([{'color': 'red', 'type': 'full'}])
                # Far left
            else:
                raise ValueError
        else:
            raise ValueError
        return blocks

    def set_rail_zone_bins(self, bins):
        self.bin_colors = bins

    def get_rail_zone_color(self, zid):
        # Index 0 is closest to the barge.
        return self.bin_colors[zid]

    def unload_rail(self, course):
        lastzid = -1
        for level in ['top', 'bottom']:
        #for level in ['top']:
            blocks = self.detect_blocks(level)
            for zid in range(4):
                if level == 'top':
                    self.move_to_rail_zone(zid-1, zid, course)
                    color = self.get_rail_zone_color(zid)
                else:
                    self.move_to_rail_zone(4 - zid, 3 - zid, course)
                    color = self.get_rail_zone_color(3 - zid)
                #self.s.open_loader_flaps()
                indices = []
                for i, col in enumerate(blocks):
                    for j, b in enumerate(col):
                        if b['color'] == color:
                            indices.append((i, b['type']))
                logging.info('%s blocks at %s.' % (color, indices))
                for i, block_type in indices:
                    logging.info((i, block_type))
                    self.bp.pick_block(i, level, block_type)
                    side = {'B': 'right', 'A': 'left'}[course]
                    self.bp.drop_block(rail=True, side=side)
                #self.s.close_loader_flaps()
                #lastzid = zid
