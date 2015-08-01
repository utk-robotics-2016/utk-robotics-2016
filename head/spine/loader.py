import time
import operator
import logging

logger = logging.getLogger(__name__)

class Loader(object):

    def __init__(self, s):
        self.s = s
        self.FLAP_ROTATION_CHOICES = ['flap_down', 'flap_up']
        self.flap_rotation = 'flap_down'
        # Measured in rotations forward from the position of not extended
        self.flap_extension = 0

    def extend(self, pos):
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

        while True in motorrunning:
            for i in range(2):
                if motorrunning[i]:
                    encval = self.s.get_loader_encoder(i)
                    if op(encval, pos):
                        self.s.stop_loader_motor(i)
                        motorrunning[i] = False

    def close_flap(self):
        self.s.close_loader_flap()

    def open_flap(self):
        self.s.open_loader_flap()
