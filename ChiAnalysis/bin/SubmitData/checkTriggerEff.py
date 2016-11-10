##from ROOT import gROOT, gStyle, gSystem, TCanvas, TF1, TFile, TH1F
##from ROOT import TColor, TLine, TLegend, TLatex, TObjArray
##from ROOT import SetOwnership
##
##from ROOT import gDirectory, gPad

from ROOT import *

import sys,string,math,os

# import myPyRootSettings
sys.path.append(os.path.join(os.environ.get("HOME"),'rootmacros'))
from myPyRootMacros import *

#################################################################################################

def SetContentsToZero(h,xmin,xmax):

    hnew=h.Clone()
    nbins= hnew.GetXaxis().GetNbins()
    for ibin in range(1,nbins+1):
        if ibin >= hnew.GetXaxis().FindBin(xmin+0.01) and ibin < hnew.GetXaxis().FindBin(xmax+0.01):
            # print ibin
            hnew.SetBinContent(ibin,0.0)
            hnew.SetBinError(ibin,0.0)
    
    return hnew

if __name__ == '__main__':

    SetStyle()

    RootDir="root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/Data/76x/"
    
    HistFile800=RootDir + "chiNtuple_PFHT800_20160530.root"
    HistFile650=RootDir + "chiNtuple_PFHT650_20160530.root"
    

    writePlot=True
    
    outfile="comp_PFHT650_PTHT800"

    xc0=1400
    cname="pT"
    c1,pad1,pad2=prep1by2Plot("c0","comp" ,xc0)    

    pad1.SetTopMargin(0.07);        
    pad2.SetBottomMargin(0.28);    
    lmargin=0.13    
    pad1.SetLeftMargin(lmargin);
    pad2.SetLeftMargin(lmargin);    
    pad1.Draw(); pad2.Draw()
        
    ## massBins=[1900,2400,3000,3600,4200,4800,13000]
    massBins=[1500,1900,2400]

    legs=[]
    for i in range(len(massBins)-1):

        minMass=massBins[i]
        maxMass=massBins[i+1]
        strMinM=str(int(minMass)); strMaxM=str(int(maxMass)); 
        mbin=strMinM + "_" +strMaxM
        
        hname="dijet_"+mbin+"_chi"
    
    
        h800   = Get1DHist(HistFile800,hname,False)
        h650   = Get1DHist(HistFile650,hname,False)
        
        SetHistColorAndMarker(h650,ROOT.kMagenta,20,.8)
        SetHistColorAndMarker(h800,ROOT.kBlue,20,.8)

        h800.Scale(1./h800.Integral())
        h650.Scale(1./h650.Integral())

        hRat= h800.Clone()

        hRat.SetName("Ratio")
        hRat.Divide(h800,h650,1.,1.,"");

        Hlist=TObjArray()
        Hlist.Add(hRat);

        pad1.cd()
        pad1.SetLogy(0);    

        h800.SetTitleSize(0.05, "Y" )        
        h800.SetTitleOffset(1.15, "Y");
        h650.SetTitleSize(0.05, "Y" )        
        h650.SetTitleOffset(1.15, "Y");
        h800.SetMaximum(0.12)        
        h800.GetYaxis().SetTitle("1/N dN/d#chi")
        ## hPythia.Draw()
        h800.Draw("")
        h650.Draw("same")

        #cname="Ratio"
        #c2 = prepPlot("c2",cname,750,120,500,500)
        #c2.SetLogy(0);

        xl1=.55; yl1=0.65; xl2=xl1+.32; yl2=yl1+.15;
        leg=PrepLegend(xl1,yl1,xl2,yl2,.038,ROOT.kWhite)    

        leg.AddEntry(h800,"PFHT800 - Corrected","lp");
        leg.AddEntry(h650,"PTHT650","lp");        
        leg.Draw()
        legs.append(leg)

        txtsize=0.04
        dy=0.06; dyl=0.1
        
        xlabel=0.75; ylabel=0.83
        ## DrawText(xlabel,ylabel,"#sqrt{s} = 13 TeV",txtsize,22)
        ## ylabel=ylabel-dy
        massBin=str(minMass) + " < M_{jj} [GeV] < " + str(maxMass)
        if str(maxMass) == "13000":
            massBin="M_{jj} > " + str(minMass) + " GeV"
        DrawText(xlabel,ylabel,massBin,txtsize,22)
        
        pad2.cd()

        ## hRat.GetYaxis().SetTitle("PFHT800/PFHT650")
        hRat.GetYaxis().SetTitle("Ratio")
        hRat.GetXaxis().SetTitle("#chi")    
        ResetAxisAndLabelSizes(hRat,0.08,0.012)
        hRat.SetTitleSize(0.11, "X" )    
        hRat.SetTitleOffset(1.15, "X");    

        hRat.SetTitleSize(0.11, "Y" )        
        hRat.SetTitleOffset(0.5, "Y");    
        hRat.GetYaxis().SetNdivisions(505)

        ymin=0.7; ymax=1.3

        hRat.SetMaximum(ymax)
        hRat.SetMinimum(ymin)
        hRat.Draw()

        l=TLine(1.,1.,16.,1.)
        l.SetLineWidth(2)
        l.SetLineStyle(2)
        l.Draw()

        c1.Update()
        if writePlot:
            outf=outfile+ "_" + str(minMass) + "_M_" + str(maxMass) + ".gif"
            print "Output written to: ",outf
            c1.Print(outf)

        raw_input('\npress return to end the program...')
            
    # f2=TFile(OutFile,"RECREATE")
    # f2.cd()
    # hRatP.Write()
    # f2.Close()
