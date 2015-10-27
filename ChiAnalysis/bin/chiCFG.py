import FWCore.ParameterSet.Config as cms
import os
NEVT=-1

mass="AAAA"
XSECTION=BBBB
# mass="2500"
# mass="3700"

## SMEARING="Gaussian"
SMEARING="CrystalBall"
smearMax=CCCC

## Generator="pythia8"
Generator="DDDD"

DOSYS=False
## DOSYS=True
SysPlus=False

IFILE="XXXX"
## FileList="filelists/QCD_"+Generator+"_m" + mass + "/filelist_"+IFILE+".list"
FileList="filelists/"+Generator+"_m" + mass + "_50000__Oct1" + "/filelist_"+IFILE+".list"

print FileList
infiles = [line.strip() for line in open(FileList, 'r')]

OutDir=os.path.join('GenOutput_13TeV',Generator+"_"+SMEARING)
if SMEARING == "CrystalBall":
    OutDir=OutDir +"_Trunc" + str(smearMax)

## OutDir=os.path.join(OutDir,'_m'+mass)

OutFile=os.path.join(OutDir,'chiSmearing_8TeV_m' +mass)
# OutFile='GenOutput_new/chiSmearing_8TeV_'+ Generator +'_m'+mass+'_'+SMEARING
if SMEARING == "Gaussian":
    if DOSYS:
        if SysPlus:
            OutFile=OutFile + "_SysPlus"
        else:
            OutFile=OutFile + "_SysMinus"
elif SMEARING == "CrystalBall":
    pass
    # OutFile=OutFile + "_Trunc" + str(smearMax)
else:
    print "Undefined smearing"
    OutFile="XXX"

OutFile=OutFile + "_" + IFILE + ".root"
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
    # fileName  = cms.string('analyzeChi_8TeV_ci_90.root'),  ## mandatory
)

process.chiAnalyzer = cms.PSet(
    ## input specific for this analyzer
    GenJets = cms.InputTag('ak4GenJets'),
    Smearing = cms.string(SMEARING),
    CrossSection = cms.double(XSECTION),
    doSys = cms.bool(DOSYS),
    sysPlus = cms.bool(SysPlus),
    SmearMax = cms.double(smearMax)
)
