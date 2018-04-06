#!/usr/bin/env python
############################################################################
#
# Edgar Carrera
# ecarrera@cern.ch
#
# July 14, 2017
# Script to plot the timing vs Lumi and vs LS
############################################################################

"""
   usage: %prog [options]
   -f, --dqmfile = DQMFILE: DQM file from the harvesting step
   -r, --run = RUN: Run number
   -p, --proc = PROC: Name of the process
   -w, --lumimin = LUMIMIN: Luminosity min value
   -x, --lumimax = LUMIMAX: Luminosity max value
   -y, --lsmin = LSMIN: Min lumi section
   -z, --lsmax = LSMAX: Max lumi section

"""

import os,sys
import string, re
import fileinput
import commands
from time import gmtime, localtime, strftime
from ROOT import gROOT, TCanvas, TFile, TLegend, gStyle, TH1F, TH2F, TProfile, TAttMarker

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
def print_histogram_in_terminal(hist):
#######################################################
    print "Histogram "+hist.GetName()
    nbins = hist.GetNbinsX()
    for thebin in range(0,nbins+1):
        thecon = hist.GetBinContent(thebin)
        theerr = hist.GetBinError(thebin)
        if(thecon <> 0):
            print "bin: "+str(thebin)+" content: "+str(thecon)+" error: "+str(theerr)
    


#######################################################
def make_plot_timing_vs_lumi(dicOpt):
#######################################################
    thefile = dicOpt['dqmfile']
    therun = dicOpt['run']
    theproc = dicOpt['proc']
    maxlumi = float(dicOpt['lumimax'])
    minlumi = float(dicOpt['lumimin'])
    
    theTFile = TFile(thefile)
    pathname = "DQMData/Run %s/HLT/Run summary/TimerService/process %s time_real_VsScalLumi" %(therun,theproc)
#    pathname = "DQMData/Run %s/HLT/Run summary/TimerService/eventtime_real_VsScalLumi" %(therun)
    print pathname
    hist = theTFile.Get(pathname)
    #print "Type is", type(hist)
    hist.GetXaxis().SetRangeUser(minlumi,maxlumi)
    print_histogram_in_terminal(hist)
    c1 = TCanvas('c1')
    c1.cd()
    hist.Draw()
    c1.Print("Timing_vs_Luminosity.png")


    


#_________________________________________________________________________

#######################################################
def get_default_options(option):
#######################################################
    dicOpt = {}

    dicOpt['dqmfile']= str(option.dqmfile)
    dicOpt['run']= str(option.run)

    if not option.proc:
        dicOpt['proc']= "TIMING"
    else:
        dicOpt['proc']= str(option.proc)

    #this is in units of 10e30 Hz/cm2 as the FastTimerService
    if not option.lumimax:
        dicOpt['lumimax'] = 20000
    else:
        dicOpt['lumimax'] = option.lumimax
        
    #this is in units of 10e30 Hz/cm2 as the FastTimerService
    if not option.lumimin:
        dicOpt['lumimin'] = 0
    else:
        dicOpt['lumimin'] = option.lumimin


    if not option.lsmax:
        dicOpt['lsmax'] = 500
    else:
        dicOpt['lsmax'] = option.lsmax

    if not option.lsmin:
        dicOpt['lsmin'] = 0
    else:
        dicOpt['lsmin'] = option.lsmin

    return dicOpt

#######################################################
if __name__ =='__main__':
#######################################################

    #import optionparser
    option,args = parse(__doc__)
    if not args and not option:
        exit()

    #safety checks 
    if not option.dqmfile:
        print "Provide a DQM file. Quiting ..."
        exit()
        
    if not option.run:
        print "Provide a run number. Quiting ..."
        exit()
        

    #set default options
    dicOpt = get_default_options(option)

    #print configuration
    for k in dicOpt:
        print str(k)+" = "+str(dicOpt[k])

    #make plot timing vs luminosity
    make_plot_timing_vs_lumi(dicOpt)
    
    
