from ROOT import *

gROOT.ForceStyle()
gStyle.SetOptStat(0)
gStyle.SetPadRightMargin(0.15)
gStyle.SetPadLeftMargin(0.07)
gStyle.SetPadTopMargin(0.03)
gStyle.SetPadBottomMargin(0.07)

gStyle.SetPadTopMargin(0.07)


#outDir="./results_MatrixInvert/"
outDir="./results_Iter4/"

infile=TFile(outDir+"Unfolded_chiNtuple_dataReReco_v3_PFHT900_fromCB_AK4SF_pythia8_Pt_170toInf.root")

outfile=TFile("CovMatrix.root","RECREATE")

matrix=infile.Get("TMatrixT<double>;6")

#matrix.Print()
#print matrix.GetNrows()

nb=matrix.GetNrows()

h1=TH2D("Covariance Matrix","Covariance Matrix",nb,0,nb,nb,0,nb)

h2=TH2D("Error Matrix","Error Matrix",nb,0,nb,nb,0,nb)

for i in range(0,nb):
    for j in range(0,nb):
        if i%11<3 or j%11<3: continue
        Viijj=matrix(i,i)*matrix(j,j)
        if Viijj>0.0:
            if matrix(i,j) >0:
                coe=matrix(i,j)
            else:
                coe = -matrix(i,j)
            #print coe/sqrt(Viijj)
            h1.SetBinContent(i+1, j+1, coe/sqrt(Viijj))
            #h.SetBinContent(i+1,j+1,)

canvas1=TCanvas("mycanvas","",800,600)
canvas1.SetLogz()
canvas1.cd()
h1.Draw("colz")
canvas1.SaveAs("corrMatrix.pdf")
h1.Write()

for i in range(0,nb):
    for j in range(0,nb):
        if i%11<3 or j%11<3: continue
        if matrix(i,j)>=0:
            h2.SetBinContent(i,j,sqrt(matrix(i,j)))
        else:
            h2.SetBinContent(i,j,sqrt(-matrix(i,j)))


canvas2=TCanvas("mycanvas","",800,600)
canvas2.SetLogz()
canvas2.cd()
h2.Draw("colz")
canvas2.SaveAs("covMatrix.pdf")
h2.Write()



infile2=TFile("responseMatrices.root")

response=infile2.Get("TMatrixT<double>;2")
nb=response.GetNrows()

h3=TH2D("Response Matrix","Response Matrix",nb,0,nb,nb,0,nb)

canvas3=TCanvas("mycanvas","",800,600)
canvas3.cd()
for i in range(0,nb):
    for j in range(0,nb):
        if i%11<3 or j%11<3: continue
        h3.SetBinContent(i,j,response(i,j))

h3.Draw("colz")
canvas3.SaveAs("responseMatrix.pdf")





