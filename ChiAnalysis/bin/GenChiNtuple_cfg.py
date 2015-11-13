import FWCore.ParameterSet.Config as cms
import os
NEVT=100

## SMEARING="Gaussian"
SMEARING="CrystalBall"
smearMax=2.5

Generator="pythia8"
XSECTION=1.

DOSYS=False
## DOSYS=True
SysPlus=False

FileList="genfiles_" +Generator+ ".list"

print FileList
infiles = [line.strip() for line in open(FileList, 'r')]

OutDir=os.path.join('root://eoscms//eos/cms/store/caf/user/apana/Chi/GenOutput_13TeV',Generator+"_"+SMEARING)

if SMEARING == "CrystalBall":
    OutDir=OutDir +"_Trunc" + str(smearMax)


OutFile=os.path.join(OutDir,'chiSmearing_13TeV')
if SMEARING == "Gaussian":
    if DOSYS:
        if SysPlus:
            OutFile=OutFile + "_SysPlus"
        else:
            OutFile=OutFile + "_SysMinus"
elif SMEARING == "CrystalBall":
    pass
else:
    print "Undefined smearing"
    OutFile="XXX"

OutFile=OutFile + ".root"

#####################################################################################################

process = cms.PSet()

process.fwliteInput = cms.PSet(
    fileNames   = cms.vstring(
        infiles
        # 'root://eoscms//eos/cms/store/cmst3/user/hinzmann/fastsim/herwigpp_qcd_m1400___Sep4/PFAOD_1.root'
                              ), ## mandatory
    maxEvents   = cms.int32(NEVT),                             ## optional
    outputEvery = cms.uint32(50000),                            ## optional
)
    
process.fwliteOutput = cms.PSet(
    ## fileName  = cms.string('analyzeChi_14TeV_m'+massCut+'inf_CI20TEV.root'),  ## mandatory
    fileName  = cms.string(OutFile),  ## mandatory
)

process.GenChiAnalysis = cms.PSet(
    ## input specific for this analyzer
    GenJets = cms.InputTag('ak4GenJets'),
    Smearing = cms.string(SMEARING),
    CrossSection = cms.double(XSECTION),
    doSys = cms.bool(DOSYS),
    sysPlus = cms.bool(SysPlus),
    SmearMax = cms.double(smearMax)
)
