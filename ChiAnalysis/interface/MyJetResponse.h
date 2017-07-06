#ifndef MYJETRESPONSE_H
#define MYJETRESPONSE_H

#include <vector>
#include <string>

using std::cout;
using std::endl;
using std::string;
using std::vector;
using std::map;

#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "TRandom.h"
#include "TMath.h"

double fnc_dscb(double*xx,double*pp)
{
  double x   = xx[0];
  double N   = pp[0];
  double mu  = pp[1];
  double sig = pp[2];
  double a1  = pp[3];
  double p1  = pp[4];
  double a2  = pp[5];
  double p2  = pp[6];

  
  double u   = (x-mu)/sig;
  double A1  = TMath::Power(p1/TMath::Abs(a1),p1)*TMath::Exp(-a1*a1/2);
  double A2  = TMath::Power(p2/TMath::Abs(a2),p2)*TMath::Exp(-a2*a2/2);
  double B1  = p1/TMath::Abs(a1) - TMath::Abs(a1);
  double B2  = p2/TMath::Abs(a2) - TMath::Abs(a2);
  
  double result(N);
  if      (u<-a1) result *= A1*TMath::Power(B1-u,-p1);
  else if (u<a2)  result *= TMath::Exp(-u*u/2);
  else            result *= A2*TMath::Power(B2+u,-p2);
  return result;
}

class MyJetResponse {
 public:
 MyJetResponse(bool AK4_SF=false, bool DATAtoMC_SF=false, int SYSUNC=0) : ak4_sf(AK4_SF), datamc_sf(DATAtoMC_SF), sysunc(SYSUNC) {}
  
  double doGaussianSmearing(double pt,double eta){

    double fact;
  
    int ibin=WhichEtaBin(eta,etaMinBins_Sigmas,etaMaxBins_Sigmas);
    std::vector<float> thePars= parameters_Sigmas[ibin];
  
    double x=pt;
    double e=eta;
    Double_t p0=thePars[0];
    double mean = 1.;
    double sigma = sqrt(((TMath::Sign(1.,p0)*pow(thePars[0]/x,2))+(pow(thePars[1],2)*pow(x,(thePars[3]-1))))+pow(thePars[2],2));

    //std::cout << "Sigma: "<< sigma << std::endl;

    if (ak4_sf) sigma=sigma*ak4_scalefact(x,e);
    if (datamc_sf) sigma=sigma*DataToMC_scalefact(e);

    // if (sysunc == 1) sigma  = sigma*(1 + 0.1);
    // if (sysunc == -1) sigma = sigma*(1 - 0.1);
    if (sysunc == 1) sigma  = sigma*(1 + DataToMC_scalefactorUncert(e));
    if (sysunc == -1) sigma = sigma*(1 - DataToMC_scalefactorUncert(e));
    
    double r = rnd.Gaus(mean,sigma);
  
    //TF1 *f1 = new TF1("f1","gaus",0,5);
    //f1->SetParameter(0,1.);
    //f1->SetParameter(1,mean);
    //f1->SetParameter(2,sigma);
    //double r=f1->GetRandom();
    //delete f1;
 
    //fact=r/mean;
    fact=r;
    return fact;
  }

