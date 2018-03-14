#!/bin/tcsh
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
source /cvmfs/cms.cern.ch/cmsset_default.csh  ## if a bash script, use .sh instead of .csh
### copy the input root files if they are needed only if you require local reading
#xrdcp root://cmseos.fnal.gov//store/user/username/Filename1.root .
#xrdcp root://cmseos.fnal.gov//store/user/username/Filename2.root .
xrdcp -s root://cmseos.fnal.gov//store/user/jingyu/CMSSW8023.tgz .
tar -xf CMSSW8023.tgz
rm CMSSW8023.tgz
setenv SCRAM_ARCH slc6_amd64_gcc530
cd CMSSW_8_0_23/src/
scramv1 b ProjectRename
eval `scramv1 runtime -csh` # cmsenv is an alias not on the workers
echo "Arguments passed to this script are: for 1: $1"
echo ${MBIN}
cd MyChi/ChiAnalysis/bin/SubmitNP/genCFGS/${SAMPLE}CrystalBall/m${MBIN}/
GenChiAnalysis ${1}
#xrdcp nameOfOutputFile.root root://cmseos.fnal.gov//store/user/username/nameOfOutputFile.root
### remove the input and output files if you don't want it automatically transferred when the job ends
#rm nameOfOutputFile.root
#rm Filename1.root
#rm Filename2.root
cd ${_CONDOR_SCRATCH_DIR}
rm -rf CMSSW_8_0_23
