#!/bin/sh
#

export X509_USER_PROXY=/afs/cern.ch/user/z/zhangj/x509up_u69244

echo "Number of arguments: " $#
if [ $# -lt 1 ]
then
    echo "Usage: toBatchGEN.sh [cfgfile] "
    echo "" 
    exit
fi


cfgFile=$1
cmsswDir=$LS_SUBCWD

echo
echo ">>> Beginning cmsRun execution on `date`  <<<"
echo

cd $cmsswDir

echo "Current directory: $cmsswDir"
echo ""

#echo "CPUINFO:"
#cat /proc/cpuinfo
#echo ""
#echo "MEMINFO:"
#cat /proc/meminfo
#echo ""



echo "Current directory $PWD"

#eval `scramv1 runtime -sh`
if [ -n "${CMS_PATH:-}" ]; then
  echo "CMSSW computing environment already setup"
else
  export SCRAM_ARCH=`scramv1 arch`
fi
eval `scramv1 runtime -sh`

echo $cfgFile
echo "------------------------------------"
cat $cfgFile
echo "------------------------------------"


GenChiAnalysis ${cfgFile}

## echo ""
## echo "Directory listing:"
## ls -xs 
## echo " "

echo
echo ">>> Ending cmsRun execution on `date`  <<<"
echo

exit
