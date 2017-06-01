import FWCore.ParameterSet.Config as cms
import os 

process = cms.PSet()

process.fwliteInput = cms.PSet(
    fileNames   = cms.vstring(
                #"root://eoscms//eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7/EXOVVTree_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIIFall15MiniAODv2_PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1_76.root",
                #"root://eoscms//eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7/EXOVVTree_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIIFall15MiniAODv2_PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1_77.root",
                #"root://eoscms//eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7/EXOVVTree_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIIFall15MiniAODv2_PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1_78.root",
                #"root://eoscms//eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7/EXOVVTree_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIIFall15MiniAODv2_PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1_79.root",
                #"root://eoscms//eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7/EXOVVTree_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIIFall15MiniAODv2_PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1_8.root",
                #"root://eoscms//eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7/EXOVVTree_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIIFall15MiniAODv2_PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1_80.root",
                #"root://eoscms//eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7/EXOVVTree_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIIFall15MiniAODv2_PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1_81.root",
                #"root://eoscms//eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7/EXOVVTree_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIIFall15MiniAODv2_PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1_83.root",
                #"root://eoscms//eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7/EXOVVTree_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIIFall15MiniAODv2_PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1_84.root",
                #"root://eoscms//eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7/EXOVVTree_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIIFall15MiniAODv2_PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1_85.root",
        #"root://cmseos.fnal.gov//store/mc/RunIIFall15MiniAODv2/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/50000/0E115FDD-0CBA-E511-9145-44A842CF0600.root",
        "root://cmseos.fnal.gov//store/mc/RunIIFall15MiniAODv2/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/10000/9C60DF82-46B9-E511-978A-002590AC4C56.root",
    ),
    maxEvents   = cms.int32(1000),
    outputEvery = cms.uint32(50000),
)

process.fwliteOutput = cms.PSet(
    fileName  = cms.string("root://cmseos.fnal.gov//store/user/jingyu/jetUnfold/GenNtuple/2016PromptReco/madgraphMLM_CrystalBall/chiSmearing_13TeV_ht500to700_AK4sf_1_DataToMCsf_1_6.root"),
    #fileName = cms.string("/afs/cern.ch/user/z/zhangj/private/chi_analysis_2016/jetUnfold/CMSSW_8_0_23/src/MyChi/ChiAnalysis/bin/SubmitGen/test.root"),
)

process.GenChiAnalysis = cms.PSet(
    GenJets = cms.InputTag('slimmedGenJets'),
    Smearing = cms.string("CrystalBall"),
    AK4_SF = cms.bool(True),
    DATAtoMC_SF = cms.bool(True),
    doSys = cms.bool(False),
    sysPlus = cms.bool(False),
    CrossSection = cms.double(32100.0),
    SmearMax = cms.double(2)
)

