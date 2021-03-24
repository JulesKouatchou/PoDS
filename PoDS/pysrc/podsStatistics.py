#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import time
import subprocess
from datetime import datetime

def printStatistics(begDate, endDate, totNumTasks, listNodes, numCoresPerNode, fileName): 
   """
     Prints the timing statistics at the end of the run.

     Required arguments:
        - begDate:         recorded date/time at the beginning of the run
        - endDate:         recorded date/time at the end       of the run
        - totNumTasks:     total number of tasks
        - listNodes:       list of nodes requested by the user
        - numCoresPerNode: total number of core per node
        - fileName:        name of the file containing individual tasks timing numbers

     Outputs:
        - A print out of the timing summuary.
   """

   totNumNodes = len(listNodes)

   # Read the file and extract individual task timing information
   with open(fileName, "r") as fid:
        globArrayIndex = []
        globArrayTimes = []
        try:
           # For Python 2
           timesNode = [[] for x in xrange(totNumNodes)]
        except:
           # For Python 3
           timesNode = [[] for x in  range(totNumNodes)]
        for line in fid:
            if (line.strip() != ''):
               w = line.split()
               globArrayIndex.append( int(w[3]) )
               globArrayTimes.append( float(w[5]) )

               for nd in listNodes:
                   if nd.strip() in line:
                      it = listNodes.index(nd)
                      timesNode[it].append(float(w[5]))
                      break

   globMinTime = min(globArrayTimes)
   globMaxTime = max(globArrayTimes)
   globAvgTime = sum(globArrayTimes)/float(len(globArrayTimes))

   indMin = globArrayTimes.index(globMinTime)
   indMax = globArrayTimes.index(globMaxTime)

   taskID_min = globArrayIndex[indMin]
   taskID_max = globArrayIndex[indMax]
              
   print(" ", 96*"=")
   print("|", "="*13, " "*19, "Summary of PoDS Calculations",  " "*19, "="*13, "|")
   print(" ", 96*"=")
   print("  Number of completed tasks: ", totNumTasks)
   print(" ")
   print("  Number of nodes selected:  ", totNumNodes)
   print(" ", 96*"-")
   print("| Node       | Cores Used | Tasks ran |     Slowest Task    |     Fastest Task    | Avg Time/Task |")
   print(" ", 96*"-")
   num_nodes_used = 0
   for i in range(totNumNodes):
       ntpn    = len(timesNode[i])
       if (ntpn > 0):
          num_nodes_used += 1
          minNode = min(timesNode[i])
          maxNode = max(timesNode[i])
          avtpn   = sum(timesNode[i])/float(ntpn)
          idxmin  = globArrayIndex[globArrayTimes.index(minNode)]
          idxmax  = globArrayIndex[globArrayTimes.index(maxNode)]
          print('| %-10s | %5i      | %5i     | %4i-> %10.4f s | %4i-> %10.4f s | %10.4f s  |' %(listNodes[i].strip(), numCoresPerNode[i], ntpn, idxmax, maxNode, idxmin, minNode, avtpn))
   print(" ", 96*"-")
  
   print(" ")

   print("     Overall Statistics: ")
   print("         - Number of nodes used: ", num_nodes_used ,'(out of ',totNumNodes,')')
   print("         - The average time per task: %f seconds " %(globAvgTime))
   print("         - Task %4d was the fastest: %f seconds " %(taskID_min, globMinTime))
   print("         - Task %4d was the slowest: %f seconds " %(taskID_max, globMaxTime))
   print

   delta = endDate-begDate
   total_time = ((1000000 * delta.seconds + delta.microseconds) / 1000000.0)
   print("        - Total Time Elapsed:       ", total_time, "seconds")
   print(" ")
   print('        - Starting Date/Time:       ', begDate.strftime("%Y-%m-%d %H:%M:%S"))
   print('        - Ending   Date/Time:       ', endDate.strftime("%Y-%m-%d %H:%M:%S"))
   print("", 96*"=")
