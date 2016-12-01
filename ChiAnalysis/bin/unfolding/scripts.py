import os, sys
import ROOT
from ROOT import *

sys.path.append(os.path.join(os.environ.get("HOME"),'rootmacros'))
from myPyRootMacros import *

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

        h1.SetLineColor(ROOT.kBlack)
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
