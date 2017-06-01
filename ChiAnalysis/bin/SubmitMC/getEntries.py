import subprocess
import sys,string,math,os
import ConfigParser
import glob
from ROOT import TFile

from makeFileLists import *

#INDIR="/eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCD_HT_*"

ptBins={"HT300to500":"300_madgraph","HT500to700":"500_madgraph","HT700to1000":"700_madgraph","HT1000to1500":"1000_madgraph","HT1500to2000":"1500_madgrap","HT2000toInf":"2000_madgraph"}

for ptBin in ptBins:

    nevents=0

    workingDir=os.getcwd()
    
    os.chdir(workingDir)

    inputDir=INDIR
    if inputDir.find("*")>-1:
        inputDir=inputDir.replace("*",ptBins[ptBin])
    
    files=GetFileList(inputDir,searchstring)
    
    for filename in files:
        if filename=="root://eoscms//eos/cms/store/cmst3/user/hinzmann/dijet_angular/QCD_HT_700_madgraph/datacard_shapelimit13TeV_25ns_chi90_tree.root":
            continue
        print filename
        file=TFile.Open(filename)
        tree=file.Get("tree")
        nevents+=tree.GetEntries()

        
    print "***********************************"
    print "Number of Events in "+ptBin, nevents
    print "***********************************"
