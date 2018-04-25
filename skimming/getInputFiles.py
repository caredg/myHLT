import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils

process = cms.Process("CMA")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(50000))
#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(30000))

mylist = FileUtils.loadListFromFile ('filelist.txt')
readFiles = cms.untracked.vstring( *mylist)


process.source = cms.Source("PoolSource",
                            fileNames = readFiles,
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

process.source.lumisToProcess = LumiList.LumiList(filename = 'myjson.json').getVLuminosityBlockRange()


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('HLTPhysics_305178.root'),
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
        
