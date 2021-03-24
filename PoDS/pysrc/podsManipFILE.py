#!/usr/bin/env python

"""
  Module containing functions to manipulate
  files (open, remove, etc.)
"""
from __future__ import print_function
import os
import sys
import shutil

def getLines(fileName):
    """
      Opens a file and reads all the file in the file.

      Required argument:
         - fileName: name of a file

      Returned value:
         - A list containing lines in the file.
    """
    try:
       fp = open(fileName)
       return fp.readlines()
       fp.close()
    except:
       print("Can not open the file: ", fileName)
       sys.exit(1)

def removeFile(rmFile):
    """
      Removes an existing file.

      Required argument:
         - rmName: name of a file

    """
    if (os.system('/bin/rm -f ' + rmFile)) == 0:
       pass
    else:
       print('Can not remove the file ',  rmFile)
       os.exit(110)

def touchFile(tFile):
    """
      Updates the access and modification time of a file to the current time.

      Required argument:
         - tName: name of a file
    """
    if (os.system('touch ' + tFile)) == 0:
       pass
    else:
       print('Can not touch the file ',  tFile)
       os.exit(111)

def emptydir(top):
    """
      Delete a directory.
    """
    if(top == '/' or top == "\\"): return
    else:
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))


def deleteFileOrFolder(directory):
    if os.path.exists(directory):
        try:
            if os.path.isdir(directory):
                # delete folder
                shutil.rmtree(directory)
            else:
                # delete file
                os.remove(directory)
        except:
            print("Ecxeption ",str(sys.exc_info()))
    else:
        print("not found ",directory)
