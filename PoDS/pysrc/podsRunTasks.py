#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import time
import subprocess
import logging

import podsNumRunningTasks

logger = logging.getLogger(__name__)

def runTasks(STAT_DIR, fileName, listNodes, listTasks, numCoresPerNode, 
             podSrcDIR, my_env): 
  """
    Loop until all individual tasks have been launched.

    Required arguments:
      - STAT_DIR:        directory name
      - fileName:        file to record timing statistics
      - listNodes:       list of available nodes
      - listTasks:       list of available tasks
      - numCoresPerNode: a list containing the number of codes for each node
      - podSrcDIR:       source directory for PoDS
      - my_env:          environment variables
  """

  # Write the environment dictionary as a string
  #---------------------------------------------
  podsEnv = " "
  if (my_env):
     for e in my_env:
         if (my_env[e].strip() != ""):
             podsEnv += str(e).strip() + "___ " + str(my_env[e]) + " "

  # Determine the total number of nodes
  #------------------------------------
  totNumNodes = len(listNodes)

  # Determine the total number of tasks
  #------------------------------------
  totNumTasks = len(listTasks)

  ne = 0

  logger.info("Total number of nodes:    %d" %(totNumNodes))
  for i in range(len(listNodes)):
      logger.info("   --<> Node %s has %d cores" %(listNodes[i], numCoresPerNode[i]))

  taskIndex = 1
  while (taskIndex <= totNumTasks):

     # Loop over all of the available nodes
     #-------------------------------------
     nodeIndex = 1
     while (nodeIndex <= totNumNodes):

        # Get a node
        #-----------
        thisNode = listNodes[nodeIndex-1].strip()

        # Create a directory associated with the node
        #--------------------------------------------
        dirName = os.path.join(STAT_DIR, thisNode.strip())

        if not os.path.exists(dirName):
           os.mkdir(dirName)

        # Determine how many tasks are left to be run on the node
        #--------------------------------------------------------
        if (os.path.isdir(dirName.strip())):
           spawn_procs = numCoresPerNode[nodeIndex-1] - len(os.listdir(dirName.strip())) 
        else:
           logger.error("The directory", dirName, "does not exist")
           ne += 1
           sys.exit(ne)
  
        # Launch enough tasks to fill up the current 
        # node, except if all tasks have been launched
        #---------------------------------------------
  
        i_sub_task = 0
        while ((i_sub_task < spawn_procs) and (taskIndex <= totNumTasks)):
  
           i_sub_task +=  1
           cmd = listTasks[taskIndex-1]
  
           # Remote launches the wrapper script (in charge of creating/deleting
           # the trigger files before/after launching the user's command
           #-------------------------------------------------------------------
  
           sshCMD1 = 'ssh -nf '+ thisNode 
           sshCMD2 = podSrcDIR+'/podsWrapper.py ' + \
                     STAT_DIR +' '+ \
                     thisNode +' '+ \
                     str(taskIndex) + ' '+\
                     fileName +' '+ \
                     ' podsEnv ' + podsEnv.strip() + \
                     ' podsCmd '+ cmd + '&'
           sshCMD = sshCMD1.strip() + ' ' + sshCMD2.strip()
           sshCMD = sshCMD.replace('\n', ' ')

           pr = subprocess.Popen(sshCMD.strip(), env=os.environ.copy(), shell=True, stderr=subprocess.PIPE)

           taskIndex += 1
  
        nodeIndex += 1

     numCurTasks = podsNumRunningTasks.runningTasks(listNodes,STAT_DIR)
     logger.debug("There are currently %i running tasks " %numCurTasks)
     time.sleep(5)

