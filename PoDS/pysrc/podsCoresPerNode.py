#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import time
import subprocess
import logging

logger = logging.getLogger(__name__)

def createNodeList(myString):
    """
    Using myString is of the form 'borgb[049,057,097,101-102,037-045]', 
    this function creates the list:
    
    ['borgb049', 'borgb057', 'borgb097', 
     'borgb101', 'borgb102', 'borgb037', 
     'borgb038', 'borgb039', 'borgb040', 
     'borgb041', 'borgb042', 'borgb043', 
     'borgb044', 'borgb045']
    """

    (a,b,c) = myString.partition('[')

    (b,c,d) = myString.partition(a+b)

    (b,c,d) = d.partition(']')

    x = b.split(',')

    y = []
    for i in x:
        if (i.find('-') != -1):
           y.append(i)
           b = i.split('-')
           for j in range(int(b[0]), int(b[1])+1):
               x.append(str(j).zfill(3))
    
    if len(y) > 0:
       for i in y:
           x.remove(i)

    myList = [a+i for i in x]

    return myList


def getNumCoresPerNode(listNodes): 
  """
    Determines the number of cores per node.

    Required argument:
      - listNodes: list of available nodes

    Returned value:
      - A list containing the number of cores for each node.
  """
  logger.info("Inside getNumCoresPerNode")
  
  totNumNodes = len(listNodes)
  numCoresPerNode = [0 for i in range(totNumNodes)]
  ne = 0
  nodeIndex = 1

  while (nodeIndex <= totNumNodes):
      thisNode = listNodes[nodeIndex-1]

      sshCMD = 'ssh -nf ' + thisNode.strip() + ' cat /proc/cpuinfo | grep processor | wc -l &'
      sshCMD = sshCMD.replace('\n', ' ')
  
      proc = subprocess.Popen(sshCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      stdout_value, stderr_value = proc.communicate()
      numCoresPerNode[nodeIndex-1] = int(stdout_value)

      nodeIndex += 1

  return numCoresPerNode

def checkRangeCores(numCPUS, minCores, maxCores):
    """
       Checks the range of the number of cores provided by the user
    """
    logger.info("PoDS: Inside checkRangeCores")

    if ((numCPUS < minCores) or (numCPUS > maxCores) ):
       logger.error("PoDS: Please provide the number of cpus per node between %i2 and %i3" %(minCores, maxCores))
       logger.error("PoDS: This will avoid oversubscription on the nodes.")
       sys.exit(10)
    else:
       logger.info("PoDS: Number of cores is valid!")
       pass
