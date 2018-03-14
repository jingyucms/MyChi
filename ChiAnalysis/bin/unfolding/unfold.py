from ROOT import gROOT, gStyle, gSystem, TCanvas, TF1, TFile, TH1F, TColor, TLine, TLegend, TLatex, SetOwnership, gDirectory, TH1
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

compToGen=False  # compare Unfolded SMR MC to Gen MC, use when do closure test
#compToGen=True

saveSMR=False  # use when you want to save smr mc distribution in output root file
#saveSMR=True

suffix=".gif"

DAgostini=False

if DAgostini==False:
    outDir="results_MatrixInvert"
else:
    NITER=4
    outDir="results_Iter"+str(int(NITER))

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

    dataFile="root://cmseos.fnal.gov//store/user/jingyu/jetUnfold/DataNtuple/chiNtuple_dataReReco_v3_PFHT900.root"

    responseFile="ResponseMatrices/Response_"+MCSAMPLE+"_" +smearFunc + "_" +date +".root"
    #responseFile="ResponseMatrices/Response_madgraphMLM_HT_300toInf_CB_AK4SF_20161214.root"
    #responseFile="../ResponseMatrices/Response_"+MCSAMPLE+"_" +smearFunc + "_" +date +"_Train.root"
    #responseFile="ResponseMatrices/Response_pythia8_Pt_170toInf_CB_AK4SF_Test_20161214_Test.root"
    
    if doMC:
        #dataFile="ResponseMatrices/Response_madgraphMLM_HT_300toInf_CB_AK4SF_20161214.root"
        #dataFile="ResponseMatrices/Response_pythia8_Pt_170toInf_CB_AK4SF_20161202.root"

        #dataFile="ResponseMatrices/Response_"+MCSAMPLE+"_" +smearFunc + "_" +date +".root"
        #dataFile="ResponseMatrices/Response_"+MCSAMPLE+"_" +smearFunc + "_Test_" +date +"_Test.root"
        #responseFile="ResponseMatrices/Response_"+MCSAMPLE+"_" +smearFunc + "_Train_" +date +"_Train.root"
        dataFile="ResponseMatrices/Response_madgraphMLM_HT_300toInf_CB_AK4SF_20170206.root"
        #dataFile="ResponseMatrices/Response_herwigpp_Pt_170toInf_CB_AK4SF_20170201.root"

    ## get 2D reco hist to be Unfolded
    if doMC:
        
        Reco2d_Chi1=Get2DHist(dataFile,"dijet_mass2_chi1_" + WhichJets)
        Reco2d_Chi2=Get2DHist(dataFile,"dijet_mass2_chi2_" + WhichJets)
        Reco2d_Chi3=Get2DHist(dataFile,"dijet_mass2_chi3_" + WhichJets)
        Reco2d_Chi4=Get2DHist(dataFile,"dijet_mass2_chi4_" + WhichJets)

        Gen2d_Chi1=Get2DHist(dataFile,"dijet_mass2_chi1_" + "GEN")
        Gen2d_Chi2=Get2DHist(dataFile,"dijet_mass2_chi2_" + "GEN")
        Gen2d_Chi3=Get2DHist(dataFile,"dijet_mass2_chi3_" + "GEN")
        Gen2d_Chi4=Get2DHist(dataFile,"dijet_mass2_chi4_" + "GEN")

    else:

        Reco2d_Chi1=Get2DHist(dataFile,"dijet_mass2_chi1")
        Reco2d_Chi2=Get2DHist(dataFile,"dijet_mass2_chi2")
        Reco2d_Chi3=Get2DHist(dataFile,"dijet_mass2_chi3")
        Reco2d_Chi4=Get2DHist(dataFile,"dijet_mass2_chi4")        

        Gen2d_Chi1=Get2DHist(responseFile,"dijet_mass2_chi1_" + "GEN")
        Gen2d_Chi2=Get2DHist(responseFile,"dijet_mass2_chi2_" + "GEN")
        Gen2d_Chi3=Get2DHist(responseFile,"dijet_mass2_chi3_" + "GEN")
        Gen2d_Chi4=Get2DHist(responseFile,"dijet_mass2_chi4_" + "GEN")
        
        
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


    Reco2d=Reco2d_Chi1
    print "CCLA: Reco2d ",Reco2d
    response=response_m2c1
    massBins=getMassBins(Reco2d)
    
    chiHists1d=[]; chiTests1d=[]; unfChiHists1d=[]; covMatrix=[]; new_hists=[]
    for i in range(1,len(massBins)-1):
        minMass=int(massBins[i])
        maxMass=int(massBins[i+1])
        strMinM=str(int(minMass)); strMaxM=str(int(maxMass)); 
        if minMass<2400: continue

        chiHist="dijet_"+strMinM+"_"+strMaxM+"_chi"

        if doMC:
            
            chiHist="dijet_M2_"+strMinM+"_"+strMaxM+"_chi"
            chiHist=chiHist+WhichJets
        #chiHist=chiHist+'GEN'
        if minMass<4800:
            Gen2d=Gen2d_Chi1
        elif minMass<6000:
            #Gen2d=Gen2d_Chi2
            Gen2d=Gen2d_Chi2
        else:
            #Gen2d=Gen2d_Chi3
            Gen2d=Gen2d_Chi3
            
        print i,chiHist, minMass,maxMass
        horg=GetHist(dataFile,chiHist)

        #horg=reBin(horg)

        if minMass<4800:
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

        if not saveSMR:
            chiHists1d.append(horg)
        else:
            chiHists1d.append(Proj2D_Y(Reco2d,minMass,maxMass,Reco2d.GetName(),True))
        
        if compToGen:
            chiTests1d.append(Proj2D_Y(Gen2d,minMass,maxMass,Gen2d.GetName(),True))
        else:
            chiTests1d.append(Proj2D_Y(Reco2d,minMass,maxMass,Reco2d.GetName(),True))

        ## now do unfolding
        print "CCLA: Unfolding ",Reco2d,"using matix ",response

        if DAgostini == True:
            unfold2d = RooUnfoldBayes     (response, Reco2d, NITER)
        else: 
            unfold2d = RooUnfoldInvert    (response, Reco2d)
            
        unfold2d.Print()

        new_hists.append(unfold2d)

        unfold2d.SetNToys(30000)
        
        hUnf2d = unfold2d.Hreco(2)

        hErr2d = unfold2d.Ereco(2)   

        #chi2 = RooUnfold.Chi2 (unfold2d,2)
        chi2comp=Proj2D_Y(Gen2d,minMass,maxMass,Gen2d.GetName(),True)
        hraw=Proj2D_Y(Reco2d,minMass,maxMass,Gen2d.GetName(),True)
        hUnf1d=Proj2D_Y(hUnf2d,minMass,maxMass,Gen2d.GetName(),True)
        print "------",hraw.Integral(), hUnf1d.Integral(),hUnf2d.Integral(), chi2comp.Integral()
        chi2comp.Scale(hUnf1d.Integral()/chi2comp.Integral())
        #chi2 = unfold2d.Chi2 (hUnf1d,2)
        chi2 = hUnf2d.Chi2 (hUnf1d,2)
        print "---chi square:",chi2

        covMatrix.append(hErr2d)
            
        print "XXX: ",hUnf2d
        hD=Proj2D_Y(hUnf2d,minMass,maxMass,hUnf2d.GetName(),True)

        h=TH1F()
        hD.Copy(h)  ## convert TH1D to TH1F
        unfChiHists1d.append(h)
        f.Close()

    if CheckProj:
        print chiHists1d
        print chiTests1d
        plotComparison(chiHists1d,chiTests1d,"Projection",True,doMC)


    if PlotUnfolded:  ## print UnfChiHists
        
        print chiTests1d
        print unfChiHists1d
        if PlotUnfoldedAndFit:
            compAndDrawIt(chiTests1d,unfChiHists1d)
        else:
            plotComparison(chiTests1d,unfChiHists1d,"Unfolded",True,doMC)


    ## now write out the unfolded histograms
    outname=os.path.basename(dataFile)
    outname=outname[:outname.find(".root")] 

    if WhichSmearing == "Smeared":
        outname=outDir+"/Unfolded_" +outname + "_from" + smearFunc + "_" +MCSAMPLE+".root"
    else:
        outname=outDir+"/Unfolded_" +outname + "_from" + WhichSmearing + "_" +MCSAMPLE+".root"

    print "\n\n%Response file: ",responseFile
    print "%Writing unfolded histograms to: ",outname
    
    outfile = TFile.Open(outname,"RECREATE")

    for i in range(len(unfChiHists1d)):
        hOrg=chiTests1d[i]
        hUnf=unfChiHists1d[i]
        if saveSMR:
            hSmr=chiHists1d[i]
        orgname=hOrg.GetName()
        newname=orgname + "_unfolded"
        hUnf.SetName(newname)
        
        hErr=covMatrix[i]


        hOrg.SetLineColor(ROOT.kRed)
        hOrg.Write()
        hUnf.Write()
        hErr.Write()
        if saveSMR:
            hSmr.Write()
        
    outfile.Close()

    ## print ROOT.TH1.kPoisson, ROOT.TH1.kPoisson2,ROOT.TH1.kNormal

#===============================================================
    if os.getenv("FROMGUI") == None:
        print "Not from GUI"
        # raw_input('\npress return to end the program...')
