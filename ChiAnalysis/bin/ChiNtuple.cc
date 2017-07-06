#include "ChiNtuple.h"

void ChiNtuple::Loop(){


  // ccla Setup the smearing
  string   era("Spring10");
  string   alg("AK5PF");

  cout<<"era:         "<<era<<endl;
  cout<<"alg:         "<<alg<<endl;
  cout<<"gaussian:    "<<doGaussian<<endl;
  cout<<"AK4_sf:      "<<doAK4_sf<<endl;
  cout<<"DataToMC_sf: "<<doDataToMC_sf<<endl;
  cout<<"SysErr:      "<<doSysErr<<endl;
  cout<<"isData:      "<<IsData<<endl<<endl<<endl;  

  
  string cmssw_base(getenv("CMSSW_BASE"));
  string cmssw_release_base(getenv("CMSSW_RELEASE_BASE"));
  // string path = cmssw_release_base + "/src/CondFormats/JetMETObjects/data";
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
  //TF1 *fPtResol;  
  MyJetResponse jetresponse(doAK4_sf,doDataToMC_sf,doSysErr);
  
  jetresponse.GetResolutionParameters(ptFileName,doGaussian);
    
  // int                             jetAK4_N             ;
  // std::vector<float>              *jetAK4_pt=0         ;
  // std::vector<float>              *jetAK4_eta=0         ;
  // std::vector<float>              *jetAK4_phi=0         ;
  // std::vector<float>              *jetAK4_e=0         ;
  // std::vector<bool>               *jetAK4_IDLoose=0;
  // std::vector<bool>               *jetAK4_IDTight=0;
  // 
  // std::map<std::string,bool> *HLT_isFired=0;
  // 
  // Bool_t                            passFilter_HBHE_=0;
  // Bool_t                            passFilter_CSCHalo_=0;
  // Bool_t                            passFilter_GoodVtx_=0;
  // Bool_t                            passFilter_EEBadSc_=0;
  // 
  // TBranch *b_jetAK4_N; //!
  // TBranch *b_jetAK4_pt; //!
  // TBranch *b_jetAK4_eta; //!
  // TBranch *b_jetAK4_phi; //!
  // TBranch *b_jetAK4_e; //!
  // TBranch *b_jetAK4_IDLoose; //!
  // TBranch *b_jetAK4_IDTight; //!
  // 
  // TBranch *b_HLT_isFired;
  // 
  // TBranch                             *b_passFilter_HBHE; //!
  // TBranch                             *b_passFilter_CSCHalo; //!
  // TBranch                             *b_passFilter_GoodVtx; //!
  // TBranch                             *b_passFilter_EEBadSc; //!
  // 
  // int                             genJetAK4_N             ;
  // std::vector<float>              *genJetAK4_pt=0         ;
  // std::vector<float>              *genJetAK4_eta=0         ;
  // std::vector<float>              *genJetAK4_phi=0         ;
  // std::vector<float>              *genJetAK4_e=0         ;
  // 
  // float  genWeight;
  // 
  // TBranch *b_genJetAK4_N; //!
  // TBranch *b_genJetAK4_pt; //!
  // TBranch *b_genJetAK4_eta; //!
  // TBranch *b_genJetAK4_phi; //!
  // TBranch *b_genJetAK4_e; //!
  // TBranch *b_genWeight; //!

  float jetAK4_pt1,jetAK4_pt2,jetAK4_pt3;
  float jetAK4_eta1,jetAK4_eta2,jetAK4_eta3;
  float jetAK4_phi1,jetAK4_phi2,jetAK4_phi3;
  float jetAK4_y1,jetAK4_y2,jetAK4_y3;
  float jetAK4_mass1,jetAK4_mass2,jetAK4_mass3;  
  //float jetAK4_IDLoose1,jetAK4_IDLoose2,jetAK4_IDLoose3;
  float jetAK4_IDTight1,jetAK4_IDTight2,jetAK4_IDTight3;

  float genJetAK4_pt1,genJetAK4_pt2,genJetAK4_pt3;
  float genJetAK4_eta1,genJetAK4_eta2,genJetAK4_eta3;
  float genJetAK4_phi1,genJetAK4_phi2,genJetAK4_phi3;
  float genJetAK4_y1,genJetAK4_y2,genJetAK4_y3;
  float genJetAK4_mass1,genJetAK4_mass2,genJetAK4_mass3;  

  TBranch *b_jetAK4_pt1; //!
  TBranch *b_jetAK4_eta1; //!
  TBranch *b_jetAK4_phi1; //!
  TBranch *b_jetAK4_y1; //!
  TBranch *b_jetAK4_mass1; //!
  //TBranch *b_jetAK4_IDLoose1; //!
  TBranch *b_jetAK4_IDTight1; //!

  TBranch *b_jetAK4_pt2; //!
  TBranch *b_jetAK4_eta2; //!
  TBranch *b_jetAK4_phi2; //!
  TBranch *b_jetAK4_y2; //!
  TBranch *b_jetAK4_mass2; //!
  //TBranch *b_jetAK4_IDLoose2; //!
  TBranch *b_jetAK4_IDTight2; //!

  TBranch *b_jetAK4_pt3; //!
  TBranch *b_jetAK4_eta3; //!
  TBranch *b_jetAK4_phi3; //!
  TBranch *b_jetAK4_y3; //!
  TBranch *b_jetAK4_mass3; //!  
  //TBranch *b_jetAK4_IDLoose3; //!
  TBranch *b_jetAK4_IDTight3; //!  

  TBranch *b_genJetAK4_pt1; //!
  TBranch *b_genJetAK4_eta1; //!
  TBranch *b_genJetAK4_phi1; //!
  TBranch *b_genJetAK4_y1; //!
  TBranch *b_genJetAK4_mass1; //!

  TBranch *b_genJetAK4_pt2; //!
  TBranch *b_genJetAK4_eta2; //!
  TBranch *b_genJetAK4_phi2; //!
  TBranch *b_genJetAK4_y2; //!
  TBranch *b_genJetAK4_mass2; //!

  TBranch *b_genJetAK4_pt3; //!
  TBranch *b_genJetAK4_eta3; //!
  TBranch *b_genJetAK4_phi3; //!
  TBranch *b_genJetAK4_y3; //!
  TBranch *b_genJetAK4_mass3; //!

  std::map<std::string,bool> *HLT_isFired=0;
  TBranch *b_HLT_isFired;
  
  float  genWeight;
  TBranch *b_genWeight; //!
 
/*------------------------EVENT infos-------------------------*/    
  int                               EVENT_event            ;
  int                               EVENT_run              ;
  int                               EVENT_lumiBlock        ;
  
  TBranch *b_EVENT_event, *b_EVENT_run, *b_EVENT_lumiBlock; //!
  
  // fChain->SetBranchAddress("jetAK4_N",   &jetAK4_N,   &b_jetAK4_N);
  fChain->SetBranchAddress("jetAK4_pt1",  &jetAK4_pt1,  &b_jetAK4_pt1);
  fChain->SetBranchAddress("jetAK4_pt2",  &jetAK4_pt2,  &b_jetAK4_pt2);
  fChain->SetBranchAddress("jetAK4_pt3",  &jetAK4_pt3,  &b_jetAK4_pt3);
  fChain->SetBranchAddress("jetAK4_eta1", &jetAK4_eta1,&b_jetAK4_eta1);
  fChain->SetBranchAddress("jetAK4_eta2", &jetAK4_eta2,&b_jetAK4_eta2);
  fChain->SetBranchAddress("jetAK4_eta3", &jetAK4_eta3,&b_jetAK4_eta3);
  fChain->SetBranchAddress("jetAK4_phi1", &jetAK4_phi1, &b_jetAK4_phi1);
  fChain->SetBranchAddress("jetAK4_phi2", &jetAK4_phi2, &b_jetAK4_phi2);
  fChain->SetBranchAddress("jetAK4_phi3", &jetAK4_phi3, &b_jetAK4_phi3);
  fChain->SetBranchAddress("jetAK4_y1",   &jetAK4_y1,   &b_jetAK4_y1);
  fChain->SetBranchAddress("jetAK4_y2",   &jetAK4_y2,   &b_jetAK4_y2);
  fChain->SetBranchAddress("jetAK4_y3",   &jetAK4_y3,   &b_jetAK4_y3);
  fChain->SetBranchAddress("jetAK4_mass1",   &jetAK4_mass1,   &b_jetAK4_mass1);
  fChain->SetBranchAddress("jetAK4_mass2",   &jetAK4_mass2,   &b_jetAK4_mass2);
  fChain->SetBranchAddress("jetAK4_mass3",   &jetAK4_mass3,   &b_jetAK4_mass3);  
  //fChain->SetBranchAddress("jetAK4_IDLoose1",   &jetAK4_IDLoose1,   &b_jetAK4_IDLoose1);
  //fChain->SetBranchAddress("jetAK4_IDLoose2",   &jetAK4_IDLoose2,   &b_jetAK4_IDLoose2);
  //fChain->SetBranchAddress("jetAK4_IDLoose3",   &jetAK4_IDLoose3,   &b_jetAK4_IDLoose3);
  fChain->SetBranchAddress("jetAK4_IDTight1",   &jetAK4_IDTight1,   &b_jetAK4_IDTight1);
  fChain->SetBranchAddress("jetAK4_IDTight2",   &jetAK4_IDTight2,   &b_jetAK4_IDTight2);
  fChain->SetBranchAddress("jetAK4_IDTight3",   &jetAK4_IDTight3,   &b_jetAK4_IDTight3);  

  fChain->SetBranchAddress("HLT_isFired",   &HLT_isFired,   &b_HLT_isFired);
  
  // fChain->SetBranchAddress("passFilter_HBHE",      &passFilter_HBHE_,      &b_passFilter_HBHE);
  // fChain->SetBranchAddress("passFilter_CSCHalo",   &passFilter_CSCHalo_,   &b_passFilter_CSCHalo);
  // fChain->SetBranchAddress("passFilter_GoodVtx",   &passFilter_GoodVtx_,   &b_passFilter_GoodVtx);
  // fChain->SetBranchAddress("passFilter_EEBadSc",   &passFilter_EEBadSc_,   &b_passFilter_EEBadSc);  
  
  if (!IsData){
    std::cout << "Setting Branch Address" << std::endl;
    // fChain->SetBranchAddress("genJetAK4_N",   &genJetAK4_N,   &b_genJetAK4_N);
    fChain->SetBranchAddress("genJetAK4_pt1",  &genJetAK4_pt1,  &b_genJetAK4_pt1);
    fChain->SetBranchAddress("genJetAK4_pt2",  &genJetAK4_pt2,  &b_genJetAK4_pt2);
    fChain->SetBranchAddress("genJetAK4_pt3",  &genJetAK4_pt3,  &b_genJetAK4_pt3);    
    fChain->SetBranchAddress("genJetAK4_eta1", &genJetAK4_eta1, &b_genJetAK4_eta1);
    fChain->SetBranchAddress("genJetAK4_eta2", &genJetAK4_eta2, &b_genJetAK4_eta2);
    fChain->SetBranchAddress("genJetAK4_eta3", &genJetAK4_eta3, &b_genJetAK4_eta3);
    fChain->SetBranchAddress("genJetAK4_phi1", &genJetAK4_phi1, &b_genJetAK4_phi1);
    fChain->SetBranchAddress("genJetAK4_phi2", &genJetAK4_phi2, &b_genJetAK4_phi2);
    fChain->SetBranchAddress("genJetAK4_phi3", &genJetAK4_phi3, &b_genJetAK4_phi3);
    fChain->SetBranchAddress("genJetAK4_y1",   &genJetAK4_y1,   &b_genJetAK4_y1);
    fChain->SetBranchAddress("genJetAK4_y2",   &genJetAK4_y2,   &b_genJetAK4_y2);
    fChain->SetBranchAddress("genJetAK4_y3",   &genJetAK4_y3,   &b_genJetAK4_y3);
    fChain->SetBranchAddress("genJetAK4_mass1",   &genJetAK4_mass1,   &b_genJetAK4_mass1);
    fChain->SetBranchAddress("genJetAK4_mass2",   &genJetAK4_mass2,   &b_genJetAK4_mass2);
    fChain->SetBranchAddress("genJetAK4_mass3",   &genJetAK4_mass3,   &b_genJetAK4_mass3);

    fChain->SetBranchAddress("genWeight",   &genWeight,   &b_genWeight);    
  }
  fChain->SetBranchAddress("EVENT_event", &EVENT_event, &b_EVENT_event);
  fChain->SetBranchAddress("EVENT_run", &EVENT_run, &b_EVENT_run);
  fChain->SetBranchAddress("EVENT_lumiBlock", &EVENT_lumiBlock, &b_EVENT_lumiBlock);

  // fChain->SetBranchStatus("jetAK4_N",  1);
  // fChain->SetBranchStatus("jetAK4_pt", 1);
  // fChain->SetBranchStatus("jetAK4_eta",1);
  // fChain->SetBranchStatus("jetAK4_phi",1);
  // fChain->SetBranchStatus("jetAK4_e",  1);
  // fChain->SetBranchStatus("jetAK4_IDLoose",  1);
  // fChain->SetBranchStatus("jetAK4_IDTight",  1);

  //fChain->SetBranchStatus("HLT_isFired",  1);
  
  // fChain->SetBranchStatus("passFilter_HBHE",      1);
  // fChain->SetBranchStatus("passFilter_CSCHalo",   1);
  // fChain->SetBranchStatus("passFilter_GoodVtx",   1);
  // fChain->SetBranchStatus("passFilter_EEBadSc",   1);

  if (!IsData){
    std::cout << "Setting Branch Status" << std::endl;
    // fChain->SetBranchStatus("genJetAK4_N",  1);
    // fChain->SetBranchStatus("genJetAK4_pt", 1);
    // fChain->SetBranchStatus("genJetAK4_eta",1);
    // fChain->SetBranchStatus("genJetAK4_phi",1);
    // fChain->SetBranchStatus("genJetAK4_e",  1);
    // fChain->SetBranchStatus("genWeight",  1);    
  }
  
  //fChain->SetBranchStatus("EVENT_event",1);
  //fChain->SetBranchStatus("EVENT_run",1);
  //fChain->SetBranchStatus("EVENT_lumiBlock",1);
  
  int nevents(0);
  if (Nevts>0){
    nevents=Nevts;
  }else{
    nevents=fChain->GetEntries();
  }

  cout << "Number of events: " << nevents << endl;  
  
  std::vector<string> htBins, ptBins, mBins,flatBins;

  flatBins.push_back("flatQCD");
  
  htBins.push_back("HT300to500");
  htBins.push_back("HT500to700");
  htBins.push_back("HT700to1000");
  htBins.push_back("HT1000to1500");
  htBins.push_back("HT1500to2000");
  htBins.push_back("HT2000toInf");


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
  if (htBin==-1 && !IsData){
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
  if (ptBin==-1 && !IsData){
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
  if (mBin==-1 && !IsData){
    std::cout << "Mass Bin not found in output file name"  << std::endl;
  }
  MBin=mBin;


  int flatBin=-1;
  for (uint i=0; i<flatBins.size(); ++ i){
    string stringToFind= flatBins.at(i) ;
    std::size_t found = outName.find(stringToFind);
    if (found != std::string::npos){
      flatBin=i;
      break;
    }
  }
  if (flatBin==-1 && !IsData){
    std::cout << "Flat QCD Bin not found in output file name"  << std::endl;
  }
  FlatBin=flatBin;
  

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

      fillHist("counter",0.);
      fillHist("evtsHT",float(HTBin),1.);
      fillHist("evtsM",float(MBin),1.);
      fillHist("evtsPT",float(PTBin),1.);
      fillHist("evtsFLAT",float(FlatBin),1.);      
      
      fChain->GetEntry( iEvent );
      
      //std::cout << "passFilter_HBHE\t" << passFilter_HBHE_ << std::endl;
      //std::cout << "passFilter_CSCHalo\t" << passFilter_CSCHalo_ << std::endl;
      //std::cout << "passFilter_GoodVtx\t" << passFilter_GoodVtx_ << std::endl;
      //std::cout << "passFilter_EEBadSc\t" << passFilter_EEBadSc_ << std::endl;

      /*
      if (IsData and (not passFilter_HBHE_ or
		      not passFilter_CSCHalo_ or
		      not passFilter_GoodVtx_ or not passFilter_EEBadSc_)
	  ) continue;
      */
      
      fillHist("counter",1.);              
      
      double evtweight(1.);
      double xswght=xsweight;
      if (fabs(xsweight - -1.)< 0.001) xswght=genWeight;
      
      double weight=xswght*evtweight;
      XSweight=xswght;
      EVTweight=evtweight;
      Event=EVENT_event;
      Run=EVENT_run;
      Lumi=EVENT_lumiBlock;

      //  update for reduced size ntuples
      //int  jetAK4_N(0);
      std::vector<float>              jetAK4_pt(0,0)         ;
      std::vector<float>              jetAK4_eta(0,0)         ;
      std::vector<float>              jetAK4_phi(0,0)         ;
      std::vector<float>              jetAK4_e(0,0)         ;
      //std::vector<bool>               jetAK4_IDLoose(0,0);
      std::vector<bool>               jetAK4_IDTight(0,0);      

      TLorentzVector tmpP4_1,tmpP4_2,tmpP4_3;
      //int  jetAK4_N(0);      
      if (jetAK4_pt1>0){
	//jetAK4_N=1;
	jetAK4_pt.push_back(jetAK4_pt1);
	jetAK4_eta.push_back(jetAK4_eta1);
	jetAK4_phi.push_back(jetAK4_phi1);
	jetAK4_IDTight.push_back(jetAK4_IDTight1);
	tmpP4_1.SetPtEtaPhiM(jetAK4_pt1,jetAK4_eta1,jetAK4_phi1,jetAK4_mass1);
	jetAK4_e.push_back(tmpP4_1.Energy());
	//std::cout << "CCLA: " << jetAK4_y1 << "\t" << tmpP4_1.Rapidity() << std::endl;
      }
      if (jetAK4_pt2>0){
	//jetAK4_N=2;
	jetAK4_pt.push_back(jetAK4_pt2);
	jetAK4_eta.push_back(jetAK4_eta2);
	jetAK4_phi.push_back(jetAK4_phi2);	
	jetAK4_IDTight.push_back(jetAK4_IDTight2);
	tmpP4_2.SetPtEtaPhiM(jetAK4_pt2,jetAK4_eta2,jetAK4_phi2,jetAK4_mass2);
	jetAK4_e.push_back(tmpP4_2.Energy());	
      }      
      if (jetAK4_pt3>0){
	//jetAK4_N=3;
	jetAK4_pt.push_back(jetAK4_pt3);
	jetAK4_eta.push_back(jetAK4_eta3);
	jetAK4_phi.push_back(jetAK4_phi3);
	jetAK4_IDTight.push_back(jetAK4_IDTight3);
	tmpP4_3.SetPtEtaPhiM(jetAK4_pt3,jetAK4_eta3,jetAK4_phi3,jetAK4_mass3);
	jetAK4_e.push_back(tmpP4_3.Energy());	
      }

      int  genJetAK4_N(0);
      std::vector<float>              genJetAK4_pt(0,0)         ;
      std::vector<float>              genJetAK4_eta(0,0)         ;
      std::vector<float>              genJetAK4_phi(0,0)         ;
      std::vector<float>              genJetAK4_e(0,0)         ;

      if (genJetAK4_pt1>0){
	genJetAK4_N=1;
	genJetAK4_pt.push_back(genJetAK4_pt1);
	genJetAK4_eta.push_back(genJetAK4_eta1);
	genJetAK4_phi.push_back(genJetAK4_phi1);
	tmpP4_1.SetPtEtaPhiM(genJetAK4_pt1,genJetAK4_eta1,genJetAK4_phi1,genJetAK4_mass1);
	genJetAK4_e.push_back(tmpP4_1.Energy());	
      }
      if (genJetAK4_pt2>0){
	genJetAK4_N=2;
	genJetAK4_pt.push_back(genJetAK4_pt2);
	genJetAK4_eta.push_back(genJetAK4_eta2);
	genJetAK4_phi.push_back(genJetAK4_phi2);	
	tmpP4_2.SetPtEtaPhiM(genJetAK4_pt2,genJetAK4_eta2,genJetAK4_phi2,genJetAK4_mass2);
	genJetAK4_e.push_back(tmpP4_2.Energy());	
      }      
      if (genJetAK4_pt3>0){
	genJetAK4_N=3;
	genJetAK4_pt.push_back(genJetAK4_pt3);
	genJetAK4_eta.push_back(genJetAK4_eta3);
	genJetAK4_phi.push_back(genJetAK4_phi3);
	tmpP4_3.SetPtEtaPhiM(genJetAK4_pt3,genJetAK4_eta3,genJetAK4_phi3,genJetAK4_mass3);
	genJetAK4_e.push_back(tmpP4_3.Energy());	
      }
      //
      
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
	std::cout << "\n\tNumber of triggers: " << HLT_isFired->size() << std::endl;
	std::map<std::string,bool>::iterator hlt_iter;	
	for (hlt_iter = HLT_isFired->begin(); hlt_iter!=HLT_isFired->end(); ++ hlt_iter){
	  std::cout << hlt_iter->first << std::endl;
	}
	std::cout << "\n\tUsing XS weight: " << XSweight << std::endl;
	std::cout << "\tUsing EVT weight: " << EVTweight << "\n" <<std::endl;
      }

      bool yesTrigger(true);
      bool hltPFHT900(true);
      bool hltPFHT800(true);      
      bool hltPFHT650(true);

      bool hltPFJet450(true);
      bool hltPFJet320(true);
      
      if (IsData){
	yesTrigger=false;
	hltPFHT900=false;	
	hltPFHT800=false;
	hltPFHT650=false;	

	hltPFJet450=false;
	hltPFJet320=false;
	
	bool hltPFHT650_v1(false);
	bool hltPFHT650_v2(false);
	bool hltPFHT650_v3(false);
	bool hltPFHT650_v4(false);
	bool hltPFHT650_v5(false);
	bool hltPFHT650_v6(false);
	bool hltPFHT650_v7(false);
	bool hltPFHT650_v8(false);

	bool hltPFHT800_v1(false);
	bool hltPFHT800_v2(false);
	bool hltPFHT800_v3(false);

	bool hltPFHT900_v1(false);
	bool hltPFHT900_v2(false);
	bool hltPFHT900_v3(false);
	bool hltPFHT900_v4(false);
	bool hltPFHT900_v5(false);
	bool hltPFHT900_v6(false);

	bool hltPFJet450_v4(false);
	bool hltPFJet450_v5(false);
	bool hltPFJet450_v7(false);
	bool hltPFJet450_v9(false);
	
	bool hltPFJet320_v4(false);
	bool hltPFJet320_v5(false);
	bool hltPFJet320_v7(false);
	bool hltPFJet320_v9(false);
	
	std::map<std::string,bool>::iterator trig_iter;		
	trig_iter=HLT_isFired->find("HLT_PFHT650_v1");
	if (trig_iter!=HLT_isFired->end())hltPFHT650_v1=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFHT650_v2");
	if (trig_iter!=HLT_isFired->end())hltPFHT650_v2=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFHT650_v3");
	if (trig_iter!=HLT_isFired->end())hltPFHT650_v3=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFHT650_v4");
	if (trig_iter!=HLT_isFired->end())hltPFHT650_v4=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFHT650_v5");
	if (trig_iter!=HLT_isFired->end())hltPFHT650_v5=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFHT650_v6");
	if (trig_iter!=HLT_isFired->end())hltPFHT650_v6=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFHT650_v7");
	if (trig_iter!=HLT_isFired->end())hltPFHT650_v7=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFHT650_v8");
	if (trig_iter!=HLT_isFired->end())hltPFHT650_v8=trig_iter->second;

	trig_iter=HLT_isFired->find("HLT_PFHT800_v1");
	if (trig_iter!=HLT_isFired->end())hltPFHT800_v1=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFHT800_v2");
	if (trig_iter!=HLT_isFired->end())hltPFHT800_v2=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFHT800_v3");
	if (trig_iter!=HLT_isFired->end())hltPFHT800_v3=trig_iter->second;

	trig_iter=HLT_isFired->find("HLT_PFHT900_v1");
	if (trig_iter!=HLT_isFired->end())hltPFHT900_v1=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFHT900_v2");
	if (trig_iter!=HLT_isFired->end())hltPFHT900_v2=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFHT900_v3");
	if (trig_iter!=HLT_isFired->end())hltPFHT900_v3=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFHT900_v4");
	if (trig_iter!=HLT_isFired->end())hltPFHT900_v4=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFHT900_v5");
	if (trig_iter!=HLT_isFired->end())hltPFHT900_v5=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFHT900_v6");
	if (trig_iter!=HLT_isFired->end())hltPFHT900_v6=trig_iter->second;


	trig_iter=HLT_isFired->find("HLT_PFJet450_v4");
	if (trig_iter!=HLT_isFired->end())hltPFJet450_v4=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFJet450_v5");
	if (trig_iter!=HLT_isFired->end())hltPFJet450_v5=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFJet450_v7");
	if (trig_iter!=HLT_isFired->end())hltPFJet450_v7=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFJet450_v9");
	if (trig_iter!=HLT_isFired->end())hltPFJet450_v9=trig_iter->second;

	trig_iter=HLT_isFired->find("HLT_PFJet320_v4");
	if (trig_iter!=HLT_isFired->end())hltPFJet320_v4=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFJet320_v5");
	if (trig_iter!=HLT_isFired->end())hltPFJet320_v5=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFJet320_v7");
	if (trig_iter!=HLT_isFired->end())hltPFJet320_v7=trig_iter->second;
	trig_iter=HLT_isFired->find("HLT_PFJet320_v9");
	if (trig_iter!=HLT_isFired->end())hltPFJet320_v9=trig_iter->second;	
	
	hltPFHT650=hltPFHT650_v1 || hltPFHT650_v2 || hltPFHT650_v3 ||
	  hltPFHT650_v4 || hltPFHT650_v5 || hltPFHT650_v6 || hltPFHT650_v7 || hltPFHT650_v8;
	
	hltPFHT800=hltPFHT800_v1 || hltPFHT800_v2 || hltPFHT800_v3;

	hltPFHT900=hltPFHT900_v1 || hltPFHT900_v2 || hltPFHT900_v3 || hltPFHT900_v4 ||
	  hltPFHT900_v5 || hltPFHT900_v6;

	hltPFJet450=hltPFJet450_v4 || hltPFJet450_v5 || hltPFJet450_v7 || hltPFJet450_v9;
	hltPFJet320=hltPFJet320_v4 || hltPFJet320_v5 || hltPFJet320_v7 || hltPFJet320_v9;
	
	if (WhichTrigger == "PFHT650") yesTrigger=hltPFHT650 || hltPFJet320;
	if (WhichTrigger == "PFHT800") yesTrigger=hltPFHT800 ; // early 13 TeV no OR with jet
	if (WhichTrigger == "PFHT900") yesTrigger=hltPFHT900 || hltPFJet450;
      }
      
      int ngenJets=0;
      if (!IsData) ngenJets=genJetAK4_pt.size();
      
      int njets=jetAK4_pt.size();      
      
      smrjet_energy.clear();
      smrjet_et.clear();
      smrjet_pt.clear();
      smrjet_eta.clear();
      smrjet_phi.clear();
      smrjet_rapidity.clear();
      smrjet_nConstituents.clear();
      
      vector<TLorentzVector> smearedJets;
      if (!IsData and ngenJets>0 and genJetAK4_N>0){
	for (int genj=0; genj<ngenJets; ++ genj){	
	  double genpt=genJetAK4_pt.at(genj);
	  double geneta=genJetAK4_eta.at(genj);
	  double fact=1.;
	  if (genpt >50.){
	    if (doGaussian){
	      // fact=SmearFactor(genpt,std::abs(geneta),1.);  // Suvadeep's Gaussian smearing


	      fact=jetresponse.doGaussianSmearing(genpt,geneta);
	      
	      // if (fact>1.001 && genpt>300.){
	      // 	fact=.99;
	      // 	while (fact < 1.){
	      // 
	      // 	  double xx=genpt;
	      // 	  if (xx<300) xx=300;
	      // 	  if (xx>900.)xx=900;
	      // 
	      // 	  double scaleSigma=0.99601+0.000241919*xx;
	      // 	  // double scaleSigma=1.15;	      
	      // 	  fact=SmearFactor(genpt,std::abs(geneta),scaleSigma);
	      // 	  // std::cout << "Sigma scale factor: "<< scaleSigma << std::endl;
	      // 	}	    
	      // }
	      
	    }else{
	      fact=10.;
	      int nloop=0;
	      while (fact>SmrMax){
		//fPtResol  = ptResol.resolutionEtaPt(geneta,genpt);
		//fact = fPtResol ->GetRandom();

		fact=jetresponse.doCrystalBallSmearing(genpt,geneta);		
		nloop++;
		if (nloop>10) break;
	      }
	    }
	  }
	  
	  TLorentzVector jetP4,smrP4;
	  jetP4.SetPtEtaPhiE(genJetAK4_pt.at(genj),genJetAK4_eta.at(genj),genJetAK4_phi.at(genj),genJetAK4_e.at(genj));	  
	  
	  //std::cout << "Rapidities: " << genjet_rapidity[genj] << " " << jetP4.Rapidity() << std::endl;
	  double px=jetP4.Px();
	  double py=jetP4.Py();
	  double pz=jetP4.Pz();
	  double e=jetP4.Energy();

	  smrP4.SetPxPyPzE(px*fact,py*fact,pz*fact,e*fact);
	  smearedJets.push_back(smrP4);

	  double spt=smrP4.Pt();
	  double seta=smrP4.Eta();
	  double sphi=smrP4.Phi();
	  double se=smrP4.Energy();
	  double set=smrP4.Et();
	  double sy=smrP4.Rapidity();

	  // std::cout << "Generated 4 vec: " << genpt << " " << geneta << std::endl;
	  // std::cout << "Smeared 4 vec  : " << spt << " " << seta << " " << sphi << std::endl;
	  smrjet_energy.push_back(se);
	  smrjet_et.push_back(set);
	  smrjet_pt.push_back(spt);
	  smrjet_eta.push_back(seta);
	  smrjet_phi.push_back(sphi);
	  smrjet_rapidity.push_back(sy);
	  smrjet_nConstituents.push_back(genjet_nConstituents[genj]);	  
	  
	}// endof loop over genjets
	smearedJets=sortJets(smearedJets);
	// check the sorting
	for (uint ijet=0; ijet<smearedJets.size()-1; ijet++){
	  double pt1=smearedJets.at(ijet).Pt();
	  double pt2=smearedJets.at(ijet+1).Pt();
	  if (pt2 > pt1) std::cout << "Smeared jets not ordered pt1/pt2: " << pt1 << " / " << pt2 << std::endl;
	}
      }// endof genjets if
      // RecoJets
      bool selectReco=false;
      if (njets>1){
	TLorentzVector Jet1,Jet2;
	Jet1.SetPtEtaPhiE(jetAK4_pt.at(0),jetAK4_eta.at(0),jetAK4_phi.at(0),jetAK4_e.at(0));
	Jet2.SetPtEtaPhiE(jetAK4_pt.at(1),jetAK4_eta.at(1),jetAK4_phi.at(1),jetAK4_e.at(1));
	
	selectReco=(
		    (Jet1.Pt()>30) &&
		    (Jet2.Pt()>30) &&		     
		    (fabs(Jet1.Rapidity())<2.5) &&
		    (fabs(Jet2.Rapidity())<2.5) &&
		    (fabs(Jet1.Rapidity()+Jet2.Rapidity())/2.<1.11) &&
		    (exp(fabs(Jet1.Rapidity()-Jet2.Rapidity()))<16) &&	  
		    (jetAK4_IDTight.at(0)==1) &&
		    (jetAK4_IDTight.at(1)==1)
		    );
	if (selectReco){	     
	    
	  double DijetMass = (Jet1+Jet2).M();
	  double DijetChi=exp(fabs(Jet1.Rapidity()-Jet2.Rapidity()));
	  
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

	  double teff(1.);
	  if (WhichTrigger == "PFHT800"){
	    teff=TriggerEff2015(recoDijets.mass,recoDijets.chi);
	  }else if (WhichTrigger == "PFHT900"){
	    teff=TriggerEff2016(recoDijets.mass,recoDijets.chi);
	  }
	  //if (recoDijets.mass>1500)
	  //  std::cout << "%mass/chi/teff: " << recoDijets.mass << "\t" << recoDijets.chi << "\t" << teff << std::endl;
	  double wt=weight/teff;
	  if (!yesTrigger) wt=0.;

	  fillHist("dijet_mass",DijetMass,weight);
	  if (yesTrigger) fillHist("dijet_mass_trg",DijetMass,weight);
	  fillHist("dijet_mass_trgcorr",DijetMass,wt);
	  
	  if (DijetMass>=massBins1[0] && DijetMass<massBins1[massBins1.size()-1]){
	    dijet_mass1_chi1->Fill(DijetMass,DijetChi, wt);
	    dijet_mass1_chi2->Fill(DijetMass,DijetChi, wt);
	    dijet_mass1_chi3->Fill(DijetMass,DijetChi, wt);
	    dijet_mass1_chi4->Fill(DijetMass,DijetChi, wt);
	  }

	  if (DijetMass>=massBins2[0] && DijetMass<massBins2[massBins2.size()-1]){

	    dijet_mass2_chi1->Fill(DijetMass,DijetChi, wt);
	    dijet_mass2_chi2->Fill(DijetMass,DijetChi, wt);
	    dijet_mass2_chi3->Fill(DijetMass,DijetChi, wt);
	    dijet_mass2_chi4->Fill(DijetMass,DijetChi, wt);
	  }
	  
          for ( size_t j = 0; j < (chiBins1.size()-1); ++j )
          {

              if((DijetChi>=chiBins1[j])&&
	         (DijetChi<chiBins1[j+1]))
              {
                  mhists[j]->Fill(DijetMass, wt);
	      }
	  }
	  
          for ( size_t j = 0; j < (massBins2.size()-1); ++j )
          {
              if((DijetMass>=massBins2[j])&&
	         (DijetMass<massBins2[j+1]))
              {
                  hists[j]->Fill(DijetChi, wt);
	      }
	  }
	  
	}
      }

      // GenJets
      bool selectGen=false;
      if (!IsData && ngenJets>1){
	TLorentzVector Jet1,Jet2;
	Jet1.SetPtEtaPhiE(genJetAK4_pt.at(0),genJetAK4_eta.at(0),genJetAK4_phi.at(0),genJetAK4_e.at(0));
	Jet2.SetPtEtaPhiE(genJetAK4_pt.at(1),genJetAK4_eta.at(1),genJetAK4_phi.at(1),genJetAK4_e.at(1));
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

          for ( size_t j = 0; j < (massBins2.size()-1); ++j )
          {
              if((DijetMass>=massBins2[j])&&
	         (DijetMass<massBins2[j+1]))
              {
                  ghists[j]->Fill(genDijets.chi, weight);
	      }
	  }	  
	};

	int i1=findLeading(smrjet_pt);
	int i2=findNextLeading(smrjet_pt,i1);
	if ( (smrjet_pt.size()>=2) && (i1 == -1 || i2 == -1 || i1 == i2) ){
	  std::cout << "Trouble with sorting" << std::endl;
	  std::cout << "Pt1: " << smrjet_pt[i1] << " Pt2: " << smrjet_pt[i2] << std::endl;
	}
	
	bool selectSmr = 
	  (smrjet_pt.size()>=2)&&
	  (smrjet_pt[i1]>30)&&
	  (smrjet_pt[i2]>30)&&
	  (fabs(smrjet_rapidity[i1])<2.5)&&
	  (fabs(smrjet_rapidity[i2])<2.5)&&
	  (fabs(smrjet_rapidity[i1]+smrjet_rapidity[i2])/2.<1.11)&&
	  (exp(fabs(smrjet_rapidity[i1]-smrjet_rapidity[i2]))<16);
	  
	  //(smrjet_nConstituents[i1]>1)&&	     
	  //(smrjet_nConstituents[i2]>1);
	if(selectSmr)
	  {
	    // fill smrjets
	    TLorentzVector j1P4,j2P4,dijet;
	    j1P4=smearedJets.at(0);
	    j2P4=smearedJets.at(1);
	    dijet=j1P4+j2P4;
	    double invmass=dijet.M();
	    double DijetMass=invmass;
	    fillHist("dijet_mass_smeared",invmass,weight);
	    
	    double pt1=smearedJets.at(0).Pt();
	    double pt2=smearedJets.at(1).Pt();
	    if (abs(pt1-smrjet_pt[i1]) > 0.0005)
	      std::cout << "Problems wLeading: " << pt1 << " " <<  smrjet_pt[i1] << std::endl;
	    if (abs(pt2-smrjet_pt[i2]) > 0.0005)
	      std::cout << "Problems wNextLeading: " << pt2 << " " <<  smrjet_pt[i2] << std::endl;
	    
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

	    for ( size_t j = 0; j < (massBins2.size()-1); ++j )
	      {
		if((DijetMass>=massBins2[j])&&
		   (DijetMass<massBins2[j+1]))
		    {
		      shists[j]->Fill(smrDijets.chi, weight);
		    }
	      }	      
	  }
	//now check the response
	for (int genj=0; genj<ngenJets; ++ genj){
	  if (genj>1)break;
	  
	  double genpt=genJetAK4_pt.at(genj);
	  if (genpt > 50.){
	    TLorentzVector GJet;
	    GJet.SetPtEtaPhiE(genJetAK4_pt.at(genj),genJetAK4_eta.at(genj),genJetAK4_phi.at(genj),genJetAK4_e.at(genj));
	    double geny=GJet.Rapidity();
	    double genphi=GJet.Phi();
	
	    // loop over recojets; find best match
	    double drmin=99.;
	    int indx_m=-1.;
	    for (uint recj=0; recj<jetAK4_pt.size(); ++ recj){
	      TLorentzVector RJet;
	      RJet.SetPtEtaPhiE(jetAK4_pt.at(recj),jetAK4_eta.at(recj),jetAK4_phi.at(recj),jetAK4_e.at(recj));
	      double dr=deltaR(geny,genphi,RJet.Rapidity(),RJet.Phi());
	      if (dr<drmin) {
		drmin=dr;
		indx_m=recj;
	      }
	    }//end of loop over reco jets
	    if (drmin<0.25){
	      double recpt=jetAK4_pt.at(indx_m);
	      double rat=recpt/genpt;

	      double tpt=genpt;
	      if (tpt<400.) tpt=400;
	      if (tpt>1900) tpt=1900;
	      double fact=1.;
	      // double fact=0.970847-3.13224e-05*tpt+5.21555e-08*tpt*tpt-1.52647e-11*tpt*tpt*tpt;
			   
	      fill3DHist("Resp3D",genpt,geny,rat/fact,weight);
	      if (genpt>300. and genpt < 400. and abs(geny)<1.) fillHist("Resp",rat/fact,weight);
	    }
	    // now smeared jets.  No need to find best match as there is no position smearing
	    double rat=smrjet_pt[genj]/genpt;
	    fill3DHist("SmrResp3D",genpt,geny,rat,weight);
	    // std::cout << "smrjet size: " << smrjet_pt.size() << std::endl;
	    // std::cout << "XXX: " << smrjet_pt[genj] << " -- " << genpt << " " << genjet_pt[genj]<< std::endl;
	    if ((genpt>300.) && (genpt < 400.) && (abs(geny)<1.) ) fillHist("SmrResp",rat,weight);
	    if ((genpt>600.) && (genpt < 800.) && (abs(geny)>2.0)) fillHist("SmrResp2",rat,weight);	    
	  }// genpt>50
	}// end of loop over genjets
      }// end of ngenjets if
      _outTree->Fill();
    }//endof Main Event looo
  
  return;
}

