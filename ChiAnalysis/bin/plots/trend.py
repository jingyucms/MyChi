from ROOT import gROOT, gStyle, gSystem, TCanvas, TF1, TFile, TH1F, TH3F, TColor, TLine, TLegend, TLatex, SetOwnership, TGraphErrors
import sys,string,math,os,ROOT

sys.path.append(os.path.join(os.environ.get("HOME"),'rootmacros'))
from myPyRootMacros import prepPlot,GetHist,Get3DHist,SetHistColorAndMarker, Proj3D_Z, SetStyle
from array import array

######################################################################################################

## infile1="../SubmitMC/chiNtuple_Pt_170to13000_CB2_tst.root"
infile1="../SubmitMC/chiNtuple_Pt_170to13000_GS_test_0.1.root"
infile2="root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC/chiNtuple_Pt_170to13000_GS.root"
## infile2="../SubmitMC/chiNtuple_Pt_170to13000_CB2_0_rescaled.root"

## rapidity limits
ymin=-2.5; ymax=2.5

## ptbins
ptBins=[[300,400],[400,500],[600,700],[700,800],[800,1000],[1200,1400],[1700,2000]]

######################################################################################################
if __name__ == '__main__':


    SetStyle()
    
#===============================================================

    x, y , ex, ey = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
    
    for ptBin in ptBins:

        ptmin=ptBin[0]
        ptmax=ptBin[1]
        pt=(ptmax+ptmin)/2.
        x.append(pt)
        ex.append(0)
        ey.append(0.1)
        
    c1 = prepPlot("c0","c0",700,20,500,500)
    c1.SetLogy(False)

    y.append(1.08)
    y.append(1.1)
    y.append(1.15)
    y.append(1.2)
    y.append(1.2)
    y.append(1.22)
    y.append(1.22)

    n=len(x)
    gr0 = TGraphErrors(n,x,y,ex,ey);

    gr0.SetMarkerColor(ROOT.kBlue)
    gr0.SetMarkerStyle(20)
    gr0.SetLineColor(ROOT.kBlue)
    gr0.SetMarkerSize(1.5)

    gr0.Draw();
    p1 = TF1("pol1","pol1",200,900.);
    # p1 = TF1("pol2","pol2",200,2000.);

    p1.SetLineColor(ROOT.kMagenta)

    f1 = TF1("f1","[0] +[1]*x",200,2000);
    f1.SetParameters(0.99601,0.00241919);
    f1.SetLineColor(ROOT.kBlue)
        
    gr0.Fit(p1,"0R");
    p1.Draw("sames")
    f1.Draw("sames")
    
    c1.Modified()
    c1.Update()    
    
    
#===============================================================
    if os.getenv("FROMGUI") == None:
        print "Not from GUI"
        raw_input('\npress return to end the program...')
