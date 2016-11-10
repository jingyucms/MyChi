#!/bin/sh
#

EXEC=ChiNtuple

echo "Number of arguments: " $#
if [ $# -lt 1 ]
then
    echo "Usage: toBatchCHI.sh [cfgfile] "
    echo "" 
    exit
fi


cfgFile=$1
ptBin=$2
jobNum=$3
smrmax=$4
ak4sf=$5
datatomc=$6
syserr=$7
generator=$8

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

export PTBIN=$ptBin
export JOBNUM=$jobNum
export SMRMAX=$smrmax
export AK4SF=$ak4sf
export DATATOMC=$datatomc
export SYSERR=$syserr
export GENERATOR=$generator

echo "Current directory $PWD"
echo "Running job number $JOBNUM"

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


${EXEC} ${cfgFile}

## echo ""
## echo "Directory listing:"
## ls -xs 
## echo " "

echo
echo ">>> Ending cmsRun execution on `date`  <<<"
echo

exit
