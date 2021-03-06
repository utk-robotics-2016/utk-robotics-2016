# Python modules
import logging

# Local modules
from head.spine.core import get_spine
# from head.spine.loader import Loader
from head.spine.loader import Loader

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.WARNING, datefmt='%I:%M:%S')
# logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    ldr = Loader(s)
    ldr.load(strafe_dir='right')
    # ldr.load(strafe_dir='left')
