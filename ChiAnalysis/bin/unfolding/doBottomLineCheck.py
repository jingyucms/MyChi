import os, sys,array,math
import ROOT
from ROOT import *

sys.path.append('/uscms_data/d3/jingyu/ChiAnalysis/jetUnfold/CMSSW_8_0_23/src/MyChi/ChiAnalysis/bin/unfolding/')
sys.path.append('/uscms_data/d3/jingyu/ChiAnalysis/jetUnfold/CMSSW_8_0_23/src/MyChi/ChiAnalysis/bin/unfolding/rootmacros')
from myPyRootMacros import *
from scripts import plotComparison, doPoisson, getMassBins, compAndDrawIt

#chi_binning=array.array('d',[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])

#outDir="./results_MatrixInvert/"
outDir="./results_Iter2/"

def drawUncert(h1,h2,massbin,chi_binning):

    SetStyle()

    canvas=TCanvas("myCanvas","myCanvas",0,0,500,500)
    gPad.SetTicky(1)
    gPad.SetTickx(1)

    print h1.GetNbinsX(),h2.GetNbinsX()
    
    raw=TH1F("raw data statistical error","raw data statistical error",len(chi_binning)-1,chi_binning)
    unfolded=TH1F("unfolded data statistical error","raw data statistical error",len(chi_binning)-1,chi_binning)

    for b in range(1,len(chi_binning)):
        
        raw.SetBinContent(b,h1.GetBinError(b)/h1.GetBinContent(b))
        unfolded.SetBinContent(b,h2.GetBinError(b)/h2.GetBinContent(b))

        #raw.SetBinContent(b,h1.GetBinError(b))
        #unfolded.SetBinContent(b,h2.GetBinError(b))
        #raw.SetBinContent(b,1./math.sqrt(h1.GetBinContent(b)))
        #unfolded.SetBinContent(b,1./math.sqrt(h2.GetBinContent(b)))

    raw.GetYaxis().SetTitle("Fractional Statistic Error")
    raw.GetYaxis().SetTitleOffset(0.6)
    raw.GetYaxis().SetLabelSize(0.04)
    raw.GetYaxis().SetNdivisions(503)
    
    raw.SetLineColor(9)
    raw.SetLineStyle(1)
    unfolded.SetLineColor(8)
    unfolded.SetLineStyle(1)

    max=unfolded.GetMaximum()

    raw.SetMaximum(max*1.5)
    raw.SetMinimum(0)

    raw.Draw("hist")
    unfolded.Draw("samehist")

    if massbin==[6000,13000]:
        xl1=.35; yl1=0.25; xl2=xl1+.28; yl2=yl1+.2;
    else:
        xl1=.3; yl1=0.15; xl2=xl1+.28; yl2=yl1+.2;
    #leg =TLegend(xl1,yl1,xl2,yl2,str(massbin[0])+" < m_{jj} < "+str(massbin[1]));
    leg =TLegend(xl1,yl1,xl2,yl2)
    leg.SetFillColor(0);
    leg.SetLineColor(0);
    leg.SetShadowColor(0);
    leg.SetTextSize(0.05)

    leg.AddEntry(raw,"Raw Data","l")
    leg.AddEntry(unfolded,"Unfolded Data","l")

    leg.Draw()

    t1 = TLatex();
    t1.SetNDC();
    txtsize=0.05;  t1.SetTextSize(txtsize); t1.SetTextAlign(22);
    xtxt=.5; ytxt=.75;
    t1.DrawLatex(xtxt,ytxt,str(massbin[0])+" < m_{jj} < "+str(massbin[1]));
    
    outfile="Statistical_Uncert_"+str(massbin[0])+"_"+str(massbin[1])

    canvas.Print(outDir+outfile + ".gif")
    canvas.Print(outDir+outfile + ".pdf")

    ans = raw_input('\npress return to continue, q to quit...')
    if ans == 'q':
        sys.exit()
    
    return

def calcChiSquare(h1,h2,chi_binning):

    #h1.Scale(1./h1.Integral())
    #rh1=h1.Rebin(len(chi_binning)-1,h1.GetName()+"_rebin",chi_binning)
    #rh2=h2.Rebin(len(chi_binning)-1,h2.GetName()+"_rebin",chi_binning)
    h2.Scale(h1.Integral()/h2.Integral())

    #print "===========",h1.Integral(),h2.Integral()
    
    chi2=0
    #print len(chi_binning)
    #print h1.GetNbinsX()
    for b in range(1,len(chi_binning)):
        #if b==1:
        #    print h1.GetBinContent(b),h1.GetBinError(b),h2.GetBinContent(b)
        chi2+=((h1.GetBinContent(b)-h2.GetBinContent(b))/h1.GetBinError(b))**2
        #chi2+=(h1.GetBinContent(b)-h2.GetBinContent(b))**2/h1.GetBinContent(b)
    
    return chi2

