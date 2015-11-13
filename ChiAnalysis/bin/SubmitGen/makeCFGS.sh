#!/bin/bash

NCFGs=10  ## this should correspond to the number of filelists in each filelist directory

#Generator="Herwig"
#CrossSections=(9.300e03 2.300e03 1.383e02 6.990e00) ## Herwig
#generator="herwigpp"

Generator="Pythia8"
CrossSections=(3.769e-05 3.307e-06 8.836e-07 1.649e-07 6.446e-08 1.863e-08 5.867e-09 3.507e-09) ## Pythia8
generator="pythia8_ci"

SmearMax=2.5
newDir="genCFGS"/${Generator}CrystalBallT${SmearMax}
# newDir="genCFGS"/${Generator}Gaussian
# newDir="genCFGS"/${Generator}SysMinus
# newDir="genCFGS_new"/${Generator}GaussianSysMinus
# newDir="genCFGS_PosRes"/${Generator}Gaussian

CFG=GenChiNtuple_cfg

MASS="AAAA"
XS=XSECTION
SMEAR="CCCC"
GENER="DDDD"

searchstring="XXXX"

MBIN=0
# for mass in 1000_1500 1500_1900 1900_2400 2400_2800 2800_3300 3300_3800 3800_4300 4300_13000
for mass in 1000_1500
do
    xs=${CrossSections[${MBIN}]}

    mkdir -p ${newDir}/m${mass}
    COUNTER=0
    while [  $COUNTER -lt $NCFGs ]; do
    ## echo The counter is $COUNTER

	newFile=${newDir}/m${mass}/${CFG}_${COUNTER}.py
	echo $newFile $xs
	tmpFileA="abc.txt"
	tmpFileB="def.txt"
	tmpFileC="ghi.txt"
	tmpFileD="jkl.txt"
	sed -e 's/'$searchstring'/'$COUNTER'/' ${CFG}_TEMPLATE.py > ${tmpFileA}

	sed -e 's/'$MASS'/'$mass'/' ${tmpFileA} > ${tmpFileB}
	sed -e 's/'$SMEAR'/'$SmearMax'/' ${tmpFileB} > ${tmpFileC}
	sed -e 's/'$GENER'/'$generator'/' ${tmpFileC} > ${tmpFileD}
	sed -e 's/'$XS'/'$xs'/' ${tmpFileD} > ${newFile}
	rm $tmpFileA $tmpFileB $tmpFileC $tmpFileD

	let COUNTER=COUNTER+1
    done
    let MBIN=MBIN+1
done
