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
targetx = 5000
targety = 5000
acc_lin = 500

def to_signed(n):  
    return n - ((0x80 & n) << 1) 

dir = ((math.atan2((targety - selfy),(targetx - selfx)) * 180) / math.pi)
motor_dir = -dir
speed = 0.75
facing = 0
ang_adj = 0
dx = 0
dy = 0
dx1 = 0
dx2 = 0
dy1 = 0
dy2 = 0
dif = 0

#offsets in inches from the center of each mouse is mounted relative to the center of the robot
#right is +x
#forward is +y
m1_x = -3.25
m1_y = 2.625
m2_x = 0.0 - m1_x #assumed
m2_y = 0.0 - m1_y #assumed

#radii of mice from center
r1 = math.sqrt((m1_x * m1_x) + (m1_y * m1_y))
r2 = math.sqrt((m2_x * m2_x) + (m2_y * m2_y))
r_avg = 0.5 * (r1 + r2)

circum = 2 * math.pi * r_avg

deviation = 0
ratio = 855.8 / 382.6 #Mouse DPI ratios between the two
    
slope = 0 #Slope is registered by the change in X/Y dictated by the direction given

if(motor_dir > 180):
    motor_dir -= 360
elif(motor_dir < -180):
    motor_dir += 360

s.move(speed, motor_dir, 0)

count = 0
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
        dx = to_signed(dx) #* ratio
        dy = to_signed(dy) #* ratio
        dx1 = dx1 + dx
        dy1 = dy1 + dy
        print "DX1: %d DY1: %d" % (dx, dy)
        dif = dx
        rlist, wlist, elist = select.select([mouse1], [], [], 0.0)
    #read mouse2 if it's ready
    rlist, wlist, elist = select.select([mouse2], [], [], 0.0)
    while rlist:
        status, dx, dy = tuple(ord(c) for c in mouse2.read(3))
        dx = to_signed(dx) * ratio 
        dy = to_signed(dy) * ratio
        dx2 = dx2 + dx
        dy2 = dy2 + dy
        print "DX2: %d DY2: %d" % (dx, dy)
        rlist, wlist, elist = select.select([mouse2], [], [], 0.0)

    #Update Position via system
    selfx = (0.5 * (dx1 + dx2))
    selfy = (0.5 * (dy1 + dy2))
    #Update 'Slope' for deviation checking
    slope = math.fabs((math.atan2(selfy,selfx) * 180) / math.pi)
	
    #slope = slope + (dir - facing)
    deviation = slope - dir
	
	
    print "Slope: %d Deviation: %d" % (slope, deviation)
    #SUBJECT TO BE MOVED: Check our deviation and adjust 'rough' PID style
    if(deviation <= -1):
        #motor_dir = motor_dir + (deviation/2)
        #insert rotational adjustment	
        s.move(speed, motor_dir + (deviation/2), 0)
    if(deviation >= 1):
        #motor_dir = motor_dir - (deviation/2)
        #insert rotational adjustment
        s.move(speed, motor_dir - (deviation/2), 0)

    #dif = dif / dx
    print "Dif: %d" % (dif)

    #Dif of each DXs to determine rotation and compensate
    #if((dif < -1) or (0 < dif < 1)):
    #    ang_adj = 0.1
    #if((dif > 1) or (-1 < dif < 0)):
    #    ang_adj = -0.1	

    #s.move(speed, motor_dir, 0)

    #Rotational checking
    #Mouse 1 Check
    tang_x = selfx - dx1
    tang_y = selfy - dy1
    mouse_hyp1 = math.sqrt((tang_x*tang_x)+(tang_y*tang_y))
    mouse_rot1 = 360 * mouse_hyp1 * circum
    if(tang_x > 0):
        mouse_rot1 = -mouse_rot1

    #Mouse 2 Check
    tang_x = selfx - dx2
    tang_y = selfy - dy2
    mouse_hyp2 = math.sqrt((tang_x*tang_x)+(tang_y*tang_y))
    mouse_rot2 = 360 * mouse_hyp2 * circum
    if(tang_x < 0):
        mouse_rot2 = -mouse_rot2	

    print "Mouse1: %d Mouse2: %d" % (mouse_rot1, mouse_rot2)

    #SUBJECT TO BE MOVED: If the deviation checks out then, no adjustments
    if(math.fabs(dir - slope) <= 1):
        s.move(speed, motor_dir, 0)

    #SUBJECT TO BE MOVED: Check if we've arrived in the target zone
    if((selfx <= targetx + acc_lin) and (selfx >= targetx - acc_lin) and (selfy <= targety + acc_lin) and (selfy >= targety - acc_lin)):
    #if((math.fabs(selfx) > math.fabs(targetx)) and (math.fabs(selfy) > math.fabs(targety))):
        break
		
    if(count >= 190):
        break
    count+=1
    print "\n"


s.move(0,0,0)
print("Gone off course or at destination")
