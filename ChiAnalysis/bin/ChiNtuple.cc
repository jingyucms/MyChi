#include "ChiNtuple.h"

void ChiNtuple::Loop(){


  // ccla Setup the smearing
  string   era("Spring10");
  string   alg("AK5PF");
  bool     doGaussian(false);
  // bool     doGaussian(true);

  cout<<"era:      "<<era<<endl;
  cout<<"alg:      "<<alg<<endl;
  cout<<"gaussian: "<<doGaussian<<endl<<endl;

  
  string cmssw_base(getenv("CMSSW_BASE"));
  string cmssw_release_base(getenv("CMSSW_RELEASE_BASE"));
  string path = cmssw_base + "/src/CondFormats/JetMETObjects/data";
  // struct stat st;
  // if (stat(path.c_str(),&st)!=0)
  //   path = cmssw_release_base + "/src/CondFormats/JetMETObjects/data";
  // if (stat(path.c_str(),&st)!=0) {
  //   cerr<<"ERROR: tried to set path but failed, abort."<<endl;
  //   return 0;
  // }
  string ptFileName  = path + "/" + era + "_PtResolution_" +alg+".txt";
  string etaFileName = path + "/" + era + "_EtaResolution_"+alg+".txt";
  string phiFileName = path + "/" + era + "_PhiResolution_"+alg+".txt";

  cout<<ptFileName<<endl;
  cout<<etaFileName<<endl;
  cout<<phiFileName<<endl;
  cout<<endl;

  JetResolution ptResol(ptFileName,doGaussian);
  //JetResolution etaResol(etaFileName,doGaussian);
  //JetResolution phiResol(phiFileName,doGaussian);

  // TF1* fPtResol;
  
  int                             jetAK4_N             ;
  std::vector<float>              *jetAK4_pt=0         ;
  std::vector<float>              *jetAK4_eta=0         ;
  std::vector<float>              *jetAK4_phi=0         ;
  std::vector<float>              *jetAK4_e=0         ;
  std::vector<bool>               *jetAK4_IDLoose=0;
  std::vector<bool>               *jetAK4_IDTight=0;
  TBranch *b_jetAK4_N; //!
  TBranch *b_jetAK4_pt; //!
  TBranch *b_jetAK4_eta; //!
  TBranch *b_jetAK4_phi; //!
  TBranch *b_jetAK4_e; //!
  TBranch *b_jetAK4_IDLoose; //!
  TBranch *b_jetAK4_IDTight; //!

  fChain->SetBranchAddress("jetAK4_N",   &jetAK4_N,   &b_jetAK4_N);
  fChain->SetBranchAddress("jetAK4_pt",  &jetAK4_pt,  &b_jetAK4_pt);
  fChain->SetBranchAddress("jetAK4_eta", &jetAK4_eta, &b_jetAK4_eta);
  fChain->SetBranchAddress("jetAK4_phi", &jetAK4_phi, &b_jetAK4_phi);
  fChain->SetBranchAddress("jetAK4_e",   &jetAK4_e,   &b_jetAK4_e);
  fChain->SetBranchAddress("jetAK4_IDLoose",   &jetAK4_IDLoose,   &b_jetAK4_IDLoose);
  fChain->SetBranchAddress("jetAK4_IDTight",   &jetAK4_IDTight,   &b_jetAK4_IDTight);
  
  fChain->SetBranchStatus("jetAK4_N",  1);
  fChain->SetBranchStatus("jetAK4_pt", 1);
  fChain->SetBranchStatus("jetAK4_eta",1);
  fChain->SetBranchStatus("jetAK4_phi",1);
  fChain->SetBranchStatus("jetAK4_e",  1);
  fChain->SetBranchStatus("jetAK4_IDLoose",  1);
  fChain->SetBranchStatus("jetAK4_IDTight",  1);


  int                             genJetAK4_N             ;
  std::vector<float>              *genJetAK4_pt=0         ;
  std::vector<float>              *genJetAK4_eta=0         ;
  std::vector<float>              *genJetAK4_phi=0         ;
  std::vector<float>              *genJetAK4_e=0         ;

  TBranch *b_genJetAK4_N; //!
  TBranch *b_genJetAK4_pt; //!
  TBranch *b_genJetAK4_eta; //!
  TBranch *b_genJetAK4_phi; //!
  TBranch *b_genJetAK4_e; //!

  fChain->SetBranchAddress("genJetAK4_N",   &genJetAK4_N,   &b_genJetAK4_N);
  fChain->SetBranchAddress("genJetAK4_pt",  &genJetAK4_pt,  &b_genJetAK4_pt);
  fChain->SetBranchAddress("genJetAK4_eta", &genJetAK4_eta, &b_genJetAK4_eta);
  fChain->SetBranchAddress("genJetAK4_phi", &genJetAK4_phi, &b_genJetAK4_phi);
  fChain->SetBranchAddress("genJetAK4_e",   &genJetAK4_e,   &b_genJetAK4_e);
  
  fChain->SetBranchStatus("genJetAK4_N",  1);
  fChain->SetBranchStatus("genJetAK4_pt", 1);
  fChain->SetBranchStatus("genJetAK4_eta",1);
  fChain->SetBranchStatus("genJetAK4_phi",1);
  fChain->SetBranchStatus("genJetAK4_e",  1);

  
/*------------------------EVENT infos-------------------------*/    
  int                               EVENT_event            ;
  int                               EVENT_run              ;
  int                               EVENT_lumiBlock        ;
  

  TBranch *b_EVENT_event, *b_EVENT_run, *b_EVENT_lumiBlock; //!
  fChain->SetBranchAddress("EVENT_event", &EVENT_event, &b_EVENT_event);
  fChain->SetBranchAddress("EVENT_run", &EVENT_run, &b_EVENT_run);
  fChain->SetBranchAddress("EVENT_lumiBlock", &EVENT_lumiBlock, &b_EVENT_lumiBlock);
  
  fChain->SetBranchStatus("EVENT_event",1);
  fChain->SetBranchStatus("EVENT_run",1);
  fChain->SetBranchStatus("EVENT_lumiBlock",1);
  
  int nentries=fChain->GetEntries();

  //int nevents=100;
  int nevents=nentries;
  cout << "Number of events: " << nevents << endl;  
  
  std::vector<string> htBins, ptBins, mBins;
  htBins.push_back("HT-100To250");
  htBins.push_back("HT-250To500");
  htBins.push_back("HT-500To1000");
  htBins.push_back("HT-1000ToInf");


  mBins.push_back("m900_1400");
  mBins.push_back("m1400_2500");
  mBins.push_back("m2500_3700");
  mBins.push_back("m3700_8000");

  ptBins.push_back("Pt_170to300");
  ptBins.push_back("Pt_300to470");
  ptBins.push_back("Pt_470to600");
  ptBins.push_back("Pt_600to800");
  ptBins.push_back("Pt_800to1000");
  ptBins.push_back("Pt_1000to1400");
  ptBins.push_back("Pt_1400to1800");
  ptBins.push_back("Pt_1800to2400");
  ptBins.push_back("Pt_2400to3200");  
  ptBins.push_back("Pt_3200");

  int htBin=-1;
  for (uint i=0; i<htBins.size(); ++ i){
    string stringToFind= htBins.at(i) ;
    std::size_t found = outName.find(stringToFind);
    if (found != std::string::npos){
      htBin=i;
      break;
    }
  }
  if (htBin==-1){
    std::cout << "HT Bin not found in output file name"  << std::endl;
  }
  HTBin=htBin;


  int ptBin=-1;
  for (uint i=0; i<ptBins.size(); ++ i){
    string stringToFind= ptBins.at(i) ;
    std::size_t found = outName.find(stringToFind);
    if (found != std::string::npos){
      ptBin=i;
      break;
    }
  }
  if (ptBin==-1){
    std::cout << "PT Bin not found in output file name"  << std::endl;
  }
  PTBin=ptBin;

  int mBin=-1;
  for (uint i=0; i<mBins.size(); ++ i){
    string stringToFind= mBins.at(i) ;
    std::size_t found = outName.find(stringToFind);
    if (found != std::string::npos){
      mBin=i;
      break;
    }
  }
  if (mBin==-1){
    std::cout << "Mass Bin not found in output file name"  << std::endl;
  }
  MBin=mBin;


  std::vector<double>	genjet_energy(10,0);
  std::vector<double>	genjet_et(10,0);
  std::vector<double>	genjet_pt(10,0);
  std::vector<double>	genjet_eta(10,0);
  std::vector<double>	genjet_phi(10,0);
  std::vector<double>	genjet_mass(10,0);
  std::vector<double>	genjet_rapidity(10,0);
  std::vector<double>	genjet_nConstituents(10,0);

  std::vector<double>	smrjet_energy(0,0);
  std::vector<double>	smrjet_et(0,0);
  std::vector<double>	smrjet_pt(0,0);
  std::vector<double>	smrjet_eta(0,0);
  std::vector<double>	smrjet_phi(0,0);
  std::vector<double>	smrjet_rapidity(0,0);
  std::vector<double>	smrjet_nConstituents(0,0);
  
  std::cout << "event...\n" << std::endl;

  fillHist("nevts",0.,float(nevents));
  
  for( int iEvent = 0; iEvent < nevents; iEvent++ )
    {
      int freq=10000;
      if(iEvent%freq==0) std::cout << iEvent << " events processed..." << std::endl;

      fillHist("evtsHT",float(HTBin),1.);
      fillHist("evtsM",float(MBin),1.);
      fillHist("evtsPT",float(PTBin),1.);
      
      fChain->GetEntry( iEvent );

      double evtweight(1.);
      double weight=xsweight*evtweight;
      XSweight=xsweight;
      EVTweight=evtweight;
      Event=EVENT_event;
      Run=EVENT_run;
      Lumi=EVENT_lumiBlock;

      double initval=-999.;
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

      if (iEvent == 0){
	std::cout << "\n\tUsing XS weight: " << XSweight << std::endl;
	std::cout << "\tUsing EVT weight: " << EVTweight << "\n" <<std::endl;
      }
      // fillHist("ngenjet",ngenjet,1.);

      smrjet_energy.clear();
      smrjet_et.clear();
      smrjet_pt.clear();
      smrjet_eta.clear();
      smrjet_phi.clear();
      smrjet_rapidity.clear();
      smrjet_nConstituents.clear();
      
      vector<TLorentzVector> smearedJets;

      // RecoJets
      int njets=jetAK4_pt->size();      
      bool selectReco=false;
      if (njets>1){
	TLorentzVector Jet1,Jet2;
	Jet1.SetPtEtaPhiE(jetAK4_pt->at(0),jetAK4_eta->at(0),jetAK4_phi->at(0),jetAK4_e->at(0));
	Jet2.SetPtEtaPhiE(jetAK4_pt->at(1),jetAK4_eta->at(1),jetAK4_phi->at(1),jetAK4_e->at(1));
	
	selectReco=(
		    (Jet1.Pt()>30) &&
		    (Jet2.Pt()>30) &&		     
		    (fabs(Jet1.Rapidity())<2.5) &&
		    (fabs(Jet2.Rapidity())<2.5) &&
		    (fabs(Jet1.Rapidity()+Jet2.Rapidity())/2.<1.11) &&
		    (exp(fabs(Jet1.Rapidity()-Jet2.Rapidity()))<16) &&	  
		    (jetAK4_IDTight->at(0)) &&
		    (jetAK4_IDTight->at(1))
		    );
	if (selectReco){	     
	    
	  double DijetMass = (Jet1+Jet2).M();
	  fillHist("dijet_mass",DijetMass,weight);
	  
	  recoDijets.dijetFlag=1;
	  recoDijets.mass=DijetMass;
	  recoDijets.pt=(Jet1+Jet2).Pt();
	  recoDijets.chi=exp(fabs(Jet1.Rapidity()-Jet2.Rapidity()));
	  recoDijets.yboost=fabs(Jet1.Rapidity()+Jet2.Rapidity())/2.;
	  recoDijets.pt1= Jet1.Pt();
	  recoDijets.eta1=Jet1.Eta();
	  recoDijets.phi1=Jet1.Phi();
	  recoDijets.e1=  Jet1.Energy();
	  recoDijets.pt2= Jet2.Pt();
	  recoDijets.eta2=Jet2.Eta();
	  recoDijets.phi2=Jet2.Phi();
	  recoDijets.e2=  Jet2.Energy();
	}
      }

      // GenJets
      int ngenJets=genJetAK4_pt->size();      
      bool selectGen=false;
      if (ngenJets>1){
	TLorentzVector Jet1,Jet2;
	Jet1.SetPtEtaPhiE(genJetAK4_pt->at(0),genJetAK4_eta->at(0),genJetAK4_phi->at(0),genJetAK4_e->at(0));
	Jet2.SetPtEtaPhiE(genJetAK4_pt->at(1),genJetAK4_eta->at(1),genJetAK4_phi->at(1),genJetAK4_e->at(1));
	selectGen=(
		   (Jet1.Pt()>30) &&
		   (Jet2.Pt()>30) &&		     
		   (fabs(Jet1.Rapidity())<2.5) &&
		   (fabs(Jet2.Rapidity())<2.5) &&
		   (fabs(Jet1.Rapidity()+Jet2.Rapidity())/2.<1.11) &&
		   (exp(fabs(Jet1.Rapidity()-Jet2.Rapidity()))<16)
		   );
	if (selectGen){
	  double DijetMass = (Jet1+Jet2).M();
	  fillHist("dijet_mass_gen",DijetMass,weight);
	  
	  genDijets.dijetFlag=1;
	  genDijets.mass=DijetMass;
	  genDijets.pt=(Jet1+Jet2).Pt();
	  genDijets.chi=exp(fabs(Jet1.Rapidity()-Jet2.Rapidity()));
	  genDijets.yboost=fabs(Jet1.Rapidity()+Jet2.Rapidity())/2.;
	  genDijets.pt1= Jet1.Pt();
	  genDijets.eta1=Jet1.Eta();
	  genDijets.phi1=Jet1.Phi();
	  genDijets.e1=  Jet1.Energy();
	  genDijets.pt2= Jet2.Pt();
	  genDijets.eta2=Jet2.Eta();
	  genDijets.phi2=Jet2.Phi();
	  genDijets.e2=  Jet2.Energy();	  
	};
      }
      
      _outTree->Fill();
    }//endof Main Event looo
}

int main(int argc, char* argv[])
{
  cout << "Beginning ChiNtuple maker" << endl;
  ChiNtuple* chiNtuple = new ChiNtuple();


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
  const edm::ParameterSet& process = edm::readPSetsFrom(argv[1])->getParameter<edm::ParameterSet>("process");
  const edm::ParameterSet& ana = process.getParameter<edm::ParameterSet>("chiNtuples");
  double XS_( ana.getParameter<double>("CrossSection") );
  string INPUTFILES_( ana.getParameter<string>("InputFiles") );
  string OUTPUTFILE_( ana.getParameter<string>("OutputFile") );  
  //double smearMax_( ana.getParameter<double>("SmearMax") );
  
  chiNtuple->SetXSWeight(XS_);
  cout << "Booking Histograms..." << endl;
  chiNtuple->BookHistograms(OUTPUTFILE_);

  cout << "Reading Ntuples from: "<< INPUTFILES_ << endl;  
  bool fok =chiNtuple->OpenWithList(INPUTFILES_);
  if ( not fok ){
    cout << "Trouble opening list" <<endl;
    return 1;
  }

  chiNtuple->Loop();
  chiNtuple->WriteHistograms();
  
  delete chiNtuple;
  return 0;
}
