#!/bin/bash
#

# echo "Number of arguments: " $#
if [ $# -lt 2 ]
then
    echo "Usage: toBatch.sh [outputfile] [inputfile] "
    echo "" 
    exit
fi

EXEC=CreateResponseMatrix.py

outfile=$1
infile=$2
Split=$3

echo
echo ">>> Beginning ${EXEC} execution on `date`  <<<"
echo

cmsswDir=$LS_SUBCWD
cd $cmsswDir

echo "Current directory: $cmsswDir"
echo $PWD
echo ""

## setup root ###########################

. setup_root.sh

## run the job ###################################

if [ $Split == 1 ]; then
    python ${EXEC} -n 0 --train ${outfile} ${infile}
elif [ $Split == 2 ]; then
    python ${EXEC} -n 0 --test ${outfile} ${infile}
else
    python ${EXEC} -n 0 ${outfile} ${infile}
fi




##################################################

echo
echo ">>> Ending ${EXEC} execution on `date`  <<<"
echo

exit
