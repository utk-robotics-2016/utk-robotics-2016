# Global
import time
import signal
import sys
import os

# Third-party
import serial

# Project specific
import mecanum

DEF_PORTS = {
    'mega': '/dev/mega',
    'teensy': '/dev/teensy',
}

class SerialLockException(Exception):
    pass

class Spine:
    def __init__(self, t_out=1, delim='\n', **kwargs):
        self.ser = {}
        self.use_lock = kwargs.get('use_lock', True)
        self.lock_dir = kwargs.get('lock_dir', '/var/lock/')
        self.ports = kwargs.get('ports', DEF_PORTS)
        for devname, port in self.ports.iteritems():
            if self.use_lock:
                fndevname = port.split('/dev/')[1]
                lockfn = '%sLCK..%s' % (self.lock_dir, fndevname)
                if os.path.isfile(lockfn):
                    self.close()
                    raise SerialLockException("Lockfile %s exists. It's possible that someone is using this serial port. If not, remove this lock file. Closing and raising error." % lockfn)
            self.ser[devname] = serial.Serial(port, 115200, timeout=t_out)
            if self.use_lock:
                with open(lockfn, 'w') as f:
                    f.write('-1')
        self.delim = delim
        self.compass_tare = 0
        self.loglevel = 0
        # Hook in SIGINT abort handler for clean aborts
        signal.signal(signal.SIGINT, self.signal_handler)
        # Read in enough bytes to clear the buffer
        for devname in self.ser.keys():
            self.ser[devname].read(1000)

    def set_log_level(self, level):
        self.loglevel = level

    def send(self, devname, command):
        if self.loglevel:
            print "Sending '%s' to '%s'" % (command, devname)
        self.ser[devname].write(command + self.delim)
        echo = self.ser[devname].readline()
        assert echo == '> ' + command + '\r\n'
        response = self.ser[devname].readline()
        if self.loglevel:
            print "Response: '%s'" % response[:-2]
        # Be sure to chop off newline. We don't need it.
        return response[:-2]

    def ping(self):
        for devname in self.ser.keys():
            response = self.send(devname, 'ping')
            assert response == 'ok'

    def set_led(self, devname, status):
        command = 'le ' + ('on' if status else 'off')
        response = self.send(devname, command)
        assert response == 'ok'

    def move_for(self, delay, *args):
        self.move(*args)
        time.sleep(delay)
        self.stop()

    def set_wheel(self, w_id, speed, direction):
        assert w_id in [1, 2, 3, 4]
        assert 0 <= speed <= 255
        # TODO: convert these to fw and bw
        assert direction in ['fw', 'rv']
        if w_id in [3, 4]:
            if direction == 'fw':
                direction = 'rv'
            else:
                direction = 'fw'
        # Reassign wheel numbers to accomodate them being switched
        w_id = [2,4,1,3][w_id-1]
        direction = {'fw': 'cw', 'rv': 'ccw'}[direction]
        command = 'go ' + str(w_id) + ' ' + str(speed) + ' ' + direction
        response = self.send('teensy', command)
        assert response == 'ok'

    def set_arm(self, rot):
        assert len(rot) == 5
        for r in rot:
            assert 0 <= r <= 180
        command = 'sa %d %d %d %d %d' % tuple(rot)
        response = self.send('mega', command)
        assert response == 'ok'

    def set_suction(self, suction):
        assert 0 <= suction <= 180
        command = 'ss %d' % suction
        response = self.send('mega', command)
        assert response == 'ok'

    def detach_servos(self):
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

    def signal_handler(self, signal, frame):
        print '\nCleaning up after unclean exit...'
        self.stop()
        self.close()
        sys.exit(0)

    def close(self):
        for devname in self.ser.keys():
            port = self.ports[devname]
            if self.use_lock:
                fndevname = port.split('/dev/')[1]
                lockfn = '%sLCK..%s' % (self.lock_dir, fndevname)
            self.ser[devname].close()
            if self.use_lock:
                os.remove(lockfn)
            print 'Closed serial connection %s.' % self.ser[devname].port
