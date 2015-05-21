#uses one mouse and a compass to make controlled movements

import math
import select
import time

mouse = open('/dev/input/mouse0')

#spine.read_compass(s)

#shorthand functions
def rot_mov(s, rot, deg): #rot is angular speed [-1 - 1](signed), deg is desired rotation in degrees (absolute)
    ctrl_move(s, 0, 0, rot, deg)
def lin_mov(s, speed, dir, dist): #dist in inches
    ctrl_move(s, speed, dir, 0, dist)

def ctrl_move(s, speed, dir, rot, dist): #dist in inches if linear, degrees if rotational
#do not use this function with both linear motion and rotational motion; use one or the other
#i.e., either rot or speed should be zero
    
    dist = math.fabs(dist)
    
    #set distance moved to 0
    dx1 = 0.0
    dy1 = 0.0
    dx2 = 0.0
    dy2 = 0.0
    
#read until end of stream; skip past old mouse readings that occurred between calls of ctrl_move()
#to-do: eliminate/reduce system calls here
    rlist, wlist, elist = select.select([mouse], [], [], 0.0)
    while rlist:
        mouse.read(3)
        rlist, wlist, elist = select.select([mouse], [], [], 0.0)
    
    #adjustment factors
    near = 1.0
    invert = 1.0
    lateral = 0.0
    spin = 0.0
    
    #set distance moved to 0
    dx1 = 0.0
    dy1 = 0.0
    dx2 = 0.0
    dy2 = 0.0
    
    #get original heading
    init_dir = spine.read_compass(s)
    
    #make dist absolute
    dist = math.fabs(dist)
    
    if rot == 0 and speed != 0: #linear case
        s.move(speed, dir, 0)
        
    elif rot != 0 and speed == 0: #rotational case
        s.move(0,0, rot)
        
        if rot < 0.0:
            target = init_dir + dist
            if target > 360.0:
                target -= 360.0
        else:
            target = init_dir - dist
        
        while True:
            s.move(0,0, (rot * invert * near))
            time.sleep(0.025)
            
            #read mouse
            
            #if passed, invert
            
            #if near, half
            #if in target, break
        
    else:
        print "Err: ctrl_move called with both linear and rotational parts"
    s.move(0,0,0)
    return