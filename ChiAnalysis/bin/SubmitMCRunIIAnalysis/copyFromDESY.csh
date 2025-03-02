#!/bin/bash

for file in $(/usr/bin/gfal-ls srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/hinzmann/dijetangular/qcdUL16postVFPoct/); do
    echo $file
    echo gfal-copy srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/hinzmann/dijetangular/qcdUL16postVFPoct/$file root://cmseos.fnal.gov//eos/uscms/store/user/zhangj/DijetAngularRunII/qcdUL16postVFPoct/$file
done
