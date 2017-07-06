{

  gROOT->Reset();
  gStyle->SetPalette(1);
  gStyle->SetOptStat(0);
  gStyle->SetOptLogy(1);
  gStyle->SetOptLogx(1);
  gStyle->SetOptLogz(0);
  gStyle->SetPaintTextFormat("4.3f");

  // const Int_t NRGBs = 5;
  // const Int_t NCont = 255;
  // //const Int_t NCont = 100;
  // 
  // Double_t stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
  // Double_t red[NRGBs]   = { 0.00, 0.00, 0.87, 1.00, 0.51 };
  // Double_t green[NRGBs] = { 0.00, 0.81, 1.00, 0.20, 0.00 };
  // Double_t blue[NRGBs]  = { 0.51, 1.00, 0.12, 0.00, 0.00 };
  // TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
  // gStyle->SetNumberContours(NCont);

  TString Sample="pythia8_Pt_170toInf_CB_AK4SF";
  
  // TFile *_file0 = new TFile("Response_CB1.6_wExtra_pythia8_ci_170pt13000_partial_20151123.root");
  // TFile *_file0 = new TFile("../ResponseMatrices/Response_Pt_170to13000_CB2_AK4SF_partial.root");
  TFile *_file0 = new TFile("ResponseMatrices/Response_"+Sample+"_20170130.root");
  
  // _file0->ls();

  string hname="dijet_massgen_massSMR_1";
  // string hname="dijet_massgen_massRECO_1";
  TH2F *h = (TH2F*)_file0->Get(hname.c_str());

  double xmin(1900), xmax(13000);

  int nbinsx=h->GetNbinsX();
  int nbinsy=h->GetNbinsY();

  bool genNorm(true);
  if (genNorm){
    for (int i=3; i<nbinsx+1; i++){
      std::cout << i << std::endl;
      double sum(0);
      for (int j=3; j<nbinsy+1; j++){
	double cont=h->GetBinContent(i,j);
	sum=sum+cont;
	// std::cout << j << "\t" << cont << std::endl;
      }
      for (int j=3; j<nbinsy+1; j++){
	double cont=h->GetBinContent(i,j);
	h->SetBinContent(i,j,cont/sum);
      }
    }
  }
  h->GetXaxis()->SetTitle("M_{jj} (GeV) Generated");
  h->GetYaxis()->SetTitle("M_{jj} (GeV) Reconstructed");

  h->GetXaxis()->SetRangeUser(xmin,xmax);
  h->GetYaxis()->SetRangeUser(xmin,xmax);
  h->GetZaxis()->SetRangeUser(1e-7,1.);

  h->GetXaxis()->SetNoExponent(true);

  h->GetYaxis()->SetNoExponent(true);

  h->GetXaxis()->SetNdivisions(202);
  h->GetYaxis()->SetNdivisions(202);

  h->GetXaxis()->SetMoreLogLabels(true);
  h->GetYaxis()->SetMoreLogLabels(true);

  h->SetTitleOffset(1.88, "Y");
  h->SetTitleOffset(1.28, "X");

  TCanvas *c1 = new TCanvas("c1","Root Canvas 1",60,40,540,550);
  c1->SetRightMargin(.125);
  c1->SetLeftMargin(.135);
  // h->Scale(1e10);
  // h->SetMinimum(0.01);
  h->SetMarkerSize(1.3);
  h->Draw("colz,text45");
  // h->Draw("colz");

  c1->Print("ResponseMatrix_"+Sample+".pdf");

}
