from ROOT import gROOT, gStyle, gSystem, TCanvas, TF1, TFile, TH1F, TColor, TLine, TLegend, TLatex, SetOwnership, gDirectory, TH1, TDecompSVD
import sys,string,math,os,ROOT

# ROOT.gSystem.Load(os.path.join(os.environ.get("HOME"),'Chi/RooUnfold-1.1.1/libRooUnfold.so'))
# ROOT.gSystem.Load(os.path.join(os.environ.get("HOME"),'Chi/RooUnfold-1.1.1/libRooUnfold.rootmap'))

ROOT.gSystem.Load('RooUnfold/libRooUnfold.so')
ROOT.gSystem.Load('RooUnfold/libRooUnfold.rootmap')

from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import RooUnfoldInvert

sys.path.append(os.path.join(os.getcwd(),'rootmacros'))
from myPyRootMacros import *
from scripts import plotComparison, doPoisson, getMassBins, compAndDrawIt,reBin

#===============================================================

#doMC=True
doMC=False
CheckProj=False
#CheckProj=True

#PlotUnfolded=False
PlotUnfolded=True
PlotUnfoldedAndFit=False  # make ratio histogram and fit the ratio (aka fit to get uncertainty)
#PlotUnfoldedAndFit=True

compToGen=False  # compare SMR MC to Gen MC, use when do closure test
#compToGen=True

saveSMR=False  # use when you want to save smr mc distribution in output foot file
#saveSMR=True

suffix=".gif"

outDir="results_MatrixInvert"


#===============================================================

