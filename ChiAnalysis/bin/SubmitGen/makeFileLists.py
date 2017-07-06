#!/usr/bin/env python

import subprocess
import sys,string,math,os
import ConfigParser
import glob


###############################################################################################

FilesPerCfg=10  ##  number of files per fileslist

## MCSAMPLE="pythia8_ci"
MCSAMPLE="herwigpp"
## MCSAMPLE="madgraphMLM"
if MCSAMPLE=="pythia8_ci" or MCSAMPLE=="herwigpp":
    mBins=["1000_1500", "1500_1900", "1900_2400", "2400_2800", "2800_3300", "3300_3800", "3800_4300", "4300_13000"]
    INDIR="/eos/cms/store/cmst3/user/hinzmann/dijet_angular"
elif MCSAMPLE=="madgraphMLM":
    mBins=["300to500", "500to700", "700to1000","1000to1500","1500to2000","2000toInf"]
    INDIR="/eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7"
else:
    print "Please specify a MCSAMPLE. --existing"

eosCommand="/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select" ## if this doesn't work check name using ouput from "which eos"

################## should not need to change anything below this ################################


def createCFG(CFGFILE,filelist):
    
    ifile = open(CFGFILE,'w')
    for infile in filelist:
       outstring=infile
       ifile.write(outstring + "\n")

    ifile.close()

def isEOSdir(dir):

    isEOS=False
    if dir.find("eos")>-1: isEOS=True

    return isEOS

def removeTrailingSlash(dir):
    ## print len(dir)
    if dir.rfind("/")==len(dir)-1:
        dir=dir[:len(dir)-1]
    return dir

def GetFileList(dir,searchstring=""):
    Debug=False
    if Debug: print len(searchstring)

    dir=removeTrailingSlash(dir)
    if Debug: "dir: ",dir
    fileList=[]
    if isEOSdir(dir):
        filePrefix="root://eoscms/"
        commands=[eosCommand, "ls", dir]
    else:
        filePrefix=""
        commands=["ls", dir]

    if Debug: print commands
    p1 = subprocess.Popen(commands, shell=False, stdout=subprocess.PIPE)
        
    (stdout, stderr)=p1.communicate()
    if stderr is not None:
        print "Trouble executing the srmls command"
        sys.exit(1)
    
    if Debug:
        print "Raw output:\n"
        print stdout
        print "Done\n"
    
    files=stdout.split('\n')
    if Debug:
        print "\n Number of files in directory: ",len(files),"\n"
        print "\n"
    
    i=0
    filepre=filePrefix + dir
    for infile in files:
        if infile.find(".root")>-1:
            if len(searchstring)==0 or infile.find(searchstring)>-1:
                i=i+1
                # print i,infile
                filename=os.path.join(filepre,infile)
                fileList.append(filename)
                # filename=os.path.join(remoteDir,infile)

    return fileList


if __name__ == "__main__":

    FILEMAX=100000

    workingDir=os.getcwd()
    for mBin in mBins:
        os.chdir(workingDir)
        
        inputDir=INDIR
        if inputDir.find("*")>-1:
            inputDir=inputDir.replace("*",ptBin)

        print "\nSearching for root files in: ",inputDir,"\n"

        if MCSAMPLE=="pythia8_ci":
            searchstring="jobtmp_pythia8_ci_m" +mBin+ "_50000_1_0_0_13TeV_Nov14"
            OUTDIR="filelists/pythia8_ci_50000__Nov14/m" + mBin
        elif MCSAMPLE=="herwigpp":
            searchstring="jobtmp_herwigpp_qcd_m" + mBin + "___Nov28"
            OUTDIR="filelists/herwigpp_Nov28/m" + mBin
        elif MCSAMPLE=="madgraphMLM":
            searchstring="EXOVVTree_QCD_HT"+mBin+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIIFall15MiniAODv2_PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1"
            OUTDIR="filelists/madgraphMLM_2016/ht" + mBin
        else:
            print "\t Not yet setup for MCSAMPLE: ",MCSAMPLE,"  -- exiting"
            sys.exit(1)
            
        OutName="fileList.txt"
            
        fileList=GetFileList(inputDir,searchstring)
        if len(fileList)==0:
            print "\tNo root files found in directory!! Exiting"
            sys.exit(1)
        
        ## print fileList
    
        print "Creating filelists with ",FilesPerCfg," files per list"
        print "\nNumber of files found: ",len(fileList)
        print "First file: ",fileList[0],"\n"

            
        OutFile=os.path.join(OUTDIR,OutName)
        
        BaseName=os.path.basename(OutFile)
    
        indx=BaseName.find(".")
        if indx==-1:
            print "Could not determine file suffix. Please give name in the form: filebase.sfx"
            sys.exit(1)
        else:
            Suffix=BaseName[indx:]
            BaseName=BaseName[:indx]

            ### Print BaseName,Suffix

        if not os.path.exists(OUTDIR):
            print "Output directory does not exist. Creating: ",OUTDIR
            os.makedirs(OUTDIR)
        os.chdir(OUTDIR)
    
        i=0
        ibatch=0
        cfglist=[]    
        for ifile in fileList:
            i=i+1
            filename=ifile
            cfglist.append(filename)
            if i%FilesPerCfg == 0 or i==len(fileList):
                if FilesPerCfg<FILEMAX:
                    cfgfile=BaseName + "_" + str(ibatch) + Suffix
                else:
                    cfgfile=BaseName + Suffix

                createCFG(cfgfile,cfglist)
                print "Wrote ",os.path.join(OUTDIR,cfgfile)
                ibatch=ibatch+1
                cfglist=[]
        print "\nDone\n"


    
