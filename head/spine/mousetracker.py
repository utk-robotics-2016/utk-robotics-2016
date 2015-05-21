import math
import select
import time

mouse1 = open('/dev/input/mouse0') #front mouse
mouse2 = open('/dev/input/mouse2') #rear mouse

acc_lin = 250.0 #desired accuracy in pixels.  Getting this close to the goal is "good enough"
acc_rot = 150.0

min_speed = 0.35 #minimum linear or angular speed for motion
interval = 0.1 #time between reads/course corrections

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

#pixels per inch
dist_factor_1 = 855.812 #863.74, 855.74, 847.73
dist_factor_2 = 855.8 #382.658 #403.45, 384.75, 359.78
ratio = dist_factor_1 / dist_factor_2
dist_factor = dist_factor_1 #900.0 #temporary value, to be determined

def to_signed(n):  
    return n - ((0x80 & n) << 1) 

#shorthand functions
def rot_mov(s, rot, deg): #rot is angular speed (signed), deg is desired rotation (absolute)
    ctrl_move(s, 0, 0, rot, deg)
def lin_mov(s, speed, dir, dist): #dist in inches
    ctrl_move(s, speed, dir, 0, dist)
    
def ctrl_move(s, speed, dir, rot, dist): #dist in inches if linear, degrees if rotational
#do not use this function with both linear motion and rotational motion; use one or the other
#i.e., either rot or speed should be zero
    
    dist = math.fabs(dist)
    invert = 1.0 #set to -1 if we've moved too far
    
#read until end of stream; skip past old mouse readings that occurred between calls of ctrl_move()
#to-do: eliminate/reduce system calls here
#    rlist, wlist, elist = select.select([mouse1], [], [], 0.0)
#    while rlist:
#        mouse1.read(3)
#        rlist, wlist, elist = select.select([mouse1], [], [], 0.0)
#    rlist, wlist, elist = select.select([mouse2], [], [], 0.0)
#    while rlist:
#        mouse2.read(3)
#        rlist, wlist, elist = select.select([mouse2], [], [], 0.0)
 
#seek to end of stream
    mouse1.seek(0,2)
    mouse2.seek(0,2)
 
