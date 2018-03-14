#!/bin/sh

QUEUE=1nd
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
bsub -q ${QUEUE} -oo ${logfile} ${SUB_SCRIPT} ${cfgfile}

}

#################################################################################

theDate=`date '+%Y%m%d'`

COUNTER=0
# for GENR in Pythia8 Herwig
#for GENR in Herwig
#for GENR in madgraph
for GENR in Pythia8
do
    for TRUNC in 0
    #for TRUNC in 2
    do
	if [ ${TRUNC} == 0 ]; then
	    #CFGDIR=genCFGS/${GENR}Gaussian
	    #CFGDIR=genCFGS/${GENR}GaussianSysPlus
	    CFGDIR=genCFGS/${GENR}GaussianSysMinus
        else
	    CFGDIR=genCFGS/${GENR}CrystalBall
	fi
	
	for mass in 1000_1500 1500_1900 1900_2400 2400_2800 2800_3300 3300_3800 3800_4300 4300_13000
	## for mass in 1000_1500
	#for mass in 300to500 500to700 700to1000 1000to1500 1500to2000 2000toInf
	do
	    njobs=`ls -1 ${CFGDIR}/m${mass}/*py | wc -l`
	    #njobs=`ls -1 ${CFGDIR}/ht${mass}/*py | wc -l`
	    njobs=$(($njobs - 1))
            for a in $(seq 0 $njobs);
	    # or a in 0
	    do
		config=$CFGDIR/m${mass}/GenChiNtuple_cfg_${a}.py
		#config=$CFGDIR/ht${mass}/GenChiNtuple_cfg_${a}.py
		logfile=$CFGDIR/m${mass}/GenChiNtuple_cfg_${a}_${theDate}.log
		#logfile=$CFGDIR/ht${mass}/GenChiNtuple_cfg_${a}_${theDate}.log

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
