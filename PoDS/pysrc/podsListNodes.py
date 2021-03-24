#!/usr/bin/env python
"""
    Portable Distributed Scripts (PoDS) 
    NASA GSFC - SSSO Code 610.3         
    Greenbelt, MD 20771                 

    Functions to get the list of available nodes.
"""

###############################
# Import python related modules
###############################

import os
import sys
import subprocess

##############################
# Import PoDS internal modules
##############################

import podsManipFILE

def nodeList_SLURM():
    """
      This function returns the list of selected nodes when
      in a SLURM environment
    """
    listNodes = []

    cmd = 'scontrol show hostname'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    proc.wait()

    # Get the Python version
    python_version = sys.version_info[0]

    for line in proc.stdout:
        if python_version == 2:
           my_string = line.rstrip()
        elif python_version == 3:
           my_string = line.decode('utf-8').rstrip()
        listNodes.append(my_string.strip())

    proc.stdout.close()

    return listNodes

def nodeList_PBS():
    """
      This function returns the list of selected nodes when
      in a PBS environment
    """
    nodeFileName = os.environ.get("PBS_NODEFILE")

    listNodes   = podsManipFILE.getLines(nodeFileName)

    # Remove duplicate node names
    listNodes   = dict.fromkeys(listNodes)
    listNodes   = listNodes.keys()

    return listNodes

