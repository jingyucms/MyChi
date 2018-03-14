#include <TH1F.h>
#include <TH2F.h>
#include <TH3F.h>
#include <TROOT.h>
#include <TFile.h>
#include <TSystem.h>
#include "TRandom.h"
#include <TLorentzVector.h>
#include <TTree.h>

#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/FWLite/interface/AutoLibraryLoader.h"

#include "DataFormats/FWLite/interface/InputSource.h"
#include "DataFormats/FWLite/interface/OutputFiles.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/PythonParameterSet/interface/MakeParameterSets.h"

#include "PhysicsTools/FWLite/interface/TFileService.h"

#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/JetReco/interface/GenJet.h"

#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/WeightsInfo.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "CondFormats/JetMETObjects/interface/JetResolution.h"

#include "MyChi/ChiAnalysis/interface/MyJetResponse.h"

TRandom rnd;

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

double SmearFunc(double, double, double, double, bool, bool);
double SmearMass(double, double);
double SmearMassFunc(double, double, double, double);
double SmearFactor(double, double, bool, bool);
std::vector <TLorentzVector> sortJets(const std::vector <TLorentzVector>);

int findLeading(const std::vector<double> );
int findNextLeading(const std::vector<double>, const uint );

class PtGreater {
  public:
  template <typename T> bool operator () (const T& i, const T& j) {
    return (i.Pt() > j.Pt());
  }
};

typedef struct
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
} DijetInfo;