  double doCrystalBallSmearing(double pt,double eta){

    double fact;
    //double smf_e=1.;

 
    int ibin=WhichEtaBin(eta,etaMinBins_Sigmas,etaMaxBins_Sigmas);
    std::vector<float> sigmas= parameters_Sigmas[ibin];

    double x=pt;
    double e=eta;
    Double_t p0=sigmas[0];
    double mean = 1.;
    double sigma = sqrt(((TMath::Sign(1.,p0)*pow(sigmas[0]/x,2))+(pow(sigmas[1],2)*pow(x,(sigmas[3]-1))))+pow(sigmas[2],2));

    ibin=WhichEtaBin(eta,etaMinBins_Aones,etaMaxBins_Aones);
    std::vector<float> aones= parameters_Aones[ibin];
    double a1=aones[0];
  
    ibin=WhichEtaBin(eta,etaMinBins_Atwos,etaMaxBins_Atwos);
    std::vector<float> atwos= parameters_Atwos[ibin];
    double a2=atwos[0]*pow(x,atwos[1]);  

    ibin=WhichEtaBin(eta,etaMinBins_Pones,etaMaxBins_Pones);
    std::vector<float> pones= parameters_Pones[ibin];
    double p1=TMath::Max(0.0,(pones[0]-pones[3])/(1.+exp(pones[1]*(x-pones[2])))+pones[3]);

    ibin=WhichEtaBin(eta,etaMinBins_Ptwos,etaMaxBins_Ptwos);
    std::vector<float> ptwos= parameters_Ptwos[ibin];
    double p2=TMath::Max(0.0,(ptwos[0]-ptwos[3])/(1.+exp(ptwos[1]*(x-ptwos[2])))+ptwos[3]);   

    // std::cout << sigma << "\t" << sf << "\t" << sf << "\t" << sf << "\t" << sf << "\t" << sf << std::cout;
    
    if (ak4_sf) sigma=sigma*ak4_scalefact(x,e);    
    if (datamc_sf) sigma=sigma*DataToMC_scalefact(e);

    // if (sysunc == 1) sigma  = sigma*(1 + 0.1);
    // if (sysunc == -1) sigma = sigma*(1 - 0.1);
    if (sysunc == 1) sigma  = sigma*(1 + DataToMC_scalefactorUncert(e));
    if (sysunc == -1) sigma = sigma*(1 - DataToMC_scalefactorUncert(e));
    
    TF1 *f1 = new TF1("f1",fnc_dscb,0.,5.,7);
    f1->SetParameter(0,1.);
    f1->SetParameter(1,mean);
    f1->SetParameter(2,sigma);
    f1->SetParameter(3,a1);
    f1->SetParameter(4,p1);
    f1->SetParameter(5,a2);
    f1->SetParameter(6,p2);
  
    double r=f1->GetRandom();

    delete f1;
  
    //fact=r/mean;
    fact=r;
    return fact;
  }
  
  void GetResolutionParameters(const std::string& fileName,const bool doGauss){

    JetCorrectorParameters resolutionPars(fileName,"resolution");
  
    size_t pos;
    string tmp = resolutionPars.definitions().level();
    pos = tmp.find(':');
    while (!tmp.empty()) {
      string paramAsStr = tmp.substr(0,pos);
      std::cout << "CCLA1 paramAsStr: << " << paramAsStr << std::endl;
    
      if (!doGauss||paramAsStr=="mean"||paramAsStr=="sigma") {
	JetCorrectorParameters* parameters = new JetCorrectorParameters(fileName,paramAsStr);
	std::cout << "CCLA: " << parameters->size() << "\t" << parameters->definitions().level() << std::endl;
	if (paramAsStr=="sigma"){
	  const unsigned npar(6);
	  assert(parameters->size() != npar); // does nothing at the moment

	  for (unsigned iPar=0;iPar<parameters->size();iPar++) {
   
	    const JetCorrectorParameters::Record& record=parameters->record(iPar);
	    //std::cout << "\tCCLA: npars: " << record.nParameters() << std::endl;
	    //std::cout << "\tCCLA: npars: " << record.xMin(0) << " - " << record.xMax(0) << std::endl;
	    etaMinBins_Sigmas.push_back(record.xMin(0));
	    etaMaxBins_Sigmas.push_back(record.xMax(0));
	    const std::vector<float>& pars = record.parameters();
	    std::vector<float> thePars;
	    for (unsigned i=2;i<pars.size();i++) {
	      //std::cout << "\t\t pars: " << pars[i] << std::endl;
	      thePars.push_back(pars[i]);
	    }
	    parameters_Sigmas.push_back(thePars);
	  
	  }
	  //std::cout << "Size of sigmas vector: " << parameters_Sigmas.size() << std::endl;
	  //std::cout << "Size of etamins vector: " << etaMinBins_Sigmas.size() << std::endl;
      
	}else if (paramAsStr=="aone"){

	  const unsigned npar(3);
	  assert(parameters->size() != npar); // does nothing at the moment

	  for (unsigned iPar=0;iPar<parameters->size();iPar++) {
   
	    const JetCorrectorParameters::Record& record=parameters->record(iPar);
	    //std::cout << "\tCCLA: npars: " << record.nParameters() << std::endl;
	    //std::cout << "\tCCLA: aone etabins: " << record.xMin(0) << " - " << record.xMax(0) << std::endl;
	    etaMinBins_Aones.push_back(record.xMin(0));
	    etaMaxBins_Aones.push_back(record.xMax(0));
	    const std::vector<float>& pars = record.parameters();
	    std::vector<float> thePars;
	    for (unsigned i=2;i<pars.size();i++) {
	      //std::cout << "\t\t aone pars: " << pars[i] << std::endl;
	      thePars.push_back(pars[i]);
	    }
	    parameters_Aones.push_back(thePars);
	  }
	
	}else if (paramAsStr=="pone"){

	  const unsigned npar(6);
	  assert(parameters->size() != npar); // does nothing at the moment

	  for (unsigned iPar=0;iPar<parameters->size();iPar++) {
   
	    const JetCorrectorParameters::Record& record=parameters->record(iPar);
	    //std::cout << "\tCCLA: npars: " << record.nParameters() << std::endl;
	    //std::cout << "\tCCLA: pone etabins: " << record.xMin(0) << " - " << record.xMax(0) << std::endl;
	    etaMinBins_Pones.push_back(record.xMin(0));
	    etaMaxBins_Pones.push_back(record.xMax(0));
	    const std::vector<float>& pars = record.parameters();
	    std::vector<float> thePars;
	    for (unsigned i=2;i<pars.size();i++) {
	      //std::cout << "\t\t pone pars: " << pars[i] << std::endl;
	      thePars.push_back(pars[i]);
	    }
	    parameters_Pones.push_back(thePars);
	  }
	  
	}else if (paramAsStr=="atwo"){

	  const unsigned npar(4);
	  assert(parameters->size() != npar); // does nothing at the moment

	  for (unsigned iPar=0;iPar<parameters->size();iPar++) {
   
	    const JetCorrectorParameters::Record& record=parameters->record(iPar);
	    //std::cout << "\tCCLA: npars: " << record.nParameters() << std::endl;
	    //std::cout << "\tCCLA: atwo etabins: " << record.xMin(0) << " - " << record.xMax(0) << std::endl;
	    etaMinBins_Atwos.push_back(record.xMin(0));
	    etaMaxBins_Atwos.push_back(record.xMax(0));
	    const std::vector<float>& pars = record.parameters();
	    std::vector<float> thePars;
	    for (unsigned i=2;i<pars.size();i++) {
	      //std::cout << "\t\t atwo pars: " << pars[i] << std::endl;
	      thePars.push_back(pars[i]);
	    }
	    parameters_Atwos.push_back(thePars);
	  
	  }
	
	}else if (paramAsStr=="ptwo"){

	  const unsigned npar(6);
	  assert(parameters->size() != npar); // does nothing at the moment

	  for (unsigned iPar=0;iPar<parameters->size();iPar++) {
   
	    const JetCorrectorParameters::Record& record=parameters->record(iPar);
	    //std::cout << "\tCCLA: npars: " << record.nParameters() << std::endl;
	    //std::cout << "\tCCLA: ptwo etabins: " << record.xMin(0) << " - " << record.xMax(0) << std::endl;
	    etaMinBins_Ptwos.push_back(record.xMin(0));
	    etaMaxBins_Ptwos.push_back(record.xMax(0));
	    const std::vector<float>& pars = record.parameters();
	    std::vector<float> thePars;
	    for (unsigned i=2;i<pars.size();i++) {
	      //std::cout << "\t\t ptwo pars: " << pars[i] << std::endl;
	      thePars.push_back(pars[i]);
	    }
	    parameters_Ptwos.push_back(thePars);
	  }
	}
      }
    
      tmp = (pos==string::npos) ? "" : tmp.substr(pos+1);
      pos = tmp.find(':');
    }  
  }
  
