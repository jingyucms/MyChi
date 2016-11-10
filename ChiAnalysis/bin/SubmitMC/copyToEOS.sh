#!/bin/bash

EOSDIR=/eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC/76x/hsts

EOS=/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select

nfiles=0
cd hsts
## for rootfile in `ls chiNtuple_madgraphMLM_HT*GS*root`
## for rootfile in `ls chiNtuple_madgraphMLM_HT*CB*root`
## for rootfile in `ls chiNtuple_pythia8_*GS*root`
for rootfile in `ls chiNtuple_pythia8_*CB2*root`
do
    let "nfiles++"
    target="root://eoscms/$EOSDIR/"${rootfile}
    echo ${nfiles} ${rootfile} ${target}
    $EOS cp $rootfile $target
done
cd -
## pwd

