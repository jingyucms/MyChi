//////////////////////////////////////

#ifndef ChiNtuple_h
#define ChiNtuple_h

#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <sstream>
#include <cassert>
#include <time.h>

#include <TROOT.h>
#include <TSystem.h>
#include <TChain.h>
#include <TFile.h>
#include <TTree.h>
#include <TFriendElement.h>
#include <TList.h>
#include <TMatrix.h>
#include <TH1D.h>
#include <TH1F.h>
#include <TH2D.h>
#include <TH2F.h>
#include <TH3D.h>
#include <TH3F.h>
#include <TLorentzVector.h>
#include <TMath.h>
#include "TRandom.h"

#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/PythonParameterSet/interface/MakeParameterSets.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "CondFormats/JetMETObjects/interface/JetResolution.h"

#include "MyChi/ChiAnalysis/interface/MyJetResponse.h"

// #include <TCanvas.h>

using std::cout;
using std::endl;
using std::string;
using std::vector;
using std::map;

// typedef struct
// {
//     int dijetFlag;
//     float mass;
//     float pt;
//     float chi;
//     float yboost;
//     float pt1;
//     float eta1;
//     float phi1;
//     float e1;
//     float pt2;
//     float eta2;
//     float phi2;
//     float e2;
// } Dijetinfo;

class PtGreater {
  public:
  template <typename T> bool operator () (const T& i, const T& j) {
    return (i.Pt() > j.Pt());
  }
};

struct Dijet
{
    int dijetFlag;
    float mass;
    float pt;
    float chi;
    float yboost;
    float pt1;
    float eta1;
    float phi1;
    float e1;
    float pt2;
    float eta2;
    float phi2;
    float e2;
};

typedef struct Dijet DijetInfo;

class ChiNtuple {

public:
  
  Int_t            fCurrent; //!current Tree number in a TChain

  ChiNtuple();
  ChiNtuple(const std::string & fname);

  ~ChiNtuple();

  bool Open(const std::string & fname);
  bool OpenWithList(const std::string & fname);
  void BookHistograms(const std::string & fname);
  void WriteHistograms();
  void SetXSWeight(const double &);
  void SetSmrMax(const double &);
  void SetIsData(const bool &);
  void SetDoGaussian(const bool &);
  void SetNevents(const int &);
  void SetDoSysErr(const int &);
  void SetAK4_SF(const bool &);
  void SetDataToMC_SF(const bool &);
  vector <TLorentzVector> sortJets(const vector<TLorentzVector>);
  int findLeading(const std::vector<double> );
  int findNextLeading(const std::vector<double>, const uint);
  void Loop();
  
  string outName;
  TFile *outFile;
  TH1F *myHist;

  TTree *_outTree;
  Float_t XSweight;
  Float_t EVTweight;
  Float_t PU_Num;
  Float_t True_Num;
  Int_t Event;
  Int_t Run;
  Int_t Lumi;
  Int_t IsData;
  Int_t HTBin;
  Int_t PTBin;
  Int_t MBin;
   
  DijetInfo recoDijets,genDijets,smrDijets;
  
private :

  TChain          *fChain;   //!pointer to the analyzed TTree or TChain

  float xsweight;
  float SmrMax;
  int   Nevts;
  bool  doGaussian, doAK4_sf, doDataToMC_sf;
  int   doSysErr;
  bool  CheckFirstFile();
  bool  OpenInputFiles();
  bool  OpenNtupleList(const std::string & fname);
  std::vector<std::string> listNtuples;
  Long64_t nentries_;
  TFile* rf;

  std::vector<double> massBins1;
  std::vector<double> massBins2;
  
