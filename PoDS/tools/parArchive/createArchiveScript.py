#!/usr/bin/env python
##################################################################### 
# This script takes as inputs:                                      #
#   (1) a directory name (full path) where the compressed file      #
#       will be archived). It is assumed that the directory exists. #
#   (2) the user sponsor code account.                              #
# It automatically creates a SLURM script (archiveSLURM.job) which  #
# will be used to transfer the compressed files.                    #
#####################################################################

from __future__ import print_function
import os
import sys
import time

cmd1 = 'tar '
cmd2 = 'gzip '

# Obtain the directory name (full path)
inputDirName = sys.argv[1]
sponsorID    = sys.argv[2]

workDir = os.getcwd()

print("My working directory is ", workDir)
os.chdir(workDir)

# Create the execution file
fileHandle = open ( 'archiveSLURM.job', 'w' )

fileHandle.write ('#!/bin/csh ' + '\n')
fileHandle.write ('#SBATCH -A '+ sponsorID + '\n')
fileHandle.write ('#SBATCH -p datamove ' + '\n')
fileHandle.write ('#SBATCH -J dataArchive ' + '\n')
fileHandle.write ('#SBATCH -N 1 ' + '\n')
fileHandle.write ('#SBATCH -t 1:00:00 ' + '\n')
fileHandle.write ('#SBATCH -o archive.out' + '\n')
fileHandle.write ('#SBATCH -e archive.err' + '\n')
fileHandle.write (' ' + '\n')
fileHandle.write (' ' + '\n')
fileHandle.write ('# Go to the working directory ' + '\n')
fileHandle.write ('cd $SLURM_SUBMIT_DIR ' + '\n')
fileHandle.write (' ' + '\n')
fileHandle.write ('# Move the compessed files to the archive ' + '\n')
fileHandle.write ('mv *.gz ' + inputDirName + '\n')
fileHandle.write ('exit ' + '\n')


fileHandle.close()
