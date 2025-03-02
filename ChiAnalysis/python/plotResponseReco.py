from ROOT import gROOT, gStyle, gSystem, TCanvas, TF1, TFile, TH1F, TH3F, TColor, TLine, TLegend, TLatex, SetOwnership,TMath
import sys,string,math,os,ROOT

#sys.path.append(os.path.join(os.environ.get("HOME"),'rootmacros'))
sys.path.append(os.path.join(os.getcwd(),'rootmacros'))
from myPyRootMacros import prepPlot,GetHist,Get3DHist,SetHistColorAndMarker, Proj3D_Z, SetStyle

######################################################################################################

#Generator="Pythia8"
#Generator="madgraphMLM"
#Generator="25nsMC10"
#Generator="flatPythia8"

Generator = "madgraphMLM"
Range1 = "RunII_2016v3"
Range2 = "RunII_2017"
Range3 = "RunII_2018"
Range4 = "RunII"

Range = Range4

## SavePlots=False
SavePlots=True

#AK4SF=False
AK4SF=True

#BASEDIR="root://cmseos.fnal.gov//store/user/apana/Chi_13TeV/ChiNtuples/MC/80x"
#BASEDIR="/afs/cern.ch/user/z/zhangj/private/chi_analysis_2016/jetUnfold/CMSSW_8_0_23/src/MyChi/ChiAnalysis/bin/SubmitMC/hsts"
#BASEDIR="root://cmseos.fnal.gov//eos/uscms/store/user/jingyu/jetUnfold/MCNtuple/2016PromptReco"
#BASEDIR="root://cmseos.fnal.gov//eos/uscms/store/user/jingyu/jetUnfold/MCNtuple/pythia8_Moriond17_v5"
#BASEDIR="."
BASEDIR = "root://cmseos.fnal.gov//store/user/zhangj/DijetAngularRunII/jetUnfold/MCNtuple/"

#if Generator=="madgraphMLM":
#    Range="_HT"
#elif Generator=="25nsMC10":
#    Range="_flatQCD"
#elif Generator=="flatPythia8":
#    Range="_flatQCD"
#else:
#    Range="_Pt_170toInf"

#compSmearingDir="response_moriond17_madgraphMLM_v5_eta6"


compSmearingDir = "response_"+Generator+"_"+Range+"_RunII_v4_eta0"

if not compSmearingDir in os.listdir(os.getcwd()):
    print "Creating:",compSmearingDir
    os.system("mkdir "+compSmearingDir)

if AK4SF:
    #infile1=BASEDIR + "/chiNtuple_" + Generator + "_" + Range + "_CB2_AK4SF.root"
    #infile2=BASEDIR + "/chiNtuple_" + Generator + "_" + Range + "_GS_AK4SF.root"
    #infile1=BASEDIR + "/chiNtuple_" + Generator + "_" + Range + "_CB2_AK4SF_DataToMCSF.root"
    #infile2=BASEDIR + "/chiNtuple_" + Generator + "_" + Range + "_CB2_AK4SF_DataToMCSF.root"
    infile1=BASEDIR + "/chiNtuple_" + Generator + "_" + Range + "_CB2_AK4SF.root"
    infile2=BASEDIR + "/chiNtuple_" + Generator + "_" + Range + "_CB2_AK4SF.root"
    infile3=BASEDIR + "/chiNtuple_" + Generator + "_" + Range + "_CB2_AK4SF.root"

else:
    #infile1=BASEDIR + "/chiNtuple_" + Generator + Range + "_CB2_noTrees.root"
    #infile2=BASEDIR + "/chiNtuple_" + Generator + Range + "_GS_noTrees.root"
    infile1=BASEDIR + "/chiNtuple_" + Generator + Range1 + "_CB2.root"
    infile2=BASEDIR + "/chiNtuple_" + Generator + Range2 + "_CB2.root"
    infile3=BASEDIR + "/chiNtuple_" + Generator + Range3 + "_CB2.root"

    
## rapidity limits
ymin=-2.5; ymax=2.5
#ymin=1.5; ymax=2.1
## ymin=-3; ymax=-2.
## ymin=-2; ymax=2

## ptbins
## ptBins=[[300,400],[400,500],[500,600],[600,700],[700,800],[800,1000],[1200,1400],[1700,2000],[2000,2500]]
ptBins=[[400,500],[500,600],[600,800],[800,1000],[1000,1200],[1200,1400],[1400,1700],[1700,2000],[2000,2500],[2500,3000],[3000, 5000]]
## ptBins=[[1700,2000],[2000,2500]]
## ptBins=[[600,700],[700,800]]
## ptBins=[[400,500]]
######################################################################################################