using namespace std;
int main(int argc, char* argv[]) 
{
  // define what muon you are using; this is necessary as FWLite is not 
  // capable of reading edm::Views


  // ----------------------------------------------------------------------
  // First Part: 
  //
  //  * enable the AutoLibraryLoader 
  //  * book the histograms of interest 
  //  * open the input file
  // ----------------------------------------------------------------------

  // load framework libraries
  gSystem->Load( "libFWCoreFWLite" );
  AutoLibraryLoader::enable();

  // parse arguments
  if ( argc < 2 ) {
    std::cout << "Usage : " << argv[0] << " [parameters.py]" << std::endl;
    return 0;
  }

  if( !edm::readPSetsFrom(argv[1])->existsAs<edm::ParameterSet>("process") ){
    std::cout << " ERROR: ParametersSet 'process' is missing in your configuration file" << std::endl; exit(0);
  }
  // get the python configuration
  const edm::ParameterSet& process = edm::readPSetsFrom(argv[1])->getParameter<edm::ParameterSet>("process");
  fwlite::InputSource inputHandler_(process); fwlite::OutputFiles outputHandler_(process);

  bool Debug_=false;
  // now get each parameter
  const edm::ParameterSet& ana = process.getParameter<edm::ParameterSet>("GenChiAnalysis");
  edm::InputTag GenJetCollection_( ana.getParameter<edm::InputTag>("GenJets") );
  edm::InputTag LHEEventProduct_(ana.getParameter<edm::InputTag>("Source"));
  double XS_( ana.getParameter<double>("CrossSection") );
  string SMEARING_( ana.getParameter<string>("Smearing") );
  bool doAK4_sf( ana.getParameter<bool>("AK4_SF") );
  bool doDataToMC_sf( ana.getParameter<bool>("DATAtoMC_SF") );  
  double smearMax_( ana.getParameter<double>("SmearMax") );
  bool doSys_( ana.getParameter<bool>("doSys") );
  bool sysPlus_( ana.getParameter<bool>("sysPlus") );
  bool dmWeight_( ana.getParameter<bool>("dmWeight") );
  // book a set of histograms
  string outFile=outputHandler_.file().c_str();
  cout << "Output written to: " << outFile << endl;
  fwlite::TFileService fs = fwlite::TFileService(outFile);
  TFileDirectory dir = fs.mkdir("chiAnalysis");
  TFile* OutFile = TFile::Open(outputHandler_.file().c_str(),"RECREATE");
  OutFile->cd();

  //cout<<"debug0"<<endl;

  if (SMEARING_ == "Gaussian") smearMax_=100.;

  TString hname,htitle;
  TH1::SetDefaultSumw2();

  //---------------------------------------------------------------------------
  // Declare histograms
  //---------------------------------------------------------------------------


  Float_t mbins[] = { 1000,1200,1500,1900,2400,3000,3600,4200,8000};
  UInt_t  nmbins = sizeof(mbins)/sizeof(Float_t) - 1;

  //Float_t chibins[] = { 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
  //Int_t  nchibins = sizeof(chibins)/sizeof(Float_t) - 1;

  std::vector<double> massBins;
  for ( size_t j = 0; j < (nmbins+1); ++j )
    massBins.push_back(mbins[j]);


  // TCanvas c1("c1","c1",200,200);

  int nMass=80.;
  double minMass=0., maxMass=8000.;

  TH1F* h1=new TH1F("dijet_mass","M_{jj}",nMass,minMass,maxMass);
  h1->Sumw2();

  TH1F* g1=new TH1F("dijet_mass_gen","M_{jj} Generated",nMass,minMass,maxMass);
  g1->Sumw2();

  TH1F* s1=new TH1F("dijet_mass_smeared","M_{jj} Smeared",nMass,minMass,maxMass);
  s1->Sumw2();

  hname="nevts"; htitle="Number of Events Processed";
  m_HistNames[hname] =  Book1dHist(hname, htitle, 1, -0.5, 0.5, false );

  hname="evtsHT"; htitle="Number of Events per HT Bin";
  m_HistNames[hname] =  Book1dHist(hname, htitle, 11, -1.5, 9.5, false );

  hname="evtsPT"; htitle="Number of Events per PT Bin";
  m_HistNames[hname] =  Book1dHist(hname, htitle, 11, -1.5, 9.5, false );

  hname="evtsM"; htitle="Number of Events per Mass Bin";
  m_HistNames[hname] =  Book1dHist(hname, htitle, 11, -1.5, 9.5, false );

  hname="nGenJet"; htitle="Number of GenJets";
  m_HistNames[hname] =  Book1dHist(hname, htitle, 10, -0.5, 9.5, false );


  DijetInfo recoDijets,genDijets,smrDijets;

  TTree *_outTree;
  Float_t XSweight;
  Float_t EVTweight;
  //Float_t PU_Num;
  //Float_t True_Num;
  Int_t Event;
  Int_t Run;
  Int_t Lumi;
  Int_t IsData;
  Int_t HTBin(-1);
  Int_t PTBin(-1);
  Int_t MBin(-1);

  std::map<string,float> dmWeights;
  Float_t dmXsec;

  OutFile->cd();
  _outTree = new TTree("DijetTree", "DijetTree");
  
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

  _outTree->Branch("dmWeights", &dmWeights);
  _outTree->Branch("dmXsec",&dmXsec);

  // ccla Setup the smearing
  bool     doPTSmearing(true); // set to false to smear in eta & phi (I don't think this option works correctly presently)

  string   era("Spring10");
  string   alg("AK5PF");
  bool     doGaussian(false); // set to true only if you want to do Gaussian smearing using the JetResolution TF1 setup instead of Crystall ball smearing

  cout<<"era:           "<<era<<endl;
  cout<<"alg:           "<<alg<<endl;
  cout<<"Smearing:      "<<SMEARING_<<endl;
  cout<<"DoSys:         "<<doSys_ << "\tSysPlus: " << sysPlus_<<endl;
  cout<<"AK4_sf:        "<<doAK4_sf<<endl;
  cout<<"DataToMC_sf:   "<<doDataToMC_sf<<endl<<endl;  
  cout<<"Cross Section: "<<XS_<<endl<<endl;

  
  string cmssw_base(getenv("CMSSW_BASE"));
  string cmssw_release_base(getenv("CMSSW_RELEASE_BASE"));
  //string path = cmssw_release_base + "/src/CondFormats/JetMETObjects/data";
  string path = cmssw_base + "/src/CondFormats/JetMETObjects/data";

  string ptFileName  = path + "/" + era + "_PtResolution_" +alg+".txt";
  string etaFileName = path + "/" + era + "_EtaResolution_"+alg+".txt";
  string phiFileName = path + "/" + era + "_PhiResolution_"+alg+".txt";

  cout<<ptFileName<<endl;
  cout<<etaFileName<<endl;
  cout<<phiFileName<<endl;
  cout<<endl;

  JetResolution ptResol(ptFileName,doGaussian);
  JetResolution etaResol(etaFileName,doGaussian);
  JetResolution phiResol(phiFileName,doGaussian);

  // TF1 *fPtResol;
  TF1 *fetaResol, *fphiResol;

  int doSysErr(0);
  if (doSys_){
    if (sysPlus_){
      doSysErr=1;
    }else{
      doSysErr=-1;
    }
  }
  MyJetResponse jetresponse(doAK4_sf,doDataToMC_sf,doSysErr);  
  jetresponse.GetResolutionParameters(ptFileName,doGaussian);
  
  // CCLA done with smearing setup

  std::vector<double>	smrjet_energy(0,0);
  std::vector<double>	smrjet_et(0,0);
  std::vector<double>	smrjet_pt(0,0);
  std::vector<double>	smrjet_eta(0,0);
  std::vector<double>	smrjet_phi(0,0);
  std::vector<double>	smrjet_rapidity(0,0);
  std::vector<double>	smrjet_nConstituents(0,0);

  // loop the events
  int ievt=0;  
  int maxEvents_( inputHandler_.maxEvents() );
  for(unsigned int iFile=0; iFile<inputHandler_.files().size(); ++iFile){
    // open input file (can be located on castor)
    string inputFile=inputHandler_.files()[iFile];
    cout << "File: " << inputFile << endl;
    TFile* inFile = TFile::Open(inputHandler_.files()[iFile].c_str());
    if( inFile ){
      // ----------------------------------------------------------------------
      // Second Part: 
      //
      //  * loop the events in the input file 
      //  * receive the collections of interest via fwlite::Handle
      //  * fill the histograms
      //  * after the loop close the input file
      // ----------------------------------------------------------------------


      std::vector<string> htBins, ptBins, mBins;
      // htBins.push_back("100To250");
      // htBins.push_back("250To500");
      // htBins.push_back("500To1000");
      // htBins.push_back("1000ToInf");
      htBins.push_back("HT300to500");
      htBins.push_back("HT500to700");
      htBins.push_back("HT700to1000");
      htBins.push_back("HT1000to1500");
      htBins.push_back("HT1500to2000");
      htBins.push_back("HT2000toInf");

      ptBins.push_back("m900_1400");
      ptBins.push_back("m1400_2500");
      ptBins.push_back("m2500_3700");
      ptBins.push_back("m3700_8000");

      mBins.push_back("m1000_1500");
      mBins.push_back("m1500_1900");
      mBins.push_back("m1900_2400");
      mBins.push_back("m2400_2800");
      mBins.push_back("m2800_3300");
      mBins.push_back("m3300_3800");
      mBins.push_back("m3800_4300");
      mBins.push_back("m4300_13000");

      int htBin=-1;
      for (uint i=0; i<htBins.size(); ++ i){
	string stringToFind= htBins.at(i) ;
	std::size_t found = inputFile.find(stringToFind);
	if (found != std::string::npos){
	  htBin=i;
	  break;
	}
      }
      if (htBin==-1){
	std::cout << "HT Bin not found in input file name"  << std::endl;
      }
      HTBin=htBin;


      int ptBin=-1;
      for (uint i=0; i<ptBins.size(); ++ i){
	string stringToFind= ptBins.at(i) ;
	std::size_t found = inputFile.find(stringToFind);
	if (found != std::string::npos){
	  ptBin=i;
	  break;
	}
      }
      if (ptBin==-1){
	std::cout << "PT Bin not found in input file name"  << std::endl;
      }
      PTBin=ptBin;


      int mBin=-1;
      for (uint i=0; i<mBins.size(); ++ i){
	string stringToFind= mBins.at(i) ;
	std::size_t found = inputFile.find(stringToFind);
	if (found != std::string::npos){
	  mBin=i;
	  break;
	}
      }
      if (mBin==-1){
	std::cout << "Mass Bin not found in input file name"  << std::endl;
      }
      MBin=mBin;

      
      fwlite::Event ev(inFile);

      std::cout<< "Number of events in sample: " << ev.size() << std::endl;

      for(ev.toBegin(); !ev.atEnd(); ++ev, ++ievt){
	edm::EventBase const & event = ev;
	// break loop if maximal number of events is reached 
	if(maxEvents_>0 ? ievt+1>maxEvents_ : false) break;
	// simple event counter
	if(inputHandler_.reportAfter()!=0 ? (ievt>0 && ievt%inputHandler_.reportAfter()==0) : false) 
	  std::cout << "  processing event: " << ievt << std::endl;
	
	// Handle to the genjet collection
	edm::Handle<reco::GenJetCollection>  genJets;
	event.getByLabel( GenJetCollection_, genJets );
	
	edm::Handle<LHEEventProduct> EvtProd;
	event.getByLabel(LHEEventProduct_, EvtProd);

	std::vector<gen::WeightsInfo> weightsInfo=EvtProd->weights();

	if (genJets.isValid()){
	  if (Debug_)std::cout << "genJets size: " << genJets->size() << std::endl;
	}
	else {
	  std::cout << "Problem accessing genJet collection" << std::endl;

	}
	fillHist("nevts",0.,1.);
	int ngenjet=genJets->size();
	fillHist("nGenJet",ngenjet,1.);


	fillHist("evtsHT",float(HTBin),1.);
	fillHist("evtsPT",float(PTBin),1.);
	fillHist("evtsM",float(MBin),1.);
	
	XSweight=XS_;
	EVTweight=1.;
	Event=1.;
	Run=1.;
	Lumi=1.;
	//PU_Num=1.;
	//True_Num=1.;
	IsData=false;

	if (dmWeight_){
	  for (std::vector<gen::WeightsInfo>::const_iterator it=weightsInfo.begin(); it!=weightsInfo.end(); ++it)
	    dmWeights[it->id]=it->wgt;
	  dmXsec=EvtProd->originalXWGTUP()*1000;
	}
	else{
	  dmWeights["No_Evt_Weight"]=1.;
	  dmXsec=1.;
	}

	double initval=-999.;
	genDijets.dijetFlag=0;
	genDijets.mass=initval;
	genDijets.pt=initval;
	genDijets.chi=initval;
	genDijets.yboost=initval;
	genDijets.pt1=initval;
	genDijets.eta1=initval;
	genDijets.phi1=initval;
	genDijets.e1=initval;
	genDijets.pt2=initval;
	genDijets.eta2=initval;
	genDijets.phi2=initval;
	genDijets.e2=initval;

	smrDijets.dijetFlag=0;
	smrDijets.mass=initval;
	smrDijets.pt=initval;
	smrDijets.chi=initval;
	smrDijets.yboost=initval;
	smrDijets.pt1=initval;
	smrDijets.eta1=initval;
	smrDijets.phi1=initval;
	smrDijets.e1=initval;
	smrDijets.pt2=initval;
	smrDijets.eta2=initval;
	smrDijets.phi2=initval;
	smrDijets.e2=initval;

	recoDijets.dijetFlag=0;
	recoDijets.mass=initval;
	recoDijets.pt=initval;
	recoDijets.chi=initval;
	recoDijets.yboost=initval;
	recoDijets.pt1=initval;
	recoDijets.eta1=initval;
	recoDijets.phi1=initval;
	recoDijets.e1=initval;
	recoDijets.pt2=initval;
	recoDijets.eta2=initval;
	recoDijets.phi2=initval;
	recoDijets.e2=initval;

	if (genJets->size() > 1){
	  // reco::GenJetCollection::const_iterator j1=genJets->begin(),j2=genJets->begin()+1;

	  std::vector<double>	genjet_energy;
	  std::vector<double>	genjet_et;
	  std::vector<double>	genjet_pt;
	  std::vector<double>	genjet_eta;
	  std::vector<double>	genjet_phi;
	  std::vector<double>	genjet_mass;
	  std::vector<double>	genjet_rapidity;
	  std::vector<double>	genjet_nConstituents;

	  for(reco::GenJetCollection::const_iterator j=genJets->begin(); j!=genJets->end(); ++j){
	    genjet_energy.push_back(j->energy());
	    genjet_et.push_back(j->et());
	    genjet_pt.push_back(j->pt());
	    genjet_eta.push_back(j->eta());
	    genjet_phi.push_back(j->phi());
	    genjet_mass.push_back(j->mass());
	    genjet_rapidity.push_back(j->rapidity());
	    genjet_nConstituents.push_back(j->nConstituents());
	  }
	  // std::cout << "genJets size: " << genjet_energy.size() << std::endl;

	  float weight=1.;
	  smrjet_energy.clear();
	  smrjet_et.clear();
	  smrjet_pt.clear();
	  smrjet_eta.clear();
	  smrjet_phi.clear();
	  smrjet_rapidity.clear();
	  smrjet_nConstituents.clear();

	  vector<TLorentzVector> smearedJets;

	    // smear the genjets

	  for (uint genj=0; genj<genjet_pt.size(); ++ genj){
	    double genpt=genjet_pt[genj];
	    double geneta=genjet_eta[genj];

	    double fact=1.,etaSmear=1.,phiSmear=1.;
	    if (genpt >10.){

	      if (doPTSmearing){
	      
		if (SMEARING_ == "Gaussian"){
		  //fact=SmearFactor(genpt,std::abs(geneta),doSys_,sysPlus_);  // Suvadeep"s Gaussian smearing
		  fact=jetresponse.doGaussianSmearing(genpt,geneta);
		  // std::cout <<  genpt << "\t" << geneta << "\t" << fact << std::endl;
		}else if (SMEARING_ == "CrystalBall"){
		  fact=10.;
		  if (smearMax_ >= fact) fact = smearMax_+1.;
		  int nloop=0;
		  while (fact>smearMax_){
		    //fPtResol  = ptResol.resolutionEtaPt(geneta,genpt);
		    //fact = fPtResol ->GetRandom();
		    fact=jetresponse.doCrystalBallSmearing(genpt,geneta);		    
		    nloop++;
		    if (nloop>10) break;
		  }
		  if (fact>smearMax_) {
		    std::cout << "%%Too large smearing factor: " << fact << " genpt=  " << genpt << std::endl;
		    // revert to simple guaussian smearing
		    fact=1.;
		    std::cout << "\tReverting to gaussian smearing. Factor= " << fact << std::endl;
		  }		  
		}else{
		  std::cout << "Undefined Smearing -- " << SMEARING_ << " -- Exiting program" << std::endl;
		  return 1;
		}

	      }else{
		fetaResol  = etaResol.resolutionEtaPt(geneta,genpt);
		etaSmear = fetaResol ->GetRandom();
		fphiResol  = phiResol.resolutionEtaPt(geneta,genpt);
		phiSmear = fphiResol ->GetRandom();
	      }
	    }
	    // fact=1.;
	    // check that the genjets are ordered in pT
	    if (genj<genjet_pt.size()-1){
	      if (genjet_pt[genj+1] > genpt)
		std::cout << "Generated jets not ordered pt1/pt2: " << genpt << " / " << genjet_pt[genj+1] << std::endl;
	    }
	    TLorentzVector jetP4,smrP4;
	    jetP4.SetPtEtaPhiE(genjet_pt[genj],genjet_eta[genj],genjet_phi[genj],genjet_energy[genj]);

	    //std::cout << "Rapidities: " << genjet_rapidity[genj] << " " << jetP4.Rapidity() << std::endl;
	    double px=jetP4.Px();
	    double py=jetP4.Py();
	    double pz=jetP4.Pz();
	    double e=jetP4.Energy();

	    if (doPTSmearing){
	      smrP4.SetPxPyPzE(px*fact,py*fact,pz*fact,e*fact);
	    }else{
	      smrP4.SetPtEtaPhiE(genjet_pt[genj],etaSmear+genjet_eta[genj],phiSmear+genjet_phi[genj],genjet_energy[genj]);
	      //smrP4.SetPtEtaPhiE(genjet_pt[genj],genjet_eta[genj],genjet_phi[genj],genjet_energy[genj]);
	    }
	    smearedJets.push_back(smrP4);

	    double spt=smrP4.Pt();
	    double seta=smrP4.Eta();
	    double sphi=smrP4.Phi();
	    double se=smrP4.Energy();
	    double set=smrP4.Et();
	    double sy=smrP4.Rapidity();

	    // std::cout << "\nGenerated 4 vec: " << genpt << " " << geneta << " " << genjet_phi[genj] << " " << genjet_energy[genj] << std::endl;
	    // std::cout << "Smeared 4 vec  : " << spt << " " << seta << " " << sphi << " " << se << std::endl;
	    smrjet_energy.push_back(se);
	    smrjet_et.push_back(set);
	    smrjet_pt.push_back(spt);
	    smrjet_eta.push_back(seta);
	    smrjet_phi.push_back(sphi);
	    smrjet_rapidity.push_back(sy);
	    smrjet_nConstituents.push_back(genjet_nConstituents[genj]);
	  }
	  
	  smearedJets=sortJets(smearedJets);
	  // check the sorting
	  for (uint ijet=0; ijet<smearedJets.size()-1; ijet++){
	    double pt1=smearedJets.at(ijet).Pt();
	    double pt2=smearedJets.at(ijet+1).Pt();
	    if (pt2 > pt1) std::cout << "Smeared jets not ordered pt1/pt2: " << pt1 << " / " << pt2 << std::endl;
	  }

	  bool selectGen=(genjet_pt.size()>=2)&&
	    (genjet_pt[0]>30)&&
	    (genjet_pt[1]>30)&&
	    (fabs(genjet_rapidity[0])<2.5)&&
	    (fabs(genjet_rapidity[1])<2.5)&&
	    (fabs(genjet_rapidity[0]+genjet_rapidity[1])/2.<1.11)&&
	    (exp(fabs(genjet_rapidity[0]-genjet_rapidity[1]))<16)&&	     
	    (genjet_nConstituents[0]>1)&&	     
	    (genjet_nConstituents[1]>1);
	  
	  if(selectGen)
	    {
	      // fill genjets
	      TLorentzVector j1P4,j2P4,dijet;
	      j1P4.SetPtEtaPhiE(genjet_pt[0],genjet_eta[0],genjet_phi[0],genjet_energy[0]);
	      j2P4.SetPtEtaPhiE(genjet_pt[1],genjet_eta[1],genjet_phi[1],genjet_energy[1]);
	      dijet=j1P4+j2P4;
	      double invmass=dijet.M();
	      g1->Fill(invmass,weight);

	      genDijets.dijetFlag=1;
	      genDijets.mass=invmass;
	      genDijets.pt=dijet.Pt();
	      genDijets.chi=exp(fabs(genjet_rapidity[0]-genjet_rapidity[1]));
	      genDijets.yboost=fabs(genjet_rapidity[0]+genjet_rapidity[1])/2.;
	      genDijets.pt1= genjet_pt[0];
	      genDijets.eta1=genjet_eta[0];
	      genDijets.phi1=genjet_phi[0];
	      genDijets.e1=  genjet_energy[0];
	      genDijets.pt2= genjet_pt[1];
	      genDijets.eta2=genjet_eta[1];
	      genDijets.phi2=genjet_phi[1];
	      genDijets.e2=  genjet_energy[1];

	      for ( size_t j = 0; j < (massBins.size()-1); ++j )
		{
		  if((invmass>=massBins[j])&&
		     (invmass<massBins[j+1]))
		    {
		      // ghists[j]->Fill(exp(fabs(genjet_rapidity[0]-genjet_rapidity[1])), weight);
		      //histspt1[j]->Fill(jethelper2_pt[0], weight);
		      //histspt2[j]->Fill(jethelper2_pt[1], weight);
		      //histsy1[j]->Fill(jethelper2_rapidity[0], weight);
		      //histsy2[j]->Fill(jethelper2_rapidity[1], weight);
		      //histsyboost[j]->Fill(fabs(jethelper2_rapidity[0]+jethelper2_rapidity[1])/2., weight);
		      //histsmetsumet[j]->Fill(met2_et/met2_sumEt, weight);
		      //histsdphi[j]->Fill(fabs(reco::deltaPhi(jethelper2_phi[0],jethelper2_phi[1])));
		    }
		}
	    }

	  int i1=findLeading(smrjet_pt);
	  int i2=findNextLeading(smrjet_pt,i1);
	  if ( (smrjet_pt.size()>=2) && (i1 == -1 || i2 == -1 || i1 == i2) ){
	    std::cout << "Trouble with sorting" << std::endl;
	    std::cout << "Pt1: " << smrjet_pt[i1] << " Pt2: " << smrjet_pt[i2] << std::endl;
	    return 0;
	  }
	  
	  bool selectSmr = 
	    (smrjet_pt.size()>=2)&&
	    (smrjet_pt[i1]>30)&&
	    (smrjet_pt[i2]>30)&&
	    (fabs(smrjet_rapidity[i1])<2.5)&&
	    (fabs(smrjet_rapidity[i2])<2.5)&&
	    (fabs(smrjet_rapidity[i1]+smrjet_rapidity[i2])/2.<1.11)&&
	    (exp(fabs(smrjet_rapidity[i1]-smrjet_rapidity[i2]))<16)&&
	    
	    (smrjet_nConstituents[i1]>1)&&	     
	    (smrjet_nConstituents[i2]>1);
	  if(selectSmr)
	    {
	      // fill smrjets
	      TLorentzVector j1P4,j2P4,dijet;
	      j1P4=smearedJets.at(0);
	      j2P4=smearedJets.at(1);
	      dijet=j1P4+j2P4;
	      double invmass=dijet.M();

	      double pt1=smearedJets.at(0).Pt();
	      double pt2=smearedJets.at(1).Pt();
	      if (abs(pt1-smrjet_pt[i1]) > 0.0005)
		  std::cout << "Problems wLeading: " << pt1 << " " <<  smrjet_pt[i1] << std::endl;
	      if (abs(pt2-smrjet_pt[i2]) > 0.0005)
		  std::cout << "Problems wNextLeading: " << pt2 << " " <<  smrjet_pt[i2] << std::endl;
	      s1->Fill(invmass,weight);

	      smrDijets.dijetFlag=1;
	      smrDijets.mass=invmass;
	      smrDijets.pt=dijet.Pt();
	      smrDijets.chi=exp(fabs(smrjet_rapidity[i1]-smrjet_rapidity[i2]));
	      smrDijets.yboost=fabs(smrjet_rapidity[i1]+smrjet_rapidity[i2])/2.;
	      smrDijets.pt1= smrjet_pt[i1];
	      smrDijets.eta1=smrjet_eta[i1];
	      smrDijets.phi1=smrjet_phi[i1];
	      smrDijets.e1=  smrjet_energy[i1];
	      smrDijets.pt2= smrjet_pt[i2];
	      smrDijets.eta2=smrjet_eta[i2];
	      smrDijets.phi2=smrjet_phi[i2];
	      smrDijets.e2=  smrjet_energy[i2];

	      for ( size_t j = 0; j < (massBins.size()-1); ++j )
		{
		  if((invmass>=massBins[j])&&
		     (invmass<massBins[j+1]))
		    {
		      // shists[j]->Fill(exp(fabs(smrjet_rapidity[i1]-smrjet_rapidity[i2])), weight);
		      //histspt1[j]->Fill(jethelper2_pt[i1], weight);
		      //histspt2[j]->Fill(jethelper2_pt[i2], weight);
		      //histsy1[j]->Fill(jethelper2_rapidity[i1], weight);
		      //histsy2[j]->Fill(jethelper2_rapidity[i2], weight);
		      //histsyboost[j]->Fill(fabs(jethelper2_rapidity[i1]+jethelper2_rapidity[i2])/2., weight);
		      //histsmetsumet[j]->Fill(met2_et/met2_sumEt, weight);
		      //histsdphi[j]->Fill(fabs(reco::deltaPhi(jethelper2_phi[i1],jethelper2_phi[i2])));
		    }
		}
	    }


	}// end of genJets->size()>1 if block
	_outTree->Fill();
      } // end of event loop
      // close input file
      inFile->Close();
    }
    // break loop if maximal number of events is reached:
    // this has to be done twice to stop the file loop as well
    if(maxEvents_>0 ? ievt+1>maxEvents_ : false) break;
  }
  OutFile->Write();
  OutFile->Close();
  std::cout << "GenChiAnalysis finished normally" << std::endl;
  //_outTree->Print();
  // gDebug=7;
  return 0;
}

