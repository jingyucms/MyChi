from ROOT import gROOT, gStyle, gSystem, TCanvas, TPad, TF1, TFile, TH1F, TH3F, TColor, TLine, TLegend, TLatex, SetOwnership
import sys,string,math,os,ROOT
import array

#sys.path.append(os.path.join(os.environ.get("HOME"),'rootmacros'))
sys.path.append(os.path.join(os.getcwd(),'rootmacros'))
from myPyRootMacros import prepPlot,GetHist,Get3DHist,SetHistColorAndMarker, Proj3D_Z, SetStyle

######################################################################################################

#Generator="flatPythia8"
#Generator="madgraphMLM"

Generator = "madgraphMLM"
Range1 = "RunII_2016v3"
Range2 = "RunII_2017"
Range3 = "RunII_2018"

SavePlots=True

AK4SF=True
DataToMCSF=False

#BASEDIR="root://cmseos.fnal.gov//eos/uscms/store/user/jingyu/jetUnfold/MCNtuple/2016PromptReco"
#BASEDIR="root://cmseos.fnal.gov//eos/uscms/store/user/jingyu/jetUnfold/MCNtuple/pythia8Moriond17_v4"
#BASEDIR="."
#BASEDIR = "root://cmsxrootd.fnal.gov//store/user/zhangj/DijetAngularRunII/jetUnfold/MCNtuple"
BASEDIR = "/eos/uscms/store/user/zhangj/DijetAngularRunII/jetUnfold/MCNtuple"

if Generator=="madgraphMLM":
    Range="_HT"
elif Generator=="25nsMC10":
    Range="_flatQCD"
elif Generator=="flatPythia8":
    Range="_flatQCD"
else:
    Range="_Pt_170toInf"

Range = Range1
    
smearingUncertDir="smearing_Uncert_GaussianWidth_"+Range+"_v3"


if not smearingUncertDir in os.listdir(os.getcwd()):
    print "Creating:",smearingUncertDir
    os.system("mkdir "+smearingUncertDir)



if AK4SF:
    #print Range1
    infile1=BASEDIR + "/chiNtuple_" + Generator + "_" + Range + "_GS_AK4SF.root"
    infile2=BASEDIR + "/chiNtuple_" + Generator + "_" + Range + "_GS_AK4SF_SysPlus.root"
    infile3=BASEDIR + "/chiNtuple_" + Generator + "_" + Range + "_GS_AK4SF_SysMinus.root"

if DataToMCSF:
    
    infile1=BASEDIR + "/chiNtuple_" + Generator + "_" + Range1 + "_CB2_AK4SF_DataToMCSF.root"
    infile2=BASEDIR + "/chiNtuple_" + Generator + "_" + Range2 + "_CB2_AK4SF_DataToMCSF.root"
    infile3=BASEDIR + "/chiNtuple_" + Generator + "_" + Range3 + "_CB2_AK4SF_DataToMCSF.root"


massBins=[[1900,2400],[2400,3000],[3000,3600],[3600,4200],[4200,4800],[4800,5400],[5400,6000],[6000,7000],[7000,13000]]
#massBins = [[6000, 13000]]

chibinning1=array.array('d',[1,2,3,4,5,6,7,8,9,10,12,14,16])
chibinning2=array.array('d',[1,3,6,9,12,16])

#print infile1

######################################################################################################

def rebinAndNormalize(h, massHigh):

    #print massHigh

    if massHigh == '13000':
        chibinning = chibinning2
    else:
        chibinning = chibinning1
    
    h=h.Rebin(len(chibinning)-1,h.GetName()+"_rebin",chibinning)
    
    for b in range(h.GetXaxis().GetNbins()):
        h.SetBinContent(b+1,h.GetBinContent(b+1)/h.GetBinWidth(b+1))
        h.SetBinError(b+1,h.GetBinError(b+1)/h.GetBinWidth(b+1))

    h.Scale(1./h.Integral())

    return h


