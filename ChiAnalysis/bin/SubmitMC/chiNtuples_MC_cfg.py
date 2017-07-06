import FWCore.ParameterSet.Config as cms
import os,sys

nevents=0
## nevents=1000
## nevents=40000

PtBins={"Pt_170to300":117276.0,
        "Pt_300to470":7823.0,
        "Pt_470to600":648.2,
        "Pt_600to800":186.9,
        "Pt_800to1000":32.293,
        "Pt_1000to1400":9.4183,
        "Pt_1400to1800":0.842650,
        "Pt_1800to2400":0.114943,
        "Pt_2400to3200":0.006830,
        "Pt_3200toInf":0.000165,
        #"HT300to500":347700.0,
        #"HT500to700":32100.0,
        #"HT700to1000":6831.0,
        #"HT1000to1500":1207.0,
        #"HT1500to2000":119.9,
        #"HT2000toInf":25.24,
        "HT300to500":0.006467159312146088,
        "HT500to700":0.0005102028471673902,
        "HT700to1000":0.00015479235727186593,
        "HT1000to1500":7.981053006633407e-05,
        "HT1500to2000":1.0345466400090463e-05,
        "HT2000toInf":4.27956236940979e-06,
        "flatPythia8":-1.0,
        "flatHerwigpp":-1.0
}
theBins=PtBins.keys()
## print len(theBins),theBins


jobNum=os.environ['JOBNUM']
thePTBin=os.environ['PTBIN']
SMRMAX=os.environ['SMRMAX']
AK4SF=os.environ['AK4SF']
DATATOMC=os.environ['DATATOMC']
SYSERR=os.environ['SYSERR']
GENERATOR=os.environ['GENERATOR']

## jobNum="8"
## SMRMAX=2     ## only used for CB smearing
## thePTBin="flatPythia8"
## AK4SF="1"
## DATATOMC="0"
## SYSERR="0"
## GENERATOR="flatPythia8"

## thePTBin="Pt_300to470"
## thePTBin="Pt_470to600"
## thePTBin="Pt_600to800"
## thePTBin="Pt_800to1000"
## thePTBin="Pt_1800to2400"
## thePTBin="Pt_2400to3200"
## thePTBin="Pt_1400to1800"

doAK4_sf=False
if AK4SF=="1" : doAK4_sf=True

doDataToMC_sf=False
if DATATOMC=="1" : doDataToMC_sf=True

doGaussian=False
if SMRMAX=="0" : doGaussian=True

print "Running ChiNtuple for ptbin: ",thePTBin
print "doGaussian: ",doGaussian
print "SmearMax = ",SMRMAX
print "AK4 SF = ",doAK4_sf
print "DataToMC SF = ",doDataToMC_sf
print "SysErr = ",SYSERR


if thePTBin in PtBins:
    XSECTION=PtBins[thePTBin]
else:
    print "Error in specification of pt bins"
    XSECTION=-999.

if GENERATOR=="pythia8":
    ntuples="filelists/pythia8_newJES/ntuples_"+ thePTBin +"_"+jobNum+".list"
elif GENERATOR=="25nsMC10":
    ntuples="filelists/25nsMC10/ntuples_"+jobNum+".list"
elif GENERATOR=="flatPythia8":
    ntuples="filelists/flatPythia8/ntuples_"+jobNum+".list"
elif GENERATOR=="flatHerwigpp":
    ntuples="filelists/flatHerwigpp/ntuples_"+jobNum+".list"
else:
    ntuples="filelists/madgraphMLM/ntuples_"+ thePTBin +"_"+jobNum+".list"

if doGaussian:
    #output="root://eoscms//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/Jingyu/samples/DiJet/SMEAR/MCOutput/hstsMCmadgraphMLM_v5/chiNtuple_" + GENERATOR + "_" + thePTBin + "_GS"
    #output="/afs/cern.ch/work/z/zhangj/private/jetUnfold/data/hstsMCPythia8/chiNtuple_" + GENERATOR + "_" + thePTBin + "_GS"
    output="/afs/cern.ch/work/z/zhangj/private/jetUnfold/data/hstsMCHerwigpp/chiNtuple_" + GENERATOR + "_" + thePTBin + "_GS"
else:
    #output="root://eoscms//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/Jingyu/samples/DiJet/SMEAR/MCOutput/hstsMCmadgraphMLM_v5/chiNtuple_" + GENERATOR + "_" + thePTBin + "_CB" + str(SMRMAX)
    #output="/afs/cern.ch/work/z/zhangj/private/jetUnfold/data/hstsMCPythia8/chiNtuple_" + GENERATOR + "_" + thePTBin + "_CB" + str(SMRMAX)
    output="/afs/cern.ch/work/z/zhangj/private/jetUnfold/data/hstsMCHerwigpp/chiNtuple_" + GENERATOR + "_" + thePTBin + "_CB" + str(SMRMAX)

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
    
output=output + "_" + jobNum + ".root"

## output="tsthsts/chiNtuple_"+ thePTBin + "_GS_" + "test_func.root"
## output="chiNtuple_test.root"

## ntuples="filelists/ntuples_test.list"    
## output="chiNtuple_test"+ "_smr" + str(SMRMAX) +".root"

## output = os.path.join("root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC",output)
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
    SmearMax = cms.double(SMRMAX),
    Trigger = cms.string("PFHT800"),    
    SysErr = cms.int32(syserr) ## +-1 to smear by additional +-10%,  anything else no addtional smearing    
)
