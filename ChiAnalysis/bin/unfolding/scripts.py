import os, sys,array
import ROOT
from ROOT import *

sys.path.append(os.path.join(os.environ.get("HOME"),'rootmacros'))
from myPyRootMacros import *

def reBin(hist):
    chi_binning=chi_binning=array.array('d',[1,2,3,4,5,6,7,8,9,10,12,14,16])
    histnew=hist.Rebin(len(chi_binning)-1,hist.GetName()+"_rebin",chi_binning)
    histnew=DivideByBinWidth(histnew)
    return histnew

def doPoisson(hList):

    for i in range(len(hList)):
        h=hList[i]
        h.SetBinErrorOption(ROOT.TH1.kPoisson);

    return

def getMassBins(h):
    nx= h.GetXaxis().GetNbins()

    print "X-axis,low edge,upper edge:",\
        h.GetXaxis().GetBinLowEdge(1),h.GetXaxis().GetBinUpEdge(nx)

    massBins=[]
    for i in range(1,nx+1):
        print i,h.GetXaxis().GetBinLowEdge(i),h.GetXaxis().GetBinUpEdge(i)
        massBins.append(h.GetXaxis().GetBinLowEdge(i))
        if i==nx:
            massBins.append(h.GetXaxis().GetBinUpEdge(i))
    print massBins
    return massBins

def plotComparison(hists1,hists2,WhichCheck,plotRat=False,isMC=False):

    print "\n\n%% PlotComparison  doing ", WhichCheck," comparisons\n"
    if WhichCheck == "Unfolded":
        h2Text="Unfolded Data"
    else:
        h2Text="Projection"

    for i in range(len(hists1)):

        h1=DivideByBinWidth(hists1[i])
        h2=DivideByBinWidth(hists2[i])

        #h1=reBin(hists1[i])
        #h2=reBin(hists2[i])

        #if hists1[i].GetNbinsX()==15:
        #    h1=reBin(hists1[i])
        #    h2=reBin(hists2[i])
        #else:
        #    h1=DivideByBinWidth(hists1[i])
        #    h2=DivideByBinWidth(hists2[i])

        h1.SetLineColor(ROOT.kBlack)
        h1.SetMinimum(0)
        h2.SetLineColor(ROOT.kRed)

        h1Name=h1.GetName()
        h2Name=h2.GetName()

        print "h1Name: ",h1Name, h1.GetXaxis().GetNbins(),h1.GetXaxis().GetBinLowEdge(1),h1.GetXaxis().GetBinUpEdge(15)
        print "h2Name: ",h2Name, h2.GetXaxis().GetNbins(),h2.GetXaxis().GetBinLowEdge(1),h1.GetXaxis().GetBinUpEdge(15)

        if not isMC:
            ## h1Tmp=h1Name[h1Name.find("dijet_mass2_chi2_SMR__")+len("dijet_mass2_chi2_SMR__"):]
            ## h1Tmp=h1Name[h1Name.find("dijet_")+len("dijet_"):]
            ## h2Tmp=h2Name[h2Name.find("projY_")+len("projY_"):]
            ##
            ## print "CCLA: ",h1Tmp
            ## h1Min=h1Tmp[:h1Tmp.find("_")]
            ## h2Min=h2Tmp[:h2Tmp.find("-")]
            ##
            ## h1Max=h1Tmp[h1Tmp.find("_")+1:]
            ## h2Max=h2Tmp[h2Tmp.find("-")+1:]
            ##
            ## h1Max=h2Max[:h1Max.find("_chi")]

            h1Tmp=h1Name[h1Name.find("projY_")+len("projY_"):]
            h2Tmp=h2Name[h2Name.find("projY_")+len("projY_"):]

            if WhichCheck == "Unfolded":
                h1Min=h1Tmp[:h1Tmp.find("-")]
                h2Min=h2Tmp[:h2Tmp.find("-")]

                h1Max=h1Tmp[h1Tmp.find("-")+1:]
                h2Max=h2Tmp[h2Tmp.find("-")+1:]
            else:
                h1Min=h1Tmp[:h1Tmp.find("_")]
                h2Min=h2Tmp[:h2Tmp.find("-")]

                h1Max=h1Tmp[h1Tmp.find("_")+1:h1Tmp.find("_chi")]
                h2Max=h2Tmp[h2Tmp.find("-")+1:]

        else:

            h1Tmp=h1Name[h1Name.find("projY_")+len("projY_"):]
            h2Tmp=h2Name[h2Name.find("projY_")+len("projY_"):]

            h1Min=h1Tmp[:h1Tmp.find("-")]
            h2Min=h2Tmp[:h2Tmp.find("-")]

            h1Max=h1Tmp[h1Tmp.find("-")+1:]
            h2Max=h2Tmp[h2Tmp.find("-")+1:]


        drawLegend=True
        if h1Min != h2Min:
            print "Problem extracting min mass value from histogram name: ",h1Min,h2Min
            drawLegend=False


        if h1Max != h2Max:
            print "Problem extracting max mass value from histogram name: ",h1Max,h2Max
            drawLegend=False

        ## print h1Min,h1Max
        ## print h2Min,h2Max


        c0=prepPlot("c0","comp",40,20,540,550)
        h1.Draw()
        h2.Draw("same")

        if drawLegend:
            DrawText(0.14,0.2,h1Min + " < M_{jj} < " + h1Max,0.04)
            xl1=.6; yl1=0.2; xl2=xl1+.28; yl2=yl1+.15;
            leg =TLegend(xl1,yl1,xl2,yl2);
            leg.SetFillColor(0);
            leg.SetLineColor(0);
            leg.SetShadowColor(0);
            leg.SetTextSize(0.038)

            leg.AddEntry(h1,"Raw data","lp");
            leg.AddEntry(h2,h2Text,"lp");

            leg.Draw()

        c0.Update()

        if plotRat:

            c2 = prepPlot('c2',"Ratio",700,20,540,550)
            rat=h1.Clone()
            rat.SetName("_Clone")
            rat.Divide(h2,h1,1.,1.,"");

            rmin=0.5
            rmax=1.5
            if drawLegend and float(h1Min)>4000:
                rmin=0.
                rmax=2.
            rat.GetYaxis().SetRangeUser(rmin,rmax)
            rat.Draw()

            if drawLegend:
                DrawText(0.14,0.2,h1Min + " < M_{jj} < " + h1Max,0.04)

            c2.Update()

        ans = raw_input('\npress return to continue, q to quit...')
        if ans == 'q':
            sys.exit()

    return

