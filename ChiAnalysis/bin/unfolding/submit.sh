#!/bin/bash

# QUEUE=2nd
# QUEUE=8nh
QUEUE=1nw
# QUEUE=1nh

theDate=`date '+%Y%m%d'`
# echo $theDate

## MC=Herwig; Binning=M_1000toInf
## MC=Pythia; Binning=M_1000toInf

MC=pythia8; Binning=Pt_170toInf
# MC=madgraphMLM; Binning=HT_300toInf

Split=0 #  0=no split,1=train,2=test

## for smearing in CB_AK4SF_DataToMCSF
## for smearing in GS_AK4SF_DataToMCSF
for smearing in GS_AK4SF CB_AK4SF
## for smearing in GS_AK4SF_DataToMCSF_SysMinus GS_AK4SF_DataToMCSF_SysPlus GS_AK4SF_DataToMCSF
## for smearing in GS_AK4SF_DataToMCSF GS_AK4SF_DataToMCSF_SysMinus GS_AK4SF_DataToMCSF_SysPlus
do
    ##rootfile=chiNtuple_${Binning}_${smearing}.root
    ##rootfile=root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC/${rootfile}
    

    rootfile=filelists/chiNtuple_${MC}_${Binning}_${smearing}.list
    outfile=ResponseMatrices/Response_${MC}_${Binning}_${smearing}_${theDate}.root
    
    if [ $Split == 1 ]; then
	logfile=runResponse_${MC}_${Binning}_${smearing}_Train_${theDate}.log
    elif [ $Split == 2 ]; then
	logfile=runResponse_${MC}_${Binning}_${smearing}_Test_${theDate}.log
    else
	logfile=runResponse_${MC}_${Binning}_${smearing}_${theDate}.log
    fi
    
    echo $logfile
    bsub -q ${QUEUE} -oo logs/$logfile toBatch.sh ${outfile} ${rootfile} ${Split}
done
