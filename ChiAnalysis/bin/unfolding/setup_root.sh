#!/bin/bash
#

Debug=1

#################################################
## setup proper python and gcc versions first ###
#################################################

echo "Setting up root v5.34.34"

if [ $Debug -eq 1 ]; then
    echo -e "\nBefore root setup ========================================================" 
    echo "ROOTSYS: " $ROOTSYS
    echo "LD_LIBRARY_PATH: " $LD_LIBRARY_PATH
    echo "PATH: " $PATH
    echo -e "Done listing ============================================================\n"
fi

if [ -z "${LD_LIBRARY_PATH}" ]; then
    export LD_LIBRARY_PATH=/afs/cern.ch/sw/lcg/external/Python/2.7.3/x86_64-slc6-gcc48-opt/lib
else
    export LD_LIBRARY_PATH=/afs/cern.ch/sw/lcg/external/Python/2.7.3/x86_64-slc6-gcc48-opt/lib:$LD_LIBRARY_PATH
fi
## echo "LD_LIBRARY_PATH: " $LD_LIBRARY_PATH

if [ -z "${PATH}" ]; then
    export PATH=/afs/cern.ch/sw/lcg/external/Python/2.7.3/x86_64-slc6-gcc48-opt/lib
else
    export PATH=/afs/cern.ch/sw/lcg/external/Python/2.7.3/x86_64-slc6-gcc48-opt/bin:$PATH
fi
# echo "PATH: " $PATH
# echo "ROOTSYS: " $ROOTSYS


# . /afs/cern.ch/sw/lcg/external/gcc/4.6/x86_64-slc5/setup.sh
# source /afs/cern.ch/user/a/apana/setup_gcc.sh
source /afs/cern.ch/sw/lcg/external/gcc/4.9/x86_64-slc6-gcc49-opt/setup.sh
## echo "XXXXXXXX PATH: " $PATH
source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.34/x86_64-slc6-gcc49-opt/root/bin/thisroot.sh

if [ $Debug -eq 1 ]; then
    echo -e "\nAfter root setup ======================================================" 
    echo "ROOTSYS: " $ROOTSYS
    echo "LD_LIBRARY_PATH: " $LD_LIBRARY_PATH
    echo "PATH: " $PATH
    echo -e "Done listing ============================================================\n"
fi

echo ""
