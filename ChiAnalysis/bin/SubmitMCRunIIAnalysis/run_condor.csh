#!/bin/tcsh
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node

source /cvmfs/cms.cern.ch/cmsset_default.csh  ## if a bash script, use .sh instead of .csh
xrdcp -s root://cmseos.fnal.gov//store/user/zhangj/CMSSW8023.tgz .
tar -xf CMSSW8023.tgz
rm CMSSW8023.tgz
setenv SCRAM_ARCH slc6_amd64_gcc530
cd CMSSW_8_0_23/src/
scramv1 b ProjectRename
eval `scramv1 runtime -csh` # cmsenv is an alias not on the workers

cd MyChi/ChiAnalysis/bin/SubmitMCRunIIAnalysis
echo "Executable: $1"
echo "thePTBin: "$PTBIN
echo "SMRMAX: "$SMRMAX
echo "AK4SF: "$AK4SF
echo "DATATOMC: "$DATATOMC
echo "SYSERR: "$SYSERR
echo "GENERATOR: "$GENERATOR
ChiNtuple ${1}

if ($SMRMAX == 0) then
    set output = chiNtuple_${GENERATOR}_${PTBIN}_GS
else
    set output = chiNtuple_${GENERATOR}_${PTBIN}_CB2
endif

if ($AK4SF == 1) set output = ${output}_AK4SF

if ($DATATOMC == 1) set output = ${output}_DataToMCSF

if ($SYSERR == 1) set output = ${output}_SysPlus

if ($SYSERR == -1) set output = ${output}_SysMinus

echo "output: "${output}.root
ls

xrdcp -f ${output}.root root://cmseos.fnal.gov//store/user/zhangj/DijetAngularRunII/jetUnfold/MCNtuple/${output}.root
#cp ${output}.root /eos/uscms/store/user/zhangj/DijetAngularRunII/jetUnfold/MCNtuple/${output}.root

cd ${_CONDOR_SCRATCH_DIR}
rm -rf CMSSW_8_0_23
