# Python modules
import time
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

            def move_to_zone(self, currzone, destzone):
                raw_input('Move me to zone %d' % (destzone))

            def detect_blocks(self):
                blocks = []
                blocks.append([{'color': 'blue', 'type': 'full'}])
                blocks.append([{'color': 'red', 'type': 'full'}])
                blocks.append([{'color': 'yellow', 'type': 'full'}])
                blocks.append([{'color': 'green', 'type': 'full'}])
                blocks.append([{'color': 'red', 'type': 'full'}])
                blocks.append([{'color': 'blue', 'type': 'full'}])
                blocks.append([{'color': 'green', 'type': 'full'}])
                blocks.append([{'color': 'green', 'type': 'full'}])
                return blocks

            def get_zone_color(self, zid):
                return ['yellow', 'blue', 'red', 'green'][zid]

            def start(self):
                blocks = self.detect_blocks()
                for b in blocks:
                    assert b[0]['type'] == 'full'
                lastzid = -1
                for zid in range(4):
                    self.move_to_zone(lastzid, zid)
                    color = self.get_zone_color(zid)
                    indices = []
                    for i, b in enumerate(blocks):
                        if b[0]['color'] == color:
                            indices.append(i)
                    logging.info('%s blocks at %s.' % (color, indices))
                    for i in indices:
                        self.bp.pick_block(i, 'bottom', 'full')
                        self.bp.drop_block_right(rail=True)
                    lastzid = zid

        bot = Robot()
        bot.start()