  std::vector<double> chiBins1;
  std::vector<double> chiBins2;
  std::vector<double> chiBins3;
  std::vector<double> chiBins4;
  std::vector<TH1F*> hists;
  std::vector<TH1F*> ghists;
  std::vector<TH1F*> shists;  
  std::vector<TH1F*> mhists;
  //TH2F *dijet_m_chi_0,*dijet_m_chi_1,*dijet_m_chi_2,*dijet_m_chi_3,*dijet_m_chi_4;
  TH2F *dijet_mass1_chi1,*dijet_mass1_chi2,*dijet_mass1_chi3,*dijet_mass1_chi4;
  TH2F *dijet_mass2_chi1,*dijet_mass2_chi2,*dijet_mass2_chi3,*dijet_mass2_chi4;
  
  TString hname,htitle;
  TObjArray* Hlist;  

  std::map<TString, TH1*> m_HistNames;
  std::map<TString, TH1*>::iterator hid;

  std::map<TString, TH2*> m_HistNames2D;
  std::map<TString, TH2*>::iterator hid2D;

  std::map<TString, TH3*> m_HistNames3D;
  std::map<TString, TH3*>::iterator hid3D;
  
  void fillHist(const TString& histName, const Double_t& value, const Double_t& wt=1.0);
  void fill2DHist(const TString& histName, const Double_t& x,const Double_t& y, const Double_t& wt=1.0);
  void fill3DHist(const TString& histName, const Double_t& x,const Double_t& y, const Double_t& z,const Double_t& wt=1.0);
  
  TH1F* Book1dHist(const char*, const char*, Int_t, Double_t, Double_t, bool);
  TH2F* Book2dHist(const char*, const char*, Int_t, Double_t, Double_t, Int_t , Double_t , Double_t ,bool);
  TH3F* Book3dHist(const char*, const char*, Int_t, Double_t, Double_t, Int_t , Double_t , Double_t ,Int_t , Double_t , Double_t ,bool );

  double SmearFactor(double,double, double);
  double SmearFunc(double, double, double, double, double, double);
  double TriggerEff(double, double);
  TRandom rnd;  
};

ChiNtuple::ChiNtuple(){}
ChiNtuple::~ChiNtuple(){
  delete fChain;
}

bool ChiNtuple::OpenInputFiles()
{
  std::string commentLine ("#");
  
  fChain     = new TChain("ntuplizer/tree");

  for (unsigned int i=0;i<listNtuples.size();i++)
  {
    string ntuple=listNtuples[i];
    if (ntuple.at(0) != commentLine){
      std::cout << " -- Adding to chain: " << ntuple << std::endl;
      fChain->Add(ntuple.c_str());
    }
  }

  return true;
}

bool ChiNtuple::OpenWithList(const std::string & fname)
{
  std::cout.flush();cout<<"Opening available trees..."<<std::endl;std::cout.flush();
  
  if (!OpenNtupleList(fname)) return false;
  if (!OpenInputFiles())     return false;

  //Init();

  return true;
}

bool ChiNtuple::OpenNtupleList(const std::string & fname)
{
  std::ifstream flist(fname.c_str());
  if (!flist)
    {
      std::cout << "File "<<fname<<" is not found !"<<std::endl;
      return false;
    }

  while(!flist.eof())
    {
      std::string str;
      getline(flist,str);
      if (!flist.fail())
  {
           if (str!="") listNtuples.push_back(str);
  }
    }

  return true;
}

vector <TLorentzVector> ChiNtuple::sortJets(const vector<TLorentzVector> p4){ 
  vector <TLorentzVector> p4sorted;

  p4sorted=p4;
  std::sort(p4sorted.begin(),p4sorted.end(),PtGreater());
  //cout << "Size of jet vector: " << p4sorted.size() << endl;

  //int njets=p4sorted.size();
  //for (int ijet=0; ijet<njets; ijet++){
  //  cout << ijet << " " << p4.at(ijet).Pt() << " " << p4sorted.at(ijet).Pt() << endl;
  // }
  return p4sorted;
}

void ChiNtuple::SetXSWeight(const double & wt){
  if (wt<0) std::cout << "Negative XS given.  This will not end well..." << std::endl;
  xsweight=wt;
  
}

