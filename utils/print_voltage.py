import logging
from head.spine.voltage import get_battery_voltage

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')

logging.info(get_battery_voltage())
