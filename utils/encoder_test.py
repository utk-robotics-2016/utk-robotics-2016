# Python modules
import logging

# Local modules
from head.spine.core import get_spine
# from head.spine.loader import Loader
# from head.spine.arm import get_arm
# from head.spine.Vec3d import Vec3d

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.WARNING, datefmt='%I:%M:%S')
# logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

with get_spine() as s:
    while True:
        print s.get_loader_encoder(2, raw=True), s.get_loader_encoder(2)
