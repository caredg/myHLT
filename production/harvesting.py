import FWCore.ParameterSet.Config as cms

process = cms.Process('HARVESTING')

# read all the DQMIO files produced by the previous jobs
process.source = cms.Source("DQMRootSource",
                            fileNames = cms.untracked.vstring(
#                                "file:DQMIO.root",
                                "file:DQMIO1.root",
                                "file:DQMIO2.root",
                                )
                            )

# DQMStore service
process.load('DQMServices.Core.DQMStore_cfi')

# FastTimerService client
process.load('HLTrigger.Timer.fastTimerServiceClient_cfi')
process.fastTimerServiceClient.dqmPath = "HLT/TimerService"
# timing VS lumi
process.fastTimerServiceClient.doPlotsVsScalLumi  = cms.bool(True)
process.fastTimerServiceClient.doPlotsVsPixelLumi = cms.bool(False)
process.fastTimerServiceClient.scalLumiME = cms.PSet(
        folder = cms.string('HLT/LumiMonitoring'),
        name   = cms.string('lumiVsLS'),
        nbins  = cms.int32(5000),
        xmin   = cms.double(0),
        xmax   = cms.double(20000)
    )



# DQM file saver
process.load('DQMServices.Components.DQMFileSaver_cfi')
process.dqmSaver.workflow = "/HLT/FastTimerService/All"

# PS column VS lumi
process.load('DQM.HLTEvF.dqmCorrelationClient_cfi')
process.psColumnVsLumi = process.dqmCorrelationClient.clone(
       me = cms.PSet(
              folder = cms.string("HLT/PSMonitoring"),
              name   = cms.string("psColumnVSlumi"),
              doXaxis = cms.bool( True ),
              nbinsX = cms.int32( 5000),
              xminX  = cms.double(    0.),
              xmaxX  = cms.double(20000.),
              doYaxis = cms.bool( False ),
              nbinsY = cms.int32 (   8),
              xminY  = cms.double(   0.),
              xmaxY  = cms.double(   8.),
           ),
       me1 = cms.PSet(
              folder   = cms.string("HLT/LumiMonitoring"),
              name     = cms.string("lumiVsLS"),
              profileX = cms.bool(True)
           ),
       me2 = cms.PSet(
              folder   = cms.string("HLT/PSMonitoring"),
              name     = cms.string("psColumnIndexVsLS"),
              profileX = cms.bool(True)
           ),
    )

process.load('DQM.HLTEvF.psMonitorClient_cfi')
process.psChecker = process.psMonitorClient.clone()

process.DQMFileSaverOutput = cms.EndPath( process.fastTimerServiceClient + process.psColumnVsLumi + process.psChecker + process.dqmSaver)
