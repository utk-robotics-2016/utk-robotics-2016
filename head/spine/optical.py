# Be sure to 'xinput --list'
# export DISPLAY=:0
# xinput set-int-prop 13 "Device Enabled" 8 0

class OpticalTracker:
    def __init__(self, m_id):
        self.m_id = m_id
        self.mouse = file('/dev/input/mouse%d' % m_id)
        self.x = 0.0
        self.y = 0.0

    def update(self):
        status, dx, dy = tuple(ord(c) for c in self.mouse.read(3))
    
        def to_signed(n):
            return n - ((0x80 & n) << 1)
            
        dx = to_signed(dx)
        dy = to_signed(dy)
        self.x += dx
        self.y += dy
