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

    def extend(self, pos, **kwargs):
        '''Extend (or retract) the loader slide rails to a given position.

        :param pos:
            Absolute position, in rotations of the extension gear, to move to.
        :type pos: ``float``

        :Keyword Arguments:
            * **e_stop** (``float``) --
              Abort the rail movement if the rails do not reach their
              destination after ``e_stop`` seconds. Defaults to 4.
        '''
        encoders = [self.s.get_loader_encoder(i) for i in range(2)]

        if pos > encoders[0] and pos > encoders[1]:
            direction = 'fw'
            op = operator.ge
        elif pos < encoders[0] and pos < encoders[1]:
            direction = 'bw'
            op = operator.le
        else:
            raise ValueError

        motorrunning = []
        for i in range(2):
            self.s.set_loader_motor(i, 500, direction)
            motorrunning.append(True)
        starttime = time.time()

        while True in motorrunning:
            if time.time() - starttime > kwargs.get('e_stop', 4):
                self.s.stop_loader_motor(0)
                self.s.stop_loader_motor(1)
            for i in range(2):
                if motorrunning[i]:
                    encval = self.s.get_loader_encoder(i)
                    if op(encval, pos):
                        self.s.stop_loader_motor(i)
                        motorrunning[i] = False

    def close_flap(self):
        '''Close the loader flap.

        This method is preferred to calling Spine's direct method.
        '''
        self.s.close_loader_flap()

    def open_flap(self):
        '''Open the loader flap.

        This method is preferred to calling Spine's direct method.
        '''
        self.s.open_loader_flap()

    def load(self):
        '''Execute a sequence of Loader methods that will load a set of blocks.

        Before executing this method, make sure the robot is lined up within
        the tolerances of the loader with the blocks.
        '''
        self.open_flap()
        time.sleep(2)
        # self.extend(6.5)
        self.extend(6)
        time.sleep(2)
        self.close_flap()
        time.sleep(2)
        self.extend(0)
        time.sleep(2)
        self.open_flap()
        time.sleep(2)
        self.s.detach_loader_servos()
