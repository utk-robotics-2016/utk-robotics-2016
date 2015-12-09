# Python modules
import logging
import time
import argparse
import sys

# Local modules
from head.spine.core import get_spine
# from head.spine.loader import Loader

fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.WARNING, datefmt='%I:%M:%S')
# logging.basicConfig(format=fmt, level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Manual control of loader')
parser.add_argument('--retract', type=int, help='Retract the loader arms for SECONDS.')
parser.add_argument('--extend', type=int, help='Extend the loader arms for SECONDS.')
parser.add_argument('--compress', type=int, help='Compress the loader arms for SECONDS.')
parser.add_argument('--lift', type=int, help='Lift the loader up for SECONDS.')
parser.add_argument('--lower', type=int, help='Lower the loader for SECONDS.')
parser.add_argument('--power', default=100, type=int, help='Motor power to use. Default=80.')
args = parser.parse_args()

if args.extend is None and args.retract is None and args.compress is None and args.lift is None and args.lower is None:
    parser.print_help()
    sys.exit()

with get_spine() as s:
    # ldr = Loader(s)
    # ldr.load(strafe_dir='right')

    def retract(seconds):
        s.set_loader_motor(0, int(args.power * 3 / 4), 'bw')
        s.set_loader_motor(1, args.power, 'bw')
        time.sleep(seconds)
        s.stop_loader_motor(0)
        s.stop_loader_motor(1)

    def extend(seconds):
        s.set_loader_motor(0, args.power, 'fw')
        s.set_loader_motor(1, int(args.power * 3 / 4), 'fw')
        time.sleep(seconds)
        s.stop_loader_motor(0)
        s.stop_loader_motor(1)

    def compress(seconds):
        s.set_width_motor(int(args.power * 1.5), 'ccw')
        time.sleep(seconds)
        s.stop_width_motor()

    def lift(seconds):
        s.set_lift_motor(255, 'ccw')
        time.sleep(seconds)
        s.stop_lift_motor()

    def lower(seconds):
        s.set_lift_motor(255, 'cw')
        time.sleep(seconds)
        s.stop_lift_motor()

    if args.retract:
        retract(args.retract)
    if args.extend:
        extend(args.extend)
    if args.compress:
        compress(args.compress)
    if args.lift:
        lift(args.lift)
    if args.lower:
        lower(args.lower)
