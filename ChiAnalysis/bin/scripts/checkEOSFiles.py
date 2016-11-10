from ROOT import gROOT, gStyle, gSystem, TCanvas, TF1, TFile, TH1F, TColor, TLine, TLegend, TLatex, SetOwnership, TChain
import sys,string,math,os,ROOT
import subprocess
## from PhysicsTools.PythonAnalysis import *
from ROOT import *
## gSystem.Load("libFWCoreFWLite.so")
## AutoLibraryLoader.enable()

sys.path.append(os.path.join(os.environ.get("HOME"),'rootmacros'))
from myPyRootMacros import prepPlot, SetStyle, GetHist, PrepLegend, DrawText, prep1by2Plot, ResetAxisAndLabelSizes
#===============================================================

dist="chi"

Rebin=-1  ## used to overide default rebin value

PrintPlot=False
# PrintPlot=True


def GetEOSFileList(EOSDIR,searchstring=""):

    filePrefix="root://eoscms/"    
    eosCommand="/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select"    
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

#===============================================================

if __name__ == '__main__':
    ## SetStyle()
    ## gStyle.SetOptStat(110);

    NARG=2
    narg=len(sys.argv)
    if (narg < NARG ):
        print "Please supply EOS directory name"
        sys.exit(1)
        
    EOSDir=sys.argv[1]

    fileNames=GetEOSFileList(EOSDir,".root")
    ## print fileNames

    tree=TChain("DijetTree");
    
    i=0
    for rootfile in fileNames:
        i=i+1
        print i,rootfile
        f = ROOT.TFile.Open(rootfile)
        ## print f        
        if f==None:
            print "\n\tTrouble!!  Could not open: ", rootfile,"\n"
        ## f.ls()
        ## tree.Add(f);
    
    ## print "\n",i,"Files added to chain\n"
    ## 
    ## 
    ## branch="smrDijets.chi";   cut="smrDijets.dijetFlag==1";
    ## 
    ## print branch
    ## 
    ## h1=TH1F("chi","chi",15,1,16)
    ## tree.Project(h1.GetName(),branch)
    ## 
    ## print "h1: ",h1.GetEntries()
    ## 
    ## c1=prepPlot("c1","c1")
    ## c1.cd()
    ## c1.SetLogy(False)
    ## 
    ## h1.Draw()
    ## 
    ## if (PrintPlot):
    ##     psname="comp_" + L1Obj + "_" + dist
    ##     c1.Print(psname + ".gif")
