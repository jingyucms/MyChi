#!/bin/tcsh

#foreach file (`eosls /store/user/zhangj/DijetAngularRunII/qcd2017/ | sed "s/MC_//g" | sed "s/_v2.root//g"`)
foreach  era (qcdUL16postVFPjan2023 qcdUL16preVFPjan2023 qcdUL17jan2023 qcdUL18jan2023)
    mkdir ./filelists/madgraphMLM_RunII_${era}
    foreach bin (HT100to200 HT200to300 HT300to500 HT500to700 HT700to1000 HT1000to1500 HT1500to2000 HT2000toInf)
	#ls -d /eos/uscms/store/user/zhangj/DijetAngularRunII/${era}/*${bin}* > ./filelists/madgraphMLM_RunII_${era}/ntuple_QCD_${bin}.list
	echo "srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/hinzmann/dijetangular/${era}/"
	which gfal-ls
	/usr/bin/gfal-ls srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/hinzmann/dijetangular/${era}/ | grep ${bin} > ./filelists/madgraphMLM_RunII_${era}/ntuple_QCD_${bin}.list
	#sed -i 's#/eos/uscms#root://cmseos.fnal.gov/#g' ./filelists/madgraphMLM_RunII_${era}/ntuple_QCD_${bin}.list
    end
end

#foreach bin (HT200to300 HT300to500 HT500to700 HT700to1000 HT1000to1500 HT1500to2000 HT2000toInf)
#    echo $bin
#    echo root://cmseos.fnal.gov//store/user/zhangj/DijetAngularRunII/qcd2017/dijetChiQCD_${bin}_RunII_94X_v2.root > filelists/madgraphMLM_RunII_2017/ntuple_QCD_${bin}_TuneCP5_13TeV-madgraph-pythia8.list
#end

#foreach bin (HT200to300 HT300to500 HT500to700 HT700to1000 HT1000to1500 HT1500to2000 HT2000toInf)
#    echo $bin
#    echo root://cmseos.fnal.gov//store/user/zhangj/DijetAngularRunII/qcd2018/dijetChiQCD_${bin}_RunII_102X_v1.root > filelists/madgraphMLM_RunII_2018/ntuple_QCD_${bin}_madgraph.list
#end