class CrystalBallDS:
    def __call__(self,xx,pp):
          x   = xx[0]
          N   = pp[0]
          mu  = pp[1]
          sig = pp[2]
          a1  = pp[3]
          p1  = pp[4]
          a2  = pp[5]
          p2  = pp[6]

          u   = (x-mu)/sig
          A1  = TMath.Power(p1/TMath.Abs(a1),p1)*TMath.Exp(-a1*a1/2)
          A2  = TMath.Power(p2/TMath.Abs(a2),p2)*TMath.Exp(-a2*a2/2)
          B1  = p1/TMath.Abs(a1) - TMath.Abs(a1)
          B2  = p2/TMath.Abs(a2) - TMath.Abs(a2)
  
          if u<-a1: result = A1*TMath.Power(B1-u,-p1);
          elif u<a2: result = TMath.Exp(-u*u/2);
          else: result = A2*TMath.Power(B2+u,-p2);
          return result;

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
    SetHistColorAndMarker(h3,ROOT.kGreen+3,20)

    if ymin<2.1:
        if ptmin>=1000:
            xmin=0.9
            xmax=1.1
        else:
            xmin=0.85
            xmax=1.15
    else:
        if ptmin>=1000:
            xmin=0.9
            xmax=1.1
        else:
            xmin=0.86
            xmax=1.14
    
    h1.GetXaxis().SetTitle("Response")
    h1.SetMinimum(2.e-6)
    fName="GFit"
    fitfunc="gaus"
    h1fit = TF1(fName,fitfunc,xmin,xmax);
    h1fit.SetParameter(0, 1.)
    h1fit.SetParameter(1, 1.)
    h1fit.SetParameter(2, .1)

    h2fit=h1fit.Clone()
    h3fit=h1fit.Clone()

    cb2fit1 = TF1("CB2",CrystalBallDS(),0.2,1.8,7)
    cb2fit1.SetParameter(0,1.)
    cb2fit1.SetParameter(1,1.)
    cb2fit1.SetParameter(2,0.01)
    cb2fit1.SetParameter(3,2.5)
    cb2fit1.SetParameter(4,2.5)
    cb2fit1.SetParameter(5,7.5)
    cb2fit1.SetParameter(6,2.5)

    cb2fit2=cb2fit1.Clone()
    
    h1fit.SetLineColor(h1.GetLineColor())
    h2fit.SetLineColor(h2.GetLineColor())
    h3fit.SetLineColor(h3.GetLineColor())

    c1 = prepPlot("c0","c0",700,20,500,500)
    c1.SetLogy(1)
    
    h1.Draw()
    h2.Draw("same")
    ## h3.Scale(0.8)
    #h3.Draw("same")

    h1.Fit(h1fit,"0R");    
    #h1fit.Draw("sames")
    h2.Fit(h2fit,"0R");    
    # h2fit.Draw("sames")
    h3.Fit(h3fit,"0R");    
    #h3fit.Draw("sames")

    #h1.Fit(cb2fit1,"0R")
    #cb2fit1.SetLineColor(ROOT.kBlue)
    #cb2fit1.Draw("same")
    #h3.Fit(cb2fit2,"0R")
    #cb2fit2.SetLineColor(ROOT.kRed)
    #cb2fit2.Draw("same")

    print "**************************"
    print "ScaleFactor from Gaussian:",h1fit.GetParameter(2)/h3fit.GetParameter(2)
    print "**************************"

    #print "**************************"
    #print "ScaleFactor from CB2:",cb2fit1.GetParameter(2)/cb2fit2.GetParameter(2)
    #print "**************************"
    
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
    
    leg.AddEntry(h1,"Run 2 RECO","lp");
    leg.AddEntry(h2,"Run 2 SMR","lp");
    #leg.AddEntry(h3,"2018","lp");

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
        outfile=compSmearingDir+"/Response_" + Generator + "_" + str(int(ptmin)) + "pT" + str(int(ptmax))
        if AK4SF:
            outfile=outfile + "_wAK4SF"
        c1.Print(outfile + ".gif")
        c1.Print(outfile + ".pdf")

    ans = raw_input('\npress return to continue, q to quit...')

    return ans

#===============================================================


if __name__ == '__main__':


    SetStyle()
    
#===============================================================

    print "INFILE1: ",infile1
    print "INFILE2: ",infile2
    print "INFILE3: ",infile3
    
    reco_3d=Get3DHist(infile1,"Resp3D")
    sCB_3d =Get3DHist(infile2,"SmrResp3D")
    sGS_3d =Get3DHist(infile3,"Resp3D")
    
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

        ans=drawIt(reco0,sCB_0,sGS_0,ptmin,ptmax)

        if ans == 'q':
            sys.exit()
    

#===============================================================

    if os.getenv("FROMGUI") == None:
        print "Not from GUI"
        raw_input('\npress return to end the program...')