 private:
  TRandom rnd;
  bool ak4_sf, datamc_sf;
  int sysunc;
  std::vector<double> etaMinBins_Sigmas, etaMaxBins_Sigmas;
  std::vector<double> etaMinBins_Aones, etaMaxBins_Aones;
  std::vector<double> etaMinBins_Pones, etaMaxBins_Pones;
  std::vector<double> etaMinBins_Atwos, etaMaxBins_Atwos;
  std::vector<double> etaMinBins_Ptwos, etaMaxBins_Ptwos;  
  std::vector<std::vector<float>> parameters_Sigmas, parameters_Aones, parameters_Pones,parameters_Atwos, parameters_Ptwos;


  double ak4_scalefact(double x, double e){
    double fact(1.);
    double xx=x;
    double ee=fabs(e);
    // 74x smearing    
    // if (xx<300) xx=300;
    // if (xx>900.)xx=900;
    // fact=0.99601+0.000241919*xx;

    // 76x smearing
    // if (xx<300) xx=300;
    // if (xx>2000.)xx=2000;
    // fact=1.38043e+00*TMath::TanH(3.45865e-04*(xx-(-2.06310e+03)));

    // 80x smearing

    if (ee<=0.5) {
      if (xx<=2500) fact=0.95;
      if (xx>2500) fact=1.0;
    }

    if (ee>1.0 && ee<=1.5) {
      if (xx<=600) fact=1.0;
      if (xx>600) fact=1.1;
    }
    
    if (ee>1.5 && ee<=2.1) {
      if (xx<=600) fact=1.2;
      if (xx>600 && xx<=1400) fact=1.3;
      if (xx>=1400) fact=1.4;
    }

    if (ee>2.1) {
      if (xx<=1000) fact=1.3;
      if (xx>1000) fact=1.5;
    }
    
    // if (xx<500) xx=500;
    // if (xx>1000.)xx=900;
    // fact=1.38043e+00*TMath::TanH(3.45865e-04*(xx-(-2.06310e+03)));
    
    // std::cout << "AK4_Scalefact: " << "pt: " << x << "\t" << fact << std::endl;
    return fact;
  }

