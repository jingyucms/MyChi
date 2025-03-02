#!/bin/tcsh

setenv BASE /uscms/home/jingyu/nobackup/ChiAnalysis/jetUnfold/CMSSW_8_0_23

cd $BASE/src

tar -zcvf ../../CMSSW8023.tgz ../../CMSSW_8_0_23/ --exclude="*.root" --exclude="*.pdf" --exclude="*.gif" --exclude=.git --exclude="*.stdout" --exclude="*.stderr" --exclude="*.log"

eosrm /store/user/zhangj/CMSSW8023.tgz

xrdcp ../../CMSSW8023.tgz root://cmseos.fnal.gov//store/user/zhangj/CMSSW8023.tgz

cd $BASE/src/MyChi/ChiAnalysis/bin/SubmitMCRunIIAnalysis


setenv SMRMAX 2
setenv AK4SF 1
setenv DATATOMC 1
setenv SYSERR 0
#setenv GENERATOR madgraphMLM_RunII_2016v3
#setenv GENERATOR madgraphMLM_RunII_2017
#setenv GENERATOR madgraphMLM_RunII_2018

#setenv GENERATOR madgraphMLM_RunII_qcdUL18feb2023
setenv GENERATOR madgraphMLM_RunII_qcdUL17feb2023
#setenv GENERATOR madgraphMLM_RunII_qcdUL16postVFPfeb2023
#setenv GENERATOR madgraphMLM_RunII_qcdUL16preVFPfeb2023

#foreach bin (HT200to300 HT300to500 HT500to700 HT700to1000 HT1000to1500 HT1500to2000 HT2000toInf)
foreach bin (HT1000to1500)
    setenv PTBIN $bin
    condor_submit condor.jdl
end


## if (${GENERATOR}:q =~ *'madgraphMLM_RunII_2016v3'*) then
##     foreach bin (MC_QCD_HT200to300 MC_QCD_HT300to500 MC_QCD_HT500to700 MC_QCD_HT700to1000 MC_QCD_HT1000to1500 MC_QCD_HT1500to2000 MC_QCD_HT2000toInf)
## 	setenv PTBIN $bin
## 	condor_submit condor.jdl 
##     end
## else if (${GENERATOR}:q =~ *'madgraphMLM_RunII_2017'*) then
##     foreach bin (MC_QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8 MC_QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8 MC_QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8 MC_QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8 MC_QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8 MC_QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8 MC_QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8)
## 	setenv PTBIN $bin
## 	condor_submit condor.jdl 
##     end
## else
##     #foreach bin (QCD_HT200to300_madgraph QCD_HT300to500_madgraph QCD_HT500to700_madgraph QCD_HT700to1000_madgraph QCD_HT1000to1500_madgraph QCD_HT1500to2000_madgraph QCD_HT2000toInf_madgraph)
##     foreach bin (QCD_HT1500to2000_madgraph)
## 	setenv PTBIN $bin
## 	condor_submit condor.jdl 
##     end
## endif
