import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils

#the_json = 'myjson_[PILEUP].json'
#the_fileout = 'HLTPhysics_[PILEUP]_306091.root'
the_fileout = 'L1Skim_PS12_306432.root'

process = cms.Process("CMA")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(30000))

#mylist = FileUtils.loadListFromFile ('filelist.txt')
#readFiles = cms.untracked.vstring( *mylist)

from list_ZB_LowPU_306432_cff import *

process.source = cms.Source("PoolSource",
#                            fileNames = readFiles,
                            fileNames = cms.untracked.vstring(inputFiles),
#                            lumisToProcess = cms.untracked.VLuminosityBlockRange('239785:1800-239785:2000'),
                            skipEvents = cms.untracked.uint32(0),
                            dropDescendantsOfDroppedBranches=cms.untracked.bool(False),
                            inputCommands=cms.untracked.vstring(
        "drop *",
        "keep *_TriggerResults_*_HLT",
        "keep *_hltGtStage2ObjectMap_*_*",
        "keep *_hltTriggerSummaryAOD_*_HLT",
        "keep *_rawDataCollector_*_*"
        )
                            );

import FWCore.PythonUtilities.LumiList as LumiList

#process.source.lumisToProcess = LumiList.LumiList(filename = 'myjson_301567.json').getVLuminosityBlockRange()
#process.source.lumisToProcess = LumiList.LumiList(filename = the_json).getVLuminosityBlockRange()


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string(the_fileout),
                               maxSize = cms.untracked.int32(3500000),
                               outputCommands = cms.untracked.vstring(
        "drop *",
        "keep *_TriggerResults_*_HLT",
        "keep *_hltGtStage2ObjectMap_*_*",
        "keep *_hltTriggerSummaryAOD_*_HLT",
        "keep *_rawDataCollector_*_*",
)
);

process.myEndPath = cms.EndPath(process.out)
        
