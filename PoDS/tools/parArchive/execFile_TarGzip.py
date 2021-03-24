#!/usr/bin/env python
#################################################################
# This script takes a directory name (full path), lists all the #
# sub-directories and creates for each of them an individual    #
# she script (that tar up and gzip the sub-directory).          #
# It also creates a PoDS execution file which lists all the     #
# individual scripts as command lines.                          #
#################################################################

from __future__ import print_function
import os
import sys
import time

cmd1 = 'tar '
cmd2 = 'gzip '

# Obtain the directory name (full path)
inputDirName = sys.argv[1]

workDir = os.getcwd()

print("My working directory is ", workDir)
os.chdir(workDir)

# Create the execution file
fileHandle = open ( 'executionFile', 'w' )

# Get all the files/directories the the provided directory
names = os.listdir(inputDirName)

for filename in names:
    if os.path.isdir(os.path.join(inputDirName,filename)):
       print("Dir to be tarred up: ", filename)
       shellScriptName = filename+'.sh'
       tarFileName = filename+'.tar '
       fileHdle = open ( shellScriptName, 'w' )
       str1 = cmd1  + tarFileName + os.path.join(inputDirName,filename) + '\n'
       str2 = cmd2  + tarFileName + '\n'
       fileHdle.write (str1)
       fileHdle.write (str2)
       fileHdle.close()

       os.system('chmod 700 ' + shellScriptName)

       fileHandle.write ('./'+shellScriptName + '\n')

fileHandle.close()
