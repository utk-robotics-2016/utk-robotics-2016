#Linear case
#Using slope from the dy/dx's to assure proper lineup
#This assumes there is no rotation going on, however the robot DOES NOT have
#to be facing the direction of travel for this to still be effective

import spine
import math
import select
import time

mouse1 = open('/dev/input/mouse1') #front mouse
mouse2 = open('/dev/input/mouse2') #rear mouse

s = spine.Spine(spine.DEF_LINUX_PORT)
s.startup()

#self being a property of spine
 
selfx = 0 
selfy = 0
targetx = -5000
targety = -5000
acc_lin = 500

def to_signed(n):  
    return n - ((0x80 & n) << 1) 

dir = ((math.atan2((targety - selfy),(targetx - selfx)) * 180) / math.pi) - 90
speed = 0.5
facing = 0
dx = 0
dy = 0
dx1 = 0
dx2 = 0
dy1 = 0
dy2 = 0
deviation = 0
ratio = 855.8 / 382.6
    
slope = 0 #Slope is registered by the change in X/Y dictated by the direction given

s.move(speed, dir, 0)

#Added for tolerance aka Deviation checking
while True:
    dx = 0
    dy = 0
    print "Intended Direction: %d" % (dir)
    print "Target X: %d Target Y: %d" % (targetx, targety)
    print "Cur X: %d Cur Y: %d" % (selfx, selfy)
    #read mouse1 if it's ready
    rlist, wlist, elist = select.select([mouse1], [], [], 0.0)
    while rlist:
        status, dx, dy = tuple(ord(c) for c in mouse1.read(3))
        dx = to_signed(dx) * ratio
        dy = to_signed(dy) * ratio
        dx1 = dx1 + dx
        dy1 = dy1 + dy
        print "DX: %d DY: %d" % (dx, dy)
        rlist, wlist, elist = select.select([mouse1], [], [], 0.0)
    #read mouse2 if it's ready
    rlist, wlist, elist = select.select([mouse2], [], [], 0.0)
    while rlist:
        status, dx, dy = tuple(ord(c) for c in mouse2.read(3))
        dx = to_signed(dx) * ratio 
        dy = to_signed(dy) * ratio
        dx2 = dx2 + dx
        dy2 = dy2 + dy
        rlist, wlist, elist = select.select([mouse2], [], [], 0.0)

    #Update Position via system
    selfx = (0.5 * (dx1 + dx2))
    selfy = (0.5 * (dy1 + dy2))
    #Update 'Slope' for deviation checking
    slope = math.fabs((math.atan2(selfy,selfx) * 180) / math.pi)
	
    #slope = slope + (dir - facing)
    deviation = dir - slope
    print "Slope: %d Deviation: %d" % (slope, deviation)
    #SUBJECT TO BE MOVED: Check our deviation and adjust 'rough' PID style
    if(deviation <= -1):
        #insert rotational adjustment
        s.move(speed, dir + 5, 0)
    if(deviation >= 1):
        #insert rotational adjustment
        s.move(speed, dir - 5, 0)

    #SUBJECT TO BE MOVED: If the deviation checks out then, no adjustments
    if(math.fabs(dir - slope) <= 1):
        s.move(speed, dir, 0)

    #SUBJECT TO BE MOVED: Check if we've arrived in the target zone
    if((selfx <= targetx + acc_lin) and (selfx >= targetx - acc_lin) and (selfy <= targety + acc_lin) and (selfy >= targety - acc_lin)):
    #if((math.fabs(selfx) > math.fabs(targetx)) and (math.fabs(selfy) > math.fabs(targety))):
        break



s.move(0,0,0)
print("Gone off course or at destination")