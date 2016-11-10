#!/bin/bash


EXEC=xrdcp

inPREFIX=root://eoscms.cern.ch/
inDir=/eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC/76x/

## FNAL
outPREFIX=root://cmseos.fnal.gov/
outDIR=/eos/uscms/store/user/apana/Chi_13TeV/ChiNtuples/MC/76x/

## for FILENAME in chiNtuple_Pythia8_Pt_170toInf_CB2_AK4SF_noTrees.root chiNtuple_Pythia8_Pt_170toInf_GS_AK4SF_noTrees.root
## for FILENAME in chiNtuple_Pythia8_Pt_170toInf_CB2_noTrees.root chiNtuple_Pythia8_Pt_170toInf_GS_noTrees.root
## for FILENAME in chiNtuple_Madgraph_Ht_300toInf_CB2_AK4SF_noTrees.root chiNtuple_Madgraph_Ht_300toInf_GS_AK4SF_noTrees.root
for FILENAME in chiNtuple_Madgraph_Ht_300toInf_CB2_AK4SF_noTrees.root chiNtuple_Madgraph_Ht_300toInf_GS_AK4SF_noTrees.root chiNtuple_Madgraph_Ht_300toInf_GS_noTrees.root chiNtuple_Madgraph_Ht_300toInf_CB2_noTrees.root
do
    inFILE=$inPREFIX/$inDir/$FILENAME    
    outFILE=$outPREFIX/$outDIR/$FILENAME
    echo -e "\t" $inFILE $outFILE
    xrdcp $inFILE $outFILE
done
