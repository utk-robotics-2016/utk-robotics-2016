# Global
import time
import os
import logging

# Third-party
import serial

# Project specific
import mecanum

logger = logging.getLogger(__name__)

DEF_PORTS = {
    'mega': '/dev/mega',
    'teensy': '/dev/teensy',
    'loadmega': '/dev/loadmega',
}


class SerialLockException(Exception):
    '''Raised when attempting to access a locked serial device.

    This happens when a lockfile already exists in the lock location, usually
    in ``/var/lock``. It's possible that someone is using this serial port. If
    not, the fix is to simply remove the lock using rm.
    '''
    pass


class get_spine:

    def __enter__(self):
        self.s = Spine()
        self.s.startup()
        return self.s

    def __exit__(self, type, value, traceback):
        self.s.stop()
        self.s.detach_loader_servos()
        self.s.close()


class Spine:
    '''Provides a simple interface to the robot's peripherals.

    This class should probably not be instantiated directly. Please see
    :func:`get_spine`, which provides safe error and interrupt handling, which
    this class does not directly provide.

    There is no need to create more than one Spine object. In fact, it is not
    possible due to serial port locking.

    Note that typically commands will assert a successful response from one of
    the micros even if there is no return value.

    :param t_out:
        The serial timeout. Probably should not change
    :type t_out: ``int``
    :param delim:
        The line delimeter for serial communications. Probably should not
        change.
    :type delim: ``string``

    :Keyword Arguments:
        * **use_lock** (``bool``) --
          Whether to respect and create the lock files in ``/var/lock``. Should
          probably always be true, the default.
        * **lock_dir** (``str``) --
          Location of the lock files. Defaults to ``/var/lock/``.
        * **ports** (``dict``) --
          A dictionary of the ports and serial devices they are connected to.
          See DEF_PORTS in :module:`head.spine.core` for the default and an
          example of a valid setting.
    '''

    def __init__(self, t_out=1, delim='\n', **kwargs):
        self.ser = {}
        self.use_lock = kwargs.get('use_lock', True)
        self.lock_dir = kwargs.get('lock_dir', '/var/lock/')
        self.ports = kwargs.get('ports', DEF_PORTS)
        first = True
        for devname, port in self.ports.iteritems():
            if self.use_lock:
                fndevname = port.split('/dev/')[1]
                lockfn = '%sLCK..%s' % (self.lock_dir, fndevname)
                if os.path.isfile(lockfn):
                    self.close()
                    raise SerialLockException(
                        "Lockfile %s exists. It's possible that someone is using this serial port. If not, remove this lock file. Closing and raising error." % lockfn)
            logger.info('Connecting to %s.' % port)
            self.ser[devname] = serial.Serial(port, 115200, timeout=t_out)
            if self.use_lock:
                with open(lockfn, 'w') as f:
                    f.write('-1')
                logger.info('Created lock at %s.' % lockfn)
            if first:
                first = False
            else:
                logger.info('Waiting for connection to stabilize.')
                time.sleep(1)
        self.delim = delim

        # Startup commands
        for i in range(2):
            self.zero_loader_encoder(i)

    def send(self, devname, command):
        '''Send a command to a device and return the result.

        This is an internal method and should not be used directly. This is
        only for testing new commands that do not yet have specific Spine
        methods written for them. This method is used internally by the other
        Spine methods.

        :param devname:
            The device name to send the command to.
        :type devname: ``string``
        :param command:
            The command to send. Do not include the newline at the end.
            Information on these serial commands can be gathered through looking
            at the Spine source or the source of the various microcontrollers
            directly.
        :type command: ``string``

        :return: The string response of the command, without the newline.
        '''
        logger.debug("Sending %s to '%s'" % (repr(command), devname))
        self.ser[devname].write(command + self.delim)
        echo = self.ser[devname].readline()
        assert echo == '> ' + command + '\r\n'
        response = self.ser[devname].readline()
        logger.debug("Response: %s" % repr(response[:-2]))
        # Be sure to chop off newline. We don't need it.
        return response[:-2]

    def ping(self):
        '''Send a ping command to all devices and assert success.

        This is called automatically by :func:`startup()`.
        '''
        for devname in self.ser.keys():
            response = self.send(devname, 'ping')
            assert response == 'ok'

    def set_led(self, devname, status):
        '''Turns the debug LED on or off for certain devices.

        This is typically only used for debug purposes. LEDs are flashed three
        times on all devices during the :func:`startup()` call.

        :param devname:
            The device to direct the LED setting to.
        :type devname: ``string``
        :param status:
            True for on, False for off.
        :type status: ``bool``
        '''
        command = 'le ' + ('on' if status else 'off')
        response = self.send(devname, command)
        assert response == 'ok'

    def move_for(self, delay, *args):
        self.move(*args)
        time.sleep(delay)
        self.stop()

    def set_wheel(self, w_id, speed, direction):
        '''Set one of the bottom four wheels to a speed and direction.

        This typically sends a command to the ``teensy`` device. The wheel
        mappings on the micros tend to be out of date and updating them is much
        easier on the BBB, so wheel ID decoding is typically done in this
        function.

        :param w_id:
            Integer from 1-4. Let W1, W2, W3, and W4 be the front left, front
            right, rear left, and rear right wheels, respectively.
        :type w_id: ``int``
        :param speed:
            0 to 255 where 255 is the fastest.
        :type speed: ``int``
        :param direction:
            Either ``'fw'`` or ``'rv'``.
        :type direction: ``str``
        '''
        assert w_id in [1, 2, 3, 4]
        assert 0 <= speed <= 255
        # TODO: convert these to fw and bw
        assert direction in ['fw', 'rv']
        # Let W1, W2, W3, and W4 be the front left, front right, rear left, and rear right wheels, respectively.
        w_id = [2, 3, 1, 4][w_id - 1]
        if w_id in [1, 4]:
            if direction == 'fw':
                direction = 'rv'
            else:
                direction = 'fw'
        # Reassign wheel numbers to accomodate them being switched
        direction = {'fw': 'cw', 'rv': 'ccw'}[direction]
        command = 'go ' + str(w_id) + ' ' + str(speed) + ' ' + direction
        response = self.send('teensy', command)
        assert response == 'ok'

    def set_arm(self, rot):
        '''Move the arm to a position given in raw servo values.

        :warning:
            You probably do not want to call this method directly. Please see
            the documentation on the Arm class which can greately simplify the
            process of programming for the arm. It can help with the translation
            between cartesian coordinates and servo values, and it can also
            handle the interpolation between arm positions.

        :param rot:
            A tuple of length 5 with values between 1 and 180 that specify the
            amount of rotation for each servo in the arm. The servo order is
            (base, shoulder, elbow, wrist, wristrotate).
        :type rot: ``tuple``
        '''
        assert len(rot) == 5
        for r in rot:
            assert 0 <= r <= 180
        command = 'sa %d %d %d %d %d' % tuple(rot)
        response = self.send('mega', command)
        assert response == 'ok'

    def set_suction(self, suction):
        '''Sets the suction power for the arm gripper.

        :param suction:
            0 to 180 where 180 is the most suction. Set back to 0 to release
            suction.
        :type suction: ``int``
        '''
        assert 0 <= suction <= 180
        command = 'ss %d' % suction
        response = self.send('mega', command)
        assert response == 'ok'

    def detach_arm_servos(self):
        command = 'ds'
        response = self.send('mega', command)
        assert response == 'ok'

    def move(self, speed, direction, angular):
        assert 0 <= speed <= 1
        assert -180 <= direction <= 180
        assert -1 <= angular <= 1
        wheels = mecanum.move(speed, direction, angular)
        for w_id, wheel in enumerate(wheels, start=1):
            self.set_wheel(w_id, wheel[0], wheel[1])

    def stop(self):
        self.move(0, 0, 0)

    '''
    def set_servo(self, s_id, pos):
        assert s_id in ['A', 'B']
        assert 0 <= pos <= 255
        command = 'sv ' + s_id + ' ' + str(pos)
        response = self.send(command)
        assert response == 'ok'
    '''

    def set_loader_servos(self, right_pos, left_pos):
        assert 0 <= right_pos <= 255
        assert 0 <= left_pos <= 255
        command = 'sls ' + str(right_pos) + ' ' + str(left_pos)
        response = self.send('mega', command)
        assert response == 'ok'

    def detach_loader_servos(self):
        command = 'dls'
        response = self.send('mega', command)
        assert response == 'ok'

    def open_loader_flap(self):
        '''Set the loader servos to open the flap.
        '''
        self.set_loader_servos(85, 160)

    def close_loader_flap(self):
        '''Set the loader servos to close the flap.
        '''
        self.set_loader_servos(175, 70)

    def get_loader_encoder(self, encoder_id, raw=False):
        assert encoder_id in [0, 1]
        if raw:
            command = 'erp '
        else:
            command = 'ep '
        command += str(encoder_id)
        response = self.send('loadmega', command)
        if raw:
            return long(response)
        else:
            return float(response)

    def zero_loader_encoder(self, encoder_id):
        assert encoder_id in [0, 1]
        command = 'ez %d' % encoder_id
        response = self.send('loadmega', command)
        assert response == 'ok'

    def set_loader_motor(self, m_id, speed, direction):
        assert m_id in [0, 1]
        assert 0 <= speed <= 1024
        assert direction in ['fw', 'bw']
        if m_id == 1:
            direction = {'fw': 'bw', 'bw': 'fw'}[direction]
        command = 'mod ' + str(m_id) + ' ' + str(speed) + ' ' + direction
        response = self.send('loadmega', command)
        assert response == 'ok'

    def stop_loader_motor(self, m_id):
        assert m_id in [0, 1]
        command = 'mos ' + str(m_id)
        response = self.send('loadmega', command)
        assert response == 'ok'

    def startup(self):
        # Make sure we can ping the torso
        self.ping()

        # Flash LED for visual confirmation
        for i in range(3):
            for devname in self.ser.keys():
                self.set_led(devname, True)
            time.sleep(0.05)
            for devname in self.ser.keys():
                self.set_led(devname, False)
            # Don't waste time after the last flash
            if i != 2:
                time.sleep(0.05)

    def close(self):
        '''Close all serial connections and remove locks.

        Failing to call this when you are done with the Spine object will force
        others to manually remove the locks that you created.

        :note:
            If you are using a :func:`get_spine` environment, this method will
            get called automatically during cleanup.
        '''
        for devname in self.ser.keys():
            port = self.ports[devname]
            if self.use_lock:
                fndevname = port.split('/dev/')[1]
                lockfn = '%sLCK..%s' % (self.lock_dir, fndevname)
            self.ser[devname].close()
            logger.info('Closed serial connection %s.' %
                        self.ser[devname].port)
            if self.use_lock:
                os.remove(lockfn)
                logger.info('Removed lock at %s.' % lockfn)
