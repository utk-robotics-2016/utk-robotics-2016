import time
import operator
import logging


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
