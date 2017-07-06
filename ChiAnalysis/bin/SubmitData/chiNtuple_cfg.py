import FWCore.ParameterSet.Config as cms
import os

# nevents=50000
nevents=0

myTrigger="PFHT900";
## myTrigger="PFHT650";

jobIndex=os.environ['JOBNUM']

ntuples="filelists/ReRecoData2016v3/ntuples_"+jobIndex+".list"
output="/afs/cern.ch/work/z/zhangj/private/jetUnfold/data/hstsData_vReReco_v3/chiNtuple_"+myTrigger+"_"+jobIndex+".root"

process = cms.PSet()
process.chiNtuples = cms.PSet(
    ## input specific for this analyzer
    Nevts = cms.int32(nevents), ## 0 or negative to process all events    
    CrossSection = cms.double(1.),
    InputFiles = cms.string(ntuples),
    OutputFile = cms.string(output),
    IsData = cms.bool(True),
    DoGaussian = cms.bool(False),
    AK4_SF = cms.bool(False),
    DATAtoMC_SF = cms.bool(False),
    SmearMax = cms.double(0),
    Trigger = cms.string(myTrigger),
    SysErr = cms.int32(0) ## +-1 to smear by additional +-10%,  anything else no addtional smearing
)