def compAndDrawIt(hists1,hists2):

    #file=TFile(filename)
    #h1=file.Get("dijet_"+massLow+"_"+massHigh+"_chi_gen")
    #h2=file.Get("dijet_"+massLow+"_"+massHigh+"_chi")
    #h3=file.Get("dijet_"+massLow+"_"+massHigh+"_chi_smr")

    #h1=rebinAndNormalize(h1)
    #h2=rebinAndNormalize(h2)
    #h3=rebinAndNormalize(h3)

    massbins=[[2400,3000],[3000,3600],[3600,4200],[4200,4800],[4800,5400],[5400,6000],[6000,13000]]
    
    if len(hists1)!=len(hists2):
        print "Something is Wrong. ---Existing"
        return

    for i in range(len(hists1)):
        #h1=hists1[i]
        #h2=hists2[i]

        #h1=DivideByBinWidth(hists1[i])
        #h2=DivideByBinWidth(hists2[i])
        #print "***************",hists1[i].GetNbinsX()
        if hists1[i].GetNbinsX()==15:
            h1=reBin(hists1[i])
            h2=reBin(hists2[i])
        else:
            h1=DivideByBinWidth(hists1[i])
            h2=DivideByBinWidth(hists2[i])
        
        h1divide=h1.Clone(h1.GetName()+"_clone")
        h2divide=h2.Clone(h2.GetName()+"_clone")
        #print h1.GetName()
        #print h2.GetName()

        #h1divide.Scale(1./h1divide.Integral())
        #h2divide.Scale(1./h2divide.Integral())
        
        h2divide.Divide(h1divide)
        #h2divide.Scale(1./h2divide.Integral())

        function=TF1("Fit","pol1",1.,16.)
        function.SetLineColor(ROOT.kMagenta)
        function.SetParameters(0,1.)
        h2divide.Fit(function,"0R")

        SetHistColorAndMarker(h1,ROOT.kRed,20)
        SetHistColorAndMarker(h2,ROOT.kBlue,20)

        SetHistColorAndMarker(h1divide,ROOT.kGreen,20)
        SetHistColorAndMarker(h2divide,ROOT.kBlack,20)
        
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
        #h2.GetXaxis().SetTitle("#chi_{dijet}")
        #h2.GetYaxis().SetTitle("1/#sigma_{dijet} d#sigma_{dijet}/d#chi_{dijet}")
        h2.GetYaxis().SetTitleOffset(1.2)
        h1.Draw("same")
        #h3.Draw("same")

        xl1=.35; yl1=0.25; xl2=xl1+.28; yl2=yl1+.25;
        leg =TLegend(xl1,yl1,xl2,yl2,str(massbins[i][0])+" < m_{jj} < "+str(massbins[i][1]));
        #leg =TLegend(xl1,yl1,xl2,yl2," < m_{jj} < ")
        leg.SetFillColor(0);
        leg.SetLineColor(0);
        leg.SetShadowColor(0);
        leg.SetTextSize(0.038)

        leg.AddEntry(h1,"Generated","lp");
        leg.AddEntry(h2,"Unfolded MC","lp");
        #if "CB2" in filename:
        #    leg.AddEntry(h3,"Crystal Ball Smeared","lp");
        #else:
        #    leg.AddEntry(h3,"Gaussian Smeared","lp");
        leg.Draw()

        canvas.cd()
        pad2 = TPad("","",0, 0, 1, 0.3)
        pad2.SetLeftMargin(0.125)
        pad2.SetBottomMargin(0.23)
        pad2.SetTopMargin(0.05)
        pad2.SetRightMargin(0.05)
        pad2.Draw()
        pad2.cd()

        h2divide.SetMinimum(0.8)
        h2divide.SetMaximum(1.2)
        h2divide.GetXaxis().SetLabelSize(0.08)
        h2divide.GetXaxis().SetTitleSize(0.09)
        h2divide.GetYaxis().SetLabelSize(0.08)
        h2divide.GetYaxis().SetTitleSize(0.09)
        h2divide.GetYaxis().SetNdivisions(505)
        h2divide.GetXaxis().SetTitle("#chi_{dijet}")
        h2divide.GetYaxis().SetTitle("Ratio")
        h2divide.GetYaxis().SetTitleOffset(0.5)
        h2divide.Draw()
        #h3divide.Draw("same")
        function.Draw("same")
        
        #xl1=.35; yl1=0.25; xl2=xl1+.28; yl2=yl1+.25;
        #leg2 =TLegend(xl1,yl1,xl2,yl2);
        #leg2.SetFillColor(0);
        #leg2.SetLineColor(0);
        #leg2.SetShadowColor(0);
        #leg2.SetTextSize(0.078)

        #leg2`.AddEntry(h2divide,"RECO/Gen","lp")
        #leg2.AddEntry(h3divide,"Smeared Gen/Gen","lp")
        
        #leg2.Draw()

        canvas.Modified()
        #if "GS" in filename.replace("_","").split():
        #print filename
        #if "GS" in filename:
        #outfile=smearingUncertDir+"/SmearingUncert_" + Generator + "_" + massLow + "mass" + massHigh + "_GS"
        #else:
        #outfile="Pythia_Test_"+str(massbins[i][0])+"_"+str(massbins[i][1])
        outfile="Pythia_Vs_Herwigg_p1_"+str(massbins[i][0])+"_"+str(massbins[i][1])

        #if AK4SF:
        #    outfile=outfile + "_wAK4SF"
        canvas.Print(outfile + ".gif")
        canvas.Print(outfile + ".pdf")

        ans = raw_input('\npress return to continue, q to quit...')
        if ans == 'q':
            sys.exit()
        
    return
