# Python modules
import logging
import time
import argparse
import sys

# Local modules
from head.spine.core import get_spine
# from head.spine.loader import Loader
from head.spine.ourlogging import setup_logging

setup_logging(__file__)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Manual control of loader')
parser.add_argument('--retract', type=float, help='Retract the loader arms for SECONDS.')
parser.add_argument('--extend', type=float, help='Extend the loader arms for SECONDS.')
parser.add_argument('--compress', type=float, help='Compress the loader arms for SECONDS.')
parser.add_argument('--widen', type=float, help='Widen the loader arms for SECONDS.')
parser.add_argument('--no_right', action='store_true', help='No right extend', default=False)
parser.add_argument('--no_left', action='store_true', help='No left extend', default=False)
parser.add_argument('--open_flaps', action='store_true', default=False)
parser.add_argument('--close_flaps', action='store_true', default=False)
parser.add_argument('--lift', type=float, help='Lift the loader up for SECONDS.')
parser.add_argument('--lower', type=float, help='Lower the loader for SECONDS.')
parser.add_argument('--power', default=100, type=int, help='Motor power to use. Default=100.')
parser.add_argument('--close', help='Close the flaps.')
parser.add_argument('--open', help='Open the flaps.')
args = parser.parse_args()

if args.extend is None and args.retract is None and args.compress is None and args.widen is None and args.lift is None and args.lower is None and args.open_flaps is False and args.close_flaps is False:
    parser.print_help()
    sys.exit()

with get_spine() as s:
    # ldr = Loader(s)
    # ldr.load(strafe_dir='right')

    def retract(seconds):
        if not args.no_left:
            s.set_loader_motor(0, int(args.power * 3 / 4), 'bw')
        if not args.no_right:
            s.set_loader_motor(1, args.power, 'bw')
        time.sleep(seconds)
        if not args.no_left:
            s.stop_loader_motor(0)
        if not args.no_right:
            s.stop_loader_motor(1)

    def extend(seconds):
        if not args.no_left:
            s.set_loader_motor(0, args.power, 'fw')
        if not args.no_right:
            s.set_loader_motor(1, int(args.power * 3 / 4), 'fw')
        time.sleep(seconds)
        if not args.no_left:
            s.stop_loader_motor(0)
        if not args.no_right:
            s.stop_loader_motor(1)

    def compress(seconds):
        s.set_width_motor(int(args.power * 1.5), 'ccw')
        time.sleep(seconds)
        s.stop_width_motor()

    def widen(seconds):
        s.set_width_motor(int(args.power * 1.5), 'cw')
        time.sleep(seconds)
        s.stop_width_motor()

    def lift(seconds):
        s.set_lift_motor(127, 'ccw')
        time.sleep(seconds)
        s.stop_lift_motor()

    def lower(seconds):
        s.set_lift_motor(127, 'cw')
        time.sleep(seconds)
        s.stop_lift_motor()

    def close_flaps():
        s.close_loader_flaps()

    def open_flaps():
        s.open_loader_flaps()

    if args.retract:
        retract(args.retract)
    if args.extend:
        extend(args.extend)
    if args.compress:
        compress(args.compress)
    if args.widen:
        widen(args.widen)
    if args.lift:
        lift(args.lift)
    if args.lower:
        lower(args.lower)
    if args.open_flaps:
        open_flaps()
    if args.close_flaps:
        close_flaps()
