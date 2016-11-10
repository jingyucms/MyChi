#!/bin/bash

EOS=/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select

## EOSDIR=/eos/cms/store/caf/user/apana/Chi/GenOutput_13TeV
EOSDIR=/eos/cms/store/caf/user/apana/Chi_13TeV/GenOutput
## EOSDIR=/eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples

## EOSDIR=/eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC

## for eosDir in pythia8_ci_CrystalBall_Trunc2 pythia8_ci_CrystalBall_Trunc2.5 pythia8_ci_CrystalBall_Trunc3 pythia8_ci_Gaussian
## for eosDir in pythia8_ci_CrystalBall_Trunc2
## for eosDir in pythia8_ci_Gaussian
for eosDir in herwigpp_CrystalBall_Trunc2
## for eosDir in hsts
do
    echo $EOSDIR/$eosDir
    # for infile in `$EOS ls $EOSDIR/$eosDir | grep CB1`
    for infile in `$EOS ls $EOSDIR/$eosDir`
    do
	fullname=$EOSDIR/$eosDir/$infile
	echo Removing ${fullname} && $EOS rm ${fullname}
	## $EOS ls ${fullname}
    done
done

