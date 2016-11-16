#!/bin/bash


EXEC=xrdcp

inPREFIX=root://eoscms.cern.ch/
inDir=/eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC/80x/

## FNAL
outPREFIX=root://cmseos.fnal.gov/
outDIR=/eos/uscms/store/user/apana/Chi_13TeV/ChiNtuples/MC/80x/

for FILENAME in chiNtuple_25nsMC10_flatQCD_CB2_AK4SF.root
do
    inFILE=$inPREFIX/$inDir/$FILENAME    
    outFILE=$outPREFIX/$outDIR/$FILENAME
    echo -e "\t" $inFILE $outFILE
    xrdcp $inFILE $outFILE
done
