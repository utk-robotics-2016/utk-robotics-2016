# Python modules
import time
import logging

# Local modules
from head.spine.core import get_spine

logging.basicConfig(format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    class Robot:
        def __init__(self):
            pass

        def start(self):
            #raise ValueError()
            s.move(1,0,0)
            time.sleep(3)
            logger.info("Done!")

    bot = Robot()
    bot.start()
