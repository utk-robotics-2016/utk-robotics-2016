#Modifiers for ticks to inch
#Change when modifiers have been recieved

#mod_a.. refers to the front left dragonball
#mod_b.. refers to the back right dragonball
mod_ax = 5.0
mod_ay = 5.0
mod_by = 4.1
mod_by = 5.3

class OpticalTracker:
    def __init__(self, m_ida, m_idb):
        self.m_ida = m_ida
        self.m_idb = m_idb
        self.mouse_a = file('/dev/input/mouse%d' % m_ida)
        self.mouse_a = file('/dev/input/mouse%d' % m_ida)
        self.x = 0.0
        self.y = 0.0

	def update(self):
        status_a, dx_a, dy_a = tuple(ord(c)) for c in self.mouse_a.read(3))
        status_b, dx_b, dy_b = tuple(ord(c)) for c in self.mouse_b.read(3))
        
        def to_signed(n):
            return n - ((0x80 & n) << 1)

        #Convert the ticks to inches
        dx_a = to_signed(dx_a) #* mod_ax
        dy_a = to_signed(dy_a) #* mod_ay
        dx_b = to_signed(dx_b) #* mod_bx
        dy_b = to_signed(dy_b) #* mod_by

        #Make sure the dxs - dys are roughly the same
        #garbage collection, +/-0.1 inch tolerance

        if (dx_a + 0.1 <= dx_b) and (dx_a - 0.1 >= dx_b) and (dy_a + 0.1 <= dy_b) and (dy_b - 0.1 >= dy_b):
            self.x = self.x + ((dx_a + dx_b) / 2)
            self.y = self.y + ((dy_a + dy_b) / 2)
