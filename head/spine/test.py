import spine

# Change this port if not on OSX
s = spine.Spine(spine.DEF_OSX_PORT)
s.startup()

while True:
    print s.read_accel()

s.close()
