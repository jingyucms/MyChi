#!/bin/bash

for era in qcdUL16postVFPfeb2023 qcdUL16preVFPfeb2023 qcdUL17feb2023 qcdUL18feb2023
do
    mkdir ./filelists/madgraphMLM_RunII_${era}
    for bin in HT100to200 HT200to300 HT300to500 HT500to700 HT700to1000 HT1000to1500 HT1500to2000 HT2000toInf
    do
	echo "srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/hinzmann/dijetangular/${era}/"
	gfal-ls srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/hinzmann/dijetangular/${era}/ | grep ${bin} > ./filelists/madgraphMLM_RunII_${era}/ntuple_QCD_${bin}.list
	sed -i "s#dijetChi#xroot://dcache-cms-xrootd.desy.de//pnfs/desy.de/cms/tier2/store/user/hinzmann/dijetangular/${era}/dijetChi#g" ./filelists/madgraphMLM_RunII_${era}/ntuple_QCD_${bin}.list
    done
done

#foreach bin (HT200to300 HT300to500 HT500to700 HT700to1000 HT1000to1500 HT1500to2000 HT2000toInf)
#    echo $bin
#    echo root://cmseos.fnal.gov//store/user/zhangj/DijetAngularRunII/qcd2017/dijetChiQCD_${bin}_RunII_94X_v2.root > filelists/madgraphMLM_RunII_2017/ntuple_QCD_${bin}_TuneCP5_13TeV-madgraph-pythia8.list
#end

#foreach bin (HT200to300 HT300to500 HT500to700 HT700to1000 HT1000to1500 HT1500to2000 HT2000toInf)
#    echo $bin
#    echo root://cmseos.fnal.gov//store/user/zhangj/DijetAngularRunII/qcd2018/dijetChiQCD_${bin}_RunII_102X_v1.root > filelists/madgraphMLM_RunII_2018/ntuple_QCD_${bin}_madgraph.list
#end
