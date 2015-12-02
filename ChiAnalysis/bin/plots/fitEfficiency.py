from ROOT import gROOT, gStyle, gSystem, TCanvas, TF1, TFile, TH1F, TH3F, TColor, TLine, TLegend, TLatex, SetOwnership, TGraphErrors
import sys,string,math,os,ROOT

sys.path.append(os.path.join(os.environ.get("HOME"),'rootmacros'))
from myPyRootMacros import * 
from array import array

#===============================================================

## OnePlot=False
OnePlot=True

SavePlots=False
## SavePlots=True

#===============================================================

class DEFFFIT:
   def __call__( self, x, par ):
       value1=par[0]/2.+par[0]/2.*ROOT.TMath.Erf((x[0]-par[1])/par[2]);
       value2=par[3]/2.+par[3]/2.*ROOT.TMath.Erf((x[0]-par[4])/par[5]);

       value=value1+value2
       return value

if __name__ == '__main__':

    SetStyle()

    quote="\""
#===============================================================

    infile="turnOn_chiBins.root"
    chiBins=["0_2","2_4","4_6","6_10","10_12","12_14","14_16"]
    chiCols=[ROOT.kRed,ROOT.kBlue,ROOT.kGreen+3,ROOT.kBlack,ROOT.kRed+1,ROOT.kBlue+2,ROOT.kMagenta]
    # chiBins=["12_14","14_16"]
    # chiBins=["0_2","2_4"]

    xmin=700.; xmax=2500.

    fitparameters=""
    ibin=0

    tlats=[]
    for chiBin in chiBins:
        ibin=ibin+1
        
        hname="Efficiency_" + chiBin
        print hname
        h=Get3DHist(infile,hname)
        
        xminf=1000.; xmaxf=xmax;
        width=80
        mean=800.
        
        if chiBin == "0_2":
            xminf=800;
        elif chiBin == "2_4":
            xminf=900.
        elif chiBin == "4_6":
            xminf=1050.
            mean=1000.
        elif chiBin == "6_10":
            xminf=1250.
            mean=1200.
        elif chiBin == "10_12":
            xminf=1400.
            mean=1300.
        elif chiBin == "12_14":
            xminf=1500.
            mean=1450.
        elif chiBin == "14_16":
            xminf=1550.
            mean=1500.

            
        fitter = TF1("fitf",EFFFIT(),xminf,xmaxf,3);
        ## fitter = TF1("fitf",DEFFFIT(),xminf-100,xmaxf,6);
        fitter.SetLineColor(chiCols[ibin-1])

        fitter.SetParameters(1,mean,width);
        ## fitter.SetParameters(1,mean,width,1,mean-200.,width+20);
        
        fitter.FixParameter(0,1.0);
        # fitter.FixParameter(3,1.0);
        
        fitter.SetLineStyle(1)
        
        #fitter.SetParameter(0, 1)
        #fitter.SetParameter(1, 1)
        #fitter.SetParameter(2, .1)

        chopt=""
        if OnePlot:
            if ibin==1:
                h.GetXaxis().SetRangeUser(xmin,xmax)
                c1 = prepPlot("c0","c0",700,20,500,500)
                c1.SetLogy(False)
                
            if ibin>1:
                chopt="same"
        else:
            h.GetXaxis().SetRangeUser(xmin,xmax)
            c1 = prepPlot("c0","c0",700,20,500,500)
            c1.SetLogy(False)
            
        h.Draw(chopt)

        h.Fit(fitter,"0R");
        fitter.Draw("sames")

        chimin=chiBin[0:chiBin.find("_")]
        chimax=chiBin[chiBin.find("_")+1:]        
        if (not OnePlot):
            t1 = TLatex();
            t1.SetNDC();
            txtsize=0.048;  t1.SetTextSize(txtsize); t1.SetTextAlign(22);
            xtxt=.785; ytxt=.285;
            t1.DrawLatex(xtxt,ytxt,chimin + " < #chi < " + chimax);
        else:
            
            # t1 = TLatex();
            # t1.SetNDC();
            # txtsize=0.048;  t1.SetTextSize(txtsize); t1.SetTextAlign(22);
            # xtxt=.785; 
            if ibin==1:
                xl1=.6; yl1=0.2; xl2=xl1+.3; yl2=yl1+.35;
                leg=PrepLegend(xl1,yl1,xl2,yl2,0.05,ROOT.kWhite)

            leg.AddEntry(fitter,chimin + " < #chi < " + chimax,"l");
            leg.Draw()
            #t1.DrawLatex(xtxt,ytxt,chimin + " < #chi < " + chimax);
            #tlats.append(t1)
            
            
        ## fitparameters=fitparameters + quote + chiBin + quote + "\t:(" + str(fitter.GetParameter(0)) + ",\t" \
        ##                + str(fitter.GetParameter(1)) + ",\t" \
        ##                + str(fitter.GetParameter(2)) + ")," \
        ##                + "\n"

        begin="else if ( chi <= ";        
        if (ibin==1): begin="if ( chi <= ";
                
        fitparameters=fitparameters + begin + chimax +"){" + "\n" + \
                       "\t" + "par[0] = " + str(fitter.GetParameter(0)) + ";\n" +\
                       "\t" + "par[1] = " + str(fitter.GetParameter(1)) + ";\n" +\
                       "\t" + "par[2] = " + str(fitter.GetParameter(2)) + ";\n" +\
                       "}"
        
        
        c1.Modified()    
        c1.Update()

        ans = "xx"
        ans = raw_input('\npress return to continue, q to quit...')
        if ans == 'q':
            sys.exit()    


    c1.Modified()    
    c1.Update()
    if SavePlots:
        outfile="TriggerEfficiency_vsChi"
        outfile=outfile + ".pdf"
        c1.Print(outfile)
            
    print fitparameters[0:-1]
    
#===============================================================
    if os.getenv("FROMGUI") == None:
        print "Not from GUI"
        raw_input('\npress return to end the program...')
