#!/usr/bin/python
#

import sys,string,time,os,os.path


def createCFG(fd):
    return
    
def usage():
    """ Usage: makeCFG configname nevts
    """
    pass

if __name__ == '__main__':

    narg=len(sys.argv)
    if narg < 3 :
        print usage.__doc__
        sys.exit(1)

    CFGFILE=sys.argv[1]
    FILELIST=sys.argv[2]
    OUTFILE=sys.argv[3]
    SMEARING=sys.argv[4]
    AK4SF=sys.argv[5]
    DATATOMCSF=sys.argv[6]
    SYSERR=sys.argv[7]
    XSECTION=sys.argv[8]

    OutFile=OUTFILE
    NEVT="-1"
    smearMax="2"

    doAK4_sf="False"
    if AK4SF == "1": doAK4_sf="True"

    doDataToMC_sf="False"
    if DATATOMCSF == "1": doDataToMC_sf="True"

    DOSYS="True"
    if SMEARING != "Gaussian": DOSYS="False"
    if SYSERR=="0": DOSYS="False"

    sysPlus="False"
    if DOSYS=="True" and SYSERR=="1": sysPlus="True"
    
    if not os.path.exists(FILELIST):
        print "Filelist: ",FILELIST," does not exist.  Aborting..."
        sys.exit(1)
    
    infiles = [line.strip() for line in open(FILELIST, 'r')]

    
    
    fd = open(CFGFILE,'w')    
    fd.write("import FWCore.ParameterSet.Config as cms\n")
    fd.write("import os \n\n")
    fd.write("process = cms.PSet()\n\n")

    fd.write("process.fwliteInput = cms.PSet(\n")
    fd.write("    fileNames   = cms.vstring(\n")
    for infile in infiles:
        fd.write("                \""+infile+"\",\n")
    fd.write("    ),\n")
    fd.write("    maxEvents   = cms.int32(" + NEVT + "),\n")
    fd.write("    outputEvery = cms.uint32(50000),\n")
    fd.write(")\n\n")

    fd.write("process.fwliteOutput = cms.PSet(\n")
    fd.write("    fileName  = cms.string(\""+OutFile+"\"),\n")
    fd.write(")\n\n")

    fd.write("process.GenChiAnalysis = cms.PSet(\n")
    fd.write("    GenJets = cms.InputTag(\'ak4GenJets\'),\n")
    #fd.write("    GenJets = cms.InputTag(\'slimmedGenJets\'),\n")
    fd.write("    Smearing = cms.string(\""+SMEARING+"\"),\n")
    fd.write("    AK4_SF = cms.bool("+doAK4_sf+"),\n")
    fd.write("    DATAtoMC_SF = cms.bool("+doDataToMC_sf+"),\n")
    fd.write("    doSys = cms.bool("+DOSYS+"),\n")
    fd.write("    sysPlus = cms.bool("+sysPlus+"),\n")
    fd.write("    CrossSection = cms.double("+XSECTION+"),\n")
    fd.write("    SmearMax = cms.double("+smearMax+")\n")
    fd.write(")\n\n")    
    
    fd.close()
    print "Wrote ",CFGFILE
    
    
