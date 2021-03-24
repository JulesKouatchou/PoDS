#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import time
import subprocess
from datetime import datetime
import fcntl
import logging

"""
  Execute the given task in the assigned node.

  Arguments:
    1. directory name (string)
    2. name of the node (string)
    3. index of the task (integer)
    4. command to execute
"""

logger = logging.getLogger(__name__)

STAT_DIR   = sys.argv[1]
thisnode   = sys.argv[2]
task_index = str(sys.argv[3])
fNameStats = sys.argv[4]
EXEC_DIR   = os.path.join(STAT_DIR,'..')

###############################################################
# Ensure that a status directory has been created for this node
###############################################################

newDIR = os.path.join(STAT_DIR,thisnode)

if not os.path.exists(newDIR):
   os.mkdir(newDIR)

####################################
# Create a trigger file for this task
####################################

fName = os.path.join(newDIR, task_index) # newDIR+'/'+task_index
if not os.path.isfile(fName):
   open(fName, 'w').close()

##############################################################
# Recreate the user's command from the arguments to the script
##############################################################

s = sys.argv[5:]

pE = s.index('podsEnv')
pC = s.index('podsCmd')

# Construct the dictionary of environment variables
#--------------------------------------------------
myEnv = s[pE+1:pC]
L = []
for comd in myEnv:
    L.append(comd)

n = len(L)/2

text = '___'

podsEnv = os.environ.copy()
if ( len(L) > 1):
   index = 0
   val = ' '
   for w in L:
       if (w.endswith(text)):
          key = w[:len(w)-len(text)]
       else:
          val += w + ' '
       index += 1
       if (index == len(L)):
          podsEnv[key] = val.strip()
       elif (L[index].endswith(text)):
          podsEnv[key] = val.strip()
          val = ' '

# Extract the command to be executed
#-----------------------------------

myCmd = s[pC+1:]
podsCmd=''
#for comd in sys.argv[4:]:
for comd in myCmd:
   podsCmd +=  ' ' + comd

############################
# Execute the user's command
############################

os.chdir(EXEC_DIR)

begDate = datetime.now()

cmds = [podsCmd]
#pr = subprocess.call(cmds, env = os.environ.copy(), shell=True)
pr = subprocess.call(cmds, env = podsEnv, shell=True)

if (pr == 0):
   pass
else:
   logger.warning("^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
   logger.warning("^^^^^^^ WARNING! WARNING! WARNING! Could not execute task: ", task_index)
   logger.warning("^^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
   #sys.exit(100)

######################################
# Remove the trigger file for this task
######################################

if os.path.isfile(fName):
   os.remove(fName)

endDate    = datetime.now()
delta      = endDate-begDate
total_time = ((1000000 * delta.seconds + delta.microseconds) / 1000000.0)

logger.debug("---> Task %s took: %12.5f seconds" %(task_index, total_time))
print("---> Task %s took: %12.5f seconds" %(task_index, total_time))

#-------------------------------
# Write timing numbers in a file
#-------------------------------
with open(fNameStats, "a") as g:
    fcntl.flock(g, fcntl.LOCK_EX)
    g.write( "Node: %15s Task: %5s Time: %14.6f (seconds)\n" %(thisnode, task_index, total_time) )
    fcntl.flock(g, fcntl.LOCK_UN)
