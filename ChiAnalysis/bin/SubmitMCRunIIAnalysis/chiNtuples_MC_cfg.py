import FWCore.ParameterSet.Config as cms
import os,sys

nevents=0

## PtBins={"MC_QCD_HT200to300":1712000./56709875,
##         "MC_QCD_HT300to500":347700./53096517,
##         "MC_QCD_HT500to700":32100./52906552,
##         "MC_QCD_HT700to1000":6831./36741540,
##         "MC_QCD_HT1000to1500":1207./15210939,
##         "MC_QCD_HT1500to2000":119.9/11839357,
##         "MC_QCD_HT2000toInf":25.24/5947849,
##         "MC_QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8":1545000./58990434,
##         "MC_QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8":323300./58748739,
##         "MC_QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8":30000./54366431,
##         "MC_QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8":6324./46924322,
##         "MC_QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8":1090./16495598,
##         "MC_QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8":101./11196479,
##         "MC_QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8":20.43/5362513,
##         "QCD_HT200to300_madgraph":1461000./54289442,
##         "QCD_HT300to500_madgraph":311900./54512704,
##         "QCD_HT500to700_madgraph":29070./53919811,
##         "QCD_HT700to1000_madgraph":5962./48158738,
##         "QCD_HT1000to1500_madgraph":1005./14945819,
##         "QCD_HT1500to2000_madgraph":101.8/10707847,
##         "QCD_HT2000toInf_madgraph":20.54/5329144
## }
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


#jobNum=os.environ['JOBNUM']
thePTBin=os.environ['PTBIN']
SMRMAX=os.environ['SMRMAX']
AK4SF=os.environ['AK4SF']
DATATOMC=os.environ['DATATOMC']
SYSERR=os.environ['SYSERR']
GENERATOR=os.environ['GENERATOR']

iPTBin = GENERATOR+'_'+thePTBin

doAK4_sf=False
if AK4SF=="1" : doAK4_sf=True

doDataToMC_sf=False
if DATATOMC=="1" : doDataToMC_sf=True

doGaussian=False
if SMRMAX=="0" : doGaussian=True

eraReco = ""

print "Running ChiNtuple for ptbin: ",thePTBin
print "doGaussian: ",doGaussian
print "SmearMax = ",SMRMAX
print "AK4 SF = ",doAK4_sf
print "DataToMC SF = ",doDataToMC_sf
print "SysErr = ",SYSERR


if iPTBin in theBins:
    XSECTION=PtBins[iPTBin]
else:
    print "Error in specification of pt bins"
    XSECTION=-999.

if GENERATOR == "pythia8":
    ntuples="filelists/pythia8_newJES/ntuples_"+ thePTBin +"_"+jobNum+".list"
elif GENERATOR == "25nsMC10":
    ntuples="filelists/25nsMC10/ntuples_"+jobNum+".list"
elif GENERATOR == "flatPythia8":
    ntuples="filelists/flatPythia8/ntuples_"+jobNum+".list"
elif GENERATOR == "madgraphMLM_RunII_2016v3" or GENERATOR == "madgraphMLM_RunII_2017" or GENERATOR == "madgraphMLM_RunII_2018":
    ntuples = "filelists/"+GENERATOR+"/ntuple_"+thePTBin.replace("MC_", "")+".list"
    #eraReco = GENERATOR.split("_")[-1]
    eraReco = "2016v3"
else:
    ntuples="filelists/"+GENERATOR+"/ntuple_QCD_"+ thePTBin +".list"

if doGaussian:
    output="chiNtuple_" + GENERATOR + "_" + thePTBin + "_GS"
else:
    output="chiNtuple_" + GENERATOR + "_" + thePTBin + "_CB" + str(SMRMAX)

if doAK4_sf:
    output=output + "_AK4SF"

if doDataToMC_sf:
    output=output + "_DataToMCSF"
    
if SYSERR=="1":
    syserr=1
    output=output + "_SysPlus"
elif SYSERR=="-1":
    syserr=-1
    output=output + "_SysMinus"
else:
    syserr=0
    
#output=output + "_" + jobNum + ".root"
output=output + ".root"

## output="tsthsts/chiNtuple_"+ thePTBin + "_GS_" + "test_func.root"
## output="chiNtuple_test.root"

## ntuples="filelists/ntuples_test.list"    
## output="chiNtuple_test"+ "_smr" + str(SMRMAX) +".root"

## output = os.path.join("root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC",output)
print "Era reco:", eraReco
print "Output written to: ",output

process = cms.PSet()
process.chiNtuples = cms.PSet(
    ## input specific for this analyzer
    Nevts = cms.int32(nevents), ## 0 or negative to process all events        
    CrossSection = cms.double(XSECTION),
    InputFiles = cms.string(ntuples),
    OutputFile = cms.string(output),
    IsData = cms.bool(False),
    DoGaussian = cms.bool(doGaussian),
    AK4_SF = cms.bool(doAK4_sf),
    DATAtoMC_SF = cms.bool(doDataToMC_sf),
    EraReco = cms.string(eraReco),
    SmearMax = cms.double(SMRMAX),
    Trigger = cms.string("PFHT800"),    
    SysErr = cms.int32(syserr) ## +-1 to smear by additional +-10%,  anything else no addtional smearing    
)
