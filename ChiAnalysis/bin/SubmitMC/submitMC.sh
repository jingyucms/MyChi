#!/bin/sh

#QUEUE=1nd
QUEUE=8nh
SUB_SCRIPT=toBatchCHI.sh

ulimit -a
ulimit -S -c 0
ulimit -a

#####################################################################################
function Submit()
{

ARGS=2
if [ $# -lt "$ARGS" ]
# Test number of arguments to script (always a good idea).
then
  echo "Usage: `basename $0` <cfgfile>  <logfile> "
  exit $E_BADARGS
fi
cfgfile=$1
logfile=$2
ptBin=$3
jobnum=$4
smrmax=$5
ak4sf=$6
datatomc=$7
syserr=$8
GENERATOR=$9

echo
echo "************************************************"
echo "Submitting job to the CERN $QUEUE batch queue"
echo "************************************************"
echo 
echo "CFG: " $cfgfile
echo "LOG: " $logfile
echo


echo bsub -q ${QUEUE} -oo ${logfile} ${SUB_SCRIPT} ${cfgfile} ${ptBin} ${jobnum} ${smrmax} ${ak4sf} ${datatomc} ${syserr} ${GENERATOR}
bsub -q ${QUEUE} -oo ${logfile} ${SUB_SCRIPT} ${cfgfile} ${ptBin} ${jobnum} ${smrmax} ${ak4sf} ${datatomc}  ${syserr} ${GENERATOR}

}
######################################################################################

theDate=`date '+%Y%m%d'`
COUNTER=0

config=chiNtuples_MC_cfg.py

smrMAX=2    # set to 0 (2) for Gaussian (Crystal Ball) smearing
AK4sf=1      # set to 1 to turn on AK4 scale factor, 0=off
DataToMCsf=0  # set to 1 to turn on DataToMC scale factor, 0=off
SysErr=0      # +-1 to smear by additional +-10%,  anything else no addtional smearing    

#GENERATOR=madgraphMLM
## GENERATOR=pythia8
#GENERATOR=flatPythia8
GENERATOR=flatHerwigpp

if [ $smrMAX == 0 ]; then
    logDir=logs_${GENERATOR}_GS
else
    logDir=logs_${GENERATOR}_CB${smrMAX}
fi

if [ $SysErr == 1 ]; then
    logDir=${logDir}_sysplus
elif [ $SysErr == -1 ]; then
    logDir=${logDir}_sysminus
fi

logDir=${logDir}_${theDate}
echo $logDir


if [[ ! -e $logDir ]]; then
   mkdir $logDir
fi
cp ../ChiNtuple.cc ../ChiNtuple.h $logDir

if [[ "$GENERATOR" == "pythia8" ]]
then
    ptBins="Pt_1000to1400 Pt_1400to1800 Pt_170to300 Pt_1800to2400 Pt_2400to3200 Pt_300to470 Pt_3200toInf Pt_470to600 Pt_600to800 Pt_800to1000"
    ## ptBins="Pt_3200toInf"
elif [[ "$GENERATOR" == "flatPythia8" ]]
then
    ptBins="flatPythia8"
elif [[ "$GENERATOR" == "flatHerwigpp" ]]
then
    ptBins="flatHerwigpp" 
else
    ptBins="HT300to500 HT500to700 HT700to1000 HT1000to1500 HT1500to2000 HT2000toInf"
fi

for ptBin in `echo $ptBins`
## for ptBin in HT2000toInf
## for ptBin in Pt_3200toInf
do
    if [[ "$ptBin" == "flatPythia8" ]]
    then
	nfiles=`ls -1 filelists/${GENERATOR}/ntuples_*list | wc -l`
    elif [[ "$ptBin" == "flatHerwigpp" ]]
    then
	nfiles=`ls -1 filelists/${GENERATOR}/ntuples_*list | wc -l`
    else
	nfiles=`ls -1 filelists/madgraphMLM/ntuples_${ptBin}*list | wc -l`
	## nfiles=`ls -1 filelists/${GENERATOR}_newJES/ntuples_${ptBin}*list | wc -l`
    fi
    nfiles=$(($nfiles - 1))
    # nfiles=0
    # echo "Number of files: " $nfiles
    for i in $(seq 0 $nfiles);
    # for i in 2;
    do
	logfile=${logDir}/chiNtuples_${ptBin}_AK4sf_${AK4sf}_DataToMC_${DataToMCsf}_Job${i}.log    
    
	## echo $config $logfile ${ptBin} ${i}  ${smrMAX} ${AK4sf} ${DataToMCsf} ${SysErr} ${GENERATOR}
	Submit $config $logfile ${ptBin} ${i} ${smrMAX}  ${AK4sf} ${DataToMCsf} ${SysErr} ${GENERATOR}
	let COUNTER=COUNTER+1
    done
done
echo
echo "==> Submitted ${COUNTER} jobs <=="
echo
