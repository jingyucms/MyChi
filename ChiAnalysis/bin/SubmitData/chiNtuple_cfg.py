import FWCore.ParameterSet.Config as cms
import os

# nevents=100000
nevents=0

jobIndex=os.environ['JOBNUM']

ntuples="filelists/1pt3invfb/fileList_"+jobIndex+".txt"
output="hsts/chiNtuple_data_"+jobIndex+".root"

process = cms.PSet()
process.chiNtuples = cms.PSet(
    ## input specific for this analyzer
    Nevts = cms.int32(nevents), ## 0 or negative to process all events    
    CrossSection = cms.double(1.),
    InputFiles = cms.string(ntuples),
    OutputFile = cms.string(output),
    IsData = cms.bool(True),
    DoGaussian = cms.bool(False),
    SmearMax = cms.double(0)
)
