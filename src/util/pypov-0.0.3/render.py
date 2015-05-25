#!/usr/bin/env python

"""
PyPov-0.0.X Copyright (c) Simon Burton, 2003
See LICENSE file.
"""

import os, sys
#names = os.listdir("out")
names = sys.argv[1:]
for name in names:
  fields = name.split(".")
  if len(fields)>2 and fields[2] == "pov":
    iname = name
    oname = "%s.%.4d.png"%(fields[0],int(fields[1]))
    #cmd = "povray +I%s +O%s +A -D"%(iname,oname)
    #cmd = "povray +W1024 +H768 +I%s +O%s -GA -D"%(iname,oname)
    cmd = "povray +W768 +H576 +I%s +O%s -GA -D"%(iname,oname)
    print cmd
    if os.system(cmd) != 0:
      break
  elif fields[1] == "pov":
    iname = name
    oname = "%s.png"%(fields[0])
    #cmd = "povray +I%s +O%s +A -D"%(iname,oname)
    cmd = "povray +W1024 +H768 +I%s +O%s -GA -D"%(iname,oname)
    print cmd
    os.system(cmd)



