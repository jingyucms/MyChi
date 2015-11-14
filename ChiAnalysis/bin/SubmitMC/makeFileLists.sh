#!/bin/bash

FilesPerCfg="0" ## 0= all files

INDIR=/eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDnew
for pt in Pt_170to300 Pt_300to470 Pt_470to600 Pt_600to800 Pt_800to1000 Pt_1000to1400 Pt_1400to1800 Pt_1800to2400 Pt_2400to3200 Pt_3200
do
    outname=filelists/pythia8_newJES/ntuples_${pt}.list
    searchstring=EXOVVTree_QCD_${pt}
    python makeEOSfilelist.py $INDIR $outname $searchstring $FilesPerCfg # to make original list

done
