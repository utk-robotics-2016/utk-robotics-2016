# Python modules
import time
# Local modules
from head.spine import spine

# Change this port if not on LINUX
s = spine.Spine(spine.DEF_LINUX_PORT)
s.startup()

class Robot:
    def __init__(self):
        pass

    def start(self):
        pass

bot = Robot()
bot.start()

s.close()