int main(int argc, char* argv[])
{
  // load framework libraries
  gSystem->Load( "libFWCoreFWLite" );
  AutoLibraryLoader::enable();

  clock_t start = clock();
  
  // parse arguments
  if ( argc < 2 ) {
    std::cout << "Usage : " << argv[0] << " [parameters.py]" << std::endl;
    return 0;
  }

  cout << "Beginning ChiNtuple maker" << endl;
  ChiNtuple* chiNtuple = new ChiNtuple();


  if( !edm::readPSetsFrom(argv[1])->existsAs<edm::ParameterSet>("process") ){
    std::cout << " ERROR: ParametersSet 'process' is missing in your configuration file" << std::endl; exit(0);
  }
  const edm::ParameterSet& process = edm::readPSetsFrom(argv[1])->getParameter<edm::ParameterSet>("process");
  const edm::ParameterSet& ana = process.getParameter<edm::ParameterSet>("chiNtuples");
  int NEVENTS_( ana.getParameter<int>("Nevts") );  
  double XS_( ana.getParameter<double>("CrossSection") );
  bool ISDATA_( ana.getParameter<bool>("IsData") );
  bool DOGAUSSIAN_( ana.getParameter<bool>("DoGaussian") );
  bool AK4_SF_( ana.getParameter<bool>("AK4_SF") );
  bool DATAtoMC_SF_( ana.getParameter<bool>("DATAtoMC_SF") );
  string INPUTFILES_( ana.getParameter<string>("InputFiles") );
  string OUTPUTFILE_( ana.getParameter<string>("OutputFile") );
  string TRIGGER_( ana.getParameter<string>("Trigger") );    
  double SMEARMAX_( ana.getParameter<double>("SmearMax") );
  int SYSERR_( ana.getParameter<int>("SysErr") );
  
  chiNtuple->SetXSWeight(XS_);
  chiNtuple->SetIsData(ISDATA_);
  chiNtuple->SetDoGaussian(DOGAUSSIAN_);
  chiNtuple->SetSmrMax(SMEARMAX_);
  chiNtuple->SetNevents(NEVENTS_);
  chiNtuple->SetDoSysErr(SYSERR_);
  chiNtuple->SetAK4_SF(AK4_SF_);
  chiNtuple->SetDataToMC_SF(DATAtoMC_SF_);  
  chiNtuple->SetTrigger(TRIGGER_);
  
  cout << "Booking Histograms..." << endl;
  chiNtuple->BookHistograms(OUTPUTFILE_);

  cout << "Reading Ntuples from: "<< INPUTFILES_ << endl;  
  bool fok =chiNtuple->OpenWithList(INPUTFILES_);
  if ( not fok ){
    cout << "Trouble opening list" <<endl;
    delete chiNtuple;    
    return 1;
  }

  chiNtuple->Loop();
  chiNtuple->WriteHistograms();
  std::cout << "ChiNtuple: Finished Processing Normally" << std::endl;

  clock_t elapsedTicks = clock() - start;
  double elapsedTimeInSeconds = elapsedTicks/CLOCKS_PER_SEC;
  std::cout << "CPU processing time (in seconds): " << int(elapsedTimeInSeconds) << "\n" << std::endl;
  delete chiNtuple;
  return 0;
}
