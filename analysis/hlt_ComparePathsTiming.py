#!/usr/bin/env python
############################################################################
#
# Edgar Carrera
# ecarrera@cern.ch
# September 8, 2017
# This script takes two of the csv output file from the TimingAndRates.py
# results, and goes through them comparing paths, even if they have different
# versioning.
###########################################################################
"""
   usage: %prog <file1> <file2>
   e.g: python hlt_ComparePathsTiming.py file1.csv file2.csv
"""   

import os,sys
import subprocess
import string, re
import fileinput
import commands
import operator
from time import gmtime, localtime, strftime
import io
#just a debug flag
DEBUG = False


###############################################################
def usage():
###############################################################

    if (DEBUG):
        print "This is the usage function"
        
    print '\n'
    print 'Usage: '+sys.argv[0]+' <file1> <file2>'
    print 'e.g.:  '+sys.argv[0]+' HLT_TimingAndRates_LunaV4.csv HLT_TimingAndRates_BeatriceV8.csv\n'

###############################################################
def get_paths_info(infile):
###############################################################
    theDict = {}
    thefile = open(infile,"r")
    firstLineFlag = True
    for fline in thefile.readlines():
        if firstLineFlag:
            firstLineFlag = False
            continue
        thelist = fline.split()[0].split(",")
        origtrig = thelist[0]
        slaintrig = thelist[0].rstrip("0123456789")
        thetiming = thelist[1]
        theDict[slaintrig] = []
        theDict[slaintrig].append(origtrig)
        theDict[slaintrig].append(thetiming)

    return theDict

#######################################################
def print_tuples(sDic,label,max,thefile):
#######################################################
    print label
    thefile.write(label+"\n")
    n = 0
    for p in sDic:
        if (n < max):
            print p
            thefile.write(str(p)+"\n")
        else:
            break
        n = n + 1
        


#######################################################
def print_csv_and_txt_files(repo1,repo2,file1,file2):
#######################################################

    #compare based on first container, which
    #should have paths in the newest menu
    fname1 = file1.split("_")[2].rstrip(".csv")
    fname2 = file2.split("_")[2].rstrip(".csv")
    #print fname1
    #print fname2
    
    #create csv file
    csv_file_title = "PathTimingComparison_"+fname1+"_Vs_"+fname2+".csv"
    txt_file_title = "PathTimingComparison_"+fname1+"_Vs_"+fname2+".txt"
    theTitle = unicode(csv_file_title)
    os.system("rm -f "+csv_file_title)
    os.system("rm -f "+txt_file_title)
    f = io.open(theTitle,'w',encoding='utf8')
    #no need to encode the txt file
    ftxt = open(txt_file_title,'w')

    #to keep track of most offending paths and largest differences
    #with respect to the new menu
    mostOffending = {}
    mostIncreasing = {}
    mostRelChange = {}

    #loop over paths
    countk = 0
    for p in repo1:
        p1name = repo1[p][0]
        p1timing = float(repo1[p][1])
        pdiff = -999.0
        pratio = -999.0
        prel = -999.0
        p2name = "N/A"
        p2timing = 0.
        #check if path is in repo2
        isPath = repo2.get(p)
        if isPath:
            p2name = repo2[p][0]
            p2timing = float(repo2[p][1])
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
            theCsvLine = unicode(fname1+",Timing (ms),"+fname2+",Timing (ms),["+fname1+"-"+fname2+"] (ms),["+fname1+"/"+fname2+"] (ms),[("+fname1+"-"+fname2+")/"+fname2+"]\n")
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
    off_label = "Most time-consuming paths ["+fname1+" Menu]\n('Path', timing (ms))"
    print_tuples(sorted_mostOffending,off_label,maxitems,ftxt)
#    print sorted_mostOffending
    inc_label = "\nPaths with the most timing increment ["+fname1+" Menu - "+fname2+" Menu]\n('Path', increment in timing (ms))"
    print_tuples(sorted_mostIncreasing,inc_label,maxitems,ftxt)
    dec_label = "\nPaths with the most timing decrement ["+fname1+" Menu - "+fname2+" Menu]\n('Path', decrement in timing (ms))"
    print_tuples(sorted_mostDecreasing,dec_label,maxitems,ftxt)
    rel_label = "\nPaths with the most relative change in timing [ABS("+fname1+" Menu - "+fname2+" Menu)/"+fname2+" Menu]\n('Path', absolute relative change)"
    print_tuples(sorted_mostRelChange,rel_label,maxitems,ftxt)
    
       
###############################################################
def main():
###############################################################
    #check the number of parameter
    numarg = len(sys.argv)
    if numarg < 2:
        usage()
        return 1

    infile1 = sys.argv[1]
    infile2 = sys.argv[2]

    #check if input files exist
    if  not(os.path.isfile(infile1)):
        print infile1+" does not exist. Please check."
        sys.exit(1)
    if  not(os.path.isfile(infile2)):
        print infile2+" does not exist. Please check."
        sys.exit(1)


    #get the paths (without versioning) timing info in containers 
    repo1 = get_paths_info(infile1)
    repo2 = get_paths_info(infile2)

    #make the paths comparison and print csv file
    print_csv_and_txt_files(repo1,repo2,infile1,infile2)
    

#######################################################
if __name__ =='__main__':
#######################################################
    sys.exit(main())
