#!/usr/bin/env python

import subprocess
import sys,string,math,os
import ConfigParser
import glob


###############################################################################################

FilesPerCfg=100  ##  number of files per fileslist

INDIR="/eos/cms/store/cmst3/user/hinzmann/dijet_angular/PromptData2016/"
OUTDIR="filelists/PromptData2016"
ptBins=["data"]
searchstring="datacard_shapelimit13TeV_"

## INDIR="/eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7/QCD_*_TuneCUETP8M1_13TeV_pythia8_RunIIFall15MiniAODv2_PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1"
## OUTDIR="filelists/pythia8"
## ptBins=["Pt_170to300","Pt_300to470","Pt_470to600","Pt_600to800","Pt_800to1000","Pt_1000to1400","Pt_1400to1800","Pt_1800to2400","Pt_2400to3200","Pt_3200toInf"]
## searchstring="EXOVVTree_QCD_"

## INDIR=/eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCDv7
## OUTDIR="filelists/madgraphMLM"
## ptBins=["HT300to500","HT500to700","HT700to1000","HT1000to1500","HT1500to2000","HT2000toInf"]
## searchstring="EXOVVTree_"

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
    for ptBin in ptBins:
        os.chdir(workingDir)
        
        inputDir=INDIR
        if inputDir.find("*")>-1:
            inputDir=inputDir.replace("*",ptBin)

        print "\nSearching for root files in: ",inputDir,"\n"
        fileList=GetFileList(inputDir,searchstring)
        if len(fileList)==0:
            print "\tNo root files found in directory!! Exiting"
            sys.exit(1)
        
        ## print fileList
    
        print "Creating filelists with ",FilesPerCfg," files per list"
        print "\nNumber of files found: ",len(fileList)
        print "First file: ",fileList[0],"\n"

        if ptBin == "25nsMC10" or ptBin == "data":
            OutName="ntuples.list"
        else:
            OutName="ntuples_" + ptBin + ".list"
            
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


    