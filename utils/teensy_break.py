# Python modules
import time
import logging
import logging.handlers

# Local modules
from head.spine.core import get_spine
from head.spine.ourlogging import setup_logging

setup_logging(__file__)
logger = logging.getLogger(__name__)

with get_spine() as s:
    class Robot:

        def __init__(self):
            pass

        def start(self):
            i = 0
            lasttime = time.time()
            lasti = 0
            while True:
                # response = s.send('teensy', 'ping')
                response = s.send('mega', 'ping')
                assert response == 'ok'
                i += 1
                if (time.time() - lasttime) > 1:
                    lasttime = time.time()
                    print response, i, time.time(), i - lasti
                    lasti = i

    bot = Robot()
    bot.start()
