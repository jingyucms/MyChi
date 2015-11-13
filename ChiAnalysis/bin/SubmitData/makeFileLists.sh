#!/bin/bash

FilesPerCfg="45" ## 0= all files

INDIR=/eos/cms/store/cmst3/user/hinzmann/dijet_angular/25ns12
outname=filelists/1pt3invfb/fileList.txt
searchstring=EXOVVTree

python makeEOSfilelist.py $INDIR $outname $searchstring ${FilesPerCfg} # to make original list
