import logging
from head.spine.voltage import get_battery_voltage
import sys

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')

simple = False
if len(sys.argv) > 1:
    if sys.argv[1] == '--simple':
        simple = True

if not simple:
    logging.info(get_battery_voltage())
else:
    print '%.3fV' % get_battery_voltage()