void ChiNtuple::SetSmrMax(const double & x){
  
  SmrMax=x;
  
}

void ChiNtuple::SetIsData(const bool & isData){
  IsData=0;
  if (isData)IsData=1;
  
}

void ChiNtuple::SetDoGaussian(const bool & doG){
  doGaussian=false;
  if (doG)doGaussian=true;
  
}

void ChiNtuple::SetDoSysErr(const int & sys){
  doSysErr=sys;  
}

void ChiNtuple::SetAK4_SF(const bool & doak4){
  doAK4_sf=false;
  if (doak4)doAK4_sf=true;
  
}

void ChiNtuple::SetDataToMC_SF(const bool & doData){
  doDataToMC_sf=false;
  if (doData)doDataToMC_sf=true;
  
}

void ChiNtuple::SetNevents(const int & nev){
  Nevts=nev;  
}

int ChiNtuple::findLeading(const std::vector<double> jpt){
  int indx=-1;
  double ptmax=0.;
  for (uint i=0; i<jpt.size(); i++){
    if (jpt.at(i)> ptmax){
      ptmax=jpt.at(i);
      indx=i;
    }
  }
  return indx;
}

int ChiNtuple::findNextLeading(const std::vector<double> jpt, const uint i1){
  int indx=-1;
  double ptmax=0.;
  for (uint i=0; i<jpt.size(); i++){
    if (i==i1) continue;
    if (jpt.at(i)> ptmax){
      ptmax=jpt.at(i);
      indx=i;
    }
  }
  return indx;
}

