#!/usr/bin/env python
############################################################################
#
# Edgar Carrera
# ecarrera@cern.ch
# April 13, 2018
# This script compares the timing of modules in equivalent menus 
# Ex: python hltCompareModulesTimingInMenus.py file1DQM.root file2DQM.root 305636 305670
#
###########################################################################

"""
   usage: %prog <file1> <file2> <run1> <run2>
"""   

import os,sys
import subprocess
import string, re
import fileinput
import commands
import operator
from time import gmtime, localtime, strftime
#from ROOT import *
from ROOT import gPad, gROOT, TCanvas, TH1F, TFile, TLegend, gStyle,gDirectory
import io
#just a debug flag
DEBUG = False


###############################################################
def usage():
###############################################################

    if (DEBUG):
        print "This is the usage function"
        
    print '\n'
    print 'Usage: '+sys.argv[0]+' <file1> <file2> <run1> <run2>'
    print 'e.g.:  '+sys.argv[0]+' \n'


###############################################################
def get_modules_timing(infile,run):
###############################################################
    theDict = {}
    #this is dangerously hardcoded:
    process = "TIMING"
    tfile = TFile(infile)
    dirname = "DQMData/Run %s/HLT/Run summary/TimerService/process %s modules" % (run, process)
    gDirectory.cd(dirname)
    #type of plot
    modplot = "time_real"
    #print dirname
    for key in gDirectory.GetListOfKeys():
        histname = key.GetName()
        histnamesplit = histname.split()
        #check if the module info is the one we need
        modulename = histnamesplit[0]
        if not modulename[0].isupper():
            if histnamesplit[1] == modplot:
                hName = dirname+"/"+histname
                hist = tfile.Get(hName)
                theMean = hist.GetMean()
                theDict[modulename] = theMean
        
    return theDict

#######################################################
def print_tuples(sDic,label,max):
#######################################################
    print label
    n = 0
    for p in sDic:
        if (n < max):
            print p
        else:
            break
        n = n + 1
        


#######################################################
def print_csv_file(repo1,repo2,file1,file2):
#######################################################

    #compare based on first container, which
    #should have paths in the newest menu
    fname1 = file1.split("_")[1].strip("Menu-")
    fname2 = file2.split("_")[1].strip("Menu-")
    #print fname1
    #print fname2
    
    #create csv file
    csv_file_title = "PathModulesTimingComparisonInMenus_"+fname1+"_Vs_"+fname2+".csv"
    theTitle = unicode(csv_file_title)
    #print theTitle
    f = io.open(theTitle,'w',encoding='utf8')

    #to keep track of most offending modules and largest differences
    #with respect to the other menu
    mostOffending = {}
    mostIncreasing = {}
    mostRelChange = {}

    #loop over modules (here I use p because the code used to work with paths)
    countk = 0
    for p in repo1:
        p1name = p
        p1timing = float(repo1[p])
        pdiff = -999.0
        pratio = -999.0
        prel = -999.0
        p2name = "N/A"
        p2timing = 0.
        #check if module is in repo2
        isModule = repo2.get(p)
        if isModule:
            p2name = p
            p2timing = float(repo2[p])
            pdiff = p1timing-p2timing
            if (p2timing!=0):
                pratio = p1timing/p2timing
                prel = abs(pdiff/p2timing)
            else:
                pratio = 0.
        else:
            pdiff = p1timing
        #fill dictionaries to sort
        mostOffending[p1name] = p1timing
        mostIncreasing[p1name] = pdiff
        mostRelChange[p1name] = prel
        #print the csv file
        if (countk==0):
            theCsvLine = unicode(fname1+",Timing (ms),"+fname2+",Timing (ms),"+fname1+"-"+fname2+" (ms),"+fname1+"/"+fname2+" (ms),("+fname1+"-"+fname2+")/"+fname2+"\n")
        else:        
            theCsvLine =  unicode(p1name+","+str(p1timing)+","+p2name+","+str(p2timing)+","+str(pdiff)+","+str(pratio)+","+str(prel)+"\n")
        f.write(theCsvLine)
        countk = countk + 1

    #sort dictionaries
    sorted_mostOffending = sorted(mostOffending.items(), key=operator.itemgetter(1),reverse=True)
    sorted_mostIncreasing = sorted(mostIncreasing.items(), key=operator.itemgetter(1),reverse=True)
    sorted_mostDecreasing = sorted(mostIncreasing.items(), key=operator.itemgetter(1))
    sorted_mostRelChange = sorted(mostRelChange.items(), key=operator.itemgetter(1),reverse=True)

    #print first elements in the ordered tuples
    maxitems = 10
    off_label = "Most Offending Modules - "+fname1+" : ('Module', Timing (ms))"
    print_tuples(sorted_mostOffending,off_label,maxitems)
#    print sorted_mostOffending
    inc_label = "\nMost Increasing Modules - "+fname1+" with respect to "+fname2+": ('Module', Increased Timing (ms))"
    print_tuples(sorted_mostIncreasing,inc_label,maxitems)
    dec_label = "\nMost Decreasing Modules - "+fname1+" with respect to "+fname2+": ('Module', Decreased Timing (ms))"
    print_tuples(sorted_mostDecreasing,dec_label,maxitems)
    rel_label = "\nMost Absolute Relative Change in Timing - "+fname1+" with respect to "+fname2+": ('Module', Absolute Relative Change)"
    print_tuples(sorted_mostRelChange,rel_label,maxitems)

###############################################################
def main():
###############################################################
    #check the number of parameter
    #print sys.argv
    numarg = len(sys.argv)
    if numarg < 5:
        usage()
        return 1

    infile1 = sys.argv[1]
    infile2 = sys.argv[2]
    run1 = sys.argv[3]
    run2 = sys.argv[4]


    #check if input files exist
    if  not(os.path.isfile(infile1)):
        print infile1+" does not exist. Please check."
        sys.exit(1)
    if  not(os.path.isfile(infile2)):
        print infile2+" does not exist. Please check."
        sys.exit(1)


    #get the modules timing for the chosen path in two repos.
    #The repos correspond to the files in the order entered
    repo1 = get_modules_timing(infile1,run1)
    repo2 = get_modules_timing(infile2,run2)

    #make the modules timing comparison and print csv file
    print_csv_file(repo1,repo2,infile1,infile2)
    

#######################################################
if __name__ =='__main__':
#######################################################
    sys.exit(main())
