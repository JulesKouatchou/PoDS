#!/usr/bin/env python

"""
  Module containing functions to show how to use PoDS.
"""

from __future__ import print_function

def usagePoDS():
   desc = """
   NAME:
        pods - Portable Distributed Scripts (PoDS)

   DESCRIPTION:
        PoDS is a script that enables users to execute a series 
        of independent serial tasks on multi-core systems. Many 
        users have the need to run large sets of data processing 
        tasks which has been difficult to coordinate due to the 
        node architecture of the system. With PoDS, we intend to 
        make the process simple and flexible.

        To use PoDS, the user needs to provide:

        execFile: the executable file containing the list of 
             independent jobs to be executed. It is preferable
             to provide the absolute path.
        coresPernode: the number of selected cores per nodes.
             If the user does not provide this argument, PoDS
             will uatomatically access each reserved node to 
             extract its number of available cores.
        myEnv: environment variables

   EXAMPLES:
       To print this page:

           pods.py

       The same could be achieved with:

           pods.py -h

       To execute serial tasks (listed in the file myPoDSexeFile) on
       4 cores/node:

           pods.dy -x /discover/nobackup/userid/myPoDSexeFile -n 4

       Note that I provide the full path to myPoDSexeFile.
       The command

           pods.py -x myPoDSexeFile -n 4

       will also work. PoDS will then run in the directory where 
       myPoDSexeFile is located. The following is also acceptable

           pods.py -x myPoDSexeFile
      
       In this case, PoDS will use all the cores available in each
       reserved node.

   AUTHORS:
        Jules Kouatchou - Jules.Kouatchou-1@nasa.gov

   COPYRIGHT:
   """
   return desc
  

def warningPoDS():
   print("""
   \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
   Warning: parameter cpus_per_node not provided. 
   Default: number of available cores on ecah node.
   This may not be optimal behavior for some Discover nodes
   \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
   """)

