#!/usr/bin/env python
"""
    Portable Distributed Scripts (PoDS) 
    NASA GSFC - SSSO Code 610.3         
    Greenbelt, MD 20771                 

    Front-ennd script to execute independent tasks in parallel.
"""

###############################
# Import python related modules
###############################

from __future__ import print_function
import os
import sys
import time
import subprocess
import optparse
import string
from datetime import datetime
import logging

# Determine the location (absolute path) of this script
podSrcDIR = os.path.dirname(os.path.abspath(__file__))
podSrcDIR = podSrcDIR+'/pysrc'
sys.path.append(podSrcDIR)

##############################
# Import PoDS internal modules
##############################

import podsUsage
import podsRunTasks
import podsManipFILE
import podsStatistics
import podsCoresPerNode
import podsNumRunningTasks
import BetterFormatter
import podsListNodes
import podsLogging

logger = logging.getLogger(__name__)
#logger = logging.getLogger('main')

################################
# Get the starting date and time
################################

begDate = datetime.now()


print(56*"-")
print(" ----------------   Beginning of PoDS   ---------------")
print("|   A tool for running independent tasks in parallel   |")
print(56*"-")
print("|  Check the  file pods_logger_jobID.LOG for PoDS info |")
print(56*"-")

ne = 0

########################
# Parse the command line
########################


logger.info("Get the arguments from the command line")

parser = optparse.OptionParser(formatter=BetterFormatter.BetterFormatter(),
                               version='%prog version 3.0',
                               description=podsUsage.usagePoDS())

parser.add_option('-n', '--coresPerNode', help='set the number of cores per nodes', 
                  dest='numCoresPerNode', action='store', metavar='numCoresPerNode')

parser.add_option('-e', '--env', help='Environment variables to be passed', 
                  dest='myEnv', action='store', metavar='myEnv')

parser.add_option('-x', '--exec', help='Execution file', 
                  dest='myExecFile', action='store', metavar='executionFile')

(opts, args) = parser.parse_args()

# Make sure that the execution file is provided
#----------------------------------------------
if opts.myExecFile is None:
   logger.error("You need to provide the execution file")
   parser.print_help()
   ne += 1
   sys.exit(ne)

EXEC_FILE = os.path.basename(opts.myExecFile)
EXEC_DIR  = os.path.dirname(opts.myExecFile)

if ( not (os.path.isabs(EXEC_DIR))):
   EXEC_DIR = os.getcwd()

#########################################################
# Get the the list of available nodes assigned to the job
# and the job identifier through environment variables.
#########################################################

# under SLURM
listNodes = podsListNodes.nodeList_SLURM()
jobID = os.environ.get("SLURM_JOBID")

# under PBS
#listNodes = podsListNodes.nodeList_PBS()
#jobID     = os.environ.get("PBS_JOBID")

if not jobID:
   print("You need to submit PoDS within a SLURM job")
   sys.exit(0)
    
# Create the logger file and output format
logger_file = "pods_logger_"+str(jobID)+".LOG"
podsLogging.logger_setup(logger_file)

logger.info("This is to monitor the inner working of PoDS")

logger.info("Get the job ID and the list of nodes")

# Total number of nodes
totNumNodes = len(listNodes)

if ( totNumNodes == 0 ):
   logger.error("You do not have access to any node.")
   logger.error("Please execute the PoDS script in a valid SLURM session")
   ne += 1
   sys.exit(ne)

##################################
# Set the number of cores per node
##################################

logger.info("Verify that user did not exceed the number of cores per node")

if opts.numCoresPerNode is not None:
   # User supplied number
   numCPUS = int(opts.numCoresPerNode)


   minCores = 1  # minimum number of cores per node
   maxCores = 28 # maximum number of cores per node

   # Do error checking and exit if numCPUS < minCores or numCPUS > maxCores
   podsCoresPerNode.checkRangeCores(numCPUS, minCores, maxCores)

   numCoresPerNode = [numCPUS for i in range(totNumNodes)]

else:
   # If the user does not provide the number of cores per node, have
   # access to each node and obtain the number of available cores.

   numCoresPerNode = podsCoresPerNode.getNumCoresPerNode(listNodes)

###########################################################
# Go to the directory where the executable file is located.
###########################################################

os.chdir(EXEC_DIR)

################################################################
# Create the directory where individual tasks will be monitored.
################################################################

logger.info("Create the temporary directory: statusDIR_"+str(jobID))

STAT_DIR = os.path.join(EXEC_DIR, 'statusDIR_'+jobID)

if not os.path.exists(STAT_DIR):
   os.mkdir(STAT_DIR)

####################################################
# Get information on the available individual tasks.
####################################################

logger.info("Gather the list of tasks")

listTasks   = podsManipFILE.getLines(EXEC_FILE)
totNumTasks = len(listTasks)

logger.info("There are %d tasks" %(totNumTasks))

if ( totNumTasks == 0 ):
   logger.error("PoDS: Please provide a non-empty execution file")
   ne += 1
   sys.exit(ne)

##########################################################
# Create a dictionary for the user's environment variables
##########################################################

if (opts.myEnv == None):
   envDict = {}
else:
   envDict = eval(str(opts.myEnv))

###################################################################
# Loop over the tasks until all individual tasks have been launched
###################################################################

logger.info("Start running the tasks")

fileName = os.path.join(STAT_DIR, 'stats_file.txt')

podsRunTasks.runTasks(STAT_DIR, fileName, listNodes, listTasks, 
                      numCoresPerNode, podSrcDIR,
                      envDict)

###############################################################
# Wait until all tasks have completed before exiting the script
###############################################################

numCurTasks = podsNumRunningTasks.runningTasks(listNodes,STAT_DIR)
while ( numCurTasks > 0):
   logger.debug("The last %i tasks are finishing up" %numCurTasks)
   numCurTasks = podsNumRunningTasks.runningTasks(listNodes,STAT_DIR)
   time.sleep(1)

endDate = datetime.now()

########################
# Print a Summary Report
########################
logger.info("Generate statistics")

print("----<> ------------------------------------------------------ <>----")
print("----<> Ckeck the file "+logger_file+ " to monitor PoDS events.")
print("----<> ------------------------------------------------------ <>----")
podsStatistics.printStatistics(begDate, endDate, totNumTasks, listNodes, numCoresPerNode, fileName)

################################
# Delete the temporary directory
################################
logger.info("Delete the temporary directory")
podsManipFILE.deleteFileOrFolder(STAT_DIR)

ne += 1
sys.exit(ne)
