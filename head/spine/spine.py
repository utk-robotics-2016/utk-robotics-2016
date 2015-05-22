# Global
import time
import signal
import sys

# Third-party
import serial

# Project specific
import mecanum

#DEF_OSX_PORT= '/dev/tty.usbmodem12341'
DEF_LINUX_PORT= '/dev/mega'

class Spine:
    def __init__(self, port, baud=9600, t_out=1, delim='\n'):
        self.ser = serial.Serial(port, baud, timeout=t_out)
        self.delim = delim
        self.compass_tare = 0
        # Hook in SIGINT abort handler for clean aborts
        signal.signal(signal.SIGINT, self.signal_handler)
        # Read in enough bytes to clear the buffer
        self.ser.read(1000)

    def send(self, command):
        self.ser.write(command + self.delim)
        echo = self.ser.readline()
        assert echo == '> ' + command + '\r\n'
        response = self.ser.readline()
        # Be sure to chop off newline. We don't need it.
        return response[:-2]

    def ping(self):
        response = self.send('ping')
        assert response == 'ok'

    def set_led(self, status):
        command = 'le ' + ('on' if status else 'off')
        response = self.send(command)
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
        response = self.send(command)
        assert response == 'ok'

    def set_arm(self, rot):
        assert len(rot) == 5
        for r in rot:
            assert 0 <= r <= 180
        command = 'sa %d %d %d %d %d' % tuple(rot)
        response = self.send(command)
        assert response == 'ok'

    def set_suction(self, suction):
        assert 0 <= suction <= 180
        command = 'ss %d' % suction
        response = self.send(command)
        assert response == 'ok'

    def detach_servos(self):
        command = 'ds'
        response = self.send(command)
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

    def set_servo(self, s_id, pos):
        assert s_id in ['A', 'B']
        assert 0 <= pos <= 255
        command = 'sv ' + s_id + ' ' + str(pos)
        response = self.send(command)
        assert response == 'ok'

    def startup(self):
        # Make sure we can ping the torso
        self.ping()

        # Flash LED for visual confirmation
        for i in range(3):
            self.set_led(True)
            time.sleep(0.05)
            self.set_led(False)
            # Don't waste time after the last flash
            if i != 2:
                time.sleep(0.05)

    def signal_handler(self, signal, frame):
        print '\nCleaning up after unclean exit...'
        self.stop()
        self.close()
        sys.exit(0)

    def close(self):
        self.ser.close()
        print 'Closed serial connection %s.' % self.ser.port
