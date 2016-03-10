import logging
import logging.handlers
import os
import sys


class GroupWriteRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def _open(self):
        # prevumask = os.umask(0o022)
        prevumask = os.umask(0o000)
        # os.fdopen(os.open('/path/to/file', os.O_WRONLY, 0600))
        rtv = logging.handlers.RotatingFileHandler._open(self)
        os.umask(prevumask)
        return rtv


def setup_logging(fn):

    fmt = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    logfn = '/var/log/spine/%s.log' % os.path.split(fn)[-1].split('.')[0]
    # fh_ = logging.FileHandler('/var/log/spine/%s.log' % os.path.split(__file__)[-1])
    fh_ = GroupWriteRotatingFileHandler(logfn, maxBytes=1024 * 1024 * 5, backupCount=10)
    fh_.setLevel(logging.DEBUG)
    # Normally our Python scripts steady-state at 3.8%. With memory log buffering, this will increase.
    # Can be 5.0% after running arm_test.py now.
    fh = logging.handlers.MemoryHandler(1024 * 1024 * 10, logging.ERROR, fh_)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(fmt)
    ch.setFormatter(formatter)
    fh_.setFormatter(formatter)

    # add the handlers to logger
    # logger.addHandler(ch)
    # logger.addHandler(fh)
    root.addHandler(ch)
    root.addHandler(fh)

    def my_excepthook(excType, excValue, traceback, logger=logging):
        logger.error("Logging an uncaught exception",
                     exc_info=(excType, excValue, traceback))

    sys.excepthook = my_excepthook