  // old 74x scale factors
  // double DataToMC_scalefact(double xx){
  //   double fact(1.);
  // 
  //   double eta=fabs(xx);
  // 
  //   if (eta < 0.8) {
  //     fact=1.094;
  //   }
  //   else if (eta < 1.3) {
  //     fact=1.071;
  //   }
  //   else if (eta < 1.9) {
  //     fact=1.108;
  //   }
  //   else if (eta < 2.5) {
  //     fact=1.13;
  //   }
  //   
  //   // std::cout << "DataToMC_Scalefact: " << fact << std::endl;
  //   return fact;
  // }
  // new scale factors for 76x
//   double DataToMC_scalefact(double xx){
//     double fact(1.);
// 
//     double eta=fabs(xx);
// 
//     if (eta < 0.5) {
//       fact=1.095;
//     }
//     else if (eta < 0.8) {
//       fact=1.120;
//     }
//     else if (eta < 1.1) {
//       fact=1.097;
//     }
//     else if (eta < 1.3) {
//       fact=1.103;
//     }
//     else if (eta < 1.7) {
//       fact=1.118;
//     }
//     else if (eta < 1.9) {
//       fact=1.100;
//     }
//     else if (eta < 2.1) {
//       fact=1.162;
//     }
//     else if (eta < 2.3) {
//       fact=1.160;
//     }
//     else if (eta < 2.5) {
//       fact=1.161;
//     }
//     
//     // std::cout << "DataToMC_Scalefact: " << fact << std::endl;
//     return fact;
//   }  
// 
  // new scale factors for 80x
  double DataToMC_scalefact(double xx){
    double fact(1.);

    double eta=fabs(xx);

    if (eta < 0.5) {
      fact=1.109;
    }
    else if (eta < 0.8) {
      fact=1.138;
    }
    else if (eta < 1.1) {
      fact=1.114;
    }
    else if (eta < 1.3) {
      fact=1.123;
    }
    else if (eta < 1.7) {
      fact=1.084;
    }
    else if (eta < 1.9) {
      fact=1.082;
    }
    else if (eta < 2.1) {
      fact=1.140;
    }
    else if (eta < 2.3) {
      fact=1.067;
    }
    else if (eta < 2.5) {
      fact=1.177;
    }
    // std::cout << "DataToMC_Scalefact: " << fact << std::endl;
    return fact;
  }

  double DataToMC_scalefactorUncert(double xx){
    double fact(1.);

    double eta=fabs(xx);

    if (eta < 0.5) {
      fact=0.008;
    }
    else if (eta < 0.8) {
      fact=0.013;
    }
    else if (eta < 1.1) {
      fact=0.013;
    }
    else if (eta < 1.3) {
      fact=0.024;
    }
    else if (eta < 1.7) {
      fact=0.011;
    }
    else if (eta < 1.9) {
      fact=0.035;
    }
    else if (eta < 2.1) {
      fact=0.047;
    }
    else if (eta < 2.3) {
      fact=0.053;
    }
    else if (eta < 2.5) {
      fact=0.041;
    }
    
    // std::cout << "DataToMC_Scalefact: " << fact << std::endl;
    return fact;
  }

  
  int WhichEtaBin(double eta, const std::vector<double> etaMinBins, const std::vector<double> etaMaxBins){
    int ibin=-1;
    unsigned n=etaMaxBins.size();
    
    if (eta<etaMinBins.at(0) || eta>etaMaxBins.at(n-1)){
      std::cout << "%%% Eta out of range!!! " << eta << "\t" << etaMinBins.at(0) << "\t" << etaMaxBins.at(n-1) << std::endl;
      if (eta<etaMinBins.at(0)) eta=etaMinBins.at(0);
      if (eta>etaMaxBins.at(n-1)) eta=etaMaxBins.at(n-1);
    }
    
    for (unsigned i=0;i<n;i++) {
      if (eta<=etaMaxBins[i]) return i;
    }
    std::cout << "Could not find ETA bin "<< std::endl;
    return ibin;
  }
  
};


#endif
