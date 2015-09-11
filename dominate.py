# Python modules
import time
import logging
import thread

# Local modules
from head.spine.core import get_spine
from head.spine.loader import Loader

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    class Robot:

        def __init__(self):
            self.ldr = None #Loader(s)
            self.running = True

        def move_to_corner(self):
            logger.info("Moving out from corner")
            s.move(1, -90, 0, True)
            time.sleep(3)
            '''
            logger.info("Move through tunnel and open flap")
            s.move(1, 0, 0)
            time.sleep(3)
            s.move(1, 20, 0)
            #self.ldr.open_flap()
            time.sleep(2)
            s.move(0.5, 20, 0)
            time.sleep(0.5)

            logger.info("Align to corner")
            s.move(1, 90, 0)
            time.sleep(1)

            logger.info("Moving back for space")
            s.move(1, 180, 0)
            time.sleep(0.2)

            logger.info("Move to front of blocks")
            s.move(1, -90, 0)
            time.sleep(1.2)

            logger.info("Align to wall")
            s.move(1, 0, 0)
            time.sleep(1)

            s.stop()
            #self.ldr.load()

            logger.info("Resetting to start state")
            '''
            s.move(0, 0, 0, True)

        def start(self):
            time.sleep(1.5)
            thread.start_new_thread(self.battery_thread, ())
            self.move_to_corner()

            self.running = False
            logger.info("Done!")

        def battery_thread(self):
            while self.running:
                s.write_battery_voltage()
                time.sleep(1)

    bot = Robot()
    bot.start()