def DrawItAndFitRatio(filename1, filename2, filename3,massLow,massHigh):

    SetStyle()
    gStyle.SetOptFit(0)
    gROOT.ForceStyle()

    print filename1
    print filename2
    print filename3
    
    file1=TFile(filename1)
    file2=TFile(filename2)
    file3=TFile(filename3)
    h1=file1.Get("dijet_"+massLow+"_"+massHigh+"_chi_smr")
    h2=file2.Get("dijet_"+massLow+"_"+massHigh+"_chi_smr")
    h3=file3.Get("dijet_"+massLow+"_"+massHigh+"_chi_smr")

    h1=rebinAndNormalize(h1, massHigh)
    h2=rebinAndNormalize(h2, massHigh)
    h3=rebinAndNormalize(h3, massHigh)
    
    h2divide=h2.Clone(h2.GetName()+"_clone")
    h3divide=h3.Clone(h3.GetName()+"_clone")

    h2divide.Divide(h1)
    h3divide.Divide(h1)

    SetHistColorAndMarker(h1,ROOT.kBlack,20)
    SetHistColorAndMarker(h2,ROOT.kRed,20)
    SetHistColorAndMarker(h3,ROOT.kBlue,20)

    SetHistColorAndMarker(h2divide,ROOT.kRed,20)
    SetHistColorAndMarker(h3divide,ROOT.kBlue,20)

    function1=TF1("Fit_dijet_"+massLow+"_"+massHigh+"_chi_RunIIReco_Plus","pol1",1.,16.)
    function1.SetLineColor(ROOT.kRed)
    
    function1.SetParameters(0,1.)
    function1.SetParameters(0,0.)
    h2divide.Fit(function1,"0R")

    function2=TF1("Fit_dijet_"+massLow+"_"+massHigh+"_chi_RunIIReco_Minus","pol1",1.,16.)
    function2.SetLineColor(ROOT.kBlue)
    
    function2.SetParameters(0,1.)
    function2.SetParameters(0,0.)
    h3divide.Fit(function2,"0R")

    canvas=TCanvas("myCanvas","myCanvas",0,0,500,600)
    
    pad1=TPad("","",0, 0.3, 1, 1)
    
    pad1.SetLeftMargin(0.125)
    pad1.SetBottomMargin(0.05)
    pad1.SetTopMargin(0.05)
    pad1.SetRightMargin(0.05)
    pad1.Draw()
    pad1.cd()
        
    h2.Draw()
    h2.SetMinimum(0)
    h2.SetMaximum(h2.GetMaximum()*1.2)
    h2.GetXaxis().SetLabelSize(0.)
    h2.GetXaxis().SetTitleSize(0.)
    h2.GetYaxis().SetTitle("1/#sigma_{dijet} d#sigma_{dijet}/d#chi_{dijet}")
    h2.GetYaxis().SetTitleOffset(1.2)
    h1.Draw("same")
    h3.Draw("same")

    xl1=.6; yl1=0.15; xl2=xl1+.28; yl2=yl1+.25;
    leg =TLegend(xl1,yl1,xl2,yl2,massLow+" < m_{jj} < "+massHigh);
    leg.SetFillColor(0);
    leg.SetLineColor(0);
    leg.SetShadowColor(0);
    leg.SetTextSize(0.038)

    leg.AddEntry(h1,"Gaussian","l");
    leg.AddEntry(h2,"SysUp","lp");
    leg.AddEntry(h3,"SysDown","lp");
    leg.Draw()

    canvas.cd()
    pad2 = TPad("","",0, 0, 1, 0.3)
    pad2.SetLeftMargin(0.125)
    pad2.SetBottomMargin(0.23)
    pad2.SetTopMargin(0.05)
    pad2.SetRightMargin(0.05)
    pad2.Draw()
    pad2.cd()

    h2divide.SetMinimum(0.9)
    h2divide.SetMaximum(1.1)
    h2divide.GetXaxis().SetLabelSize(0.08)
    h2divide.GetXaxis().SetTitleSize(0.09)
    h2divide.GetYaxis().SetLabelSize(0.08)
    h2divide.GetYaxis().SetTitleSize(0.09)
    h2divide.GetYaxis().SetNdivisions(505)
    h2divide.GetXaxis().SetTitle("#chi_{dijet}")
    h2divide.Draw()
    h3divide.Draw("same")
    function1.Draw("same")
    function2.Draw("same")
        
    xl1=.25; yl1=0.65; xl2=xl1+.28; yl2=yl1+.25;
    leg2 =TLegend(xl1,yl1,xl2,yl2);
    leg2.SetFillColor(0);
    leg2.SetLineColor(0);
    leg2.SetShadowColor(0);
    leg2.SetTextSize(0.078)

    #leg2.AddEntry(h2divide,"RECO/Smeared Gen","lp")
    
    #leg2.Draw()

    canvas.Modified()
    if SavePlots:
        
        outfile=smearingUncertDir+"/SmearingUncert_" + Generator + "_" + massLow + "mass" + massHigh + "_CB2"
        if AK4SF:
            outfile=outfile + "_wAK4SF"
        canvas.Print(outfile + ".gif")
        canvas.Print(outfile + ".pdf")

    ans = raw_input('\npress return to continue, q to quit...')

    if ans == 'q':
        sys.exit()
        
    print h1,h2,h3,h2divide,h3divide,function1,function2
    
    return [h1,h2,h3,h2divide,h3divide,function1,function2]


#===============================================================


if __name__ == '__main__':

    
#===============================================================

    #fileout=TFile.Open("SysUnc_CBVsGeant_Pythiaflat_170toInf.root","RECREATE")
    
    for massBin in massBins:
        massLow=str(massBin[0])
        massHigh=str(massBin[1])

        result=DrawItAndFitRatio(infile1,infile2,infile3,massLow,massHigh)

        #ans=DrawIt(infile1,infile2,infile3,massLow,massHigh)

        #print h1,h2,h3,h2divide,function

        #result[0].Write()
        #result[2].Write()
        #result[3].Write()
        #result[4].Write()
        #result[5].Write()
            
#===============================================================

    if os.getenv("FROMGUI") == None:
        print "Not from GUI"
        raw_input('\npress return to end the program...')
