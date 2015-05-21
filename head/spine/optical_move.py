from head.spine import optical
import time

def x_move(s, ticks, direction, speed=0.7):
    assert direction in ['right', 'left']
    tracker = optical.OpticalTracker(0)
    slowdist = 1000
    ticks -= 90
    if direction == 'right':
        angle = -90
        multiplier = 1
    else:
        angle = 90
        multiplier = -1
    s.move(speed, angle, 0)
    slowing = False
    while multiplier * tracker.x < ticks:
        tracker.update()
        if multiplier * tracker.x > ticks-slowdist and not slowing:
            s.move(0.6*speed, angle, 0)
            slowing = True
    s.stop()
    time.sleep(0.1)

def y_move(s, ticks, direction, speed=0.7):
    assert direction in ['fw', 'bw']
    tracker = optical.OpticalTracker(0)
    slowdist = 1000
    ticks -= 400
    if direction == 'fw':
        angle = 0
        multiplier = 1
    else:
        angle = 180
        multiplier = -1
    s.move(speed, angle, 0)
    slowing = False
    while multiplier * tracker.y < ticks:
        tracker.update()
        if multiplier * tracker.y > ticks-slowdist and not slowing:
            s.move(0.6*speed, angle, 0)
            slowing = True
    stoptime = 0.1
    stopspeed = speed/4
    if direction == 'fw':
        s.move_for(stoptime, stopspeed, 180, 0)
    else:
        s.move_for(stoptime, stopspeed, 0, 0)
    s.stop()
    time.sleep(0.1)
