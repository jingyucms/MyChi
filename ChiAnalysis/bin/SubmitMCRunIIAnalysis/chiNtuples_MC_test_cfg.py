import FWCore.ParameterSet.Config as cms
import os,sys

nevents=-1

PtBins = {"madgraphMLM_RunII_qcdUL16preVFPfeb2023_HT200to300":19.52/36.33*1710000./17969592, # 19.52 is lumi of preVFP, 36.33 is lumi of all madgraphMLM_RunII_qcdUL16
          "madgraphMLM_RunII_qcdUL16preVFPfeb2023_HT300to500":19.52/36.33*347500./13586390, 
          "madgraphMLM_RunII_qcdUL16preVFPfeb2023_HT500to700":19.52/36.33*30363.051/55497082, 
          "madgraphMLM_RunII_qcdUL16preVFPfeb2023_HT700to1000":19.52/36.33*6428.869/15242034, 
          "madgraphMLM_RunII_qcdUL16preVFPfeb2023_HT1000to1500":19.52/36.33*1122.659/13559959, 
          "madgraphMLM_RunII_qcdUL16preVFPfeb2023_HT1500to2000":19.52/36.33*108.163/9661950, 
          "madgraphMLM_RunII_qcdUL16preVFPfeb2023_HT2000toInf":19.52/36.33*22.008/4827641, 
          "madgraphMLM_RunII_qcdUL16postVFPfeb2023_HT200to300":16.81/36.33*1710000./42723038, # 16.81 is lumi of postVFP, 36.33 is lumi of all madgraphMLM_RunII_qcdUL16
          "madgraphMLM_RunII_qcdUL16postVFPfeb2023_HT300to500":16.81/36.33*347500./45502889, 
          "madgraphMLM_RunII_qcdUL16postVFPfeb2023_HT500to700":16.81/36.33*30363.051/15066884, 
          "madgraphMLM_RunII_qcdUL16postVFPfeb2023_HT700to1000":16.81/36.33*6428.869/13714842, 
          "madgraphMLM_RunII_qcdUL16postVFPfeb2023_HT1000to1500":16.81/36.33*1122.659/12416669, 
          "madgraphMLM_RunII_qcdUL16postVFPfeb2023_HT1500to2000":16.81/36.33*108.163/9244228, 
          "madgraphMLM_RunII_qcdUL16postVFPfeb2023_HT2000toInf":16.81/36.33*22.008/4843949, 
          "madgraphMLM_RunII_qcdUL17feb2023_HT200to300":1710000./42316128,
          "madgraphMLM_RunII_qcdUL17feb2023_HT300to500":347500./42914024, 
          "madgraphMLM_RunII_qcdUL17feb2023_HT500to700":30363.051/35745565, 
          "madgraphMLM_RunII_qcdUL17feb2023_HT700to1000":6428.869/33646855, 
          "madgraphMLM_RunII_qcdUL17feb2023_HT1000to1500":1122.659/10136610, 
          "madgraphMLM_RunII_qcdUL17feb2023_HT1500to2000":108.163/7528926, 
          "madgraphMLM_RunII_qcdUL17feb2023_HT2000toInf":22.008/4089387, 
          "madgraphMLM_RunII_qcdUL18feb2023_HT200to300":1710000./56298746,
          "madgraphMLM_RunII_qcdUL18feb2023_HT300to500":347500./60991701,
          "madgraphMLM_RunII_qcdUL18feb2023_HT500to700":30363.051/48640047,
          "madgraphMLM_RunII_qcdUL18feb2023_HT700to1000":6428.869/47925782,
          "madgraphMLM_RunII_qcdUL18feb2023_HT1000to1500":1122.659/14244456,
          "madgraphMLM_RunII_qcdUL18feb2023_HT1500to2000":108.163/10751607*9538041/2124697,
          "madgraphMLM_RunII_qcdUL18feb2023_HT2000toInf":22.008/5278880
}
theBins=PtBins.keys()

thePTBin = "madgraphMLM_RunII_qcdUL18feb2023_HT1500to2000"

if thePTBin in theBins:
    XSECTION=PtBins[thePTBin]
else:
    print "Error in specification of pt bins"
    XSECTION=-999.

#ntuples = "root://xrootd.unl.edu//store/user/zhangj/DijetAngularRunII/qcd2016/dijetChiQCD_HT2000toInf_RunII_2016v3.root"
ntuples = "filelists/madgraphMLM_RunII_qcdUL18feb2023/ntuple_QCD_HT1500to2000.list"

#output="root://eoscms.fnal.gov//store/user/zhangj/DijetAngularRunII/jetUnfold/MCNtuple/chiNtuple_madgraphMLM_QCD_HT2000toInf_RunII_2016v3_CB2_AK4SF.root"
output="chiNtuple_madgraphMLM_QCD_HT1500to2000_RunII_qcdUL18feb2023_CB2_AK4SF.root"
#print sys.argv

eraReco="qcdUL18feb2023"

#output = sys.argv[1]

print "Output written to: ",output

process = cms.PSet()
process.chiNtuples = cms.PSet(
    ## input specific for this analyzer
    Nevts = cms.int32(nevents), ## 0 or negative to process all events      
    CrossSection = cms.double(XSECTION),
    InputFiles = cms.string(ntuples),
    OutputFile = cms.string(output),
    IsData = cms.bool(False),
    DoGaussian = cms.bool(False),
    AK4_SF = cms.bool(True),
    DATAtoMC_SF = cms.bool(False),
    EraReco = cms.string(eraReco),
    SmearMax = cms.double(2),
    Trigger = cms.string("PFHT800"),    
    SysErr = cms.int32(0) ## +-1 to smear by additional +-10%,  anything else no addtional smearing    
)
