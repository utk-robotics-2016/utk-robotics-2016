import time
import operator
import logging


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
    assert constanttime > 0
    keyframe(f, startargs, middleargs, rampuptime, callback)
    keyframe(f, middleargs, middleargs, constanttime, callback)
    keyframe(f, middleargs, endargs, rampdowntime, callback)
