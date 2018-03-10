#!/usr/bin/env python
############################################################################
#
# Edgar Carrera
# ecarrera@cern.ch
#
# November, 2017
# Script to plot the timing vs PU for measurements in different files
############################################################################

"""
   usage: %prog [options]
   -f, --file = FILE: text file with list of root DQM harvested files (they should be in order of ascending PU)
   -r, --run = RUN: Run number 
   -p, --proc = PROC: Name of the process (default: TIMING)
   -i, --pumin = PUMIN: PU min value
   -a, --pumax = PUMAX: PU max value
   -b, --numbin = NUMBIN: number of bins for the histogram (default: 5)
   -s, --ps = PS: name of prescale column used
"""

import os,sys
import string, re
import fileinput
import commands
from time import gmtime, localtime, strftime
from ROOT import gROOT, TCanvas, TFile, TLegend, gStyle, TH1F, TH2F, TProfile, TAttMarker
from array import array

maxTiming = 300

# _____________________OPTIONS_______________________________________________

############################################################################
# Code taken from http://code.activestate.com/recipes/278844/
############################################################################
import optparse
USAGE = re.compile(r'(?s)\s*usage: (.*?)(\n[ \t]*\n|$)')
def nonzero(self): # will become the nonzero method of optparse.Values
    "True if options were given"
    for v in self.__dict__.itervalues():
        if v is not None: return True
    return False

optparse.Values.__nonzero__ = nonzero # dynamically fix optparse.Values

class ParsingError(Exception): pass

optionstring=""

def exit(msg=""):
    raise SystemExit(msg or optionstring.replace("%prog",sys.argv[0]))

def parse(docstring, arglist=None):
    global optionstring
    optionstring = docstring
    match = USAGE.search(optionstring)
    if not match: raise ParsingError("Cannot find the option string")
    optlines = match.group(1).splitlines()
    try:
        p = optparse.OptionParser(optlines[0])
        for line in optlines[1:]:
            opt, help=line.split(':')[:2]
            short,long=opt.split(',')[:2]
            if '=' in opt:
                action='store'
                long=long.split('=')[0]
            else:
                action='store_true'
            p.add_option(short.strip(),long.strip(),
                         action = action, help = help.strip())
    except (IndexError,ValueError):
        raise ParsingError("Cannot parse the option string correctly")
    return p.parse_args(arglist)

#######################################################
def get_yvals_fromFiles(thefile,therun,theproc):
#######################################################
    yvals = []
    yerrs = []
    irun = '305636'
    filelist = open(thefile,"r")
    myindex = 0
    for filein in filelist.readlines():
        temp = []
        if myindex>3:
            irun = '306091'
        print "Working on file: "+filein
        theTFile = TFile(filein.rstrip(),"READ")
        histpath = "DQMData/Run %s/HLT/Run summary/TimerService/process %s time_real_VsPU" %(irun,theproc)
        hist = theTFile.Get(histpath)
#        print type(hist)
        yvals.append(hist.GetMean(2))
        yerrs.append(hist.GetMeanError(2))
        myindex = myindex+1
        
    return yvals,yerrs

#######################################################
def get_xvals(minpu,maxpu,numbin):
#######################################################
    binstep = (maxpu-minpu)/numbin
    upedge = minpu+binstep
    dedge = minpu
    xbins = []
    xlabels = []
    while upedge <= maxpu:
        xbins.append(dedge)
        uplabel = str(upedge)
        dlabel = str(dedge)
        xlabels.append(dlabel+"-"+uplabel)
        upedge = upedge+binstep
        dedge = dedge+binstep

    return xbins,xlabels

########################################################################################
def fill_and_print_the_histogram(xbins,xlabels,yvals,yerrs,therun,theps):
########################################################################################
    #thetitle = "Offline Timing Vs. PileUp (Run: "+therun+", PS: "+theps+")"
    thetitle = "Offline Timing Vs. PileUp (Runs 305636 and 306091, PS:1.5e34)"  
    theplotname = "timing_vs_PU_Run"+therun+"_PS"+theps
    h = TH1F("h",thetitle,len(xbins),xbins[0],xbins[len(xbins)-1])
#    gStyle.SetTitleFontSize(0.02)
    myindex = 0
    for thebin in range(1,len(xbins)+1):
        h.SetBinContent(thebin,yvals[myindex])
        h.SetBinError(thebin,yerrs[myindex])
        h.GetXaxis().SetBinLabel(thebin,xlabels[myindex])
        myindex = myindex +1

    h.GetYaxis().SetTitle("Timing [ms]")
    h.GetXaxis().SetTitle("Average PU")
    h.SetLineColor(2)
    h.SetLineWidth(3)
    gStyle.SetOptStat(False)    
    c1 = TCanvas('c1','Luminosity Vs. PU',1200,1000)
    c1.cd()
    c1.SetGrid()
    h.Draw("e")
    c1.Print(theplotname+".png")
    c1.Print(theplotname+".pdf")
    



#######################################################
def make_plot_timing_vs_pu(dicOpt):
#######################################################
    txtfile = dicOpt['file']
    therun = dicOpt['run']
    theproc = dicOpt['proc']
    maxpu = int(dicOpt['pumax'])
    minpu = int(dicOpt['pumin'])
    numbin = int(dicOpt['numbin'])
    theps = dicOpt['ps']
    
    #get the x bins for the histogram
    #xbins,xlabels = get_xvals(minpu,maxpu,numbin)
    xbins = [50,52,54,56,60,64,68,72,76,80]
    xlabels = ['50-52','52-54','54-56','56-58','60-64','64-68','68-72','72-76','76-80','80-84']
    
    #get the y and yerrors from all the files
    yvals,yerrs = get_yvals_fromFiles(txtfile,therun,theproc)

    #fill the final histogram
    fill_and_print_the_histogram(xbins,xlabels,yvals,yerrs,therun,theps)

#_________________________________________________________________________

#######################################################
def get_default_options(option):
#######################################################
    dicOpt = {}

    dicOpt['file']= str(option.file)
    dicOpt['run']= str(option.run)
    dicOpt['pumax'] = option.pumax
    dicOpt['pumin'] = option.pumin
    dicOpt['ps'] = option.ps
    
    if not option.proc:
        dicOpt['proc']= "TIMING"
    else:
        dicOpt['proc']= str(option.proc)

    if not option.numbin:
        dicOpt['numbin'] = 5
    else:
        dicOpt['numbin'] = option.numbin


    return dicOpt

#######################################################
if __name__ =='__main__':
#######################################################

    #import optionparser
    option,args = parse(__doc__)
    if not args and not option:
        exit()

    #safety checks 
    if not option.file:
        print "Provide a text file with DQM files. Quiting ..."
        exit()
    if not option.run:
        print "Provide a run number. Quiting ..."
        exit()
    if not option.pumax:
        print "Need pumax .... Quiting...."
        exit()
    if not option.pumin:
        print "Need pumin .... Quiting...."
        exit()
    if not option.ps:
        print "Need ps (prescale column name) .... Quiting...."
        exit()


    #set default options
    dicOpt = get_default_options(option)

    #print configuration
    for k in dicOpt:
        print str(k)+" = "+str(dicOpt[k])

    #make plot timing vs luminosity
    make_plot_timing_vs_pu(dicOpt)
    
    
