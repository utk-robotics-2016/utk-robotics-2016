# Python modules
import time
import logging

import numpy as np

# Local modules
from head.spine.core import get_spine
from head.spine.loader import Loader

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    class Robot:

        def __init__(self):
            self.ldr = Loader(s)

        def start(self):
            for i in np.arange(0,1,0.05):
                s.move(i, 0, 0)
            time.sleep(6)
            logger.info("Done!")
            s.stop()

    bot = Robot()
    bot.start()
