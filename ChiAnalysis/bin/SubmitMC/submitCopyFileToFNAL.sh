#!/bin/sh


export X509_USER_PROXY=/afs/cern.ch/user/z/zhangj/x509up_u69244

cd /afs/cern.ch/user/z/zhangj/private/chi_analysis_2016/jetUnfold/CMSSW_8_0_23/src/MyChi/ChiAnalysis/bin/SubmitMC

python copyFileToFNAL.py
