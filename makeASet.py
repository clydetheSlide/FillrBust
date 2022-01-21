#!/usr/bin/env python
''' makeASet [options] zipname
   make a set of dice'''

import os,sys,getopt
import subprocess, glob

try:
    options,args=getopt.getopt(sys.argv[1:], 's:')
except getopt.GetoptError:
    print 'caught getopt error'
    sys.exit(1)

if len(args) <1:
  print(' You must tell me a name for the zip file '+len(args))
  sys.exit(1)

size=64
for opt, par in options:
    if opt == '-s':
        size=int(par)

for set in (
        [0,18,'undie']
        ,[7 ,1, 'one']
        ,[8 ,2, 'two']
        ,[9 ,3, 'three']
        ,[10 ,4, 'four']
        ,[11 ,5, 'five']
        ,[12 ,6, 'six']
        ):
    subprocess.call(['povray', '+H%d'%size, '+W%d'%size, '+A', '+K%d'%set[0], '../dice.pov'])
    subprocess.call(['convert', '../dice.png', '%sb.gif'%set[2]])
    subprocess.call(['povray', '+H%d'%size, '+W%d'%size, '+A', '+K%d'%set[1], '../dice.pov'])
    subprocess.call(['convert', '../dice.png', '%s.gif'%set[2]])
    print ('povray +H%d'%size, '+W%d'%size, '+A', '+K%d'%set[0], '%sb.gif'%set[2])

glor = glob.glob('*.gif')
print (glor)
subprocess.call(["ls", glor])
#call(['zip', arg[0], '*.gif'],shell=True)