if __name__ == '__main__':
    
    file1=TFile(outDir+"Unfolded_chiNtuple_dataReReco_v3_PFHT900_fromCB_AK4SF_pythia8_Pt_170toInf.root")
    #file1=TFile(outDir+"Unfolded_chiNtuple_PFHT800_20160530_fromCB_AK4SF_DataToMCSF_Pythia_M_1000toInf.root")
    file2=TFile(outDir+"Unfolded_Response_pythia8_Pt_170toInf_CB_AK4SF_20170130_fromCB_AK4SF_pythia8_Pt_170toInf.root")
    #file2=TFile(outDir+"Unfolded_Response_herwigpp_Pt_170toInf_CB_AK4SF_20170201_fromCB_AK4SF_pythia8_Pt_170toInf.root")
    #file2=TFile(outDir+"Unfolded_Response_madgraphMLM_HT_300toInf_CB_AK4SF_20170206_fromCB_AK4SF_pythia8_Pt_170toInf.root")

    print file2

    massbins=[[2400,3000],[3000,3600],[3600,4200],[4200,4800],[4800,5400],[5400,6000],[6000,13000]]
    #massbins=[[1900,2400],[2400,3000],[3000,3600],[3600,4200],[4200,4800],[4800,13000]]

    for i in range(1,8):

        if i<=4:
            data_raw=file1.Get("dijet_mass2_chi1;"+str(i))
            data_unfolded=file1.Get("dijet_mass2_chi1_unfolded;"+str(i))
            chi_binning=array.array('d',[1,2,3,4,5,6,7,8,9,10,12,14,16])
            data_raw_rebin=data_raw.Rebin(len(chi_binning)-1,data_raw.GetName()+"_rebin",chi_binning)
            data_unfolded_rebin=data_unfolded.Rebin(len(chi_binning)-1,data_unfolded.GetName()+"_rebin",chi_binning)
        elif i<=6:
            data_raw=file1.Get("dijet_mass2_chi2;"+str(i-4))
            data_unfolded=file1.Get("dijet_mass2_chi2_unfolded;"+str(i-4))
            chi_binning=array.array('d',[1,2,3,4,5,6,7,8,9,10,12,14,16])
            data_raw_rebin=data_raw.Rebin(len(chi_binning)-1,data_raw.GetName()+"_rebin",chi_binning)
            data_unfolded_rebin=data_unfolded.Rebin(len(chi_binning)-1,data_unfolded.GetName()+"_rebin",chi_binning)
        else:
            data_raw=file1.Get("dijet_mass2_chi3;1")
            data_unfolded=file1.Get("dijet_mass2_chi3_unfolded;1")
            chi_binning=array.array('d',[1,3,6,9,12,16])
            data_raw_rebin=data_raw.Rebin(len(chi_binning)-1,data_raw.GetName()+"_rebin",chi_binning)
            data_unfolded_rebin=data_unfolded.Rebin(len(chi_binning)-1,data_unfolded.GetName()+"_rebin",chi_binning)

        #data_raw=file1.Get("dijet_mass1_chi2__projY_"+str(float(massbins[i-1][0]))+"-"+str(float(massbins[i-1][1])))
        #data_unfolded=file1.Get("dijet_mass1_chi2__projY_"+str(float(massbins[i-1][0]))+"-"+str(float(massbins[i-1][1]))+"_unfolded")

        if i<=4:
            smr_mc=file2.Get("dijet_mass2_chi1_SMR;"+str(i))
            gen_mc=file2.Get("dijet_mass2_chi1_GEN;"+str(i))
            chi_binning=array.array('d',[1,2,3,4,5,6,7,8,9,10,12,14,16])
            smr_mc_rebin=smr_mc.Rebin(len(chi_binning)-1,smr_mc.GetName()+"_rebin",chi_binning)
            gen_mc_rebin=gen_mc.Rebin(len(chi_binning)-1,gen_mc.GetName()+"_rebin",chi_binning)
        elif i<=6:
            smr_mc=file2.Get("dijet_mass2_chi2_SMR;"+str(i-4))
            gen_mc=file2.Get("dijet_mass2_chi2_GEN;"+str(i-4))
            chi_binning=array.array('d',[1,2,3,4,5,6,7,8,9,10,12,14,16])
            smr_mc_rebin=smr_mc.Rebin(len(chi_binning)-1,smr_mc.GetName()+"_rebin",chi_binning)
            gen_mc_rebin=gen_mc.Rebin(len(chi_binning)-1,gen_mc.GetName()+"_rebin",chi_binning)   
        else:
            smr_mc=file2.Get("dijet_mass2_chi3_SMR;1")
            gen_mc=file2.Get("dijet_mass2_chi3_GEN;1")
            chi_binning=array.array('d',[1,3,6,9,12,16])
            smr_mc_rebin=smr_mc.Rebin(len(chi_binning)-1,smr_mc.GetName()+"_rebin",chi_binning)
            gen_mc_rebin=gen_mc.Rebin(len(chi_binning)-1,gen_mc.GetName()+"_rebin",chi_binning)

        #chi_binning=array.array('d',[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        #drawUncert(data_raw_rebin,data_unfolded_rebin,massbins[i-1],chi_binning)
        #drawUncert(data_raw,data_unfolded,massbins[i-1],chi_binning)

        #chi_binning=array.array('d',[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        
        chismear=calcChiSquare(data_raw_rebin,smr_mc_rebin,chi_binning)
        chiunfold=calcChiSquare(data_unfolded_rebin,gen_mc_rebin,chi_binning)

        print str(massbins[i-1][0])+" < m_{jj} < "+str(massbins[i-1][1]), chiunfold,chismear
        
