#!/bin/bash

########################################################################

AK4sf=1       # set to 1 to turn on AK4 scale factor, 0=off
DataToMCsf=1  # set to 1 to turn on DataToMC scale factor, 0=off
SysErr=0      # +-1 to smear by additional +-10%,  anything else no addtional smearing   only for Gaussian smearing

Generator="Herwig"
# Generator="Pythia8"

# SMEARING=CrystalBall
SMEARING=Gaussian

########################################################################

NCFGs=10  ## this should correspond to the number of filelists in each filelist directory

cfgDir=genCFGS/${Generator}${SMEARING}
if [[ "$SysErr" -eq 1 ]]; then
    cfgDir=genCFGS/${Generator}${SMEARING}SysPlus
elif [[ "$SysErr" -eq -1 ]]; then
    cfgDir=genCFGS/${Generator}${SMEARING}SysMinus
fi


if [[ "$Generator" == "Herwig" ]]
then
    CrossSections=(26.5361 2.26487 0.588676 0.109694 0.0431171 0.0126252 0.00404967 0.00253067) ## Herwig
    generator="herwigpp"
    filelistbase=${generator}_Nov28
else
    CrossSections=(3.769e-05 3.307e-06 8.836e-07 1.649e-07 6.446e-08 1.863e-08 5.867e-09 3.507e-09) ## Pythia8
    generator="pythia8_ci"
    filelistbase=${generator}_50000__Nov14
fi

OutDir=root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/GenOutput/80x/${generator}_${SMEARING}
CFG=GenChiNtuple_cfg


MBIN=0
for mass in 1000_1500 1500_1900 1900_2400 2400_2800 2800_3300 3300_3800 3800_4300 4300_13000
## for mass in 1000_1500
do
    xs=${CrossSections[${MBIN}]}

    mkdir -p ${cfgDir}/m${mass}
    COUNTER=0
    while [  $COUNTER -lt $NCFGs ]; do
    ## echo The counter is $COUNTER

	cfgFile=${cfgDir}/m${mass}/${CFG}_${COUNTER}.py

	fileList=filelists/${filelistbase}/m${mass}/fileList_${COUNTER}.txt
	OutFile=${OutDir}/chiSmearing_13TeV_m${mass}
	OutFile=${OutFile}_AK4sf_${AK4sf}
	OutFile=${OutFile}_DataToMCsf_${DataToMCsf}
	if [ $SysErr == 1 ]; then
	    OutFile=${OutFile}_SysPlus
	elif [ $SysErr == -1 ]; then
	    OutFile=${OutFile}_SysMinus	    
	fi
	OutFile=${OutFile}_${COUNTER}.root
	
	python makeCFG.py ${cfgFile} ${fileList} ${OutFile} ${SMEARING} ${AK4sf} ${DataToMCsf} ${SysErr} ${xs}
	
	## sed -e 's/'$MASS'/'$mass'/' ${tmpFileA} > ${tmpFileB}
	## sed -e 's/'$SMEAR'/'$SmearMax'/' ${tmpFileB} > ${tmpFileC}
	## sed -e 's/'$GENER'/'$generator'/' ${tmpFileC} > ${tmpFileD}
	## sed -e 's/'$XS'/'$xs'/' ${tmpFileD} > ${newFile}
	## rm $tmpFileA $tmpFileB $tmpFileC $tmpFileD
	## 
	## OutFile=
	let COUNTER=COUNTER+1
    done
    let MBIN=MBIN+1
done
