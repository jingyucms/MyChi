import FWCore.ParameterSet.Config as cms
import os

nevents=100000
# nevents=0
isData=True
# isData=False

PtBins={"Pt_170to300":117276.0,
        "Pt_300to470":7823.0,
        "Pt_470to600":648.2,
        "Pt_600to800":186.9,
        "Pt_800to1000":32.293,
        "Pt_1000to1400":9.4183,
        "Pt_1400to1800":0.842650,
        "Pt_1800to2400":0.114943,
        "Pt_2400to3200":0.006830,
        "Pt_3200":0.000165
}

if not isData:
    theBins=PtBins.keys()
    ## print len(theBins),theBins

    ## thePTBin="Pt_470to600"
    ## thePTBin="Pt_1800to2400"
    ## thePTBin="Pt_2400to3200"

    jobIndex=os.environ['JOBNUM']
    ## thePTBin=theBins[int(jobIndex)]
    ## thePTBin="Pt_170to300"
    ## thePTBin="Pt_300to470"
    thePTBin="Pt_470to600"

    print "Running ChiNtuple for ptbin: ",thePTBin

    if thePTBin in PtBins:
        XSECTION=PtBins[thePTBin]
    else:
        print "Error in specification of pt bins"

    ## doGaussian=True
    doGaussian=False
    SMRMAX=2.5

    ntuples="filelists/ntuples_" + thePTBin + ".list"
    if doGaussian:
        output="hsts/chiNtuple_"+ thePTBin + "_Gaussian.root"
    else:
        output="hsts/chiNtuple_"+ thePTBin + "_CB" + str(SMRMAX) +".root"

else:
    XSECTION=1.
    doGaussian=False
    SMRMAX=0    
    ntuples="filelists/ntuples_data.list"
    output="chiNtuple_data.root"
    
ntuples="filelists/ntuples_test.list"    
output="chiNtuple_test_data_v1.root"
## output = "root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/" + output ;

process = cms.PSet()
process.chiNtuples = cms.PSet(
    ## input specific for this analyzer
    Nevts = cms.int32(nevents), ## 0 or negative to process all events    
    CrossSection = cms.double(XSECTION),
    InputFiles = cms.string(ntuples),
    OutputFile = cms.string(output),
    IsData = cms.bool(isData),
    DoGaussian = cms.bool(doGaussian),
    SmearMax = cms.double(SMRMAX)
)
