import operator
import time
import logging
from head.spine.control import trapezoid
from head.spine.ultrasonic import ultrasonic_go_to_position

logger = logging.getLogger(__name__)


class EStopException(Exception):
    pass


class Loader(object):
    '''An abstraction for the loader that simplifies many aspects of programming
    the loader.

    :param s:
        The Spine object to use.
    :type s: ``Spine``

    You should only need one Loader object in any program.
    '''

    def __init__(self, s):
        self.s = s
        self.FLAP_ROTATION_CHOICES = ['flap_down', 'flap_up']
        self.flap_rotation = 'flap_down'
        # Measured in rotations forward from the position of not extended
        self.flap_extension = 0

    def extend(self, pos, side, **kwargs):
        '''Extend (or retract) the loader slide rails to a given position.

        :param pos:
            Absolute position, in rotations of the extension gear, to move to.
        :type pos: ``float``

        :Keyword Arguments:
            * **e_stop** (``float``) --
              Abort the rail movement if the rails do not reach their
              destination after ``e_stop`` seconds. Defaults to 4.
        '''

        # This is because telling it to go to zero could cause an E-stop
        assert pos > 0.075

        if side == 'left':
            encoders = [0]
        elif side == 'right':
            encoders = [1]
        elif side == 'both':
            encoders = [0, 1]

        encVals = [self.s.get_loader_encoder(i) for i in encoders]

        condition1 = True
        for i in range(len(encoders)):
            condition1 = condition1 and pos > encVals[i]
        condition2 = True
        for i in range(len(encoders)):
            condition2 = condition2 and pos < encVals[i]

        if condition1:
            direction = 'fw'
            op = operator.ge
        elif condition2:
            direction = 'bw'
            op = operator.le
        else:
            raise ValueError

        motorrunning = []
        for i in encoders:
            self.s.set_loader_motor(i, 500, direction)
            motorrunning.append(True)
        starttime = time.time()

        while True in motorrunning:
            if time.time() - starttime > kwargs.get('e_stop', 4):
                for i in encoders:
                    self.s.stop_loader_motor(i)
                raise EStopException
            for i in range(len(encoders)):
                if motorrunning[i]:
                    encVal = self.s.get_loader_encoder(encoders[i])
                    if op(encVal, pos):
                        self.s.stop_loader_motor(encoders[i])
                        motorrunning[i] = False

    def widen(self, pos, **kwargs):
        ''' Widen (or retract) the loader to a given position

        :param pos:
            Absolute position, in rotations of the gear, to move to.
        :type pos: ``float``

        :Keyword Arguments:
            * **e_stop** (``float``) --
              Abort the movement if destination not reach after ``e_stop`` seconds. Defaults to 4.
        '''

        encVal = self.s.get_loader_encoder(2)

        if pos > encVal:
            direction = 'cw'
            op_direction = 'ccw'
            op = operator.ge
        elif pos < encVal:
            direction = 'ccw'
            op_direction = 'cw'
            op = operator.le
        else:
            raise ValueError

        self.s.set_width_motor(750, direction)
        starttime = time.time()
        TOT_TRIES = 3
        tries = 0

        while True:
            if time.time() - starttime > kwargs.get('e_stop', 4):
                if tries >= TOT_TRIES:
                    self.s.stop_width_motor()
                    print self.s.get_loader_encoder(2)
                    print self.s.get_loader_encoder(2, raw=True)
                    raise EStopException
                else:
                    # Run in reverse briefly to counter internal jamming
                    self.s.set_width_motor(1023, op_direction)
                    time.sleep(0.6)
                    self.s.set_width_motor(1023, direction)
                    starttime = time.time()
                    tries += 1

            encVal = self.s.get_loader_encoder(2)
            if op(encVal, pos):
                self.s.stop_width_motor()
                break

    def lift(self, pos, **kwargs):
        ''' Lift (or lower) the loader to a given position

        :param pos:
            Absolute position, in rotations of the gear, to move to.
        :type pos: ``float``

        :Keyword Arguments:
            * **e_stop** (``float``) --
              Abort the movement if destination not reach after ``e_stop`` seconds. Defaults to 10.
        '''
        def encoder_inches():
            return ( self.s.read_lift_encoder() / 464.64 / 20.0 ) * (9.68 / 34) 

        encVal = encoder_inches()
        motor_speed = 190

        if pos > encVal:
            direction = 'ccw'
            op = operator.ge
            self.s.set_lift_motor(motor_speed, direction)
        elif pos < encVal:
            direction = 'cw'
            op = operator.le
            self.s.set_lift_motor(motor_speed, direction)
        else:
            raise ValueError

        starttime = time.time()

        while True:
            if time.time() - starttime > kwargs.get('e_stop', 25):
                self.s.stop_lift_motor()
                raise EStopException
            encVal = encoder_inches()
            if op(encVal, pos):
                self.s.stop_lift_motor()
                break

    def control_flaps(self, left, right):
        '''Control the loader flaps independently

        This method is preferred to calling Spine's direct method.
        '''
        self.s.control_loader_flaps(left, right)

    def close_flaps(self):
        '''Close the loader flaps.

        This method is preferred to calling Spine's direct method.
        '''
        self.s.close_loader_flaps()

    def open_flaps(self):
        '''Open the loader flaps.

        This method is preferred to calling Spine's direct method.
        '''
        self.s.open_loader_flaps()

    def dump_blocks(self):
        self.s.open_loader_flaps()
        self.extend(6.0, 'both')
        # do not go back to 0.0 because it may E STOP
        self.extend(0.1, 'both')
        self.s.close_loader_flaps()

    def initial_zero_lift(self, use_widen=True, open_flaps=False):
        if open_flaps:
            self.open_flaps()
            time.sleep(.4)

        # So the wings do not collide with the beaglebone, etc
        if use_widen:
            self.widen(3)

        if open_flaps:
            self.close_flaps()
            time.sleep(.4)

        if not self.s.read_switches()['lift']:
            self.s.set_lift_motor(190, 'cw')
            while not self.s.read_switches()['lift']:
                time.sleep(.01)
            self.s.stop_lift_motor()
        self.s.zero_lift_encoder()
        # raw_input('')
        # self.widen(0)

    def load_sea_blocks(self, **kwargs):
        '''Execute a sequence of Loader methods that will load the sea blocks.

        Before executing this method, make sure the robot is lined up within
        the tolerances of the loader with the blocks.
        '''
        strafe_dir = kwargs.get('strafe_dir', None)
        # assert strafe_dir == 'right'
        assert strafe_dir in ['right', 'left']

        FWD_EXTEND_ROTS = 6.5
        # Open flaps and extend left
        self.open_flaps()
        self.s.move(1, 0, 0)
        self.widen(2.3)
        time.sleep(1)
        self.s.stop()
        logging.info("Free RAM: %s" % self.s.get_teensy_ram())

        # Compress blocks
        self.s.move(1, 0, 0)
        if strafe_dir == 'right':
            self.extend(FWD_EXTEND_ROTS + 1, 'left')
        else:
            self.extend(FWD_EXTEND_ROTS + 1, 'right')
        self.s.stop()
        logging.info("Free RAM: " + self.s.get_teensy_ram())

        time.sleep(0.5)

        if strafe_dir == 'right':
            thedir = -80
        else:
            thedir = 80

        logging.info("Free RAM: %s" % self.s.get_teensy_ram())
        trapezoid(self.s.move_pid, (0, thedir, 0), (0.5, thedir, 0), (0, thedir, 0), 1.2)
        time.sleep(1)
        self.s.stop()

        time.sleep(0.5)

        # Bring home the bacon
        self.s.move(1, 0, 0)
        time.sleep(0.5)
        if strafe_dir == 'right':
            self.control_flaps('close', 'open')
        else:
            self.control_flaps('open', 'close')
        time.sleep(1)  # Wait for servos to close
        self.widen(1)
        self.s.stop()

        # Do not extend to 0.0 because we may E STOP
        if strafe_dir == 'right':
            try:
                self.extend(0.1, 'left')
            except EStopException:
                logging.info("Ignoring E-stop on load retract.")
                pass
        else:
            try:
                self.extend(0.1, 'right')
            except EStopException:
                logging.info("Ignoring E-stop on load retract.")
                pass
        logging.info("Free RAM: %s" % self.s.get_teensy_ram())
        self.close_flaps()

        # self.widen(0)
        # Allow servos time to move:
        time.sleep(2)

    def load(self, **kwargs):
        '''Execute a sequence of Loader methods that will load a set of blocks.

        Before executing this method, make sure the robot is lined up within
        the tolerances of the loader with the blocks.
        '''
        strafe_dir = kwargs.get('strafe_dir', None)
        # assert strafe_dir == 'right'
        assert strafe_dir in ['right', 'left']
        FWD_EXTEND_ROTS = 6.5
        # Open flaps and extend left
        self.open_flaps()
        self.s.move(1, 0, 0)
        self.widen(4.3 - .5)
        if strafe_dir == 'right':
            self.extend(FWD_EXTEND_ROTS, 'left')
        else:
            self.extend(FWD_EXTEND_ROTS + 1, 'right')
        time.sleep(1)
        self.s.stop()
        logging.info("Free RAM: %s" % self.s.get_teensy_ram())

        # Strafe right to compress left side
        # self.s.move_pid(.5, -90, 0)
        if strafe_dir == 'right':
            thedir = -80
        else:
            thedir = 80

        logging.info("Free RAM: %s" % self.s.get_teensy_ram())
        trapezoid(self.s.move_pid, (0, thedir, 0), (0.5, thedir, 0), (0, thedir, 0), 2.0)
        time.sleep(1)
        self.s.stop()

        # Compress blocks
        self.s.move_pid(1, 0, 0)
        if strafe_dir == 'right':
            self.extend(FWD_EXTEND_ROTS + 1, 'right')
        else:
            self.extend(FWD_EXTEND_ROTS + 1, 'left')
        self.s.stop()
        logging.info("Free RAM: " + self.s.get_teensy_ram())

        # Do this when our compression issues are fixed
        # self.widen(1)
        '''
        # Manually enable compression
        self.s.set_width_motor(750, 'ccw')
        time.sleep(0.2)
        self.s.move_pid(0.5, 180, 0)
        time.sleep(0.5)
        # Manually disable compression
        self.s.stop_width_motor()
        self.s.stop()
        '''
        # Remove this 'except' when our compression issues are fixed
        try:
            self.widen(1.6)
        except EStopException:
            logging.warning('Caught EStopException!!!!!')

        # Bring home the bacon
        self.s.move(1, 0, 0)
        time.sleep(0.5)
        self.close_flaps()
        time.sleep(1)  # Wait for servos to close
        self.widen(1)
        self.s.stop()
        # '''
        # Do not extend to 0.0 because we may E STOP
        try:
            self.extend(0.1, 'both')
        except EStopException:
            # Ignore the E-stop because we had problems with it E-stopping when
            # very close to the target
            logging.info("Ignoring E-stop on load retract.")
            pass
        logging.info("Free RAM: %s" % self.s.get_teensy_ram())

        self.s.set_width_motor(150, 'ccw')
        time.sleep(2)
        self.s.stop_width_motor()

        # self.widen(0)
        # Allow servos time to move:
        time.sleep(2)
        # '''

        # we no longer want the servos to be depowered
        # self.s.detach_loader_servos()

        # self.lift(0.3)
        # raw_input("continue...")
        # self.lift(0)
