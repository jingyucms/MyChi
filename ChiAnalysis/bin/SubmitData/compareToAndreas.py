from ROOT import *
import sys,string,math,os,ROOT

sys.path.append(os.path.join(os.environ.get("HOME"),'rootmacros'))
from myPyRootMacros import SetStyle, prepPlot, RebinHist, Get1DHist

## chiBin=["1900_2400"]
## chiBins=["4200_4800"]
chiBins=["1900_2400", "2400_3000", "3000_3600", "3600_4200", "4200_4800", "4800_5400", "5400_6000", "6000_13000"]

## --------------------------------------------------------------------------- ##

def getBinLimits(h):

    theBins=[]
    nbins=h.GetNbinsX()
    for ibin in range(1,nbins+1):
        xlow=h.GetXaxis().GetBinLowEdge(ibin)
        theBins.append(xlow)
        if ibin == nbins:
            w=h.GetXaxis().GetBinWidth(ibin)
            theBins.append(xlow+w)
        # print ibin,xlow
        
    return theBins

if __name__ == '__main__':

    SetStyle()

    HistFile1="./chiNtuple_PFHT900.root"
    HistFile2="./datacard_shapelimit13TeV_JetHT_25ns_data_2016AllPromptReco_v1.root"

    for chiBin in chiBins:

        hname1="dijet_"+chiBin+"_chi"
        hname2="datacard_shapelimit13TeV_#chi"+chiBin+"_rebin1"

        htmp=Get1DHist(HistFile1,hname1)
        hDen=Get1DHist(HistFile2,hname2)

        theBins=getBinLimits(hDen)

        hNum=RebinHist(htmp,theBins,False)
        # print theBins

        intNum=hNum.Integral();
        intDen=hDen.Integral();
        hNum.Scale(intDen/intNum)

        hRat= hNum.Clone()
        hRat.SetName("Ratio")
        hRat.Divide(hNum,hDen,1.,1.,"");
        Hlist=TObjArray()
        Hlist.Add(hRat);

        cname="pT"
        c1 = prepPlot("c1",cname,300,20,500,500)
        c1.SetLogy(False);    

        # i1=90; i2=110
        i1=0; i2=500
        hNum.GetXaxis().SetRange(i1,i2)
        hDen.SetLineColor(ROOT.kRed)
        hNum.Draw()
        hDen.Draw("same")

        c1.Update()
        cname="Ratio"
        c2 = prepPlot("c2",cname,750,120,500,500)
        c2.SetLogy(0);    

        min=0.; max=1.24

        hRat.SetMaximum(1.24)
        hRat.SetMinimum(0.0)
        hRat.Draw()
        c2.Update()

        # f2=TFile(OutFile,"RECREATE")
        # f2.cd()
        # hRat.Write()
        # f2.Close()

        print "\nChiBin: ",chiBin
        raw_input('\npress return to end the program...')
