#!/bin/bash

FilesPerCfg="5" ## 0= all files


INDIR=/eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7
for pt in Pt_170to300 Pt_300to470 Pt_470to600 Pt_600to800 Pt_800to1000 Pt_1000to1400 Pt_1400to1800 Pt_1800to2400 Pt_2400to3200 Pt_3200toInf
## for pt in Pt_3200toInf
do
    INPUTDIR=$INDIR/QCD_${pt}_TuneCUETP8M1_13TeV_pythia8_RunIIFall15MiniAODv2_PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1
    
    outname=filelists/pythia8_newJES/ntuples_${pt}.list
    searchstring=EXOVVTree_QCD_${pt}
    python makeEOSfilelist.py $INPUTDIR $outname $searchstring $FilesPerCfg # to make original list
 
done


## INDIR=/eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7
## 
## for ht in HT300to500 HT500to700 HT700to1000 HT1000to1500 HT1500to2000 HT2000toInf
## do
##     INPUTDIR=$INDIR
##     
##     outname=filelists/madgraphMLM_newJES/ntuples_${ht}.list
##     searchstring=EXOVVTree_QCD_${ht}
##     python makeEOSfilelist.py $INPUTDIR $outname $searchstring $FilesPerCfg # to make original list
##  
## done


