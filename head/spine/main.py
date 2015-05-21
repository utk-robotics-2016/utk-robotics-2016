# Python modules
import time
# Local modules
import spine
import zones

cur=0
dest=0


# Change this port if not on LINUX
s = spine.Spine(spine.DEF_LINUX_PORT)
s.startup()

#zones.x_return(s, 16, 4, 2)
s.bat()
y=0
x=0
blah = raw_input("Input Y Tick: ")

mouse = file('/dev/input/mouse0')  
s.move(1, 0, 0)
while ((y < blah)):  
    status, dx, dy = tuple(ord(c) for c in mouse.read(3))  
  
    def to_signed(n):  
        return n - ((0x80 & n) << 1)  
          
    dx = to_signed(dx)  
    dy = to_signed(dy)  
    #print "%#02x %d %d" % (status, dx, dy)
    x = x + dx
    y = y + dy

print("Moved X: ")
print(x)
print(" Moved Y:  ")
print(y)
s.move(0,0,0)

#cur=zones.to_zone(s, cur, 1)
#
#print(cur)
#time.sleep(4)
#
#cur=zones.x_slide(s, 4, 4)
#cur=zones.x_slide(s, 1, 3)
#print(cur)
#time.sleep(4)
#
#
#
s.close()
