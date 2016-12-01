#!/bin/csh
#

#################################################
## setup proper python and gcc versions first ###
#################################################

set THISHOST = LXPLUS
## set THISHOST = CMSLPC
echo
echo "Setting up Root to run on the $THISHOST cluster"
echo
if ( $THISHOST == LXPLUS ) then
## CERN
    setenv PATH "/afs/cern.ch/sw/lcg/external/Python/2.7.3/x86_64-slc6-gcc48-opt/bin:$PATH"
    setenv  LD_LIBRARY_PATH "/afs/cern.ch/sw/lcg/external/Python/2.7.3/x86_64-slc6-gcc48-opt/lib"

    source /afs/cern.ch/sw/lcg/external/gcc/4.9/x86_64-slc6-gcc49-opt/setup.csh
    setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.34/x86_64-slc6-gcc49-opt/root
else if ( $THISHOST == CMSLPC ) then
## FNAL
    setenv ROOTSYS /uscms/home/apana/work/root/root
endif
##  done ######################################### 

set path = ($ROOTSYS/bin $path)

if ($?LD_LIBRARY_PATH) then
   setenv LD_LIBRARY_PATH $ROOTSYS/lib:$LD_LIBRARY_PATH      # Linux, ELF HP-UX
else
   setenv LD_LIBRARY_PATH $ROOTSYS/lib
endif

if ($?DYLD_LIBRARY_PATH) then
   setenv DYLD_LIBRARY_PATH $ROOTSYS/lib:$DYLD_LIBRARY_PATH  # Mac OS X
else
   setenv DYLD_LIBRARY_PATH $ROOTSYS/lib
endif

if ($?SHLIB_PATH) then
   setenv SHLIB_PATH $ROOTSYS/lib:$SHLIB_PATH                # legacy HP-UX
else
   setenv SHLIB_PATH $ROOTSYS/lib
endif

if ($?LIBPATH) then
   setenv LIBPATH $ROOTSYS/lib:$LIBPATH                      # AIX
else
   setenv LIBPATH $ROOTSYS/lib
endif

if ($?PYTHONPATH) then
   setenv PYTHONPATH $ROOTSYS/lib:$PYTHONPATH
else
   setenv PYTHONPATH $ROOTSYS/lib
endif

if ($?MANPATH) then
   setenv MANPATH `dirname $ROOTSYS/man/man1`:$MANPATH
else
   setenv MANPATH `dirname $ROOTSYS/man/man1`
endif
