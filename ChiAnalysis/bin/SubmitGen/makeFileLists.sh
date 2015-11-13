#!/bin/bash

FilesPerCfg="10" ## 0= all files

INDIR=/eos/cms/store/cmst3/user/hinzmann/dijet_angular
# for mass in 1000_1500 1500_1900 1900_2400 2400_2800 2800_3300 3300_3800 3800_4300 4300_13000
for mass in 1000_1500
do
    outname=filelists/pythia8_ci_50000__Oct1/m${mass}/fileList.txt
    searchstring=jobtmp_pythia8_ci_m${mass}_50000
    python makeEOSfilelist.py $INDIR $outname $searchstring ${FilesPerCfg} # to make original list

    #inList=${outname}
    #outDir=filelists/pythia8_ci_m${mass}_50000__Oct1
    ## python SplitFileList.py $inList $outDir  # make split lists
done
