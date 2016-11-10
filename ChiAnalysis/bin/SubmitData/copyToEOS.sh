#!/bin/bash

EOS=/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select

EOSDIR=/eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/Data/76x

for srcfile in chiNtuple_PFHT650_20160530.root
do
    $EOS cp $srcfile $EOSDIR/$srcfile
done



## EOSSRC=/eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/Data
## EOSTGT=$EOSSRC/74x
## 
## for srcfile in chiNtuple_data_25nsData5.root chiNtuple_data_25nsData5_teff.root chiNtuple_data_2pt4invfb_ht650.root chiNtuple_data_2pt4invfb_newteff.root chiNtuple_data_2pt4invfb_noteff.root chiNtuple_data_2pt4invfb_teff.root
## do
##     echo $EOSSRC/$srcfile $EOSTGT/$srcfile
##     ## $EOS cp $EOSSRC/$srcfile $EOSTGT/$srcfile
##     ## $EOS rm $EOSSRC/$srcfile
## done

