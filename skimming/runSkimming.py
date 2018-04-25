#!/usr/bin/env python
############################################################################
#
# Edgar Carrera
# ecarrera@cern.ch
# November 24, 2017
# This script handle the launching of skimming jobs based on different PU
# ranges.  These pu ranges are taken from the myjson_PU*.json files in the
#directory, which should be already available 
###############################################################################

import sys, os
import commands

theDataset = "HLTPhysics2"
theRun = "306091"

#Don't change anything from here
puranges = []
LSCOMMAND = "ls -1 myjson_PU*"
thePUlist = commands.getstatusoutput(LSCOMMAND)
for k in thePUlist[1].split("\n"):
    puranges.append(k.split("_")[1].split(".json")[0])

#print puranges    

for pu in puranges:
    newfilename = 'getInputFiles_'+pu+'.py'
    rmstr = "rm -f "+newfilename
    os.system(rmstr)
    logfile = "full_"+pu+".log"
    rmstr = "rm -f "+logfile
    os.system(rmstr)
    sedstr = "sed -e 's/\[PILEUP\]/"+pu+"/g' -e 's/\[DATASET\]/"+theDataset+"/g' -e 's/\[RUN\]/"+theRun+"/g' getInputFiles.py > "+newfilename
    print sedstr
    os.system(sedstr)
    cmsstr = "cmsRun "+newfilename+"> "+logfile+ " 2>&1 &"
    print cmsstr
    os.system(cmsstr)
    os.system('sleep 40s')

