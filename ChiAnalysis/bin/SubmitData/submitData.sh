#!/bin/sh

QUEUE=1nd
SUB_SCRIPT=toBatchCHI.sh

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
jobnum=$3

echo
echo "************************************************"
echo "Submitting job to the CERN $QUEUE batch queue"
echo "************************************************"
echo 
echo "CFG: " $cfgfile
echo "LOG: " $logfile
echo


echo bsub -q ${QUEUE} -oo ${logfile} ${SUB_SCRIPT} ${cfgfile} ${jobnum}
bsub -q ${QUEUE} -oo ${logfile} ${SUB_SCRIPT} ${cfgfile} ${jobnum}

}
######################################################################################

theDate=`date '+%Y%m%d'`
logDir=logs_${theDate}
if [[ ! -e $logDir ]]; then
   mkdir $logDir
fi

cp ../ChiNtuple.cc ../ChiNtuple.h $logDir

for a in {0..116}
## for a in 0
do
    config=chiNtuple_cfg.py
    logfile=$logDir/chiCFG_data_${a}.log
    
    echo $config $logfile $a
    Submit $config $logfile ${a}
    let COUNTER=COUNTER+1
done

echo
echo "==> Submitted ${COUNTER} jobs <=="
echo
