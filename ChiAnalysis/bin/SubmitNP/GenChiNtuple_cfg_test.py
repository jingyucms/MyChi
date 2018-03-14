import FWCore.ParameterSet.Config as cms
import os 

process = cms.PSet()

process.fwliteInput = cms.PSet(
    fileNames   = cms.vstring(
                "/uscms_data/d3/jingyu/ChiAnalysis/DMsample/Axial_Dijet_LO_Mphi_4000_1_1p0_1p0_Mar515.root",
    ),
    maxEvents   = cms.int32(-1),
    outputEvery = cms.uint32(50000),
)

process.fwliteOutput = cms.PSet(
    fileName  = cms.string("Axial_Dijet_LO_Mphi_4000_1_1p0_1p0_Mar515_smr_test.root"),
)

process.GenChiAnalysis = cms.PSet(
    GenJets = cms.InputTag('ak4GenJets'),
    Source = cms.InputTag("externalLHEProducer"),
    Smearing = cms.string("CrystalBall"),
    AK4_SF = cms.bool(True),
    DATAtoMC_SF = cms.bool(True),
    doSys = cms.bool(False),
    sysPlus = cms.bool(False),
    CrossSection = cms.double(0.1634881),
    SmearMax = cms.double(2),
    dmWeight = cms.bool(True)
)

