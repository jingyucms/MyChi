#!/bin/tcsh

setenv SAMPLE DMAxial

cd $CMSSW_BASE/src

tar -zcvf ../../CMSSW8023.tgz ../../CMSSW_8_0_23/ --exclude="*.root" --exclude="*.pdf" --exclude="*.gif" --exclude=.git

eosrm /store/user/jingyu/CMSSW8023.tgz

xrdcp ../../CMSSW8023.tgz root://cmseos.fnal.gov//store/user/jingyu/CMSSW8023.tgz

cd $CMSSW_BASE/src/MyChi/ChiAnalysis/bin/SubmitNP

#foreach n (2250 2500 3000 3500 4000 4500 5000 6000)
foreach n (6000)
    setenv MBIN $n
    #echo $MBIN
    condor_submit condor.jdl
end
