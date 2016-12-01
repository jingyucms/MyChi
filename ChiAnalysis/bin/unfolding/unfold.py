from ROOT import gROOT, gStyle, gSystem, TCanvas, TF1, TFile, TH1F, TColor, TLine, TLegend, TLatex, SetOwnership, gDirectory, TH1
import sys,string,math,os,ROOT


# ROOT.gSystem.Load(os.path.join(os.environ.get("HOME"),'Chi/RooUnfold-1.1.1/libRooUnfold.so'))
# ROOT.gSystem.Load(os.path.join(os.environ.get("HOME"),'Chi/RooUnfold-1.1.1/libRooUnfold.rootmap'))

ROOT.gSystem.Load('RooUnfold/libRooUnfold.so')
ROOT.gSystem.Load('RooUnfold/libRooUnfold.rootmap')

from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes


sys.path.append(os.path.join(os.environ.get("HOME"),'rootmacros'))
from myPyRootMacros import *
from scripts import plotComparison, doPoisson, getMassBins
#===============================================================

doMC=False
# doMC=True

CheckProj=False
## CheckProj=True

# PlotUnfolded=False
PlotUnfolded=True


writePlot=False

suffix=".gif"

#===============================================================

if __name__ == '__main__':


    SetStyle()

    ## MCSAMPLE="Pt_170to13000" ; date="20151202"
    ## MCSAMPLE="Pythia_M_1000to13000"; date="20151202"
    MCSAMPLE="Herwig_M_1000to13000"; date="20151203_partial"

    WhichSmearing="Smeared"  ## unsmearing matrix derived from Smeared jets
    ## WhichSmearing="Reco"   ## unsmearing matrix derived from RECO 

    if WhichSmearing=="Smeared":
        WhichJets="SMR"
        ## smearFunc="CB2_AK4SF_DataToMCSF"
        smearFunc="GS_AK4SF_DataToMCSF"
        ## smearFunc="GS_AK4SF"
    elif WhichSmearing=="Reco":
        WhichJets="RECO"
        smearFunc="CB2_AK4SF_DataToMCSF"
    else:
        print "Problems"
        sys.exit(1)

    ## dataFile="/eos/uscms/store/user/apana/Chi_13TeV/ChiNtuples/Data/chiNtuple_data_25nsData5_teff.root"
    dataFile="/eos/uscms/store/user/apana/Chi_13TeV/ChiNtuples/Data/chiNtuple_data_2pt4invfb_teff.root"

    responseFile="../ResponseMatrices/Response_"+MCSAMPLE+"_" +smearFunc + "_" +date +".root"
    #responseFile="../ResponseMatrices/Response_"+MCSAMPLE+"_" +smearFunc + "_" +date +"_Train.root"

    if doMC:
        # dataFile=responseFile
        # dataFile=dataFile.replace("Train","Test")
        dataFile="../ResponseMatrices/Response_Pythia_M_1000to13000_GS_AK4SF_DataToMCSF_20151202_partial.root"

    dataFile="../SubmitData/chiNtuple_PFHT900.root"
    responseFile="response.root"

    ## get 2D reco hist to be Unfolded
    if doMC:
        Reco2d_Chi1=Get2DHist(dataFile,"dijet_mass1_chi1_" + WhichJets)
        Reco2d_Chi2=Get2DHist(dataFile,"dijet_mass1_chi2_" + WhichJets)
        Reco2d_Chi3=Get2DHist(dataFile,"dijet_mass1_chi3_" + WhichJets)
        Reco2d_Chi4=Get2DHist(dataFile,"dijet_mass1_chi4_" + WhichJets)

        Gen2d_Chi1=Get2DHist(dataFile,"dijet_mass1_chi1_" + "GEN")
        Gen2d_Chi2=Get2DHist(dataFile,"dijet_mass1_chi2_" + "GEN")
        Gen2d_Chi3=Get2DHist(dataFile,"dijet_mass1_chi3_" + "GEN")
        Gen2d_Chi4=Get2DHist(dataFile,"dijet_mass1_chi4_" + "GEN")

    else:
        ##Reco2d_Chi1=Get2DHist(dataFile,"dijet_m_chi_1")
        ##Reco2d_Chi2=Get2DHist(dataFile,"dijet_m_chi_2")
        ##Reco2d_Chi3=Get2DHist(dataFile,"dijet_m_chi_3")
        ##Reco2d_Chi4=Get2DHist(dataFile,"dijet_m_chi_4")        

        Reco2d_Chi1=Get2DHist(dataFile,"dijet_mass2_chi1")
        Reco2d_Chi2=Get2DHist(dataFile,"dijet_mass2_chi2")
        Reco2d_Chi3=Get2DHist(dataFile,"dijet_mass2_chi3")
        Reco2d_Chi4=Get2DHist(dataFile,"dijet_mass2_chi4")        


    ## get the Response matrix
    print "Response file: ",responseFile
    f = TFile.Open(responseFile)
    ## f.ls()
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


    Reco2d=Reco2d_Chi2
    print "CCLA: Reco2d ",Reco2d
    response=response_m2c2
    massBins=getMassBins(Reco2d)
    
    chiHists1d=[]; chiTests1d=[]; unfChiHists1d=[]
    for i in range(1,len(massBins)-1):
        minMass=int(massBins[i])
        maxMass=int(massBins[i+1])
        strMinM=str(int(minMass)); strMaxM=str(int(maxMass)); 
        if minMass<1900: continue

        chiHist="dijet_"+strMinM+"_"+strMaxM+"_chi"

        if doMC:
            chiHist="dijet_M1_"+strMinM+"_"+strMaxM+"_chi"
            chiHist=chiHist+WhichJets
            Gen2d=Gen2d_Chi1
            
        print i,chiHist, minMass,maxMass
        horg=GetHist(dataFile,chiHist)

        Reco2d=Reco2d_Chi1
        
        response=response_m2c1
        ##if strMinM == "4800":
        ##    Reco2d=Reco2d_Chi4
        ##    response=response_m2c4
        ##    chiBins4=[1,3,5,7,10,12,14,16]
        ##    horg=RebinHist(horg,chiBins4,False)

        chiHists1d.append(horg)
        ## fill this array with hists extracted from 2d hist.  Should be identical to those in chiHists1d
        chiTests1d.append(Proj2D_Y(Reco2d,minMass,maxMass,True))

        ## now do unfolding
        print "CCLA: Bayes Unfolding ",Reco2d,"using matix ",response
        NITER=7
        
        unfold2d = RooUnfoldBayes     (response, Reco2d, NITER)
        unfold2d.Print()
        
        hUnf2d= unfold2d.Hreco(2)
        if doMC:
            hUnf2d.PrintTable (cout, Gen2d, 2);
            
        print "XXX: ",hUnf2d
        hD=Proj2D_Y(hUnf2d,minMass,maxMass,True)

        h=TH1F()
        hD.Copy(h)  ## convert TH1D to TH1F
        unfChiHists1d.append(h)
        f.Close()

    # doPoisson(chiTests1d)
    # doPoisson(unfChiHists1d)

    if CheckProj:
        print chiHists1d
        print chiTests1d
        plotComparison(chiHists1d,chiTests1d,"Projection",True,doMC)


    if PlotUnfolded:  ## print UnfChiHists
        
        print chiTests1d
        print unfChiHists1d
        plotComparison(chiTests1d,unfChiHists1d,"Unfolded",True,doMC)


    ## now write out the unfolded histograms
    outname=os.path.basename(dataFile)
    outname=outname[:outname.find(".root")] 
    #if doMC:
    #    outname="mc_independent" + MCSAMPLE

    if WhichSmearing == "Smeared":
            outname="results/Unfolded_" +outname + "_from" + smearFunc + "_" +MCSAMPLE+".root"
    else:
        outname="results/Unfolded_" +outname + "_from" + WhichSmearing + "_" +MCSAMPLE+".root"

    print "\n\n%Response file: ",responseFile
    print "%Writing unfolded histograms to: ",outname
    
    outfile = TFile.Open(outname,"RECREATE")

    for i in range(len(unfChiHists1d)):
        hOrg=chiTests1d[i]
        hUnf=unfChiHists1d[i]
        orgname=hOrg.GetName()
        newname=orgname + "_unfolded"
        hUnf.SetName(newname)

        ##print i,orgname
        ##if i == 5:
        ##    print "Rebinning histogram ",orgname
        ##    newchiBins=[1,3,5,7,10,12,14,16]
        ##    hOrg=RebinHist(hOrg,newchiBins,False)

        hOrg.SetLineColor(ROOT.kRed)
        hOrg.Write()
        hUnf.Write()
    outfile.Close()

    ## print ROOT.TH1.kPoisson, ROOT.TH1.kPoisson2,ROOT.TH1.kNormal

#===============================================================
    if os.getenv("FROMGUI") == None:
        print "Not from GUI"
        # raw_input('\npress return to end the program...')
