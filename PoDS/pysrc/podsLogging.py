#!/usr/bin/env python
"""
  Utilities for logging

"""
from __future__ import print_function
import os
import sys
import logging

logger = logging.getLogger('pods_logging')

#------------------------------------------------------------------------------
#---- logger_setup
#------------------------------------------------------------------------------
def logger_setup(filename):
    # extract the file name without the extension
    logger_name = os.path.splitext(filename)[0]

    # log messages to a file
    logging.basicConfig(
        filename = logger_name + '.LOG',
        #format   = "%(levelname)s %(module)s:%(lineno)s %(funcName)s %(message)s",
        format   = "%(levelname)s %(module)s:%(lineno)s %(message)s",
        level    = logging.DEBUG,
        filemode = 'w')

    ## Add a stream handler (using stdout) to default logger
    #stdout_log = logging.StreamHandler(sys.stdout)

    ## Set level to INFO
    #stdout_log.setLevel(logging.INFO)
    #formatter = logging.Formatter('%(levelname)s %(name)s : %(message)s')
    #stdout_log.setFormatter(formatter)
    #root = logging.getLogger()
    #root.addHandler(stdout_log)
