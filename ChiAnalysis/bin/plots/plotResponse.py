from ROOT import gROOT, gStyle, gSystem, TCanvas, TF1, TFile, TH1F, TH3F, TColor, TLine, TLegend, TLatex, SetOwnership
import sys,string,math,os,ROOT

sys.path.append(os.path.join(os.environ.get("HOME"),'rootmacros'))
from myPyRootMacros import prepPlot,GetHist,Get3DHist,SetHistColorAndMarker, Proj3D_Z, SetStyle

######################################################################################################

## SavePlots=False
SavePlots=True

wExtraSmearing=False
## wExtraSmearing=True

## infile1="../SubmitMC/chiNtuple_Pt_170to13000_CB2_tst.root"
## infile1="../SubmitMC/chiNtuple_Pt_170to13000_GS_test_func.root"
## infile2="../SubmitMC/chiNtuple_Pt_170to13000_CB2_0_rescaled.root"

if wExtraSmearing:
    # infile1="root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC/chiNtuple_Pt_170to13000_CB2_0_wExtraSmearing.root"
    # infile2="root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC/chiNtuple_Pt_170to13000_GS_0_wExtraSmearing.root"
    infile1="root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC/chiNtuple_Pt_170to13000_CB2_AK4SF.root"
    infile2="root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC/chiNtuple_Pt_170to13000_GS_AK4SF.root"    
else:
    infile1="root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC/chiNtuple_Pt_170to13000_CB2.root"
    infile2="root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC/chiNtuple_Pt_170to13000_GS.root"
    
## rapidity limits
ymin=-2.5; ymax=2.5
## ymin=2.; ymax=3.
## ymin=-3; ymax=-2.
## ymin=-2; ymax=2

## ptbins
## ptBins=[[300,400],[400,500],[500,600],[600,700],[700,800],[800,1000],[1200,1400],[1700,2000],[2000,2500]]
ptBins=[[400,500],[500,600],[800,1000],[1200,1400],[1700,2000],[2000,2500]]
## ptBins=[[600,700],[700,800]]
## ptBins=[[400,500]]
######################################################################################################

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

