########################
# Authors:
# Original from Daniel Aguilar, dalejandro_acdc@yahoo.com (June, 2018)
# Modified by Edgar Carrera, ecarrera@cern.ch (April, 2020)
# 
# This script analyze the structure of the peaks
# in the overall timing plot from HLT timing measurements.
# Ex: python hlt_AnalyzeTimingPeakStructure.py DQMfile.root runnumber lowerlimit upperlimit (in ms)
########################

import os,sys
import subprocess
import string, re
import fileinput
import operator
from time import gmtime, localtime, strftime
from ROOT import gPad, gROOT, TCanvas, TH1F, TFile, TLegend, gStyle,gDirectory
import io

#Common limit for individual path timing plots histograms
#The overall histogram goes up to 2000 ms but the individual ones only
#up to 1000 ms.
MAXUPPERLIM = 1000
#The main process name.  By default is TIMING.  Needs to be changed
#if needed
THEPROCESS = "TIMING"

###############################################################
class Duplet:
    def __init__(self, path, weight):
        self.path=path
        self.weight=weight
###############################################################

###############################################################
class Quartet:
    def __init__(self, path, module, pweight, mweight):
        self.path=path
        self.module=module
        self.pweight=pweight
        self.mweight=mweight
        self.weight=pweight*mweight
###############################################################


###############################################################
def usage():
###############################################################

    print 'Usage: '+sys.argv[0]+' <file> <run> <lowerlimit (ms)> <upperlimit (ms)>'
    print 'Example: '+sys.argv[0]+' myDQM.root 365645 100 200'

###############################################################
def getMostContributingModulesinRange(file,run,pathduplet):
###############################################################
    moduleList = []
    firstpathswitch = True
    maxmodtime = 0.
    tfile = TFile(file)
    dirname = "DQMData/Run %s/HLT/Run summary/TimerService/process %s paths" % (run, THEPROCESS)
    gDirectory.cd(dirname)
    #Loop over all the paths that were found to contribute
    #in the speciied range
    for pduplet in pathduplet:
        thepathname = pduplet.path
        hName = dirname+"/"+thepathname+"/module_time_real_running"
        thepathweight = pduplet.weight
        hist = tfile.Get(hName)
        #If first path get the denominator for the weight
        if firstpathswitch:
            maxmodtime = hist.GetMaximum()
            firstpathswitch = False
            #Loop over the modules and store the triplet
            nbins = hist.GetNbinsX()
        for thebin in range(1,nbins):
            themodname = hist.GetXaxis().GetBinLabel(thebin)
            themodtime = hist.GetBinContent(thebin)
            themodweight = themodtime/maxmodtime
            moduleList.append(Quartet(thepathname,themodname,thepathweight,themodweight))
            #print thepathname+", "+themodname+", "+str(themodweight*thepathweight)
    moduleList = sorted(moduleList,key=lambda quartet: quartet.weight,reverse=True)
    return moduleList
    
###############################################################
def getMostContributingPathsInRange(file,run,lowerlimit,upperlimit):
###############################################################
    pathList = []
    tfile = TFile(file)
    dirname = "DQMData/Run %s/HLT/Run summary/TimerService/process %s paths" % (run, THEPROCESS)
    gDirectory.cd(dirname)
    #Loop over all the paths in the file to check which ones most contribute
    #to the specified timing range
    for thepath in gDirectory.GetListOfKeys():
        pathName = thepath.GetName()
        if (pathName.startswith("path ") and pathName.find("HLTriggerFinalPath") == -1):
            hName = dirname+"/"+thepath.GetName()+"/path time_real"
            hist=tfile.Get(hName)
            #manipulate the lowerlimit and upperlimit
            #to get the appropiate range in histogram
            #Get the bin numbers for the lowerlimit and upperlimit
            nbins = hist.GetNbinsX()
            lowerbin = 1
            upperbin = nbins
            for thebin in range(1,nbins):
                lowbinedge = hist.GetBinLowEdge(thebin)
                highbinedge =hist.GetBinLowEdge(thebin+1)
                if (lowerlimit>= lowbinedge and lowerlimit<highbinedge):
                    lowerbin = thebin
                if (upperlimit> lowbinedge and upperlimit<=highbinedge):
                    upperbin = thebin
            pathweight = hist.Integral(lowerbin,upperbin)/hist.Integral()
            #only add paths that actually contribute to the range
            if (pathweight>0):
                pathList.append(Duplet(pathName,pathweight))
    #order the paths by weight            
    pathList=sorted(pathList,key=lambda duplet: duplet.weight, reverse=True)

    return pathList

###############################################################
def print_results(modulequartet,file,lowerLimit,upperLimit):
###############################################################
    csv_file_title = unicode("PeakAnalysis_"+str(lowerLimit)+"To"+str(upperLimit)+".csv")
    os.system("rm -f "+csv_file_title)
    f = io.open(csv_file_title,'w',encoding='utf8')
    for modq in modulequartet:
        f.write(unicode(modq.path+", "))
        f.write(unicode(modq.module+", "))
        f.write(unicode(str(modq.weight)+", "))
        f.write(unicode(str(modq.pweight)+", "))
        f.write(unicode(str(modq.mweight)))
        f.write(unicode("\n"))
    
###############################################################
def main():
###############################################################    
    #check the number of parameter
    if len(sys.argv) < 5:
        usage()
        return 1
    #process input
    infile = sys.argv[1]
    run = sys.argv[2]
    lowerLimit = float(sys.argv[3])
    upperLimit = float(sys.argv[4])

    #check if input files exist
    if  not(os.path.isfile(infile)):
        print infile+" does not exist. Please check."
        sys.exit(1)

    #check the ranges of the limits
    if not(lowerLimit>=0 and upperLimit<=1000 and lowerLimit<upperLimit):
        print "Limits are not valid. Please check."
        sys.exit(1)
        
    #get the path list, ordered by fractional contribution to integral
    pathduplet = getMostContributingPathsInRange(infile,run,lowerLimit,upperLimit)
    #get modules weighted by path weight to integral times
    #real running time weight
    modulequartet = getMostContributingModulesinRange(infile,run,pathduplet)
    #print the results 
    print_results(modulequartet,run,lowerLimit,upperLimit)
    

#######################################################
if __name__ =='__main__':
#######################################################    
    sys.exit(main())