#set distance moved to 0
    dx1 = 0.0
    dy1 = 0.0
    dx2 = 0.0
    dy2 = 0.0
    
    if rot == 0 and speed != 0:
        #linear case
        speed = max(speed, min_speed)
        s.move(speed, dir, 0)
        
        near = 1.0
        invert = 0.0
        lateral = 0.0
        spin = 0.0
        
        target_x = dist * dist_factor * math.sin(math.radians(dir))
        target_y = dist * dist_factor * math.cos(math.radians(dir))
        
        X = 0.0
        
        while True:
            time.sleep(interval)
            print "\nTop of loop: \ndx1: ", dx1, "\ndy1: ", dy1, "\ndx2: ", dx2, "\ndy2: ", dy2, "\nnear: ", near, "\ninvert: ", invert, "\nlateral: ", lateral, "\nspin: ", spin
            
            ax = (0.5 * (dx1 + dx2))
            ay = (0.5 * (dy1 + dy2))
            
            if lateral or spin:
                X += 1.0
            if X >= 10:
                break
            
            #issue corrective move
            if lateral != 0.0:
                temp = ((ax * ax) + (ay * ay)) - (lateral * lateral)
                print "\tTemp: ", temp
                temp = math.fabs(temp)
                tA = ((dist * dist_factor) - math.sqrt(temp))
                tC = math.sqrt((tA * tA) + (lateral * lateral))
                angle = math.asin(lateral / tC) * 180.0 / math.pi
                #angle = (math.asin(math.fabs(lateral)/math.sqrt((ax * ax) + (ay * ay))) * 180.0 / math.pi)
                if lateral > 0:
                    angle = angle * -1.0
            else:
                angle = 0.0
            
            if spin != 0.0:
                #tA = ((dist * dist_factor) - math.sqrt(((ax * ax) + (ay * ay)) - (lateral * lateral)))
                #tC = math.sqrt((tA * tA) + (lateral * lateral))
                c_rot = 0.1 #temporary
                if spin > 0.0:
                    c_rot = 0.0 - c_rot
            else:
                c_rot = 0.0
            
            c_speed = (speed * near)
            c_speed = max(c_speed, min_speed)
            
            c_dir = dir + angle
            if c_dir > 180.0:
                c_dir -= 360.0
            if c_dir < -180.0:
                c_dir += 360.0
            if invert:
                cdir += 180
            if c_dir > 180.0:
                c_dir -= 360.0
            
            print "s.move(",c_speed, ",", c_dir, ",", c_rot, ")"
            s.move(c_speed, c_dir, c_rot)
            
            #read mouse1 if it's ready
            rlist, wlist, elist = select.select([mouse1], [], [], 0.0)
            while rlist:
                status, dx, dy = tuple(ord(c) for c in mouse1.read(3))
                dx = to_signed(dx)
                dy = to_signed(dy)
                dx1 = dx1 + dx
                dy1 = dy1 + dy
                rlist, wlist, elist = select.select([mouse1], [], [], 0.0)
            #read mouse2 if it's ready
            rlist, wlist, elist = select.select([mouse2], [], [], 0.0)
            while rlist:
                status, dx, dy = tuple(ord(c) for c in mouse2.read(3))
                dx = to_signed(dx)
                dy = to_signed(dy)
                dx *= ratio
                dy *= ratio
                dx2 = dx2 + dx
                dy2 = dy2 + dy
                rlist, wlist, elist = select.select([mouse2], [], [], 0.0)
            
            #half speed if close
            #if (dist - 2500) <= math.sqrt((((0.5 * (dy1 + dy2)) * (0.5 * (dx1 + dx2))) + ((0.5 * (dx1 + dx2)) * (0.5 * (dx1 + dx2))))) <= (dist + 2500):
            if ((target_x - 2500) <= (0.5 * (dx1 + dx2)) <= (target_x + 2500)) and ((target_y - 2500) <= (0.5 * (dy1 + dy2)) <= (target_y + 2500)):
                near = 0.5
                #break
            else:
                near = 1.0
                
            #reverse direction if passed
            if (((dist + acc_lin) < math.sqrt((((0.5 * (dy1 + dy2)) * (0.5 * (dy1 + dy2))) + ((0.5 * (dx1 + dx2)) * (0.5 * (dx1 + dx2))))) and (invert == 1.0))):
                invert = 1.0
            if (((dist - acc_lin) > math.sqrt((((0.5 * (dy1 + dy2)) * (0.5 * (dy1 + dy2))) + ((0.5 * (dx1 + dx2)) * (0.5 * (dx1 + dx2))))) and (invert == 0.0))):
                invert = 0.0
            
            #break if in target zone
            if ((target_x - acc_lin) <= (0.5 * (dx1 + dx2)) <= (target_x + acc_lin)) and ((target_y - acc_lin) <= (0.5 * (dy1 + dy2)) <= (target_y + acc_lin)):
                break
            
            #find midpoint of x, y
            ax = (0.5 * (dx1 + dx2))
            ay = (0.5 * (dy1 + dy2))
            
            #default no-adjustment values
            lateral = 0.0
            spin = 0.0
            
            #no adjustments unless significantly out of line
            if ((math.fabs(dx1) + math.fabs(dx2)) > acc_lin):
                #if x1, x2 have same sign; sliding laterally
                #if (((dx1 > 0.0) and (dx2 > 0.0)) or ((dx1 < 0.0) and (dx2 < 0.0))):
                #lateral = ax
                target_angle = math.radians(dir + 90)
                current_angle = math.atan(ay / ax)
                tc = math.sqrt((ax * ax) + (ay * ay))
                tb = tc * math.sin(target_angle - current_angle)
                lateral = tc
                
                #x1, x2 have differing signs; rotating
                #else:
                
                #measure CCW spin (positive angular direction)
                rot1x = ax - dx1
                rot1y = ay - dy1
                rot2x = dx2 - ax
                rot2y = dy2 - ay
                
                rot1 = math.sqrt((rot1x * rot1x) + (rot1y * rot1y))
                rot2 = math.sqrt((rot2x * rot2x) + (rot2y * rot2y))
                
                #spin = (((0.5 * (rot1 + rot2))/(2 * math.pi * r1)) * 360)
                spin = (((rot1 + rot2)/(math.pi * r_avg)) * 90)
        
        
    elif rot != 0 and speed == 0:
        #rotational case
        if 0 < rot < min_speed:
            rot = min_speed
        elif (-1.0 * min_speed) < rot < 0:
            rot = (-1.0 * min_speed)
        s.move(0,0, rot)
        
        target = (dist * dist_factor / 180.0) * (math.pi * r_avg)
        
        while (target - (0.5 * (math.sqrt((dx1 * dx1) + (dy1 * dy1)) + math.sqrt((dx2 * dx2) + (dy2 * dy2))))) > 2000:
            #while distance to move is > 2000
            #"far" loop
            
            #read mouse1 if it's ready
            rlist, wlist, elist = select.select([mouse1], [], [], 0.0)
            while rlist:
                status, dx, dy = tuple(ord(c) for c in mouse1.read(3))
                dx = to_signed(dx)
                dy = to_signed(dy)
                #dx *= math.sqrt(2)
                #dy *= math.sqrt(2)
                dx1 = dx1 + dx
                dy1 = dy1 + dy
                rlist, wlist, elist = select.select([mouse1], [], [], 0.0)
            #read mouse2 if it's ready
            rlist, wlist, elist = select.select([mouse2], [], [], 0.0)
            while rlist:
                status, dx, dy = tuple(ord(c) for c in mouse2.read(3))
                dx = to_signed(dx)
                dy = to_signed(dy)
                #dx *= math.sqrt(2)
                #dy *= math.sqrt(2)
                dx *= ratio
                dy *= ratio
                dx2 = dx2 + dx
                dy2 = dy2 + dy
                rlist, wlist, elist = select.select([mouse2], [], [], 0.0)
            
            
        if (0.5 * (math.sqrt((dx1 * dx1) + (dy1 * dy1)) + math.sqrt((dx2 * dx2) + (dy2 * dy2)))) > target:
            #moved too far
            invert = -1.0
        
        while True:
            #"near" loop
            
            c_rot = (invert * (rot / 2))
            if 0 < c_rot < min_speed:
                c_rot = min_speed
            elif (-1.0 * min_speed) < c_rot < 0:
                c_rot = (-1.0 * min_speed)
            s.move(0,0, c_rot) #move half speed in appropriate direction
            
            #read mouse1 if it's ready
            rlist, wlist, elist = select.select([mouse1], [], [], 0.0)
            while rlist:
                status, dx, dy = tuple(ord(c) for c in mouse1.read(3))
                dx = to_signed(dx)
                dy = to_signed(dy)
                dx1 = dx1 + dx
                dy1 = dy1 + dy
                rlist, wlist, elist = select.select([mouse1], [], [], 0.0)
            #read mouse2 if it's ready
            rlist, wlist, elist = select.select([mouse2], [], [], 0.0)
            while rlist:
                status, dx, dy = tuple(ord(c) for c in mouse2.read(3))
                dx = to_signed(dx)
                dy = to_signed(dy)
                dx *= ratio
                dy *= ratio
                dx2 = dx2 + dx
                dy2 = dy2 + dy
                rlist, wlist, elist = select.select([mouse2], [], [], 0.0)
            
            if (invert == 1):
            #moving "forward"
                if (target - acc_rot) <= (0.5 * (math.sqrt((dx1 * dx1) + (dy1 * dy1)) + math.sqrt((dx2 * dx2) + (dy2 * dy2)))):
                #moved at least into target zone
                    if (target + acc_rot) >= (0.5 * (math.sqrt((dx1 * dx1) + (dy1 * dy1)) + math.sqrt((dx2 * dx2) + (dy2 * dy2)))):
                    #not moved out of target zone
                        break
                    else:
                    #moved past target zone
                        invert = -1
                #else:
                #not moved into target zone yet
                
            else:
            #moving "backward"
                if (target - acc_rot) >= (0.5 * (math.sqrt((dx1 * dx1) + (dy1 * dy1)) + math.sqrt((dx2 * dx2) + (dy2 * dy2)))):
                #moved at least into target zone
                    if (target - acc_rot) <= (0.5 * (math.sqrt((dx1 * dx1) + (dy1 * dy1)) + math.sqrt((dx2 * dx2) + (dy2 * dy2)))):
                    #not moved out of target zone
                        break
                    else:
                    #moved past target zone
                        invert = 1
                #else:
                #not moved into target zone yet
            #
            
            
    else:
        print "Err: ctrl_move called with both linear and rotational parts"
    s.move(0,0,0)
    return
    
