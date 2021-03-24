#!/usr/bin/env python

import os


def runningTasks(line, workDir):
    """
      Determines the number of tasks currently running.
     
      Required arguments:
        - line:    a list containing the list of available nodes
        - workDir: working directory

      Returned value:
        - an integer giving the number of tasks running
    """
    numCurTasks = 0
    for nodeName in line:
        dirName = os.path.join(workDir, nodeName.strip())
        numCurTasks += len(os.listdir(dirName))
    return numCurTasks
