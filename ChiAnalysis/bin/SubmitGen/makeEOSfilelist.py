#!/usr/bin/env python

import subprocess
import sys,string,math,os
import ConfigParser
import glob

# eosCommand="/afs/cern.ch/project/eos/installation/0.2.31/bin/eos.select"
eosCommand="/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select"
filePrefix="root://eoscms/"

FILEMAX=10000

def createCFG(CFGFILE,filelist):
    
    ifile = open(CFGFILE,'w')
    for infile in filelist:
       outstring=infile
       ifile.write(outstring + "\n")

    ifile.close()

def GetEOSFileList(EOSDIR,searchstring=""):
    Debug=False
    ## print len(searchstring)

    fileList=[]

    p1 = subprocess.Popen([eosCommand, "ls", EOSDIR], shell=False, stdout=subprocess.PIPE)
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
    filepre=filePrefix+EOSDIR
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

    ## AutoLibraryLoader.enable()
    narg=len(sys.argv)
    # print narg
    if narg < 3:
        print " Please supply eos directory name and output file name"
        print " Optional 3rd argument is a search string, 4th is number of files per list"
        sys.exit(1)

    ## print sys.argv[0] ## calling program name
    EOSDir=sys.argv[1]
    OutFile=sys.argv[2]
    if narg>3:
        SearchString=sys.argv[3]
    else:
        SearchString=""
    fileList=GetEOSFileList(EOSDir,SearchString)
    
    FilesPerCfg=FILEMAX
    if narg>4:
        FilesPerCfg=int(sys.argv[4])
    if FilesPerCfg<=0: FilesPerCfg=FILEMAX
    
    print "FilesPerCfg= ",FilesPerCfg
    if len(fileList)==0:
        print "No rootfiles found in ",EOSDir
        sys.exit(1)
    else:
        print "\nNumber of files found: ",len(fileList)
        print "First file: ",fileList[0],"\n"

    OutputDir=os.path.dirname(OutFile)
    BaseName=os.path.basename(OutFile)
    
    indx=BaseName.find(".")
    if indx==-1:
        print "Could not determine file suffix. Please give name in the form: filebase.sfx"
        sys.exit(1)
    else:
        Suffix=BaseName[indx:]
        BaseName=BaseName[:indx]

    ### Print BaseName,Suffix

    if not os.path.exists(OutputDir):
        print "Output directory does not exist. Creating: ",OutputDir
        os.makedirs(OutputDir)
    os.chdir(OutputDir)
    
    print "Total number of files: ", len(fileList)
    i=0
    ibatch=0
    cfglist=[]    
    for ifile in fileList:
        i=i+1
        #if (i>MAXFILES): break
        filename=ifile
        cfglist.append(filename)
        if i%FilesPerCfg == 0 or i==len(fileList):
            if FilesPerCfg<FILEMAX:
                cfgfile=BaseName + "_" + str(ibatch) + Suffix
            else:
                cfgfile=BaseName + Suffix
            
            createCFG(cfgfile,cfglist)
            print "Wrote ",os.path.join(OutputDir,cfgfile)
            ibatch=ibatch+1
            cfglist=[]
    print "\nDone\n"


    
