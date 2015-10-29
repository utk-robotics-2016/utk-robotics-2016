import time
import operator
import logging

'''
def keyframe(f, middleargs, seconds, startargs, endargs):
    ramptime = 1
    if seconds < ramptime * 2:
        ramptime = float(seconds) / 2
    start_time = time.time()
    start_difference = map(operator.sub, middleargs, startargs)
    end_difference = map(operator.sub, endargs, middleargs)
    curr_time = time.time()
    iters = 0
    while (curr_time - start_time) < seconds:
        elapsed = curr_time - start_time
        if elapsed < ramptime:
            fraction = elapsed / ramptime
            toadd = [v * fraction for v in start_difference]
            currargs = map(operator.add, startargs, toadd)
        elif elapsed > (seconds - ramptime):
            fraction = (elapsed - (seconds - ramptime)) / ramptime
            toadd = [v * fraction for v in end_difference]
            currargs = map(operator.add, middleargs, toadd)
        else:
            currargs = middleargs
        f(*currargs)
        curr_time = time.time()
        iters += 1
    logging.info("Keyframe iterations: %d", iters)
    f(*endargs)
'''


def defaultCallback():
    return True


def keyframe(f, startargs, endargs, seconds, callback=defaultCallback):
    start_time = time.time()
    difference = map(operator.sub, endargs, startargs)
    curr_time = time.time()
    iters = 0
    while (curr_time - start_time) < seconds and callback():
        elapsed = curr_time - start_time
        fraction = elapsed / seconds
        toadd = [v * fraction for v in difference]
        currargs = map(operator.add, startargs, toadd)
        f(*currargs)
        curr_time = time.time()
        iters += 1
    logging.info("Key frame iterations: %d", iters)
    f(*endargs)


def trapezoid(f, startargs, middleargs, endargs, totaltime, rampuptime=1.0, rampdowntime=1.0, callback=defaultCallback):
    constanttime = totaltime - rampdowntime - rampuptime
    keyframe(f, startargs, middleargs, rampuptime, callback)
    keyframe(f, middleargs, middleargs, constanttime, callback)
    keyframe(f, middleargs, endargs, rampdowntime, callback)