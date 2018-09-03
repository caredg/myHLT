#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
import sys
import cx_Oracle
import string
import os
#import time
#import re


#json_DCS = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/DCSOnly/json_DCSONLY.txt" # 2016
#json_DCS = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/DCSOnly/json_DCSONLY.txt" # 2017
#json_DCS = "/afs/cern.ch/work/t/tosi/public/STEAM/json/2e34_v1p0p2_cleaned.json"
#json_DCS = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/DCSOnly/json_DCSONLY.txt"
json_DCS = "myjson.json"

if len(sys.argv)!=4 :
   print "Usage:",sys.argv[0]," HLTkey minPU maxPU"
   if len(sys.argv)!=5:
      exit(0)
   else:
      input_json = sys.argv[4]
else:
   input_json = json_DCS

import json
json_raw = json.load(open(input_json))
#print json_raw

connstr='cms_trg_r/X3lmdvu4@cms_orcon_adg'
conn = cx_Oracle.connect(connstr)
curs = conn.cursor()
curs.arraysize=50

HLTkeys=[]
if (sys.argv[1]).find(","):
   tmp = (sys.argv[1]).split(",")
   from collections import OrderedDict
   HLTkeys=list(OrderedDict.fromkeys(tmp))
else:
   HLTkeys=sys.argv[1]
#print HLTkeys

minPU=sys.argv[2]
maxPU=sys.argv[3]

#print minPU,maxPU

DEBUG=False
#DEBUG=True
if DEBUG:

   for runnumber in json_raw:
      for rangeLS in json_raw[runnumber]:
         print rangeLS[0],rangeLS[1]

#   query="select runnumber from cms_wbm.runsummary a, cms_hlt_gdr.u_confversions b where a.hltkey=b.configid and b.name='/cdaq/physics/firstCollisions17/v3.0/HLT/V2'"
#   query="select runnum,lsnum,recorded,avgpu from cms_lumi_prod.online_result_4 where runnum=294943" # last run in this table is 293707
#   query="select runnum,lsnum,recorded,avgpu from cms_lumi_prod.online_result_5 where runnum=294943"
   for HLTkey in HLTkeys:
      query="select runnum,lsnum,recorded,avgpu from cms_lumi_prod.online_result_5 where runnum in (select runnumber from cms_wbm.runsummary a, cms_hlt_gdr.u_confversions b where a.hltkey=b.configid and b.name='"+HLTkey+"') and avgpu>"+minPU+" and avgpu<"+maxPU + " order by runnum,lsnum" # 2017 (foca d'ovatta !)
      print query

      curs.execute(query)
      print curs
      for rows in curs:
#         print rows
         print rows[0],rows[1],rows[3]

   import commands
   hltPATH='HLT_ZeroBias_v*'
   BRILCALC_COMMAND="brilcalc lumi --byls -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/DCSOnly/json_DCSONLY.txt -b 'STABLE BEAMS' --without-checkjson -r 294986 -u 1e30/cm2s --normtag hfoc17v1 --type HFOC"

#   print BRILCALC_COMMAND
   out = commands.getstatusoutput(BRILCALC_COMMAND)
   print out
   if out[0] != 0:
      print 'issue w/ brilcalc'

      out_split_lines = out[1].splitlines()
      
      for line in out_split_lines:
         print line

         if "HLT_" in str(line) and ':' in str(line):
            out_split = re.split(' | ',line)
#        print out_split
            run_fill = re.split(':',out_split[1])
            for i in out_split:
               if len(i) == 0: continue
               if str(i) == '|':
                  continue
               else:
                  lumi = i

   exit()

#Run1 query="select runnum,ls,recorded,avg_pu from cms_lumi_prod.HFLUMIRESULT where runnum in (select runnumber from cms_wbm.runsummary a, cms_hlt_gdr.u_confversions b where a.hltkey=b.configid and b.name='"+sys.argv[1]+"') and avg_pu>"+sys.argv[2]+" and avg_pu<"+sys.argv[3] + " order by runnum,ls"
#Run2
print '{',
#prehlt=1

useBRILCALC=True
#useBRILCALC=False

import re
if useBRILCALC:

   import commands
   hltPATH='HLT_ZeroBias_v*'
