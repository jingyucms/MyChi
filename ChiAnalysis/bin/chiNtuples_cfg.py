import FWCore.ParameterSet.Config as cms
import os


PtBins={"Pt_170to300":9999.,
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


thePTBin="Pt_470to600"
if thePTBin in PtBins:
    XSECTION=PtBins[thePTBin]
else:
    print "Error in specification of pt bins"
    XSECTION=-999.
    

ntuples="ntuples_" + thePTBin + ".list"
output="chiNtuple_"+ thePTBin + ".root"

process = cms.PSet()
process.chiNtuples = cms.PSet(
    ## input specific for this analyzer
    CrossSection = cms.double(XSECTION),
    InputFiles = cms.string(ntuples),
    OutputFile = cms.string(output)
)
