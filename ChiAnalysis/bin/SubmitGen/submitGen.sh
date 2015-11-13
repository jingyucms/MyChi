#!/bin/sh

QUEUE=2nd
SUB_SCRIPT=toBatchGEN.sh

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


echo
echo "************************************************"
echo "Submitting job to the CERN $QUEUE batch queue"
echo "************************************************"
echo 
echo "CFG: " $cfgfile
echo "LOG: " $logfile
echo


echo bsub -q ${QUEUE} -oo ${logfile} ${SUB_SCRIPT} ${cfgfile}
# bsub -q ${QUEUE} -oo ${logfile} ${SUB_SCRIPT} ${cfgfile}

}

#################################################################################


COUNTER=0
# for GENR in Pythia8 Herwig
# for GENR in Herwig
for GENR in Pythia8
do
    # for TRUNC in 2 2.5 3
    for TRUNC in 0
    # for TRUNC in 2.5 3
    # for TRUNC in 4 5
    # for TRUNC in 3.5
    do 
	## CFGDIR=genCFGS/${GENR}CrystalBallT${TRUNC}
	CFGDIR=genCFGS/${GENR}Gaussian
	## CFGDIR=genCFGS_new/${GENR}GaussianSysMinus
	## CFGDIR=genCFGS_BigStat/${GENR}Gaussian
	## CFGDIR=genCFGS_PosRes/${GENR}Gaussian
	for mass in 1000_1500 1500_1900 1900_2400 2400_2800 2800_3300 3300_3800 3800_4300 4300_13000
	## for mass in 3700_8000
	do
            for a in {0..9}
	    # for a in 0
	    do
		##config=$CFGDIR/chiCFG_m${mass}_${a}.py
		##logfile=$CFGDIR/chiCFG_m${mass}_${a}.log

		config=$CFGDIR/m${mass}/chiCFG_${a}.py
		logfile=$CFGDIR/m${mass}/chiCFG_${a}.log

		echo $config $logfile
		Submit $config $logfile
		let COUNTER=COUNTER+1
	    done
	done
    done
done

echo
echo "==> Submitted ${COUNTER} jobs <=="
echo
