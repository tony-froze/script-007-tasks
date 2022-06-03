import logging
import logging.handlers
import os
import sys


def create_logs(logfile, log_level):
    if not os.path.isabs(logfile):
        logfile = os.path.join(os.getcwd(), logfile)
    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(levelname)-7s %(module)s.%(funcName)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            logging.handlers.TimedRotatingFileHandler(filename=logfile, when='midnight'),
                            logging.StreamHandler(sys.stdout)])