void ChiNtuple::BookHistograms(const std::string & fname){

  Hlist = new TObjArray();

  outName=fname;
  
  std::cout << "Output written to: " << outName << std::endl;
  //outFile = new TFile::Open(outName.c_str(),"recreate");
  outFile = TFile::Open(outName.c_str(),"recreate");
  //outFile = new TFile();
  //outFile->Open(outName.c_str(),"recreate");
  outFile->cd();
  
  //myHist = new TH1F("h1","pt",100,0,1100);
  //Hlist->Add(myHist);
  // TCanvas c1("c1","c1",200,200);

  int nMass=80.;
  double minMass=0., maxMass=8000.;

  hname="dijet_mass"; htitle="M_{jj}";
  m_HistNames[hname] =  Book1dHist(hname,htitle,nMass,minMass,maxMass, true);

  hname="dijet_mass_trg"; htitle="M_{jj} w/ Trigger Eff";
  m_HistNames[hname] =  Book1dHist(hname,htitle,nMass,minMass,maxMass, true);
  
  hname="dijet_mass_gen"; htitle="M_{jj} Generated";  
  m_HistNames[hname] =  Book1dHist(hname,htitle,nMass,minMass,maxMass, true);

  hname="dijet_mass_smeared"; htitle="M_{jj} Smeared";  
  m_HistNames[hname] =  Book1dHist(hname,htitle,nMass,minMass,maxMass, true);

  hname="nevts"; htitle="Number of Events Processed";
  m_HistNames[hname] =  Book1dHist(hname, htitle, 1, -0.5, 0.5, false );

  hname="counter"; htitle="Cut counter";
  m_HistNames[hname] =  Book1dHist(hname, htitle, 10, -0.5, 9.5, false );
  
  hname="evtsHT"; htitle="Number of Events per HT Bin";
  m_HistNames[hname] =  Book1dHist(hname, htitle, 5, -1.5, 3.5, false );

  hname="evtsM"; htitle="Number of Events per Mass Bin";
  m_HistNames[hname] =  Book1dHist(hname, htitle, 11, -1.5, 9.5, false );

  hname="evtsPT"; htitle="Number of Events per PT Bin";
  m_HistNames[hname] =  Book1dHist(hname, htitle, 11, -1.5, 9.5, false );


  int njr=60;
  double jrmin=0.,jrmax=3.;

  int neta=20;
  double etamin=-5.,etamax=5.;

  hname="Resp"; htitle="Jet Response -- 300 < p_{T} Gen < 400,  |y| < 1.";
  m_HistNames[hname] =  Book1dHist(hname, htitle, njr, jrmin, jrmax, true );

  hname="SmrResp"; htitle="Smeared Jet Response -- 300 < p_{T} Gen < 400, |y| < 1." ;
  m_HistNames[hname] =  Book1dHist(hname, htitle, njr, jrmin, jrmax, true );

  hname="SmrResp2"; htitle="Smeared Jet Response -- 600 < p_{T} Gen < 800, |y| > 2." ;
  m_HistNames[hname] =  Book1dHist(hname, htitle, njr, jrmin, jrmax, true );
  
  hname="Resp3D"; htitle="Jet response vs pt,y";
  m_HistNames3D[hname]=Book3dHist(hname, htitle, 200, 0. ,2000., neta, etamin, etamax, njr, jrmin, jrmax, true);

  hname="SmrResp3D"; htitle="Smeared Jet response vs pt,y";
  m_HistNames3D[hname]=Book3dHist(hname, htitle, 200, 0. ,2000., neta, etamin, etamax, njr, jrmin, jrmax, true);

  Float_t mbins1[] = { 1000,1200,1500,1900,2400,3000,3600,4200,4800,13000};
  Int_t  nmbins1 = sizeof(mbins1)/sizeof(Float_t) - 1;

  Float_t mbins2[] = { 1000,1200,1500,1900,2400,3000,3600,4200,4800,5400,6000,8000,10000,13000};
  Int_t  nmbins2 = sizeof(mbins2)/sizeof(Float_t) - 1;
  
  Float_t chibins1[] = { 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
  Int_t  nchibins1 = sizeof(chibins1)/sizeof(Float_t) - 1;

  Float_t chibins2[] = { 1,2,3,4,5,6,7,8,9,10,12,14,16};
  Int_t  nchibins2 = sizeof(chibins2)/sizeof(Float_t) - 1;

  //Float_t chibins3[] = { 1,2,4,6,8,10,12,14,16};
  Float_t chibins3[] = {1,3,6,9,12,16};
  Int_t  nchibins3 = sizeof(chibins3)/sizeof(Float_t) - 1;

  Float_t chibins4[] = { 1,3,5,7,10,12,14,16};
  Int_t  nchibins4 = sizeof(chibins4)/sizeof(Float_t) - 1;

  for ( Int_t j = 0; j < (nmbins1+1); ++j )
    massBins1.push_back(mbins1[j]);

  for ( Int_t j = 0; j < (nmbins2+1); ++j )
    massBins2.push_back(mbins2[j]);
  
  for ( Int_t j = 0; j < (nchibins1+1); ++j )
    chiBins1.push_back(chibins1[j]);

  for ( Int_t j = 0; j < (nchibins2+1); ++j )
    chiBins2.push_back(chibins2[j]);

  for ( Int_t j = 0; j < (nchibins3+1); ++j )
    chiBins3.push_back(chibins3[j]);

  for ( Int_t j = 0; j < (nchibins4+1); ++j )
    chiBins4.push_back(chibins4[j]);

  
  dijet_mass1_chi1 = new TH2F("dijet_mass1_chi1","M_{jj} vs #chi",nmbins1,mbins1,nchibins1,chibins1);
  dijet_mass1_chi2 = new TH2F("dijet_mass1_chi2","M_{jj} vs #chi",nmbins1,mbins1,nchibins2,chibins2);
  dijet_mass1_chi3 = new TH2F("dijet_mass1_chi3","M_{jj} vs #chi",nmbins1,mbins1,nchibins3,chibins3);
  dijet_mass1_chi4 = new TH2F("dijet_mass1_chi4","M_{jj} vs #chi",nmbins1,mbins1,nchibins4,chibins4);  

  dijet_mass2_chi1 = new TH2F("dijet_mass2_chi1","M_{jj} vs #chi",nmbins2,mbins2,nchibins1,chibins1);
  dijet_mass2_chi2 = new TH2F("dijet_mass2_chi2","M_{jj} vs #chi",nmbins2,mbins2,nchibins2,chibins2);
  dijet_mass2_chi3 = new TH2F("dijet_mass2_chi3","M_{jj} vs #chi",nmbins2,mbins2,nchibins3,chibins3);
  dijet_mass2_chi4 = new TH2F("dijet_mass2_chi4","M_{jj} vs #chi",nmbins2,mbins2,nchibins4,chibins4);  

  
  dijet_mass1_chi1->Sumw2();
  dijet_mass1_chi2->Sumw2();
  dijet_mass1_chi3->Sumw2();
  dijet_mass1_chi4->Sumw2();
 
  dijet_mass2_chi1->Sumw2();
  dijet_mass2_chi2->Sumw2();
  dijet_mass2_chi3->Sumw2();
  dijet_mass2_chi4->Sumw2();
 
  Hlist->Add(dijet_mass1_chi1);        
  Hlist->Add(dijet_mass1_chi2);        
  Hlist->Add(dijet_mass1_chi3);        
  Hlist->Add(dijet_mass1_chi4);
  
  Hlist->Add(dijet_mass2_chi1);        
  Hlist->Add(dijet_mass2_chi2);        
  Hlist->Add(dijet_mass2_chi3);        
  Hlist->Add(dijet_mass2_chi4);        

  for ( size_t j = 0; j < (massBins1.size()-1); ++j )
  {
      std::stringstream name;
      name << "dijet_" << massBins1[j] << "_" << massBins1[j+1] << "_" << "chi";
      hists.push_back(new TH1F(name.str().c_str(),name.str().c_str(),15,1,16));
      hists[j]->Sumw2();
      Hlist->Add(hists[j]);

      if (!IsData){
	std::stringstream gname;
	gname << "dijet_" << massBins1[j] << "_" << massBins1[j+1] << "_" << "chi_gen";
	ghists.push_back(new TH1F(gname.str().c_str(),gname.str().c_str(),15,1,16));
	ghists[j]->Sumw2();
	Hlist->Add(ghists[j]);

	std::stringstream sname;	
	sname << "dijet_" << massBins1[j] << "_" << massBins1[j+1] << "_" << "chi_smr";
	shists.push_back(new TH1F(sname.str().c_str(),sname.str().c_str(),15,1,16));
	shists[j]->Sumw2();
	Hlist->Add(shists[j]);
      }
  }

  for ( size_t j = 0; j < (chiBins1.size()-1); ++j )
  {
      std::stringstream name;
      name << "dijet_" << chiBins1[j] << "_chi1_" << chiBins1[j+1] << "_" << "mass1";
      mhists.push_back(new TH1F(name.str().c_str(),name.str().c_str(),nmbins1,mbins1));
      mhists[j]->Sumw2();
      Hlist->Add(mhists[j]);
  }

  
  _outTree = new TTree("DijetTree", "");
  Hlist->Add(_outTree);
  
  _outTree->Branch("XSweight",   &XSweight  ,  "XSweight/F");
  _outTree->Branch("EVTweight",   &EVTweight  ,  "EVTweight/F");
  _outTree->Branch("Event",   &Event  ,  "Event/I");
  _outTree->Branch("Run",   &Run  ,  "Run/I");
  _outTree->Branch("Lumi",  &Lumi ,  "Lumi/I");
  _outTree->Branch("IsData",  &IsData ,  "IsData/I");
  _outTree->Branch("HTBin",  &HTBin ,  "HTBin/I");
  _outTree->Branch("MBin",   &MBin ,   "MBin/I");
  _outTree->Branch("PTBin",  &PTBin ,  "PTBin/I");
  
  _outTree->Branch("recoDijets", &recoDijets, "dijetFlag/I:mass/F:pt/F:chi/F:yboost/F:pt1/F:eta1/F:phi1/F:e1/F:pt2/F:eta2/F:phi2/F:e2/F");
  _outTree->Branch("genDijets",  &genDijets , "dijetFlag/I:mass/F:pt/F:chi/F:yboost/F:pt1/F:eta1/F:phi1/F:e1/F:pt2/F:eta2/F:phi2/F:e2/F");
  _outTree->Branch("smrDijets",  &smrDijets , "dijetFlag/I:mass/F:pt/F:chi/F:yboost/F:pt1/F:eta1/F:phi1/F:e1/F:pt2/F:eta2/F:phi2/F:e2/F");
  
}

void ChiNtuple::WriteHistograms(){

  outFile->cd();
  Hlist->Write();
  outFile->Close();
}

void ChiNtuple::fillHist(const TString& histName, const Double_t& value, const Double_t& wt) {

  hid=m_HistNames.find(histName);
  if (hid==m_HistNames.end())
    std::cout << "%fillHist -- Could not find histogram with name: " << histName << std::endl;
  else
    hid->second->Fill(value,wt); 

}

void ChiNtuple::fill3DHist(const TString& histName, const Double_t& x,const Double_t& y,const Double_t& z,const Double_t& wt) {

  hid3D=m_HistNames3D.find(histName);
  if (hid3D==m_HistNames3D.end())
    std::cout << "%fillHist -- Could not find histogram with name: " << histName << std::endl;
  else
    hid3D->second->Fill(x,y,z,wt); 

}

TH1F* ChiNtuple::Book1dHist(const char* name, const char* title, Int_t nbins, Double_t xmin, Double_t xmax,bool DoSumw2=true){


  TH1F *h= new TH1F(name, title, nbins, xmin, xmax); 
  Hlist->Add(h);

  if (DoSumw2) h->Sumw2();

  return h;
}

TH2F* ChiNtuple::Book2dHist(const char* name, const char* title, Int_t nbinsx, Double_t xmin, Double_t xmax,
		 Int_t nbinsy, Double_t ymin, Double_t ymax, bool DoSumw2=true){


  TH2F *h= new TH2F(name, title, nbinsx, xmin, xmax, nbinsy, ymin, ymax); 
  Hlist->Add(h);
  
  if (DoSumw2) h->Sumw2();

  return h;
}

TH3F* ChiNtuple::Book3dHist(const char* name, const char* title, Int_t nbinsx, Double_t xmin, Double_t xmax , 
		 Int_t nbinsy, Double_t ymin, Double_t ymax , Int_t nbinsz, Double_t zmin, 
		 Double_t zmax , bool DoSumw2=true){

  TH3F *h= new TH3F(name, title, nbinsx, xmin, xmax, nbinsy, ymin, ymax, nbinsz, zmin, zmax);
  Hlist->Add(h);  
  if (DoSumw2) h->Sumw2();

  return h;
}

double ChiNtuple::TriggerEff(double mass, double chi){
  double eff=1.; 
  if (!IsData) return eff;
  if (mass<1000.) return eff;
  
  double par[] { 0, 0., 0. }; 
  if ( chi <= 2){
    par[0] = 1.0;
    par[1] = 796.928610698;
    par[2] = 77.1506076781;
  }else if ( chi <= 4){
    par[0] = 1.0;
    par[1] = 886.176274484;
    par[2] = 119.74926938;
  }else if ( chi <= 6){
    par[0] = 1.0;
    par[1] = 1034.43359036;
    par[2] = 129.769721544;
  }else if ( chi <= 10){
    par[0] = 1.0;
    par[1] = 1221.16044494;
    par[2] = 176.482231463;
  }else if ( chi <= 12){
    par[0] = 1.0;
    par[1] = 1393.81742045;
    par[2] = 174.130748889;
  }else if ( chi <= 14){
    par[0] = 1.0;
    par[1] = 1510.93614717;
    par[2] = 163.404589511;
  }else if ( chi <= 16){
    par[0] = 1.0;
    par[1] = 1569.32715144;
    par[2] = 237.517019129;
  }else{
    return eff.
  }
    

  double xx=mass;
  if (xx<1500.) xx=1500.;
  
  eff=par[0]/2.+par[0]/2.*TMath::Erf((xx-par[1])/par[2]);
  return eff;
  
}

double ChiNtuple::SmearFunc(double mean, double eta, double p0, double p1, double p2,double sf){
  double sigma=0;
  
  bool addSmear=true; // additional data/mc smearing

  sigma = mean*(sqrt(pow(p0,2)+pow((p1/sqrt(mean)),2)+pow((p2/mean),2)));

  sigma=sigma*sf; // sf is additional scale factor for ak4/ak5 differences

  double errPlus=1.;
  double errMinus=1.;

  if (addSmear){ // additional smearing to account for data/mc differences
    if (eta < 0.5) {
      sigma   = sigma*1.052;
      errPlus=1.+sqrt(0.012*0.012+0.062*0.062);
      errMinus=1.-sqrt(0.012*0.012+0.061*0.061);
    } 
    else if (eta < 1.1) {
      sigma   = sigma*1.057;
      errPlus=1.+sqrt(0.012*0.012+0.056*0.056);
      errMinus=1.-sqrt(0.012*0.012+0.055*0.055);
    } 
    else if (eta < 1.7) {
      sigma   = sigma*1.096;
      errPlus=1.+sqrt(0.017*0.017+0.063*0.063);
      errMinus=1.-sqrt(0.017*0.017+0.062*0.062);
    }
    else if (eta < 2.3) {
      sigma   = sigma*1.134;
      errPlus=1.+sqrt(0.035*0.035+0.087*0.087);
      errMinus=1.-sqrt(0.035*0.035+0.085*0.085);
    }
    else if (eta < 3) {
      sigma   = sigma*1.288;
      errPlus=1.+sqrt(0.127*0.127+0.155*0.155);
      errMinus=1.-sqrt(0.127*0.127+0.153*0.153);
    }
  }
  
  bool doSys = false;
  if (doSys){
    bool errplus =true;
    if (errplus){
      sigma=sigma*errPlus;
    }else{
      sigma=sigma*errMinus;
    }
  }

  //sigma=sigma*1.05
  // std::cout << "mean/p0/p1/p2  sigma: " << mean << " " << p0 << " " << p1 << " " << p2 << " " << sigma << std::endl; 
  double r = rnd.Gaus(mean,sigma);
  return r/mean; 
}

double ChiNtuple::SmearFactor(double pt,double eta, double scaleFactor){

  double sf=scaleFactor;
  double smf_e=1.;
  if (eta < 0.5) {
    smf_e   = SmearFunc(pt,eta,2.87265e-02,1.01485e+00,5.25613e+00,sf);
  } 
  else if (eta < 1.0) {
    smf_e   = SmearFunc(pt,eta,3.43555e-02,9.49218e-01,5.92528e+00,sf);
  } 
  else if (eta < 1.5) {
    smf_e   = SmearFunc(pt,eta,3.95103e-02,1.00204e+00,6.07558e+00,sf);
  }
  else if (eta < 2.0) {
    smf_e   = SmearFunc(pt,eta,1.42866e-02,8.48049e-01,6.67823e+00,sf);
  }
  else if (eta < 2.5) {
    smf_e   = SmearFunc(pt,eta,1.34450e-02,7.14309e-01,6.77620e+00,sf);
  }
  else if (eta < 3.0) {
    smf_e   = SmearFunc(pt,eta,2.08877e-07,8.59187e-01,6.84957e+00,sf);
  }  
  return smf_e;
}
 
#endif
