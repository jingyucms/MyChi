from ROOT import *
import sys, array

gROOT.ForceStyle()
gStyle.SetOptStat(0)
gStyle.SetPadRightMargin(0.15)
gStyle.SetPadLeftMargin(0.1)
gStyle.SetPadTopMargin(0.15)
gStyle.SetPadBottomMargin(0.1)
gStyle.SetPadTopMargin(0.07)

gStyle.SetPaintTextFormat("4.2f");

gStyle.SetOptTitle(0)

gStyle.SetPalette(1)

outDir="./results_MatrixInvert/"
#outDir="./results_Iter4/"

infile=TFile(outDir+"Unfolded_chiNtuple_dataReReco_v3_PFHT900_fromCB_AK4SF_pythia8_Pt_170toInf.root")

#infile=TFile(outDir+"Unfolded_Response_pythia8_Pt_170toInf_CB_AK4SF_20170130_fromCB_AK4SF_pythia8_Pt_170toInf.root")

outfile=TFile("CovMatrix.root","RECREATE")

matrix=infile.Get("TMatrixT<double>;5")

hist=infile.Get("dijet_mass2_chi1_unfolded;1")
print hist
print hist.GetBinContent(1)
print hist.GetBinError(1)
print hist.Integral()

#matrix.Print()
#print matrix.GetNrows()

nb=matrix.GetNrows()

nb=11

print "Number of elements in the matrix:",nb
#sys.exit()

chibins=[1,2,3,4,5,6,7,8,9,10,12,14,16]

massbins=array.array('d',[2400,3000,3600,4200,4800,5400,6000,13000])

massbins2=array.array('d',[1900,2400,3000,3600,4200,4800,5400,6000,13000])

for ichi in range(len(chibins)-1):

    h1=TH2D("Correlation Coefficient","Correlation Coefficient",len(massbins)-1,massbins,len(massbins)-1,massbins)

    h2=TH2D("Covariance Matrix","Covariance Matrix",len(massbins)-1,massbins,len(massbins)-1,massbins)

    chiText=TLatex(2800,11500,str(chibins[ichi])+"<#chi_{dijet}<"+str(chibins[ichi+1]))
    
    for i in range(0,nb):
        for j in range(0,nb):
            if i<3 or j<3: continue
            Viijj=matrix(ichi*11+i,ichi*11+i)*matrix(ichi*11+j,ichi*11+j)
            if Viijj>0.0:
                if matrix(ichi*11+i,ichi*11+j) >0:
                    coe = matrix(ichi*11+i,ichi*11+j)
                else:
                    coe = matrix(ichi*11+i,ichi*11+j)
                h1.SetBinContent(i-3, j-3, coe/sqrt(Viijj))

    h1.SetMaximum(1)
    h1.SetMinimum(-1)
    canvas1=TCanvas("mycanvas","",820,800)
    canvas1.SetLogx()
    canvas1.SetLogy()
    canvas1.cd()
    h1.Draw("colztext")
    h1.GetXaxis().SetMoreLogLabels()
    h1.GetYaxis().SetMoreLogLabels()
    h1.GetXaxis().SetTitle("M_{jj} (GeV)")
    h1.GetYaxis().SetTitle("M_{jj} (GeV)")
    h1.GetXaxis().SetTitleOffset(1.3)
    h1.GetYaxis().SetTitleOffset(1.3)
    chiText.Draw("same")
    canvas1.SaveAs("corrMatrix_chi_"+str(chibins[ichi])+".pdf")
    h1.Write()

    #print "--- "+str(chibins[ichi])+" TO "+str(chibins[ichi+1])
    for i in range(0,nb):
        for j in range(0,nb):
            if i<3 or j<3: continue
            #print i-3, j-3, matrix(ichi*11+i,ichi*11+j)
            if matrix(ichi*11+i,ichi*11+j)>=0:
                h2.SetBinContent(i-3,j-3,matrix(ichi*11+i,ichi*11+j))
            else:
                h2.SetBinContent(i-3,j-3,matrix(ichi*11+i,ichi*11+j))

    #print "--- "+str(chibins[ichi])+" TO "+str(chibins[ichi+1])
    for i in range(0,nb):
        for j in range(0,nb):
            if i<4 or j<4: continue
            if j<i: continue
            Viijj=matrix(ichi*11+i,ichi*11+i)*matrix(ichi*11+j,ichi*11+j)
            #print str(massbins[i-4])+" TO "+str(massbins[i-3])+" "+str(massbins[j-4])+" TO "+str(massbins[j-3])+": "+str(matrix(ichi*11+i,ichi*11+j)/sqrt(Viijj))

    canvas2=TCanvas("mycanvas","",800,800)
    #canvas2.SetLogz()
    canvas2.SetLogx()
    canvas2.SetLogy()
    h2.GetXaxis().SetMoreLogLabels()
    h2.GetYaxis().SetMoreLogLabels()
    h2.GetXaxis().SetTitle("M_{jj} (GeV)")
    h2.GetYaxis().SetTitle("M_{jj} (GeV)")
    h2.GetXaxis().SetTitleOffset(1.3)
    h2.GetYaxis().SetTitleOffset(1.3)
    h2.SetMinimum(-1*h2.GetMaximum())
    canvas2.cd()
    h2.Draw("colztext")
    chiText.Draw("same")
    canvas2.SaveAs("covMatrix_chi_"+str(chibins[ichi])+".pdf")
    h2.Write()

    #sys.exit()

#nb=matrix.GetNrows()
nb=22
h3=TH2D("All Correlation Coefficient","All Correlation Coefficient",nb,0,nb,nb,0,nb)
for i in range(0,nb):
    for j in range(0,nb):
        if i%11<4 or j%11<4: continue
        Viijj=matrix(i,i)*matrix(j,j)
        if Viijj>0.0:
            if matrix(i,j) >0:
                coe=matrix(i,j)
            else:
                coe=matrix(i,j)
            #print coe/sqrt(Viijj)
            #if abs(coe/sqrt(Viijj))>0.01:
            #    print i, j, coe/sqrt(Viijj)
            h3.SetBinContent(i+1, j+1, coe/sqrt(Viijj))

canvas3=TCanvas("mycanvas","",1200,1200)
#canvas3.SetLogz()
canvas3.cd()
h3.SetMaximum(1)
h3.SetMinimum(-1)
h3.Draw("colztext")
canvas3.SaveAs("CorrMatrix.pdf")
#print h3.GetBinContent(5,8), h3.GetBinContent(5,9), h3.GetBinContent(5,16),h3.GetBinContent(5,17)
h3.Write()


infile2=TFile("responseMatrices.root")

response=infile2.Get("TMatrixT<double>;2")
nb=response.GetNrows()

h4=TH2D("Response Matrix","Response Matrix",nb,0,nb,nb,0,nb)

print "Response Matrix"

canvas4=TCanvas("mycanvas","",800,600)
canvas4.cd()
for i in range(0,nb):
    for j in range(0,nb):
        if i%11<3 or j%11<3: continue
        h4.SetBinContent(i,j,response(i,j))
        if response(i,j)>0.01 and abs(i-j)>2:
            print i,j,response(i,j)

#print h4.GetBinContent(5,8), h4.GetBinContent(5,9), h4.GetBinContent(5,16),h4.GetBinContent(5,17)
#h4.Draw("colztext")
#canvas4.SaveAs("responseMatrix.pdf")


