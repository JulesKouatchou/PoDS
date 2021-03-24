                        Portable Distributed Scripts (PoDS)

                 Goddard Space Flight Center, Greenbelt, Maryland 

“Portable Distributed Scripts” (PoDS) is a Python application that allows users 
to execute serial independent tasks concurrently across nodes on multicore clusters. 
The package consists of a set of scripts working together through a simple 
text-based interface. A user only needs to provide minimal information to perform 
the desired tasks. 

Scientists run their applications on high-performance computers and generate a 
large number of data files. The data need to be processed in order to extract 
meaningful scientific results. In general, the manipulation of output files 
consists of executing a series of independent serial tasks on single processors 
on the same platform where the initial data were produced. This can take a 
significant amount of time and leads to an inefficient use of available resources. 
With the advent of multicore clusters, in-house tools are being designed for serial 
data processing. 

PoDS does not require any knowledge of the individual tasks and does not make any 
assumptions about the underlying application. As a matter of fact, the tasks to be 
executed can be from different applications. It can be seen as a task parallelism 
tool where concurrent independent jobs are executed in parallel. 

PoDS consists of a front-end Python script through which a user provides a list 
of tasks to be performed. In a practical sense, PoDS determines the list of nodes 
reserved by the user and connects (through a password-less ssh command) to 
individual nodes to distribute the workload (independent tasks). As long as tasks 
are available, each node receives as many of them as it has processors 
(if the user chooses to employ all the processors within the node). PoDS internally 
monitors the progress of each task and moves to the next available one as soon as 
one is completed. At any given time, all the nodes (in fact all the processors) 
remain busy until there is no more work to do. 

Prior to the development of PoDS, there was no tool available to help users who 
were running serial independent tasks. Users had to request one compute node 
(or a set of compute nodes) and underutilize it. PoDS produces timing statistics 
that can be useful to determine how the individual tasks were distributed to the 
available processors, and how they can be properly balanced in future runs. 

PoDS is actively maintained and can easily be modified to meet NASA users’ needs 
as they emerge.

This work was done by Jules Kouatchou and Amidu Oloso of SSAI for 
Goddard Space Flight Center.
https://modelingguru.nasa.gov/docs/DOC-1582
https://modelingguru.nasa.gov/docs/DOC-2425
https://modelingguru.nasa.gov/docs/DOC-2633
