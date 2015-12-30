# Python modules
#import time
# Local modules
import spine
#import zones
import mousetracker

cur = 0
dest = 0

# Change this port if not on LINUX
s = spine.Spine(spine.DEF_LINUX_PORT)
s.startup()

# while True:
#    input('>')

#mouse = open('/dev/input/mouse0')

#mousetracker.rot_mov(s, 0.5, 360)
mousetracker.lin_mov(s, 1, 0, 20.0)

import select

y = 0
x = 0


s.move(1, 0, 0)

mouse = open('/dev/input/mouse1')
while True:
    break
    # only read if data exists to be read, otherwise loop
#    rlist, wlist, elist = select.select([mouse], [], [], 0.0)
#    while not rlist:
#        rlist, wlist, elist = select.select([mouse], [], [], 0.0)
#        print("Mouse not ready to read yet")
    status, dx, dy = tuple(ord(c) for c in mouse.read(3))

    def to_signed(n):
        return n - ((0x80 & n) << 1)

    dx = to_signed(dx)
    dy = to_signed(dy)
    print "%#02x %d %d" % (status, dx, dy)
    x = x + dx
    y = y + dy
    print "%d %d" % (x, y)

    if y > 50000:
        break

#    break


s.move(0, 0, 0)
#print("Moved X: ")
# print(x)
#print(" Moved Y:  ")
# print(y)
