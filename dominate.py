# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    class Robot:

        def __init__(self):
            pass

        def start(self):
            # raise ValueError()
            s.move(1, 180, 0)
            # s.set_wheel(1, 100, 'fw')
            time.sleep(1)
            logger.info("Done!")

    bot = Robot()
    bot.start()