#   BRILCALC_COMMAND="brilcalc lumi --byls -i "+ input_json + " -b 'STABLE BEAMS' --without-checkjson -u 1e30/cm2s --normtag hfoc17v1 --type HFOC -r 304119"
#   BRILCALC_COMMAND="brilcalc lumi --byls -i "+ input_json + " -b 'STABLE BEAMS' --without-checkjson -u 1e30/cm2s --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json -r 302674"
#   BRILCALC_COMMAND="brilcalc lumi --byls -i "+ input_json + " -b 'STABLE BEAMS' --without-checkjson -u 1e30/cm2s -r 316457"
#   BRILCALC_COMMAND="brilcalc lumi --byls -i "+ input_json + " -b 'STABLE BEAMS' --without-checkjson -u 1e30/cm2s --type HFET -r 319941"
   BRILCALC_COMMAND="brilcalc lumi --byls -i "+ input_json + " -b 'STABLE BEAMS' -u 1e30/cm2s --type HFET -r 321755"


#   print BRILCALC_COMMAND
   out = commands.getstatusoutput(BRILCALC_COMMAND)
#   print out
#   print out
   if out[0] != 0:
      print 'issue w/ brilcalc'
   
   prerun=0
   prels=0
   lastlumi=0


   out_split_lines = out[1].splitlines()

   for line in out_split_lines:
#      print line
      
      if "STABLE" in str(line) and ':' in str(line):
         out_split = re.split(' | ',line)
#         print out_split
         run_fill = re.split(':',out_split[1])
#         print run_fill
         run = run_fill[0]
#         print run
         LS = re.split(':',out_split[3])
         lumisection = LS[0]
         count=0
         for i in out_split:
#            print count,i 
            count=count+1
            if len(i) == 0: continue
            if str(i) == '|': continue
#            if str(i) == 'HFOC': continue
#            if str(i) == 'PLTZERO': continue
            if str(i) == 'HFET': continue
            else:
               pu = i
#         print pu

         if pu > maxPU or pu < minPU: continue

         for i in range(0,len(json_raw[str(run)])):
            if lumisection < json_raw[str(run)][i][0] and lumisection > json_raw[str(run)][i][1]:
               continue

         if run!=prerun:

            prerun=run
            if prels>0:
               string = ',',str(prels),']],'
               print "".join(string),
               prels=0
               lastlumi=0
            string = '"',str(run),'": [[',str(lumisection)
            print "".join(string),
            prels=lumisection
         else:
            if prels>0:
               if  lumisection!=str((int(prels)+1)):
                  string = ',',str(prels),'],[',str(lumisection)
                  print "".join(string),
               prels=lumisection
               lastlumi=prels
               continue
            else:
               prels=lumisection   

   lastlumi=prels
   string = ',',str(lastlumi),']]'
   print "".join(string),         
   
else:
   for HLTkey in HLTkeys:
      if prehlt!=0:
         print ',',
     
         prehlt+=1
#   query="select runnum,lsnum,recorded,avgpu from cms_lumi_prod.online_result_4 where runnum in (select runnumber from cms_wbm.runsummary a, cms_hlt_gdr.u_confversions b where a.hltkey=b.configid and b.name='"+HLTkey+"') and avgpu>"+minPU+" and avgpu<"+maxPU + " order by runnum,lsnum" # 2016
         query="select runnum,lsnum,recorded,avgpu from cms_lumi_prod.online_result_5 where runnum in (select runnumber from cms_wbm.runsummary a, cms_hlt_gdr.u_confversions b where a.hltkey=b.configid and b.name='"+HLTkey+"') and avgpu>"+minPU+" and avgpu<"+maxPU + " order by runnum,lsnum" # 2017 (foca d'ovatta !)
         print query

         curs.execute(query)
##   print curs

         prerun=0
         prels=0
         lastlumi=0

         for rows in curs:
#      print rows
            run=rows[0]

            if str(run) not in json_raw:
#         print run,"is not available ... SKIP IT"
               continue

         lumisection=rows[1]
         instlumi=rows[2]
         pu=rows[3]


         for i in range(0,len(json_raw[str(run)])):
            if lumisection < json_raw[str(run)][i][0] and lumisection > json_raw[str(run)][i][1]:
               continue

         if run!=prerun:
            if prels>0:
               string = ',',str(prels),']],'
               print "".join(string),
            string = '"',str(run),'": [[',str(lumisection)
            print "".join(string),
         else:
            if  lumisection!=(prels+1):
               string = ',',str(prels),'],[',str(lumisection)
               print "".join(string),
     
         prerun=run
         prels=lumisection
         lastlumi=prels
         string = ',',str(lastlumi),']]'
         print "".join(string),

print '}'


#print "Run =",run," lumi =",lumisection," instlumi =",instlumi,' pu =',pu 
     #os.system("source ./setup_pyroot.sh;which root ;root -l   -b make_rate_plots.C+\("+temp+"\);")
     #ii=ii+1


