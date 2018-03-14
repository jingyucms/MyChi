#!/bin/bash

########################################################################

AK4sf=1       # set to 1 to turn on AK4 scale factor, 0=off
DataToMCsf=1  # set to 1 to turn on DataToMC scale factor, 0=off
SysErr=0      # +-1 to smear by additional +-10%,  anything else no addtional smearing   only for Gaussian smearing
dmweight=1    # set to 1 for DM samples, 0 for other samples

# Generator="Herwig"
# Generator="Pythia8"
# Generator="QBHADD6"
Generator="DMAxial"

SMEARING=CrystalBall
# SMEARING=Gaussian

########################################################################

NCFGs=6  ## this should correspond to the number of filelists in each filelist directory

cfgDir=genCFGS/${Generator}${SMEARING}
if [[ "$SysErr" -eq 1 ]]; then
    cfgDir=genCFGS/${Generator}${SMEARING}SysPlus
elif [[ "$SysErr" -eq -1 ]]; then
    cfgDir=genCFGS/${Generator}${SMEARING}SysMinus
fi


if [[ "$Generator" == "Herwig" ]]; then
    CrossSections=(26.5361 2.26487 0.588676 0.109694 0.0431171 0.0126252 0.00404967 0.00253067) ## Herwig
    generator="herwigpp"
    filelistbase=${generator}_Nov28
elif [[ "$Generator" == "QBHADD6" ]]; then
    CrossSections=(0.1634881 0.05385596 0.01678352 0.004871688 0.001292072 0.0003054339 0.00006221544) ## QBH
    generator="qbhadd6"
    filelistbase=${generator}_2017
elif [[ "$Generator" == "DMAxial" ]]; then
    CrossSections=(1. 1. 1. 1. 1. 1. 1. 1. 1.) ## QBH
    generator="dmaxial"
    filelistbase=${generator}_2017
else
    CrossSections=(3.769e-05 3.307e-06 8.836e-07 1.649e-07 6.446e-08 1.863e-08 5.867e-09 3.507e-09) ## Pythia8
    generator="pythia8_ci"
    filelistbase=${generator}_50000__Nov14
fi

OutDir=root://cmseos.fnal.gov//eos/uscms/store/user/jingyu/events/${generator}_${SMEARING}
CFG=GenChiNtuple_cfg


MBIN=0
## for mass in 1000_1500 1500_1900 1900_2400 2400_2800 2800_3300 3300_3800 3800_4300 4300_13000
#for mass in 6500 7000 7500 8000 8500 9000 9500
#for mass in 2000 2250 2500 3000 3500 4000 4500 5000 6000
for mass in 6000
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
	
	python makeCFG.py ${cfgFile} ${fileList} ${OutFile} ${SMEARING} ${AK4sf} ${DataToMCsf} ${SysErr} ${xs} ${dmweight}
	
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
