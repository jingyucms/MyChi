import ROOT
from ROOT import *

import sys,string,math,os

# import myPyRootSettings
sys.path.append(os.path.join(os.environ.get("HOME"),'rootmacros'))
from myPyRootMacros import prepPlot,SetStyle, GetHist, PrepLegend, DrawText

if __name__ == '__main__':

    SetStyle()
    ## gStyle.SetOptStat(110);
    gStyle.SetOptStat(0);    


    RootDir="root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/Data/76x/"
    
    HistFile1=RootDir + "chiNtuple_PFHT800_20160530.root"
    HistFile2=RootDir + "chiNtuple_PFHT650_20160530.root"

    f1 = TFile.Open(HistFile1)
    f2 = TFile.Open(HistFile2)
    # f2.ls()
    # f1.cd("pf")

    hname="dijet_1500_1900_chi"
    hNum = f1.Get(hname)
    hDen = f2.Get(hname)

    norm1=hNum.Integral();
    norm2=hDen.Integral();
    print norm1, norm2

    hNum.Scale(1./norm1)
    hDen.Scale(1./norm2)
    hRat= hNum.Clone()
    hRat.SetName("Ratio")
    hRat.Divide(hNum,hDen,1.,1.,"");
    Hlist=TObjArray()
    Hlist.Add(hRat);

    cname="pT"
    c1 = prepPlot("c1",cname,300,20,500,500)
    c1.SetLogy(0);    

    # i1=90; i2=110
    # i1=0; i2=500
    # hNum.GetXaxis().SetRange(i1,i2)
    hDen.SetLineColor(ROOT.kRed)
    hNum.SetMaximum(.11)
    hNum.Draw()
    hDen.Draw("same")

    cname="Ratio"
    c2 = prepPlot("c2",cname,750,120,500,500)
    c2.SetLogy(0);    

    min=0.; max=1.24

    hRat.SetMaximum(1.24)
    hRat.SetMinimum(0.5)
    hRat.Draw()


    # f2=TFile(OutFile,"RECREATE")
    # f2.cd()
    # hRat.Write()
    # f2.Close()


    raw_input('\npress return to end the program...')
