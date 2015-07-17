# Python modules
import time
import logging

# Local modules
from head.spine.spine import get_spine

with get_spine() as s:
    class Robot:
        def __init__(self):
            pass

        def start(self):
            print "Done!"

    bot = Robot()
    bot.start()