if __name__ == '__main__':

    SetStyle()

    gStyle.SetOptFit(0001)
    gROOT.ForceStyle()

    MCSAMPLE="pythia8_Pt_170toInf"; date="20170130"
    #MCSAMPLE="madgraphMLM_HT_300toInf"; date="20161214"

    WhichSmearing="Smeared"  ## unsmearing matrix derived from Smeared jets

    if WhichSmearing=="Smeared":
        WhichJets="SMR"
        smearFunc="CB_AK4SF"
        #smearFunc="GS_AK4SF"
    elif WhichSmearing=="Reco":
        WhichJets="RECO"
        smearFunc="CB2_AK4SF_DataToMCSF"
    else:
        print "Problems"
        sys.exit(1)

    if not outDir in os.listdir(os.getcwd()):
        os.system('mkdir '+outDir)

    #dataFile="/uscms_data/d3/jingyu/ChiAnalysis/jetUnfold/CMSSW_8_0_23/src/MyChi/ChiAnalysis/bin/unfolding/ResponseMatrices/chiNtuple_dataReReco_prelimJEC_PFHT900.root"
    #dataFile="/uscms_data/d3/jingyu/ChiAnalysis/jetUnfold/CMSSW_8_0_23/src/MyChi/ChiAnalysis/bin/unfolding/ResponseMatrices/chiNtuple_data_PFHT900_v2.root"
    dataFile="/uscms_data/d3/jingyu/ChiAnalysis/jetUnfold/CMSSW_8_0_23/src/MyChi/ChiAnalysis/bin/unfolding/chiNtuple_dataReReco_v3_PFHT900.root"

    responseFile="ResponseMatrices/Response_"+MCSAMPLE+"_" +smearFunc + "_" +date +".root"
    #responseFile="ResponseMatrices/Response_madgraphMLM_HT_300toInf_CB_AK4SF_20161214.root"
    #responseFile="../ResponseMatrices/Response_"+MCSAMPLE+"_" +smearFunc + "_" +date +"_Train.root"
    #responseFile="ResponseMatrices/Response_pythia8_Pt_170toInf_CB_AK4SF_Test_20161214_Test.root"
    
    

    Reco2d_Chi1=Get2DHist(dataFile,"dijet_mass2_chi1")
    Reco2d_Chi2=Get2DHist(dataFile,"dijet_mass2_chi2")
    Reco2d_Chi3=Get2DHist(dataFile,"dijet_mass2_chi3")
    Reco2d_Chi4=Get2DHist(dataFile,"dijet_mass2_chi4")        

    
    ## get the Response matrix
    print "Response file: ",responseFile
    f = TFile.Open(responseFile)
    response_m2c1=gDirectory.Get("response2d"+WhichJets+"_m2c1")
    response_m2c2=gDirectory.Get("response2d"+WhichJets+"_m2c2")
    response_m2c3=gDirectory.Get("response2d"+WhichJets+"_m2c3")
    response_m2c4=gDirectory.Get("response2d"+WhichJets+"_m2c4")
    print "=== Response matrices ======================"
    print response_m2c1
    print response_m2c2
    print response_m2c3
    print response_m2c4
    print "============================================="

    Response1=response_m2c1.Mresponse()
    Response2=response_m2c2.Mresponse()
    Response3=response_m2c3.Mresponse()
    Response4=response_m2c4.Mresponse()

    Response2.Print()

    responseOut=TFile("responseMatrices.root","RECREATE")
    Response1.Write()
    Response2.Write()
    Response3.Write()
    Response4.Write()

    sys.exit()
    
    print "============================================="
    singular1=TDecompSVD(Response1)
    print singular1.Condition()

    sig1=singular1.GetSig()
    sig1.Print()

    print "============================================="
    singular2=TDecompSVD(Response2)
    print singular2.Condition()
    
    sig2=singular2.GetSig()
    sig2.Print()
    
    Reco2d=Reco2d_Chi1
    massBins=getMassBins(Reco2d)

    chiHists1d=[]; chiTests1d=[]; unfChiHists1d=[]
    for i in range(1,len(massBins)-1):
        minMass=int(massBins[i])
        maxMass=int(massBins[i+1])
        strMinM=str(int(minMass)); strMaxM=str(int(maxMass)); 
        if minMass<2400: continue

        if minMass<2400:
            Reco2d=Reco2d_Chi1
            response=response_m2c1
        
        elif minMass<6000:
            Reco2d=Reco2d_Chi2
            response=response_m2c2
            #Reco2d=Reco2d_Chi1
            #response=response_m2c1
        else:
            Reco2d=Reco2d_Chi3           
            response=response_m2c3
            #Reco2d=Reco2d_Chi1           
            #response=response_m2c1
            #Reco2d.SetBinContent(11,1,16)
            #Reco2d.SetBinError(11,1,4)

        chiTests1d.append(Proj2D_Y(Reco2d,minMass,maxMass,Reco2d.GetName(),True))

        ## now do unfolding
        print "CCLA: D'Agostini Unfolding ",Reco2d,"using matix ",response
        
        unfold2d = RooUnfoldInvert     (response, Reco2d)
        unfold2d.Print()

        hUnf2d= unfold2d.Hreco(2)
            
        print "XXX: ",hUnf2d
        hD=Proj2D_Y(hUnf2d,minMass,maxMass,hUnf2d.GetName(),True)

        h=TH1F()
        hD.Copy(h)  ## convert TH1D to TH1F
        unfChiHists1d.append(h)
        f.Close()

    plotComparison(chiTests1d,unfChiHists1d,"Unfolded",True,doMC)

    ## now write out the unfolded histograms
    outname=os.path.basename(dataFile)
    outname=outname[:outname.find(".root")] 

    if WhichSmearing == "Smeared":
        outname=outDir+"/Unfolded_" +outname + "_from" + smearFunc + "_" +MCSAMPLE+"_MatrixInvert.root"
    else:
        outname=outDir+"/Unfolded_" +outname + "_from" + WhichSmearing + "_" +MCSAMPLE+"_MatrixInvert.root"

    print "\n\n%Response file: ",responseFile
    print "%Writing unfolded histograms to: ",outname
    
    outfile = TFile.Open(outname,"RECREATE")

    for i in range(len(unfChiHists1d)):
        hOrg=chiTests1d[i]
        hUnf=unfChiHists1d[i]
        orgname=hOrg.GetName()
        newname=orgname + "_unfolded"
        hUnf.SetName(newname)

        hOrg.SetLineColor(ROOT.kRed)
        hOrg.Write()
        hUnf.Write()
    outfile.Close()

    ## print ROOT.TH1.kPoisson, ROOT.TH1.kPoisson2,ROOT.TH1.kNormal

#===============================================================
    if os.getenv("FROMGUI") == None:
        print "Not from GUI"
        # raw_input('\npress return to end the program...')
    
