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
Range4 = "RunII"

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

Range = Range4

if DataToMCSF:
    smearingUncertDir="smearing_Uncert_Moriond_madgraph_RunII_"+Range2+"_v2"
else:
    smearingUncertDir="smearing_Uncert_Moriond_madgraph_RunII_"+Range+"_v1"



smearingUncertDir="smearing_Uncert_GaussianVsCB2_"+Range+"_v3"


if not smearingUncertDir in os.listdir(os.getcwd()):
    print "Creating:",smearingUncertDir
    os.system("mkdir "+smearingUncertDir)



if AK4SF:
    #print Range1
    infile1=BASEDIR + "/chiNtuple_" + Generator + "_" + Range + "_CB2_AK4SF.root"
    infile2=BASEDIR + "/chiNtuple_" + Generator + "_" + Range + "_GS_AK4SF.root"


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


def DrawItAndFitRatio(filename1,filename2,massLow,massHigh):

    SetStyle()
    gStyle.SetOptFit(0001)
    gROOT.ForceStyle()
    
    file1=TFile(filename1)
    file2=TFile(filename2)
    h1=file1.Get("dijet_"+massLow+"_"+massHigh+"_chi_smr")
    h2=file2.Get("dijet_"+massLow+"_"+massHigh+"_chi_smr")

    h1=rebinAndNormalize(h1, massHigh)
    h2=rebinAndNormalize(h2, massHigh)
    
    h2divide=h2.Clone(h2.GetName()+"_clone")

    h2divide.Divide(h1)

    SetHistColorAndMarker(h1,ROOT.kBlack,20)
    SetHistColorAndMarker(h2,ROOT.kRed,20)

    SetHistColorAndMarker(h2divide,ROOT.kMagenta,20)

    function=TF1("Fit_dijet_"+massLow+"_"+massHigh+"_chi_RunIIReco","pol1",1.,16.)
    function.SetLineColor(ROOT.kGreen)
    
    function.SetParameters(0,1.)
    function.SetParameters(0,0.)
    h2divide.Fit(function,"0R")

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

    xl1=.6; yl1=0.15; xl2=xl1+.28; yl2=yl1+.25;
    leg =TLegend(xl1,yl1,xl2,yl2,massLow+" < m_{jj} < "+massHigh);
    leg.SetFillColor(0);
    leg.SetLineColor(0);
    leg.SetShadowColor(0);
    leg.SetTextSize(0.038)

    leg.AddEntry(h1,"Crystal Ball Smeared","l");
    leg.AddEntry(h2,"Gaussian Smeared","lp");
    leg.Draw()

    canvas.cd()
    pad2 = TPad("","",0, 0, 1, 0.3)
    pad2.SetLeftMargin(0.125)
    pad2.SetBottomMargin(0.23)
    pad2.SetTopMargin(0.05)
    pad2.SetRightMargin(0.05)
    pad2.Draw()
    pad2.cd()

    h2divide.SetMinimum(0.75)
    h2divide.SetMaximum(1.25)
    h2divide.GetXaxis().SetLabelSize(0.08)
    h2divide.GetXaxis().SetTitleSize(0.09)
    h2divide.GetYaxis().SetLabelSize(0.08)
    h2divide.GetYaxis().SetTitleSize(0.09)
    h2divide.GetYaxis().SetNdivisions(505)
    h2divide.GetXaxis().SetTitle("#chi_{dijet}")
    h2divide.Draw()
    function.Draw("same")
        
    xl1=.25; yl1=0.65; xl2=xl1+.28; yl2=yl1+.25;
    leg2 =TLegend(xl1,yl1,xl2,yl2);
    leg2.SetFillColor(0);
    leg2.SetLineColor(0);
    leg2.SetShadowColor(0);
    leg2.SetTextSize(0.078)

    leg2.AddEntry(h2divide,"Gaussian/CB2","lp")
    
    leg2.Draw()

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
        
    print h1,h2,h2divide,function
    
    return [h1,h2,h2divide,function]


#===============================================================


if __name__ == '__main__':

    
#===============================================================

    #fileout=TFile.Open("SysUnc_CBVsGeant_Pythiaflat_170toInf.root","RECREATE")
    
    for massBin in massBins:
        massLow=str(massBin[0])
        massHigh=str(massBin[1])

        result=DrawItAndFitRatio(infile1,infile2,massLow,massHigh)

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
