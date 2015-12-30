import Pyro4

from head.spine.core import get_spine
from head.spine.arm import Arm
from head.spine.loader import Loader


with get_spine() as s:

    arm = Arm(s)
    ldr = Loader(s)

    class JoyServer(object):

        def move(self, speed, direction, angular):
            print 'move', speed, direction, angular
            s.move(speed, direction, angular)

        def load(self):
            print 'load'
            ldr.load()
            print 'load done'

        def arm_set_pos(self, cuppos, wrist, wristrotate):
            print 'arm_set_pos', cuppos, wrist, wristrotate
            arm.set_pos(cuppos, wrist, wristrotate)

        def arm_park(self, seconds):
            print 'arm_park', seconds
            arm.park(seconds)

        def set_suction(self, suction):
            print 'suction', suction
            s.set_suction(suction)

    daemon = Pyro4.Daemon(host='0.0.0.0', port=9091)
    uri = daemon.register(JoyServer())

    print "The object's uri is:", uri
    print "The object's remote uri is:", str(uri).replace('0.0.0.0', 'ieeebeagle.nomads.utk.edu')

    daemon.requestLoop()
