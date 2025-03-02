#!/bin/bash


EXEC=xrdcp

#inPREFIX=root://eoscms.cern.ch/
inPREFIX=""
inDir=/afs/cern.ch/work/z/zhangj/private/jetUnfold/data/hstsMCmadgraphMLM/

## FNAL
outPREFIX=root://cmseos.fnal.gov/
outDIR=/eos/uscms/store/user/jingyu/jetUnfold/MCNtuple/madgraphMLM_Moriond_v4/

for FILENAME in chiNtuple_25nsMC10_flatQCD_CB2_AK4SF.root
do
    inFILE=$inPREFIX/$inDir/$FILENAME    
    outFILE=$outPREFIX/$outDIR/$FILENAME
    echo -e "\t" $inFILE $outFILE
    xrdcp $inFILE $outFILE
done
