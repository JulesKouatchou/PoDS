#!/usr/bin/env python
##############################################################
# This script automatically generate a PoDS execution file.  #
# The file contains a list of gunzip commands the user wants #
# execute in parallel. The user provides the directory name  #
# (full path) and the script gathers all the files (ending   #
# with .gz) and creates the gunzip command line.             #
##############################################################
 
import os
import sys
import time
 
# File extension
ext = 'gz'

command = 'gunzip '
 
# Obtain the directory name (full path)
dirName = sys.argv[1]
 
# Get all the files/directories the the provided directory
names = os.listdir(dirName)
 
# Create the execution file
fileHandle = open ( 'executionFile', 'w' )
 
for filename in names:
    if os.path.normcase(filename).endswith(ext):
       str = command  + os.path.join(dirName,filename) + '\n'
       fileHandle.write (str)
 
fileHandle.close()
