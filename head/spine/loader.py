import operator
import time
import logging

logger = logging.getLogger(__name__)


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
        if side == 'left':
            encoders = [1]
        elif side == 'right':
            encoders = [0]
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
                break
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
            op = operator.ge
        elif pos < encVal:
            direction = 'ccw'
            op = operator.le
        else:
            raise ValueError

        self.s.set_width_motor(750, direction)
        starttime = time.time()

        while True:
            if time.time() - starttime > kwargs.get('e_stop', 4):
                self.s.stop_width_motor()
                break
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
            return self.s.read_lift_encoder() / 464.64 / 20.0

        encVal = encoder_inches()

        if pos > encVal:
            direction = 'ccw'
            op = operator.ge
            self.s.set_lift_motor(1023,direction)
        elif pos < encVal:
            direction = 'cw'
            op = operator.le
            self.s.set_lift_motor(500,direction)
        else:
            raise ValueError

        starttime = time.time()

        while True:
            if time.time() - starttime > kwargs.get('e_stop', 10):
                self.s.stop_lift_motor()
                break
            encVal = encoder_inches()
            if op(encVal, pos):
                self.s.stop_lift_motor()
                break

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
        self.extend(6.0, 'both')
        self.extend(0.0, 'both')

    def load(self):
        '''Execute a sequence of Loader methods that will load a set of blocks.

        Before executing this method, make sure the robot is lined up within
        the tolerances of the loader with the blocks.
        '''
        '''
        self.open_flaps()
        time.sleep(2)
        # self.extend(6.5)
        self.extend(6)
        time.sleep(2)
        self.close_flaps()
        time.sleep(2)
        self.extend(0)
        time.sleep(2)
        self.open_flaps()
        time.sleep(2)
        self.s.detach_loader_servos()
        '''
