#!/usr/bin/env python
############################################################################
#
# Edgar Carrera
# ecarrera@cern.ch
#
# April, 2018
# This script takes as input a directory path like
# /eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/SKIM/data/2018/ZeroBias2017F/L1Menu_2018_v040/ZB_2017F_PU56to58_L1uGT_V3/
# which has a lot of subdirectories and extract all the *.root files from them with full
# path address.  It spits out a file called filelist.txt with all the files with full path
##########################################################################
"""
   usage: %prog [options]
   -p, --path = PATH: top path of directory structure
   -f, --file = FILE: top path of directory structure
"""

import os,sys
import fileinput,io
import string, re
import subprocess

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
def scout_directories(dicOpt):
#######################################################
    thepath = dicOpt['path']
    thefilen = dicOpt['file']

    fn = io.open(thefilen,'w')  

    result = [os.path.join(dp, f) for dp, sp, filenames in os.walk(thepath) for f in filenames if os.path.splitext(f)[1] == '.root']

    for f in result:
        str_out = "root://eoscms.cern.ch/"+f+"\n"
#        print str_out
        fn.write(unicode(str_out))

    return
#######################################################
def get_default_options(option):
#######################################################
    dicOpt = {}

    dicOpt['path']= str(option.path)


    if not option.file:
        dicOpt['file']= "filelist.txt"
    else:
        dicOpt['file']= str(option.file)

    return dicOpt

#######################################################
if __name__ =='__main__':
#######################################################

    #import optionparser
    option,args = parse(__doc__)
    if not args and not option:
        exit()

    #safety checks 
    if not option.path:
        print "Provide a directory path ..."
        exit()
        

    #set default options
    dicOpt = get_default_options(option)

    #print configuration
    for k in dicOpt:
        print str(k)+" = "+str(dicOpt[k])

    #generate the filelist file
    scout_directories(dicOpt)
