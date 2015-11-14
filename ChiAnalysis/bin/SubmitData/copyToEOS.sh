#!/bin/bash

EOS=/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select

EOSDIR=/eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/Data

for srcfile in chiNtuple_data_25nsData5.root
do
    $EOS cp $srcfile $EOSDIR/$srcfile
done

