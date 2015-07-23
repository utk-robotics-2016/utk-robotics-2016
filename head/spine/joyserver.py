import Pyro.core

import spine

s = spine.Spine(spine.DEF_LINUX_PORT)
s.startup()


class JokeGen(Pyro.core.ObjBase):

    def __init__(self):
        Pyro.core.ObjBase.__init__(self)

    def joke(self, name):
        return "Sorry " + name + ", I don't know any jokes."


class JoyServer(Pyro.core.ObjBase):

    def __init__(self):
        Pyro.core.ObjBase.__init__(self)

    def move(self, speed, direction, angular):
        print speed, direction, angular
        s.move(speed, direction, angular)


Pyro.core.initServer()
daemon = Pyro.core.Daemon()
uri = daemon.connect(JokeGen(), "jokegen")
uri = daemon.connect(JoyServer(), "joyserver")

print "The daemon runs on port:", daemon.port
print "The object's uri is:", uri

daemon.requestLoop()

s.close()
