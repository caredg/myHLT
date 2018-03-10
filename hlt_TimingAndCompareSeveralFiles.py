import os, sys

therun = 305636
thefile = "filelist.txt"
filelist = open(thefile,"r")
outfiles = []
myindex = 0
for filein in filelist.readlines():
    if myindex>3:
        therun = 306091
    strTiming = "python2.7 TimingAndRates.py --inputfile "+filein.rstrip()+" --data --lumis 100 --run "+str(therun)+" --process TIMING"
    os.system(strTiming)
    tag = filein.split("_")[2]
    outfile = "HLT_TimingAndRates_"+tag+".csv"
    os.system("rm -f "+outfile)
    outfiles.append(outfile)
    os.system("mv HLT_TimingAndRates.csv "+outfile)
    myindex = myindex +1

for tfile in outfiles:
    strPadding = "python2.7 hlt_ComparePathsTiming.py "+outfiles[4]+" "+tfile
    os.system(strPadding)

