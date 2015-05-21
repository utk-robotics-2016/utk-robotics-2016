#Throw Out Extraneous DY/DXs
#Optional ATM
#if (dy < 10)

#Linear case
#Using slope from the dy/dx's to assure proper lineup

#self being a property of spine

    self.x = 0 #Set to whatever value for current X/Y position
    self.y = 0
    
    slope = 0 #Slope is registered by the change in X/Y dictated by the direction given

    s.move(speed, dir, 0)

    #Added for tolerance aka Deviation checking
    while (((dir - slope) >= -1) or ((dir - slope) <= 1)):
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
		    dx2 = dx2 + dx
            dy2 = dy2 + dy
            rlist, wlist, elist = select.select([mouse2], [], [], 0.0)
        
        #Update Position
        self.x = (0.5 * (dx1 + dx2)) + self.x 
        self.y = (0.5 * (dy1 + dy2)) + self.y
        #Update 'Slope' for deviation checking
        slope = self.y / self.x
        slope = math.fabs((math.atan2(slope) * 180) / math.pi)
        
        #SUBJECT TO BE MOVED: Check if we've arrived in the target zone
        if((self.x <= target.x + acc_lin) and (self.x >= target.x - acc_lin) and (self.y <= target.y + acc_lin) and (self.y >= target.y - acc_lin)):
            break
		
	s.move(0,0,0)
    print("Gone off course or at destination")
