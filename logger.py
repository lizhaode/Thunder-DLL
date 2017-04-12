# -*- coding:utf-8 -*-
## src/logger.py
##
## put the log information to target file
## This file is part of pyim
## author:jogger0703@@gmail.com

import logging
import logging.handlers
import sys
from inspect import *

class logger(object):
    '''
    put the log information to target file.
    there are few levels for all information.
    '''
    def __init__(self, logpath = 'log'):
        self.path = logpath

    def setlevel(self, level):
        '''
        levels:"debug", "info", "warning", "error", "critical"
        levels: 5       4          3        2       1
        '''
        l = logging.DEBUG
        if level == 'debug' or level == 5:
            l = logging.DEBUG
        elif level == 'info' or level == 4:
            l = logging.INFO
        elif level == 'warning' or level == 3:
            l = logging.WARNING
        elif level == 'error' or level == 2:
            l = logging.ERROR
        elif level == 'critical' or level == 1:
            l = logging.CRITICAL

        self.logger.setLevel(l)

    def log(self, level, line):
        if level == 5:
            self.logger.debug(line)
        elif level == 4:
            self.logger.info(line)
        elif level == 3:
            self.logger.warning(line)
        elif level == 2:
            self.logger.error(line)
        elif level == 1:
            self.logger.critical(line)

    def getpath(self):
        return self.logpath

    def init(self, logpath):
        self.path = logpath
        self.handler = logging.handlers.RotatingFileHandler(logpath)
        fmt = logging.Formatter('%(asctime)s %(name)s-%(message)s')
        self.handler.setFormatter(fmt)
        self.logger = logging.getLogger()
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.DEBUG)

    def quit(self):
        self.logger.shutdown()



glog = logger()
def log_init(path):
    glog.init(path)
    glog.setlevel("debug")

def autolog(level, message):
    "Automatically log the current function details."
    import inspect, logging
    func = inspect.currentframe().f_back.f_code
    text = ("%s:%i - %s" % (
        func.co_filename,
        inspect.currentframe().f_back.f_lineno,
        message
    ))
    print text
    glog.log(level, text)

if __name__ == '__main__':
    log = logger('test.log')
    log.setlevel('debug')
    log.log(4, 'this is info')
    log.log(5, 'this debug')
    log.log(2, 'this error')
    log.setlevel('error')
    log.log(2, 'this error')
    log.log(5, 'this debug too')