def drawIt(h1,h2,h3,ptmin,ptmax):

    scl1=h1.Integral();
    scl2=h2.Integral();
    scl3=h3.Integral();
    if scl1>0: h1.Scale(1./scl1)
    if scl2>0: h2.Scale(1./scl2)
    if scl3>0: h3.Scale(1./scl3)

    ## h1.SetMinimum(1.1e-6)
    
    SetHistColorAndMarker(h1,ROOT.kBlue,20)
    SetHistColorAndMarker(h2,ROOT.kRed,20)
    SetHistColorAndMarker(h3,ROOT.kMagenta,20)

    h1.GetXaxis().SetTitle("Response")
    h1.SetMinimum(2.e-6)
    fName="GFit"
    fitfunc="gaus"
    h1fit = TF1(fName,fitfunc,1.,1.5);
    h1fit.SetParameter(0, 1)
    h1fit.SetParameter(1, 1)
    h1fit.SetParameter(2, .1)

    h2fit=h1fit.Clone()
    h3fit=h1fit.Clone()

    h1fit.SetLineColor(h1.GetLineColor())
    h2fit.SetLineColor(h2.GetLineColor())
    h3fit.SetLineColor(h3.GetLineColor())

    c1 = prepPlot("c0","c0",700,20,500,500)
    c1.SetLogy(1)
    
    h1.Draw()
    h2.Draw("same")
    ## h3.Scale(0.8)
    h3.Draw("same")

    h1.Fit(h1fit,"0R");    
    # h1fit.Draw("sames")
    h2.Fit(h2fit,"0R");    
    # h2fit.Draw("sames")
    h3.Fit(h3fit,"0R");    
    # h3fit.Draw("sames")

    
    print "XXX: ",h1.GetTitle(), h2.GetTitle()
    label=h1.GetTitle()

    ## h1overFlow=(h1.GetBinContent(h1.GetNbinsX()+1)/h1.Integral(1,h1.GetNbinsX()+1)) * 100
    ## h2overFlow=(h2.GetBinContent(h2.GetNbinsX()+1)/h2.Integral(1,h2.GetNbinsX()+1)) * 100
    ## h3overFlow=(h3.GetBinContent(h3.GetNbinsX()+1)/h3.Integral(1,h2.GetNbinsX()+1)) * 100
    ## # print h1overFlow,h2overFlow,h3overFlow
    ## # print h1.GetEntries(),h2.GetEntries(),h3.GetEntries()
    ## 
    ## # print h1.GetEntries(),h1.Integral(),h1.Integral(1,h1.GetNbinsX()),h1.Integral(1,h1.GetNbinsX()+1)
    ## # print h2.GetEntries(),h2.Integral(),h2.Integral(1,h2.GetNbinsX()),h2.Integral(1,h2.GetNbinsX()+1)
    ## # print h2.Integral(1,h2.GetNbinsX()+1) -h2.Integral(1,h2.GetNbinsX())
    ## 
    ## print "Reco underflows/overflows: ",h1.GetBinContent(h1.GetNbinsX()+1),h1overFlow
    ## print "CB underflows/overflows: ",  h2.GetBinContent(h2.GetNbinsX()+1),h2overFlow
    ## print "GS underflows/overflows: ",  h3.GetBinContent(h3.GetNbinsX()+1),h3overFlow
    ## print

    xl1=.15; yl1=0.75; xl2=xl1+.28; yl2=yl1+.15;
    leg =TLegend(xl1,yl1,xl2,yl2);
    leg.SetFillColor(0);
    leg.SetLineColor(0);
    leg.SetShadowColor(0);
    leg.SetTextSize(0.038)
    
    leg.AddEntry(h1,"Full Sim","lp");
    leg.AddEntry(h2,"Crystal Ball","lp");
    leg.AddEntry(h3,"Gaussian","lp");

    leg.Draw()
    
    t1 = TLatex();
    t1.SetNDC();
    txtsize=0.038;  t1.SetTextSize(txtsize); t1.SetTextAlign(22);

    if ymin == -ymax:
        leglabel2="|y| < " + str(ymax)
    else:
        leglabel2= str(ymin) + " < y < " + str(ymax)
    xtxt=.785; ytxt=.885;
    t1.DrawLatex(xtxt,ytxt,label);
    t1.DrawLatex(xtxt,ytxt-0.06,leglabel2);

    c1.Modified()    
    c1.Update()
    
    if SavePlots:
        outfile="SmearedResponse_" + str(int(ptmin)) + "pT" + str(int(ptmax))
        if wExtraSmearing:
            outfile=outfile + "_wExtraSmearing"
        outfile=outfile + ".pdf"
        c1.Print(outfile)
    
    return

#===============================================================


if __name__ == '__main__':


    SetStyle()
    
#===============================================================

    print "INFILE1: ",infile1
    print "INFILE2: ",infile2
    
    reco_3d=Get3DHist(infile1,"Resp3D")
    sCB_3d =Get3DHist(infile1,"SmrResp3D")
    sGS_3d =Get3DHist(infile2,"SmrResp3D")
    
    for ptBin in ptBins:

        ptmin=ptBin[0]
        ptmax=ptBin[1]
            
        reco0=Proj3D_Z(reco_3d,ptmin,ptmax,ymin,ymax)
        sCB_0=Proj3D_Z(sCB_3d, ptmin,ptmax,ymin,ymax)
        sGS_0=Proj3D_Z(sGS_3d, ptmin,ptmax,ymin,ymax)
    
        reco0.SetTitle(str(int(ptmin)) + " < p_{T} < " + str(int(ptmax)) + " GeV")    
        reco0.GetXaxis().SetRangeUser(0.,2.)
        ## reco0.GetXaxis().SetRangeUser(0.9,1.5)        
    
        print reco0.GetEntries(),sCB_0.GetEntries(),sGS_0.GetEntries()

        drawIt(reco0,sCB_0,sGS_0,ptmin,ptmax)

        ans = raw_input('\npress return to continue, q to quit...')
        if ans == 'q':
            sys.exit()
    

#===============================================================
    if os.getenv("FROMGUI") == None:
        print "Not from GUI"
        raw_input('\npress return to end the program...')