int findLeading(const std::vector<double> jpt){
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

int findNextLeading(const std::vector<double> jpt, const uint i1){
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

vector <TLorentzVector> sortJets(const vector<TLorentzVector> p4){ 
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

void fillHist(const TString& histName, const Double_t& value, const Double_t& wt) {

  hid=m_HistNames.find(histName);
  if (hid==m_HistNames.end())
    std::cout << "%fillHist -- Could not find histogram with name: " << histName << std::endl;
  else
    hid->second->Fill(value,wt); 

}

void fill3DHist(const TString& histName, const Double_t& x,const Double_t& y,const Double_t& z,const Double_t& wt) {

  hid3D=m_HistNames3D.find(histName);
  if (hid3D==m_HistNames3D.end())
    std::cout << "%fillHist -- Could not find histogram with name: " << histName << std::endl;
  else
    hid3D->second->Fill(x,y,z,wt); 

}

TH1F* Book1dHist(const char* name, const char* title, Int_t nbins, Double_t xmin, Double_t xmax,bool DoSumw2=true){


  TH1F *h= new TH1F(name, title, nbins, xmin, xmax); 

  if (DoSumw2) h->Sumw2();

  return h;
}

TH2F* Book2dHist(const char* name, const char* title, Int_t nbinsx, Double_t xmin, Double_t xmax,
		 Int_t nbinsy, Double_t ymin, Double_t ymax, bool DoSumw2=true){


  TH2F *h= new TH2F(name, title, nbinsx, xmin, xmax, nbinsy, ymin, ymax); 

  if (DoSumw2) h->Sumw2();

  return h;
}

TH3F* Book3dHist(const char* name, const char* title, Int_t nbinsx, Double_t xmin, Double_t xmax , 
		 Int_t nbinsy, Double_t ymin, Double_t ymax , Int_t nbinsz, Double_t zmin, 
		 Double_t zmax , bool DoSumw2=true){

  TH3F *h= new TH3F(name, title, nbinsx, xmin, xmax, nbinsy, ymin, ymax, nbinsz, zmin, zmax); 
  if (DoSumw2) h->Sumw2();

  return h;
}

double SmearMass(double mass, double etamax){
  double p0=0.,p1=0.,p2=0.;
  double eta=etamax;

  if (eta > 2.5) eta =2.5;

  if (eta < 0.5){
    p0=0.02846;
    p1=0.01072;
    p2=0.9305;
  }
  else if (eta < 1.0){
    p0=0.0298;
    p1=0.01106;
    p2=0.9786;
  }
  else if (eta < 1.5){
    p0=0.03201;
    p1=0.01489;
    p2=0.9976;
  }
  else if (eta < 2.0){
    p0=0.02348;
    p1=0.02351;
    p2=0.9492;
  }
  else {
    p0=0.02716;
    p1=0.02836;
    p2=1.332;
  }

  double fact =SmearMassFunc(mass,p0,p1,p2);

  // cout << "ETAMAX/MASS: " << eta << " / " << mass << "  Fact: "<< fact << endl;   
  return fact; 
}


double SmearMassFunc(double mean, double p0, double p1, double p2){
  double sigma=0;

  double m=mean/1000.;

  sigma = m*( p0 + p1/pow(m,p2) );

  double r = rnd.Gaus(m,sigma);
  // std:: cout << "Mean: " << mean << " sigma/mean: " << sigma/m << " Smearing factor: " << r/m << std::endl;
  return r/m; 
}



double SmearFunc(double mean, double eta, double p0, double p1, double p2, bool doSys, bool sysPlus){
  double sigma=0;

  bool addSmear=true;

  sigma = mean*(sqrt(pow(p0,2)+pow((p1/sqrt(mean)),2)+pow((p2/mean),2)));
  // double sysErr=1.;
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

  if (doSys){
    if (sysPlus){
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

double SmearFactor(double pt,double eta, bool doSys, bool sysPlus){

  double smf_e=1.;
  if (eta < 0.5) {
    smf_e   = SmearFunc(pt,eta,2.87265e-02,1.01485e+00,5.25613e+00,doSys,sysPlus);
  } 
  else if (eta < 1.0) {
    smf_e   = SmearFunc(pt,eta,3.43555e-02,9.49218e-01,5.92528e+00,doSys,sysPlus);
  } 
  else if (eta < 1.5) {
    smf_e   = SmearFunc(pt,eta,3.95103e-02,1.00204e+00,6.07558e+00,doSys,sysPlus);
  }
  else if (eta < 2.0) {
    smf_e   = SmearFunc(pt,eta,1.42866e-02,8.48049e-01,6.67823e+00,doSys,sysPlus);
  }
  else if (eta < 2.5) {
    smf_e   = SmearFunc(pt,eta,1.34450e-02,7.14309e-01,6.77620e+00,doSys,sysPlus);
  }
  else if (eta < 3.0) {
    smf_e   = SmearFunc(pt,eta,2.08877e-07,8.59187e-01,6.84957e+00,doSys,sysPlus);
  }

  return smf_e;
}
