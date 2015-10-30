//////////////////////////////////////

#ifndef ChiNtuple_h
#define ChiNtuple_h

#include <vector>
#include <string>
#include <iostream>
#include <fstream>

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

#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/PythonParameterSet/interface/MakeParameterSets.h"

#include "CondFormats/JetMETObjects/interface/JetResolution.h"

// #include <TCanvas.h>

using std::cout;
using std::endl;
using std::string;
using std::vector;

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
  bool CheckFirstFile();
  bool OpenInputFiles();
  bool OpenNtupleList(const std::string & fname);
  std::vector<std::string> listNtuples;
  Long64_t nentries_;
  TFile* rf;

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
  
};

ChiNtuple::ChiNtuple(){}
ChiNtuple::~ChiNtuple(){
  delete fChain;
}

bool ChiNtuple::OpenInputFiles()
{
  fChain     = new TChain("ntuplizer/tree");

  for (unsigned int i=0;i<listNtuples.size();i++)
  {
    std::cout << " -- Adding to chain: " << listNtuples[i] << std::endl;
    fChain->Add(listNtuples[i].c_str());
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

void ChiNtuple::SetXSWeight(const double & wt){
  if (wt<0) std::cout << "Negative XS given.  This will not end well..." << std::endl;
  xsweight=wt;
  
}
void ChiNtuple::BookHistograms(const std::string & fname){

  Hlist = new TObjArray();

  outName=fname;
  
  std::cout << "Output written to: " << outName << std::endl;
  outFile = new TFile(outName.c_str(),"recreate");
  outFile->cd();
  
  //myHist = new TH1F("h1","pt",100,0,1100);
  //Hlist->Add(myHist);


  Float_t mbins[] = { 1000,1200,1500,1900,2400,3000,3600,4200,8000};
  Int_t  nmbins = sizeof(mbins)/sizeof(Float_t) - 1;

  // Float_t chibins[] = { 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
  // Int_t  nchibins = sizeof(chibins)/sizeof(Float_t) - 1;

  std::vector<double> massBins;
  for ( Int_t j = 0; j < (nmbins+1); ++j )
    massBins.push_back(mbins[j]);


  // TCanvas c1("c1","c1",200,200);

  int nMass=80.;
  double minMass=0., maxMass=8000.;

  hname="dijet_mass"; htitle="M_{jj}";
  m_HistNames[hname] =  Book1dHist(hname,htitle,nMass,minMass,maxMass, true);

  hname="dijet_mass_gen"; htitle="M_{jj} Generated";  
  m_HistNames[hname] =  Book1dHist(hname,htitle,nMass,minMass,maxMass, true);

  hname="dijet_mass_smeared"; htitle="M_{jj} Smeared";  
  m_HistNames[hname] =  Book1dHist(hname,htitle,nMass,minMass,maxMass, true);

  hname="nevts"; htitle="Number of Events Processed";
  m_HistNames[hname] =  Book1dHist(hname, htitle, 1, -0.5, 0.5, false );

  hname="evtsHT"; htitle="Number of Events per HT Bin";
  m_HistNames[hname] =  Book1dHist(hname, htitle, 5, -1.5, 3.5, false );

  hname="evtsM"; htitle="Number of Events per Mass Bin";
  m_HistNames[hname] =  Book1dHist(hname, htitle, 5, -1.5, 3.5, false );

  hname="evtsPT"; htitle="Number of Events per PT Bin";
  m_HistNames[hname] =  Book1dHist(hname, htitle, 9, -1.5, 7.5, false );


  int njr=60;
  double jrmin=0.,jrmax=3.;

  int neta=20;
  double etamin=-5.,etamax=5.;

  hname="Resp"; htitle="Jet Response -- 300 < p_{T} Gen < 400,  |y| < 1.";
  m_HistNames[hname] =  Book1dHist(hname, htitle, njr, jrmin, jrmax, true );

  hname="SmrResp"; htitle="Smeared Jet Response -- 300 < p_{T} Gen < 300, |y| < 1." ;
  m_HistNames[hname] =  Book1dHist(hname, htitle, njr, jrmin, jrmax, true );

  hname="Resp3D"; htitle="Jet response vs pt,y";
  m_HistNames3D[hname]=Book3dHist(hname, htitle, 200, 0. ,2000., neta, etamin, etamax, njr, jrmin, jrmax, true);

  hname="SmrResp3D"; htitle="Smeared Jet response vs pt,y";
  m_HistNames3D[hname]=Book3dHist(hname, htitle, 200, 0. ,2000., neta, etamin, etamax, njr, jrmin, jrmax, true);


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

  if (DoSumw2) h->Sumw2();

  return h;
}

TH3F* ChiNtuple::Book3dHist(const char* name, const char* title, Int_t nbinsx, Double_t xmin, Double_t xmax , 
		 Int_t nbinsy, Double_t ymin, Double_t ymax , Int_t nbinsz, Double_t zmin, 
		 Double_t zmax , bool DoSumw2=true){

  TH3F *h= new TH3F(name, title, nbinsx, xmin, xmax, nbinsy, ymin, ymax, nbinsz, zmin, zmax); 
  if (DoSumw2) h->Sumw2();

  return h;
}

#endif
