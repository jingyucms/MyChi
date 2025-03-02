#!/usr/bin/env python

import ROOT
#from ROOT import *
#ROOT.gROOT.SetMacroPath(ROOT.gROOT.GetMacroPath() + ":"+os.getcwd())

ROOT.gROOT.LoadMacro('./RooUnfold/libRooUnfold.so')
ROOT.gROOT.LoadMacro('../NtupleStruct_h.so')


import sys,string,os,math
import argparse
import glob

#from math import floor
from array import array
#from RootIOFuncs import *
# from PhysicsTools.PythonAnalysis import *

#from ROOT import RooUnfoldResponse
#from ROOT import RooUnfold
#from ROOT import RooUnfoldBayes


from RootIOFuncs import *

# ROOT.gROOT.SetMacroPath(ROOT.gROOT.GetMacroPath() + ":" + os.path.join(os.environ.get("CMSSW_BASE"),'src/Analysis'))
#sys.exit()

### Histogram binning
nMass=14
minMass=1000.
maxMass=13000.

nChi=15
minChi=1.
maxChi=16.

# massBins=[400,600,800,1000,1200,1500,1900,2400,3000,4000,5000,7000]


## massBins2=[0,1000,1200,1500,1900,2400,3000,3600,4200,8000]
massBins1=[1000,1200,1500,1900,2400,3000,3600,4200,4800,5400,6000,13000]
massBins2=[1000,1200,1500,1900,2400,3000,3600,4200,4800,5400,6000,7000,13000]


chiBins1=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
chiBins2=[1,2,3,4,5,6,7,8,9,10,12,14,16]
chiBins3=[1,3,6,9,12,16]
chiBins4=[1,3,5,7,10,12,14,16]

def BookHistograms():

    ### Book the histograms

    hists={}

    # currentDir=gFile.pwd()
    # print currentDir

    hName="NStep1"
    hTitle="Number of Step1 Events"
    hists[hName] = Book1D(hName,hTitle,1,-0.5,0.5,False)

    hName="Counter"
    hTitle="Counter"
    hists[hName] = Book1D(hName,hTitle,5,-0.5,4.5,False)

    hName="EvtsHT"
    hTitle="Number of Events per HT Bin";
    hists[hName] = Book1D(hName,hTitle,11,-1.5,9.5,False)

    hName="EvtsM"
    hTitle="Number of Events per Mass Bin";
    hists[hName] = Book1D(hName,hTitle,5,-1.5,3.5,False)

    hName="EvtsFLAT"
    hTitle="Number of Events in FLAT QCD Sample";
    hists[hName] = Book1D(hName,hTitle,5,-1.5,3.5,False)

    hName="EvtsPT"
    hTitle="Number of Events per PT Bin";
    hists[hName] = Book1D(hName,hTitle,11,-1.5,9.5,False)

    hName="dijet_mass_reco1"
    hTitle="M_{jj} -- Reconstructed"
    hists[hName] = Book1D(hName,hTitle,nMass,minMass,maxMass,True)

    hName="dijet_mass_reco2"
    hTitle="M_{jj} -- Reconstructed"
    hists[hName] = Book1D(hName,hTitle,1300,0.,13000.,True)

    hName="dijet_mass_reco3"
    hTitle="M_{jj} -- Reconstructed"
    hists[hName] = Book1D(hName,hTitle,76,400,8000.,True)

    hName="dijet_mass_gen1"
    hTitle="M_{jj} -- Generated"
    hists[hName] = Book1D(hName,hTitle,nMass,minMass,maxMass,True)

    hName="dijet_mass_gen2"
    hTitle="M_{jj} -- Generated"
    hists[hName] = Book1D(hName,hTitle,1300,0.,13000.,True)

    hName="dijet_mass_gen3"
    hTitle="M_{jj} -- Generated"
    hists[hName] = Book1D(hName,hTitle,76,400,8000.,True)

    hName="dijet_mass_smr1"
    hTitle="M_{jj} -- Smeared"
    hists[hName] = Book1D(hName,hTitle,nMass,minMass,maxMass,True)

    hName="dijet_mass_smr2"
    hTitle="M_{jj} -- Smeared"
    hists[hName] = Book1D(hName,hTitle,1300,0.,13000.,True)

    hName="dijet_mass_smr3"
    hTitle="M_{jj} -- Smeared"
    hists[hName] = Book1D(hName,hTitle,76,400,8000.,True)

    hName="dijet_yboost_gen"
    hTitle=hName
    hists[hName] = Book1D(hName,hTitle,40,0.,4.,True)

    hName="dijet_eta1_gen"
    hTitle=hName
    hists[hName] = Book1D(hName,hTitle,20,-5.,5.,True)

    ## ccla now create 2d hists for the 2d chi/mass unfolding
    hName="dijet_mass_chi_RECO"
    hTitle="M_{jj} vs #chi Response -- RECO jets"
    hists[hName] = Book2D(hName,hTitle,nMass,minMass,maxMass,nChi,minChi,maxChi,True)

    hName="dijet_mass1_chi1_RECO"
    hTitle="M_{jj} vs #chi Response -- RECO jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,chiBins1,True)

    hName="dijet_mass1_chi2_RECO"
    hTitle="M_{jj} vs #chi Response -- RECO jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,chiBins2,True)

    hName="dijet_mass1_chi3_RECO"
    hTitle="M_{jj} vs #chi Response -- RECO jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,chiBins3,True)

    hName="dijet_mass1_chi4_RECO"
    hTitle="M_{jj} vs #chi Response -- RECO jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,chiBins4,True)

    hName="dijet_mass2_chi1_RECO"
    hTitle="M_{jj} vs #chi Response -- RECO jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,chiBins1,True)

    hName="dijet_mass2_chi2_RECO"
    hTitle="M_{jj} vs #chi Response -- RECO jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,chiBins2,True)

    hName="dijet_mass2_chi3_RECO"
    hTitle="M_{jj} vs #chi Response -- RECO jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,chiBins3,True)

    hName="dijet_mass2_chi4_RECO"
    hTitle="M_{jj} vs #chi Response -- RECO jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,chiBins4,True)

    hName="dijet_massgen_massRECO_1"
    hTitle="M_{jj} Gen  vs M_{jj} Reco"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,massBins1,True)

    hName="dijet_massgen_massRECO_2"
    hTitle="M_{jj} Gen  vs M_{jj} Reco"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,massBins2,True)

    hName="dijet_massgen_massRECO_nowt"
    hTitle="M_{jj} Gen  vs M_{jj} Reco -- Unweighted"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,massBins1,True)

    hName="dijet_massgen_massRECO_1_nowt"
    hTitle="M_{jj} Gen  vs M_{jj} Reco -- Unweighted"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,massBins1,True)

    hName="dijet_massgen_massRECO_2_nowt"
    hTitle="M_{jj} Gen  vs M_{jj} Reco -- Unweighted"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,massBins2,True)

    hName="dijet_chigen_chiRECO"
    hTitle="#chi Gen  vs #chi Reco"
    hists[hName] = Book2DwithVarBins(hName,hTitle,chiBins2,chiBins2,True)

    hName="dijet_chigen_chiRECO_nowt"
    hTitle="#chi Gen  vs #chi Reco -- Unweighted"
    hists[hName] = Book2DwithVarBins(hName,hTitle,chiBins2,chiBins2,True)

    hName="dijet_massgen_massSMR_1"
    hTitle="M_{jj} Gen  vs M_{jj} Smeared"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,massBins1,True)

    hName="dijet_massgen_massSMR_2"
    hTitle="M_{jj} Gen  vs M_{jj} Smeared"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,massBins2,True)

    hName="dijet_massgen_massSMR_1_nowt"
    hTitle="M_{jj} Gen  vs M_{jj} Smeared -- Unweighted"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,massBins1,True)

    hName="dijet_massgen_massSMR_2_nowt"
    hTitle="M_{jj} Gen  vs M_{jj} Smeared -- Unweighted"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,massBins2,True)

    hName="dijet_chigen_chiSMR"
    hTitle="#chi Gen  vs #chi Smeared"
    hists[hName] = Book2DwithVarBins(hName,hTitle,chiBins2,chiBins2,True)

    hName="dijet_chigen_chiSMR_nowt"
    hTitle="#chi Gen  vs #chi Smeared -- Unweighted"
    hists[hName] = Book2DwithVarBins(hName,hTitle,chiBins2,chiBins2,True)

    hName="dijet_mass_chi_SMR"
    hTitle="M_{jj} vs #chi Response -- SMEARED jets"
    hists[hName] = Book2D(hName,hTitle,nMass,minMass,maxMass,nChi,minChi,maxChi,True)

    hName="dijet_mass1_chi1_SMR"
    hTitle="M_{jj} vs #chi Response -- SMEARED jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,chiBins1,True)

    hName="dijet_mass1_chi2_SMR"
    hTitle="M_{jj} vs #chi Response -- SMEARED jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,chiBins2,True)

    hName="dijet_mass1_chi3_SMR"
    hTitle="M_{jj} vs #chi Response -- SMEARED jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,chiBins3,True)

    hName="dijet_mass1_chi4_SMR"
    hTitle="M_{jj} vs #chi Response -- SMEARED jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,chiBins4,True)

    hName="dijet_mass2_chi1_SMR"
    hTitle="M_{jj} vs #chi Response -- SMEARED jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,chiBins1,True)

    hName="dijet_mass2_chi2_SMR"
    hTitle="M_{jj} vs #chi Response -- SMEARED jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,chiBins2,True)

    hName="dijet_mass2_chi3_SMR"
    hTitle="M_{jj} vs #chi Response -- SMEARED jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,chiBins3,True)

    hName="dijet_mass2_chi4_SMR"
    hTitle="M_{jj} vs #chi Response -- SMEARED jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,chiBins4,True)

    hName="dijet_mass_chi_GEN"
    hTitle="M_{jj} vs #chi Response -- GEN jets"
    hists[hName] = Book2D(hName,hTitle,nMass,minMass,maxMass,nChi,minChi,maxChi,True)

    hName="dijet_mass1_chi1_GEN"
    hTitle="M_{jj} vs #chi Response -- GEN jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,chiBins1,True)

    hName="dijet_mass1_chi2_GEN"
    hTitle="M_{jj} vs #chi Response -- GEN jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,chiBins2,True)

    hName="dijet_mass1_chi3_GEN"
    hTitle="M_{jj} vs #chi Response -- GEN jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,chiBins3,True)

    hName="dijet_mass1_chi4_GEN"
    hTitle="M_{jj} vs #chi Response -- GEN jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins1,chiBins4,True)

    hName="dijet_mass2_chi1_GEN"
    hTitle="M_{jj} vs #chi Response -- GEN jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,chiBins1,True)

    hName="dijet_mass2_chi2_GEN"
    hTitle="M_{jj} vs #chi Response -- GEN jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,chiBins2,True)

    hName="dijet_mass2_chi3_GEN"
    hTitle="M_{jj} vs #chi Response -- GEN jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,chiBins3,True)

    hName="dijet_mass2_chi4_GEN"
    hTitle="M_{jj} vs #chi Response -- GEN jets"
    hists[hName] = Book2DwithVarBins(hName,hTitle,massBins2,chiBins4,True)
    
    hName="hdummy_chi"
    hTitle="dummy vs chi"
    hists[hName] = Book1DwithVarBins(hName,hTitle,chiBins1,True)

    hName="hdummy_mass1"
    hTitle="dummy vs mass1"
    hists[hName] = Book1DwithVarBins(hName,hTitle,massBins1,True)

    hName="hdummy_mass2"
    hTitle="dummy vs mass2"
    hists[hName] = Book1DwithVarBins(hName,hTitle,massBins2,True)

    nPt=50
    minPt=0.
    maxPt=5000.

    nY=30
    minY=-3.
    maxY=3.

    nYboost=12
    minYboost=0.
    maxYboost=1.2

    nDeltaPt=50
    minDeltaPt=0.
    maxDeltaPt=1.

    nDeltaPhi=20
    minDeltaPhi=0.
    maxDeltaPhi=3.2

    for i in range(len(massBins1)-1):
        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_chiRECO"
        hists[hName] = Book1D(hName,hName,nChi,minChi,maxChi,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_chiGEN"
        hists[hName] = Book1D(hName,hName,nChi,minChi,maxChi,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_chiSMR"
        hists[hName] = Book1D(hName,hName,nChi,minChi,maxChi,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_pt1RECO"
        hists[hName] = Book1D(hName,hName,nPt,minPt,maxPt,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_pt1GEN"
        hists[hName] = Book1D(hName,hName,nPt,minPt,maxPt,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_pt1SMR"
        hists[hName] = Book1D(hName,hName,nPt,minPt,maxPt,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_pt2RECO"
        hists[hName] = Book1D(hName,hName,nPt,minPt,maxPt,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_pt2GEN"
        hists[hName] = Book1D(hName,hName,nPt,minPt,maxPt,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_pt2SMR"
        hists[hName] = Book1D(hName,hName,nPt,minPt,maxPt,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_y1RECO"
        hists[hName] = Book1D(hName,hName,nY,minY,maxY,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_y1GEN"
        hists[hName] = Book1D(hName,hName,nY,minY,maxY,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_y1SMR"
        hists[hName] = Book1D(hName,hName,nY,minY,maxY,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_y2RECO"
        hists[hName] = Book1D(hName,hName,nY,minY,maxY,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_y2GEN"
        hists[hName] = Book1D(hName,hName,nY,minY,maxY,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_y2SMR"
        hists[hName] = Book1D(hName,hName,nY,minY,maxY,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_yboostRECO"
        hists[hName] = Book1D(hName,hName,nYboost,minYboost,maxYboost,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_yboostGEN"
        hists[hName] = Book1D(hName,hName,nYboost,minYboost,maxYboost,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_yboostSMR"
        hists[hName] = Book1D(hName,hName,nYboost,minYboost,maxYboost,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_deltaPtRECO"
        hists[hName] = Book1D(hName,hName,nDeltaPt,minDeltaPt,maxDeltaPt,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_deltaPtGEN"
        hists[hName] = Book1D(hName,hName,nDeltaPt,minDeltaPt,maxDeltaPt,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_deltaPtSMR"
        hists[hName] = Book1D(hName,hName,nDeltaPt,minDeltaPt,maxDeltaPt,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_deltaPhiRECO"
        hists[hName] = Book1D(hName,hName,nDeltaPhi,minDeltaPhi,maxDeltaPhi,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_deltaPhiGEN"
        hists[hName] = Book1D(hName,hName,nDeltaPhi,minDeltaPhi,maxDeltaPhi,True)

        hName="dijet_M1_" + str(massBins1[i]) + "_" + str(massBins1[i+1]) + "_deltaPhiSMR"
        hists[hName] = Book1D(hName,hName,nDeltaPhi,minDeltaPhi,maxDeltaPhi,True)


    for i in range(len(massBins2)-1):
        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_chiRECO"
        hists[hName] = Book1D(hName,hName,nChi,minChi,maxChi,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_chiGEN"
        hists[hName] = Book1D(hName,hName,nChi,minChi,maxChi,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_chiSMR"
        hists[hName] = Book1D(hName,hName,nChi,minChi,maxChi,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_pt1RECO"
        hists[hName] = Book1D(hName,hName,nPt,minPt,maxPt,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_pt1GEN"
        hists[hName] = Book1D(hName,hName,nPt,minPt,maxPt,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_pt1SMR"
        hists[hName] = Book1D(hName,hName,nPt,minPt,maxPt,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_pt2RECO"
        hists[hName] = Book1D(hName,hName,nPt,minPt,maxPt,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_pt2GEN"
        hists[hName] = Book1D(hName,hName,nPt,minPt,maxPt,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_pt2SMR"
        hists[hName] = Book1D(hName,hName,nPt,minPt,maxPt,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_y1RECO"
        hists[hName] = Book1D(hName,hName,nY,minY,maxY,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_y1GEN"
        hists[hName] = Book1D(hName,hName,nY,minY,maxY,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_y1SMR"
        hists[hName] = Book1D(hName,hName,nY,minY,maxY,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_y2RECO"
        hists[hName] = Book1D(hName,hName,nY,minY,maxY,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_y2GEN"
        hists[hName] = Book1D(hName,hName,nY,minY,maxY,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_y2SMR"
        hists[hName] = Book1D(hName,hName,nY,minY,maxY,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_yboostRECO"
        hists[hName] = Book1D(hName,hName,nYboost,minYboost,maxYboost,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_yboostGEN"
        hists[hName] = Book1D(hName,hName,nYboost,minYboost,maxYboost,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_yboostSMR"
        hists[hName] = Book1D(hName,hName,nYboost,minYboost,maxYboost,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_deltaPtRECO"
        hists[hName] = Book1D(hName,hName,nDeltaPt,minDeltaPt,maxDeltaPt,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_deltaPtGEN"
        hists[hName] = Book1D(hName,hName,nDeltaPt,minDeltaPt,maxDeltaPt,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_deltaPtSMR"
        hists[hName] = Book1D(hName,hName,nDeltaPt,minDeltaPt,maxDeltaPt,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_deltaPhiRECO"
        hists[hName] = Book1D(hName,hName,nDeltaPhi,minDeltaPhi,maxDeltaPhi,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_deltaPhiGEN"
        hists[hName] = Book1D(hName,hName,nDeltaPhi,minDeltaPhi,maxDeltaPhi,True)

        hName="dijet_M2_" + str(massBins2[i]) + "_" + str(massBins2[i+1]) + "_deltaPhiSMR"
        hists[hName] = Book1D(hName,hName,nDeltaPhi,minDeltaPhi,maxDeltaPhi,True)


    outf.cd()
    return hists


def BookRooUnfoldMatrices():

    resp={}

    hname="response2dRECO"
    resp[hname] = ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from RECO jets");
    resp[hname].Setup(h["dijet_mass_chi_RECO"],h["dijet_mass_chi_GEN"]);

    hname="response2dRECO_m1c1"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from RECO jets");
    resp[hname].Setup(h["dijet_mass1_chi1_RECO"],h["dijet_mass1_chi1_GEN"]);

    hname="response2dRECO_m1c2"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from RECO jets");
    resp[hname].Setup(h["dijet_mass1_chi2_RECO"],h["dijet_mass1_chi2_GEN"]);

    hname="response2dRECO_m1c3"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from RECO jets");
    resp[hname].Setup(h["dijet_mass1_chi3_RECO"],h["dijet_mass1_chi3_GEN"]);

    hname="response2dRECO_m1c4"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from RECO jets");
    resp[hname].Setup(h["dijet_mass1_chi4_RECO"],h["dijet_mass1_chi4_GEN"]);

    hname="response2dRECO_m2c1"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from RECO jets");
    resp[hname].Setup(h["dijet_mass2_chi1_RECO"],h["dijet_mass2_chi1_GEN"]);

    hname="response2dRECO_m2c2"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from RECO jets");
    resp[hname].Setup(h["dijet_mass2_chi2_RECO"],h["dijet_mass2_chi2_GEN"]);

    hname="response2dRECO_m2c3"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from RECO jets");
    resp[hname].Setup(h["dijet_mass2_chi3_RECO"],h["dijet_mass2_chi3_GEN"]);

    hname="response2dRECO_m2c4"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from RECO jets");
    resp[hname].Setup(h["dijet_mass2_chi4_RECO"],h["dijet_mass2_chi4_GEN"]);


    hname="response2dSMR"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from SMEARED jets");
    resp[hname].Setup(h["dijet_mass_chi_SMR"],h["dijet_mass_chi_GEN"]);

    hname="response2dSMR_m1c1"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from SMEARED jets");
    resp[hname].Setup(h["dijet_mass1_chi1_SMR"],h["dijet_mass1_chi1_GEN"]);

    hname="response2dSMR_m1c2"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from SMEARED jets");
    resp[hname].Setup(h["dijet_mass1_chi2_SMR"],h["dijet_mass1_chi2_GEN"]);

    hname="response2dSMR_m1c3"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from SMEARED jets");
    resp[hname].Setup(h["dijet_mass1_chi3_SMR"],h["dijet_mass1_chi3_GEN"]);

    hname="response2dSMR_m1c4"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from SMEARED jets");
    resp[hname].Setup(h["dijet_mass1_chi4_SMR"],h["dijet_mass1_chi4_GEN"]);

    hname="response2dSMR_m2c1"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from SMEARED jets");
    resp[hname].Setup(h["dijet_mass2_chi1_SMR"],h["dijet_mass2_chi1_GEN"]);

    hname="response2dSMR_m2c2"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from SMEARED jets");
    resp[hname].Setup(h["dijet_mass2_chi2_SMR"],h["dijet_mass2_chi2_GEN"]);

    hname="response2dSMR_m2c3"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from SMEARED jets");
    resp[hname].Setup(h["dijet_mass2_chi3_SMR"],h["dijet_mass2_chi3_GEN"]);

    hname="response2dSMR_m2c4"
    resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass/Chi Response -- from SMEARED jets");
    resp[hname].Setup(h["dijet_mass2_chi4_SMR"],h["dijet_mass2_chi4_GEN"]);

    ## now 1d Response matrices in Chi Bins

    for i in range(len(chiBins1)-1):
        hname="responseRECO_" + str(chiBins1[i]) + "_chi1_" +  str(chiBins1[i+1])
        resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass Response -- RECO jets-- " + str(chiBins1[i]) + "_chi1_" +  str(chiBins1[i+1]))
        resp[hname].Setup(h["hdummy_mass2"],h["hdummy_mass2"])

        hname="responseSMR_" + str(chiBins1[i]) + "_chi1_" +  str(chiBins1[i+1])
        resp[hname] = ROOT.RooUnfoldResponse (hname,"Mass Response -- SMEARED jets-- " + str(chiBins1[i]) + "_chi1_" +  str(chiBins1[i+1]))
        resp[hname].Setup(h["hdummy_mass2"],h["hdummy_mass2"])

    for i in range(len(chiBins2)-1):
        hname="responseRECO_" + str(chiBins2[i]) + "_chi2_" +  str(chiBins2[i+1])
        resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass Response -- RECO jets-- " + str(chiBins2[i]) + "_chi2_" +  str(chiBins2[i+1]))
        resp[hname].Setup(h["hdummy_mass2"],h["hdummy_mass2"])

        hname="responseSMR_" + str(chiBins2[i]) + "_chi2_" +  str(chiBins2[i+1])
        resp[hname] = ROOT.RooUnfoldResponse (hname,"Mass Response -- SMEARED jets-- " + str(chiBins2[i]) + "_chi2_" +  str(chiBins2[i+1]))
        resp[hname].Setup(h["hdummy_mass2"],h["hdummy_mass2"])

    for i in range(len(chiBins3)-1):
        hname="responseRECO_" + str(chiBins3[i]) + "_chi3_" +  str(chiBins3[i+1])
        resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass Response -- RECO jets-- " + str(chiBins3[i]) + "_chi3_" +  str(chiBins3[i+1]))
        resp[hname].Setup(h["hdummy_mass2"],h["hdummy_mass2"])

        hname="responseSMR_" + str(chiBins3[i]) + "_chi3_" +  str(chiBins3[i+1])
        resp[hname] = ROOT.RooUnfoldResponse (hname,"Mass Response -- SMEARED jets-- " + str(chiBins3[i]) + "_chi3_" +  str(chiBins3[i+1]))
        resp[hname].Setup(h["hdummy_mass2"],h["hdummy_mass2"])

    for i in range(len(chiBins4)-1):
        hname="responseRECO_" + str(chiBins4[i]) + "_chi4_" +  str(chiBins4[i+1])
        resp[hname]= ROOT.RooUnfoldResponse (hname,"Mass Response -- RECO jets-- " + str(chiBins4[i]) + "_chi4_" +  str(chiBins4[i+1]))
        resp[hname].Setup(h["hdummy_mass2"],h["hdummy_mass2"])

        hname="responseSMR_" + str(chiBins4[i]) + "_chi4_" +  str(chiBins4[i+1])
        resp[hname] = ROOT.RooUnfoldResponse (hname,"Mass Response -- SMEARED jets-- " + str(chiBins4[i]) + "_chi4_" +  str(chiBins4[i+1]))
        resp[hname].Setup(h["hdummy_mass2"],h["hdummy_mass2"])


    return resp


def whichMassBin1(mass):

    for i in range(len(massBins1)-1):
        if mass>= massBins1[i] and mass <= massBins1[i+1]:
            return i
    return -1

def whichChi1Bin(chi):

    for i in range(len(chiBins1)-1):
        if chi>= chiBins1[i] and chi <= chiBins1[i+1]:
            return i
    return -1

def whichChi2Bin(chi):

    for i in range(len(chiBins2)-1):
        if chi>= chiBins2[i] and chi <= chiBins2[i+1]:
            return i
    return -1

def whichChi3Bin(chi):

    for i in range(len(chiBins3)-1):
        if chi>= chiBins3[i] and chi <= chiBins3[i+1]:
            return i
    return -1

def whichChi4Bin(chi):

    for i in range(len(chiBins4)-1):
        if chi>= chiBins4[i] and chi <= chiBins4[i+1]:
            return i
    return -1

def whichMassBin2(mass):

    for i in range(len(massBins2)-1):
        if mass>= massBins2[i] and mass <= massBins2[i+1]:
            return i
    return -1

def GetEOSFileList(searchstring):
    import subprocess
    Debug=False

    print searchstring
    fileList=[]
    eosCommand="/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select"
    # print eosCommand

    filePrefix=searchstring[:searchstring.rfind("/")]
    sString=searchstring[searchstring.rfind("/")+1:]
    sString1=sString[:sString.find("*")]
    sString2=sString[len(sString1)+1:sString.rfind("*")]
    sString2="_0.root"
    EOSDIR=filePrefix[filePrefix.find("root://eoscms/")+len("root://eoscms/"):]
    # print EOSDIR
    print "\nParsing EOS for files with string: ",sString
    print "String1: ",sString1
    print "String2: ",sString2,"\n"

    # os.system(eosCommand)
    p1 = subprocess.Popen([eosCommand, "ls", EOSDIR], shell=False, stdout=subprocess.PIPE)
    (stdout, stderr)=p1.communicate()
    if stderr is not None:
        print "Trouble executing the srmls command"
        sys.exit(1)

    if Debug:
        print "Raw output"
        print stdout
        print "Done\n"

    files=stdout.split('\n')
    # print "\n Number of files in directory: ",len(files),"\n"
    # print "\n"

    i=0
    for infile in files:
        ## if infile.find(".root")>-1:
        if infile.find(sString1)>-1:
            if infile.find(sString2)>-1:
                i=i+1
                # print i,infile
                filename=os.path.join(filePrefix,infile)
                fileList.append(filename)
                # filename=os.path.join(remoteDir,infile)


    ## fileList.append("root://eoscms//eos/cms/store/caf/user/apana/Chi_13TeV/GenOutput/pythia8_ci_CrystalBall_Trunc2.5/chiSmearing_8TeV_m1000_1500_1.root")
    return fileList

def getRootFiles(InputRootFiles,treeName):

    # import glob
    # print infiles
    # InputRootFiles = glob.glob (jobpar.inputFiles)

    nStep1=0
    nStep1WithPU=0
    tr = TChain(treeName)
    trFR = TChain("treeFriend")
    for rootfile in InputRootFiles:

        if isEOS(rootfile):
            rootfile=rootfile.replace('/eos/cms', 'root://eoscms//eos/cms')

        print "Adding to chain: ",rootfile
        if rootfile.find("pnfs")>-1:
            rootfile="dcache:" + rootfile

        ## print "XXX: ", rootfile

        f=TFile.Open(rootfile)
        h1=f.Get('nevts')  # get histogram with Step 1 event count
        #print h1.GetEntries()
        nStep1 = nStep1 + h1.GetBinContent(1)

        h2=f.Get('evtsHT')  # get histogram with number of events per HT bin
        nb=h2.GetNbinsX()
        # print "Number of bins in evtsHT histo: ",nb
        for i in range(nb):
            nnew=h2.GetBinContent(i+1)
            nold=h["EvtsHT"].GetBinContent(i+1)

            h["EvtsHT"].SetBinContent(i+1,nold+nnew)


        h3=f.Get('evtsPT')  # get histogram with number of events per PT bin
        # print nb, h3
        if h3==None:
            print "evtsPT histogram is not on file"
            nb=0
        else:
            nb=h3.GetNbinsX()

        # print "Number of bins in evtsPT histo: ",nb
        for i in range(nb):
            nnew=h3.GetBinContent(i+1)
            nold=h["EvtsPT"].GetBinContent(i+1)

            h["EvtsPT"].SetBinContent(i+1,nold+nnew)

        h4=f.Get('evtsM')  # get histogram with number of events per PT bin
        # print nb, h4
        if h4==None:
            print "evtsM histogram is not on file"
            nb=0
        else:
            nb=h4.GetNbinsX()

        # print "Number of bins in evtsM histo: ",nb
        for i in range(nb):
            nnew=h4.GetBinContent(i+1)
            nold=h["EvtsM"].GetBinContent(i+1)

            h["EvtsM"].SetBinContent(i+1,nold+nnew)

        h5=f.Get('evtsFLAT')  # get histogram with number of events per PT bin
        # print nb, h5
        if h5==None:
            print "evtsFLAT histogram is not on file"
            nb=0
        else:
            nb=h5.GetNbinsX()

        # print "Number of bins in evtsFLAT histo: ",nb
        for i in range(nb):
            nnew=h5.GetBinContent(i+1)
            nold=h["EvtsFLAT"].GetBinContent(i+1)

            h["EvtsFLAT"].SetBinContent(i+1,nold+nnew)

        f.Close()

        tr.AddFile(rootfile)

        ## ## now get friends
        ## ## FriendDir=os.path.join(os.path.dirname(rootfile),"Friends")
        ## FriendDir=os.path.join(os.path.dirname(rootfile),"NewFriends")
        ## ## FriendDir=os.path.join("/uscmst1b_scratch/lpc1/lpctrig/apana/Higgs/dev/CMSSW_6_0_0/src/Regression")
        ## ## if jobpar.ApplyBJetRegressionSubjets:
        ## AddFriends=True
        ## if AddFriends:
        ##     friendName=basename[:basename.find(".root")] + "_Friend.root"
        ##     rootFriend=os.path.join(FriendDir,friendName)
        ##     #if not os.path.isfile(rootFriend):
        ##     #    print "Could not find Friend " + rootFriend+ " -- Exiting"
        ##     #    sys.exit(1)
        ##
        ##     print "Adding friend ",rootFriend
        ##     trFR.AddFile(rootFriend)


    ## if (AddFriends and (tr.GetEntries() != trFR.GetEntries())):
    ##     print "Number of entries on Main and Friend chains differ -- exiting program"
    ##     sys.exit(1)
    ##
    ## tr.AddFriend(trFR)
    SetOwnership( tr, False )

    print "Number of Step1 events: ", nStep1

    return tr, nStep1


if __name__ == "__main__":

    ## AutoLibraryLoader.enable()
    ## narg=len(sys.argv)
    ## print narg
    ## if narg < 3:
    ##     print "Please supply gen mass threshold and WhichSmearing command line arguments"
    ##     sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--nevts", help="number of events to process",type=int,default=0)
    parser.add_argument("-v","--verbosity", help="increase output verbosity", action="store_true")
    parser.add_argument("--test", help="split sample in testing sample", action="store_true")
    parser.add_argument("--train", help="split sample in training sample", action="store_true")
    parser.add_argument("outfile", help="name of outfile file")
    parser.add_argument("infiles", help="name of input files")
    args = parser.parse_args()
    if args.verbosity:
        print "verbosity turned on"
    else:
        print "verbosity turned off"

    SplitSamples=False
    Split="xxx"
    if args.test or args.train:
        SplitSamples=True
        if args.test and args.train:
            print "Can only specify test or train, not both"
            sys.exit(1)
        if args.test: Split="Test"
        if args.train: Split="Train"

    outfile=args.outfile

    print "Reading input from: ",args.infiles
    InputRootFiles=[]
    if args.infiles.find(".root")>-1:
        InputRootFiles.append(args.infiles)
    else:
        ## read from list
        InputRootFiles=ReadFilesFromList(args.infiles)

    if SplitSamples:
        outfile=outfile[:outfile.find(".root")] + "_" + Split+".root"

    print "Output written to: ",outfile

    ## sys.exit(1)

    print InputRootFiles



    outf = TFile(outfile,"RECREATE");
    SetOwnership( outf, False )   # tell python not to take ownership
    print "Output written to: ", outfile

    h=BookHistograms()  # ## book histograms
    # print "CCLA:",h

    # infile="newdata/DiJetPt_ZH_ZToLL_HToBB_M-125_8TeV-powheg-herwigpp.root"
    # f=TFile.Open(infile)
    # tree = f.Get("tree");

    ## responseRECO= RooUnfoldResponse ("responseRECO","Mass Response -- from RECO jets");
    ## responseRECO.Setup(h["dijet_mass_reco"],h["dijet_mass_gen"]);
    ##
    ## responseSMR= RooUnfoldResponse ("responseSMR","Mass Response -- from SMEARED jets");
    ## responseSMR.Setup(h["dijet_mass_smr"],h["dijet_mass_gen"]);

    hRooUnf=BookRooUnfoldMatrices()


    ## response.Setup(nmass, mmin, mmax,nmass, mmin, mmax);
    ## response= RooUnfoldResponse (nmass, mmin, mmax);

    # print infiles

    #print h

    tree, nStep1 =getRootFiles(InputRootFiles,"DijetTree")

    NEntries = tree.GetEntries()
    
    recoDijets  = ROOT.DijetInfo()
    genDijets   = ROOT.DijetInfo()
    smrDijets   = ROOT.DijetInfo()

    tree.SetBranchAddress("recoDijets", ROOT.AddressOf(recoDijets, "dijetFlag") );
    tree.SetBranchAddress("genDijets",  ROOT.AddressOf(genDijets,  "dijetFlag") );
    tree.SetBranchAddress("smrDijets",  ROOT.AddressOf(smrDijets,  "dijetFlag") );

    #print genDijets

    h["NStep1"].Fill(0,nStep1)


    nHT=0
    nb=h["EvtsHT"].GetNbinsX()
    print "Number of bins in evtsHT histo: ",nb
    for i in range(1,nb):
        nHT= nHT+ h["EvtsHT"].GetBinContent(i+1)
    print "Number of binned HT events: ",nHT

    nPT=0
    nb=h["EvtsPT"].GetNbinsX()
    for i in range(1,nb):
        nPT= nPT+ h["EvtsPT"].GetBinContent(i+1)
    print "Number of binned PT events: ",nPT

    nM=0
    nb=h["EvtsM"].GetNbinsX()
    for i in range(1,nb):
        nM= nM+ h["EvtsM"].GetBinContent(i+1)
    print "Number of binned Mass events: ",nM

    nFLAT=0
    nb=h["EvtsFLAT"].GetNbinsX()
    for i in range(1,nb):
        nFLAT= nFLAT+ h["EvtsFLAT"].GetBinContent(i+1)
    print "Number of Flat QCD events: ",nFLAT

    
    print "Number of entries on Tree:",NEntries
    nevt=NEntries
    if args.nevts>0:
        nevt=args.nevts
    print "Number of events to process: ",nevt

    decade=100

    oMBin =-100
    oHTBin=-100
    oPTBin=-100
    oFlatBin=-100

    oweight=-1.
    nmess_1=0
    nmess_max=100
    
    nevtM=0
    nevtHT=0
    nevtPT=0
    nevtFLAT=0

    for jentry in xrange( nevt ):

        if SplitSamples:
            if args.train==1:
                if jentry % 2 == 0:
                    continue
            else:
                if jentry % 2 != 0:
                    continue
                
        tree.GetEntry(jentry)

        progress = 10.0*jentry/(1.0*nevt);
        k = math.floor(progress);
        if (k > decade):
            print 10*k," %",jentry, "\trecoDijets.dijetFlag:XSweight:HTBin:PTBin: ",recoDijets.dijetFlag, tree.XSweight, tree.HTBin, tree.PTBin
            # print 10*k," %",jentry, "\tRun:Event:lumi:json: ", tree.XSweight
        decade = k

        if args.nevts<=0:
            ## using all events from file, so use nevts from EvtHB ntuple to get proper number of events per HT bin
            ## check if this is a binned HT or binned PT file
            if nHT > 0:
                if tree.HTBin != oHTBin:
                    oHTBin=tree.HTBin
                    nevtHT=h["EvtsHT"].GetBinContent(oHTBin+2)
                    print "%%%Number of Events in HTbin: ", oHTBin," ",nevtHT
            elif nPT > 0:
                if tree.PTBin != oPTBin:
                    oPTBin=tree.PTBin
                    nevtPT=h["EvtsPT"].GetBinContent(oPTBin+2)
                    print "%%%Number of Events in PTbin: ", oPTBin," ",nevtPT
            elif nM > 0:
                if tree.MBin != oMBin:
                    oMBin=tree.MBin
                    nevtM=h["EvtsM"].GetBinContent(oMBin+2)
                    print "%%%Number of Events in Mbin: ", oMBin," ",nevtM
            elif nFLAT > 0:
                if tree.FlatBin != oFlatBin:
                    oFlatBin=tree.FlatBin
                    nevtFLAT=h["EvtsFLAT"].GetBinContent(oFlatBin+2)
                    print "%%%Number of Events in Flat QCD: ", oFlatBin," ",nevtFLAT
        else:
            nevtHT=evt
            nevtPT=evt
            nevtM =evt
            nevtFLAT=evt

        isFlatQCD=False
        if abs(tree.XSweight-1.)>0.0001:
            if nHT>0:
                weight=tree.XSweight/nevtHT
            elif nM>0:
                weight=tree.XSweight/nevtM
            elif nFLAT>0:
                weight=tree.XSweight/nevtFLAT
                isFlatQCD=True
            elif nPT>0:
                weight=tree.XSweight/nevtPT
                # if abs(tree.XSweight-3.086e02)<0.1: ## fix wrong xs weight for pythia8 1.4-2.5TeV mass bin
                #     weight=(tree.XSweight*10.)/nevtPT
        else:
            weight=1.


        if (oweight != weight):
            oweight=weight
            nmess_1=nmess_1+1
            #if nmess_1<nmess_max:
            #    print "XS weight updated. New value: ",jentry,oweight,weight,tree.XSweight,nevtPT,nevtM,nevtHT,nevtFLAT
            #elif nmess_1==nmess_max:
            #    print "\tReached XS weight update printout maximum. No more messages of this type will be printed\n"

        if abs(tree.EVTweight-1.)>0.0001:
            weight=weight*tree.EVTweight

        ## weight=1.
        h["Counter"].Fill(0.)
        h["Counter"].Fill(1.,weight)

        Jet1R=ROOT.TLorentzVector()
        Jet2R=ROOT.TLorentzVector()
        Jet1R.SetPtEtaPhiE(recoDijets.pt1,recoDijets.eta1,recoDijets.phi1,recoDijets.e1)
        Jet2R.SetPtEtaPhiE(recoDijets.pt2,recoDijets.eta2,recoDijets.phi2,recoDijets.e2)

        Jet1G=ROOT.TLorentzVector()
        Jet2G=ROOT.TLorentzVector()
        Jet1G.SetPtEtaPhiE(genDijets.pt1,genDijets.eta1,genDijets.phi1,genDijets.e1)
        Jet2G.SetPtEtaPhiE(genDijets.pt2,genDijets.eta2,genDijets.phi2,genDijets.e2)

        Jet1S=ROOT.TLorentzVector()
        Jet2S=ROOT.TLorentzVector()
        Jet1S.SetPtEtaPhiE(smrDijets.pt1,smrDijets.eta1,smrDijets.phi1,smrDijets.e1)
        Jet2S.SetPtEtaPhiE(smrDijets.pt2,smrDijets.eta2,smrDijets.phi2,smrDijets.e2)

        if recoDijets.dijetFlag:
            h["dijet_mass_reco1"].Fill(recoDijets.mass,weight)
            h["dijet_mass_reco2"].Fill(recoDijets.mass,weight)
            h["dijet_mass_reco3"].Fill(recoDijets.mass,weight)
            h["dijet_mass_chi_RECO"].Fill(recoDijets.mass,recoDijets.chi,weight)
            h["dijet_mass1_chi1_RECO"].Fill(recoDijets.mass,recoDijets.chi,weight)
            h["dijet_mass1_chi2_RECO"].Fill(recoDijets.mass,recoDijets.chi,weight)
            h["dijet_mass1_chi3_RECO"].Fill(recoDijets.mass,recoDijets.chi,weight)
            h["dijet_mass1_chi4_RECO"].Fill(recoDijets.mass,recoDijets.chi,weight)
            h["dijet_mass2_chi1_RECO"].Fill(recoDijets.mass,recoDijets.chi,weight)
            h["dijet_mass2_chi2_RECO"].Fill(recoDijets.mass,recoDijets.chi,weight)
            h["dijet_mass2_chi3_RECO"].Fill(recoDijets.mass,recoDijets.chi,weight)
            h["dijet_mass2_chi4_RECO"].Fill(recoDijets.mass,recoDijets.chi,weight)

            deltaPt=abs(recoDijets.pt1-recoDijets.pt2)/(recoDijets.pt1+recoDijets.pt2)
            deltaPhi=abs(recoDijets.phi1-recoDijets.phi2)

            iBin=whichMassBin1(recoDijets.mass)
            if iBin>-1:
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_chiRECO"
                h[hName].Fill(recoDijets.chi,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_pt1RECO"
                h[hName].Fill(recoDijets.pt1,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_pt2RECO"
                h[hName].Fill(recoDijets.pt2,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_y1RECO"
                h[hName].Fill(Jet1R.Rapidity(),weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_y2RECO"
                h[hName].Fill(Jet2R.Rapidity(),weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_yboostRECO"
                h[hName].Fill(recoDijets.yboost,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_deltaPtRECO"
                h[hName].Fill(deltaPt,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_deltaPhiRECO"
                h[hName].Fill(deltaPhi,weight)

            iBin=whichMassBin2(recoDijets.mass)
            if iBin>-1:
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_chiRECO"
                h[hName].Fill(recoDijets.chi,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_pt1RECO"
                h[hName].Fill(recoDijets.pt1,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_pt2RECO"
                h[hName].Fill(recoDijets.pt2,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_y1RECO"
                h[hName].Fill(Jet1R.Rapidity(),weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_y2RECO"
                h[hName].Fill(Jet2R.Rapidity(),weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_yboostRECO"
                h[hName].Fill(recoDijets.yboost,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_deltaPtRECO"
                h[hName].Fill(deltaPt,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_deltaPhiRECO"
                h[hName].Fill(deltaPhi,weight)


        if genDijets.dijetFlag:
            h["dijet_mass_gen1"].Fill(genDijets.mass,weight)
            h["dijet_mass_gen2"].Fill(genDijets.mass,weight)
            h["dijet_mass_gen3"].Fill(genDijets.mass,weight)
            h["dijet_mass_chi_GEN"].Fill(genDijets.mass,genDijets.chi,weight)
            h["dijet_mass1_chi1_GEN"].Fill(genDijets.mass,genDijets.chi,weight)
            h["dijet_mass1_chi2_GEN"].Fill(genDijets.mass,genDijets.chi,weight)
            h["dijet_mass1_chi3_GEN"].Fill(genDijets.mass,genDijets.chi,weight)
            h["dijet_mass1_chi4_GEN"].Fill(genDijets.mass,genDijets.chi,weight)
            h["dijet_mass2_chi1_GEN"].Fill(genDijets.mass,genDijets.chi,weight)
            h["dijet_mass2_chi2_GEN"].Fill(genDijets.mass,genDijets.chi,weight)
            h["dijet_mass2_chi3_GEN"].Fill(genDijets.mass,genDijets.chi,weight)
            h["dijet_mass2_chi4_GEN"].Fill(genDijets.mass,genDijets.chi,weight)

            deltaPt=abs(genDijets.pt1-genDijets.pt2)/(genDijets.pt1+genDijets.pt2)
            deltaPhi=abs(genDijets.phi1-genDijets.phi2)

            iBin=whichMassBin1(genDijets.mass)
            if iBin>-1:
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_chiGEN"
                h[hName].Fill(genDijets.chi,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_pt1GEN"
                h[hName].Fill(genDijets.pt1,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_pt2GEN"
                h[hName].Fill(genDijets.pt2,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_y1GEN"
                h[hName].Fill(Jet1G.Rapidity(),weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_y2GEN"
                h[hName].Fill(Jet2G.Rapidity(),weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_yboostGEN"
                h[hName].Fill(genDijets.yboost,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_deltaPtGEN"
                h[hName].Fill(deltaPt,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_deltaPhiGEN"
                h[hName].Fill(deltaPhi,weight)


            iBin=whichMassBin2(genDijets.mass)
            if iBin>-1:
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_chiGEN"
                h[hName].Fill(genDijets.chi,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_pt1GEN"
                h[hName].Fill(genDijets.pt1,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_pt2GEN"
                h[hName].Fill(genDijets.pt2,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_y1GEN"
                h[hName].Fill(Jet1G.Rapidity(),weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_y2GEN"
                h[hName].Fill(Jet2G.Rapidity(),weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_yboostGEN"
                h[hName].Fill(genDijets.yboost,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_deltaPtGEN"
                h[hName].Fill(deltaPt,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_deltaPhiGEN"
                h[hName].Fill(deltaPhi,weight)

        if smrDijets.dijetFlag:
            h["dijet_mass_smr1"].Fill(smrDijets.mass,weight)
            h["dijet_mass_smr2"].Fill(smrDijets.mass,weight)
            h["dijet_mass_smr3"].Fill(smrDijets.mass,weight)
            h["dijet_mass_chi_SMR"].Fill(smrDijets.mass,smrDijets.chi,weight)
            h["dijet_mass1_chi1_SMR"].Fill(smrDijets.mass,smrDijets.chi,weight)
            h["dijet_mass1_chi2_SMR"].Fill(smrDijets.mass,smrDijets.chi,weight)
            h["dijet_mass1_chi3_SMR"].Fill(smrDijets.mass,smrDijets.chi,weight)
            h["dijet_mass1_chi4_SMR"].Fill(smrDijets.mass,smrDijets.chi,weight)
            h["dijet_mass2_chi1_SMR"].Fill(smrDijets.mass,smrDijets.chi,weight)
            h["dijet_mass2_chi2_SMR"].Fill(smrDijets.mass,smrDijets.chi,weight)
            h["dijet_mass2_chi3_SMR"].Fill(smrDijets.mass,smrDijets.chi,weight)
            h["dijet_mass2_chi4_SMR"].Fill(smrDijets.mass,smrDijets.chi,weight)

            deltaPt=abs(smrDijets.pt1-smrDijets.pt2)/(smrDijets.pt1+smrDijets.pt2)
            deltaPhi=abs(smrDijets.phi1-smrDijets.phi2)

            iBin=whichMassBin1(smrDijets.mass)
            if iBin>-1:
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_chiSMR"
                h[hName].Fill(smrDijets.chi,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_pt1SMR"
                h[hName].Fill(smrDijets.pt1,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_pt2SMR"
                h[hName].Fill(smrDijets.pt2,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_y1SMR"
                h[hName].Fill(Jet1S.Rapidity(),weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_y2SMR"
                h[hName].Fill(Jet2S.Rapidity(),weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_yboostSMR"
                h[hName].Fill(smrDijets.yboost,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_deltaPtSMR"
                h[hName].Fill(deltaPt,weight)
                hName="dijet_M1_" + str(massBins1[iBin]) + "_" + str(massBins1[iBin+1]) + "_deltaPhiSMR"
                h[hName].Fill(deltaPhi,weight)

            iBin=whichMassBin2(smrDijets.mass)
            if iBin>-1:
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_chiSMR"
                h[hName].Fill(smrDijets.chi,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_pt1SMR"
                h[hName].Fill(smrDijets.pt1,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_pt2SMR"
                h[hName].Fill(smrDijets.pt2,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_y1SMR"
                h[hName].Fill(Jet1S.Rapidity(),weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_y2SMR"
                h[hName].Fill(Jet2S.Rapidity(),weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_yboostSMR"
                h[hName].Fill(smrDijets.yboost,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_deltaPtSMR"
                h[hName].Fill(deltaPt,weight)
                hName="dijet_M2_" + str(massBins2[iBin]) + "_" + str(massBins2[iBin+1]) + "_deltaPhiSMR"
                h[hName].Fill(deltaPhi,weight)


        ## Get histogram names for the unfolding as function of mass in chi bins
        iChi1=whichChi1Bin(recoDijets.chi)
        iChi2=whichChi2Bin(recoDijets.chi)
        iChi3=whichChi3Bin(recoDijets.chi)
        iChi4=whichChi4Bin(recoDijets.chi)

        RECO_Unf_Chi1="XXX"
        RECO_Unf_Chi2="XXX"
        RECO_Unf_Chi3="XXX"
        RECO_Unf_Chi4="XXX"

        ## print "XXX: ",iChi1,iChi2,iChi3,iChi4,recoDijets.chi
        if iChi1>-1:
            RECO_Unf_Chi1="responseRECO_" + str(chiBins1[iChi1]) + "_chi1_" +  str(chiBins1[iChi1+1])
        if iChi2>-1:
            RECO_Unf_Chi2="responseRECO_" + str(chiBins2[iChi2]) + "_chi2_" +  str(chiBins2[iChi2+1])
        if iChi3>-1:
            RECO_Unf_Chi3="responseRECO_" + str(chiBins3[iChi3]) + "_chi3_" +  str(chiBins3[iChi3+1])
        if iChi4>-1:
            RECO_Unf_Chi4="responseRECO_" + str(chiBins4[iChi4]) + "_chi4_" +  str(chiBins4[iChi4+1])

        iChi1=whichChi1Bin(smrDijets.chi)
        iChi2=whichChi2Bin(smrDijets.chi)
        iChi3=whichChi3Bin(smrDijets.chi)
        iChi4=whichChi4Bin(smrDijets.chi)

        SMR_Unf_Chi1="XXX"
        SMR_Unf_Chi2="XXX"
        SMR_Unf_Chi3="XXX"
        SMR_Unf_Chi4="XXX"

        if iChi1>-1:
            SMR_Unf_Chi1 ="responseSMR_"  + str(chiBins1[iChi1]) + "_chi1_" +  str(chiBins1[iChi1+1])
        if iChi2>-1:
            SMR_Unf_Chi2 ="responseSMR_"  + str(chiBins2[iChi2]) + "_chi2_" +  str(chiBins2[iChi2+1])
        if iChi3>-1:
            SMR_Unf_Chi3 ="responseSMR_"  + str(chiBins3[iChi3]) + "_chi3_" +  str(chiBins3[iChi3+1])
        if iChi4>-1:
            SMR_Unf_Chi4 ="responseSMR_"  + str(chiBins4[iChi4]) + "_chi4_" +  str(chiBins4[iChi4+1])

        ## names for the Miss() filling
        iChi1=whichChi1Bin(genDijets.chi)
        iChi2=whichChi2Bin(genDijets.chi)
        iChi3=whichChi3Bin(genDijets.chi)
        iChi4=whichChi4Bin(genDijets.chi)

        SMR_Unf_Chi1_GEN="XXX"
        RECO_Unf_Chi1_GEN="XXX"
        SMR_Unf_Chi2_GEN="XXX"
        RECO_Unf_Chi2_GEN="XXX"
        SMR_Unf_Chi3_GEN="XXX"
        RECO_Unf_Chi3_GEN="XXX"
        SMR_Unf_Chi4_GEN="XXX"
        RECO_Unf_Chi4_GEN="XXX"

        if iChi1>-1:
            SMR_Unf_Chi1_GEN  ="responseSMR_"  + str(chiBins1[iChi1]) + "_chi1_" +  str(chiBins1[iChi1+1])
            RECO_Unf_Chi1_GEN ="responseRECO_"  + str(chiBins1[iChi1]) + "_chi1_" +  str(chiBins1[iChi1+1])
        if iChi2>-1:
            SMR_Unf_Chi2_GEN  ="responseSMR_"  + str(chiBins2[iChi2]) + "_chi2_" +  str(chiBins2[iChi2+1])
            RECO_Unf_Chi2_GEN ="responseRECO_"  + str(chiBins2[iChi2]) + "_chi2_" +  str(chiBins2[iChi2+1])
        if iChi3>-1:
            SMR_Unf_Chi3_GEN  ="responseSMR_"  + str(chiBins3[iChi3]) + "_chi3_" +  str(chiBins3[iChi3+1])
            RECO_Unf_Chi3_GEN ="responseRECO_"  + str(chiBins3[iChi3]) + "_chi3_" +  str(chiBins3[iChi3+1])
        if iChi4>-1:
            SMR_Unf_Chi4_GEN  ="responseSMR_"  + str(chiBins4[iChi4]) + "_chi4_" +  str(chiBins4[iChi4+1])
            RECO_Unf_Chi4_GEN ="responseRECO_"  + str(chiBins4[iChi4]) + "_chi4_" +  str(chiBins4[iChi4+1])

        ## CCLA  next up, fill the roounfold 1d response matrices

        ## Fill the RooUnfold matrices using RECO jets
        ## ccla if genDijets.mass < massBins2[0]
        ### print "CCLA: ",recoDijets.dijetFlag
        ## recoDijets.dijetFlag=0
        if recoDijets.dijetFlag and genDijets.dijetFlag:
            hRooUnf["response2dRECO"].Fill(recoDijets.mass,recoDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m1c1"].Fill(recoDijets.mass,recoDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m1c2"].Fill(recoDijets.mass,recoDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m1c3"].Fill(recoDijets.mass,recoDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m1c4"].Fill(recoDijets.mass,recoDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m2c1"].Fill(recoDijets.mass,recoDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m2c2"].Fill(recoDijets.mass,recoDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m2c3"].Fill(recoDijets.mass,recoDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m2c4"].Fill(recoDijets.mass,recoDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf[RECO_Unf_Chi1].Fill(recoDijets.mass,genDijets.mass,weight)
            hRooUnf[RECO_Unf_Chi2].Fill(recoDijets.mass,genDijets.mass,weight)
            hRooUnf[RECO_Unf_Chi3].Fill(recoDijets.mass,genDijets.mass,weight)
            hRooUnf[RECO_Unf_Chi4].Fill(recoDijets.mass,genDijets.mass,weight)

            h["dijet_massgen_massRECO_1"].Fill(genDijets.mass,recoDijets.mass,weight)
            h["dijet_massgen_massRECO_2"].Fill(genDijets.mass,recoDijets.mass,weight)
            h["dijet_massgen_massRECO_1_nowt"].Fill(genDijets.mass,recoDijets.mass,1.)
            h["dijet_massgen_massRECO_2_nowt"].Fill(genDijets.mass,recoDijets.mass,1.)
            h["dijet_chigen_chiRECO"].Fill(genDijets.chi,recoDijets.chi,weight)
            h["dijet_chigen_chiRECO_nowt"].Fill(genDijets.chi,recoDijets.chi,1.)
            h["dijet_yboost_gen"].Fill(genDijets.yboost,weight)
            h["dijet_eta1_gen"].Fill(genDijets.eta1,weight)

        elif genDijets.dijetFlag:
            hRooUnf["response2dRECO"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m1c1"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m1c2"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m1c3"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m1c4"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m2c1"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m2c2"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m2c3"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dRECO_m2c4"].Miss(genDijets.mass,genDijets.chi,weight)
            if iChi1 == -1:
                print "%Troubles1 iChi1,chi,mass: ",iChi1,genDijets.chi,genDijets.mass
            else:
                hRooUnf[RECO_Unf_Chi1_GEN].Miss(genDijets.mass,weight)
            if iChi2 == -1:
                print "%Troubles1 iChi2,chi,mass: ",iChi2,genDijets.chi,genDijets.mass
            else:
                hRooUnf[RECO_Unf_Chi2_GEN].Miss(genDijets.mass,weight)
            if iChi3 == -1:
                print "%Troubles1 iChi3,chi,mass: ",iChi3,genDijets.chi,genDijets.mass
            else:
                hRooUnf[RECO_Unf_Chi3_GEN].Miss(genDijets.mass,weight)
            if iChi4 == -1:
                print "%Troubles1 iChi4,chi,mass: ",iChi4,genDijets.chi,genDijets.mass
            else:
                hRooUnf[RECO_Unf_Chi4_GEN].Miss(genDijets.mass,weight)

        elif recoDijets.dijetFlag:
            hRooUnf["response2dRECO"].Fake(recoDijets.mass,recoDijets.chi,weight)
            hRooUnf["response2dRECO_m1c1"].Fake(recoDijets.mass,recoDijets.chi,weight)
            hRooUnf["response2dRECO_m1c2"].Fake(recoDijets.mass,recoDijets.chi,weight)
            hRooUnf["response2dRECO_m1c3"].Fake(recoDijets.mass,recoDijets.chi,weight)
            hRooUnf["response2dRECO_m1c4"].Fake(recoDijets.mass,recoDijets.chi,weight)
            hRooUnf["response2dRECO_m2c1"].Fake(recoDijets.mass,recoDijets.chi,weight)
            hRooUnf["response2dRECO_m2c2"].Fake(recoDijets.mass,recoDijets.chi,weight)
            hRooUnf["response2dRECO_m2c3"].Fake(recoDijets.mass,recoDijets.chi,weight)
            hRooUnf["response2dRECO_m2c4"].Fake(recoDijets.mass,recoDijets.chi,weight)
            hRooUnf[RECO_Unf_Chi1].Fake(recoDijets.mass,weight)
            hRooUnf[RECO_Unf_Chi2].Fake(recoDijets.mass,weight)
            hRooUnf[RECO_Unf_Chi3].Fake(recoDijets.mass,weight)
            hRooUnf[RECO_Unf_Chi4].Fake(recoDijets.mass,weight)

        ## Unsmearing using SMEARED jets
        if smrDijets.dijetFlag and genDijets.dijetFlag:
            hRooUnf["response2dSMR"].Fill(smrDijets.mass,smrDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m1c1"].Fill(smrDijets.mass,smrDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m1c2"].Fill(smrDijets.mass,smrDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m1c3"].Fill(smrDijets.mass,smrDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m1c4"].Fill(smrDijets.mass,smrDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m2c1"].Fill(smrDijets.mass,smrDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m2c2"].Fill(smrDijets.mass,smrDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m2c3"].Fill(smrDijets.mass,smrDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m2c4"].Fill(smrDijets.mass,smrDijets.chi,genDijets.mass,genDijets.chi,weight)
            hRooUnf[SMR_Unf_Chi1].Fill(smrDijets.mass,genDijets.mass,weight)
            hRooUnf[SMR_Unf_Chi2].Fill(smrDijets.mass,genDijets.mass,weight)
            hRooUnf[SMR_Unf_Chi3].Fill(smrDijets.mass,genDijets.mass,weight)
            hRooUnf[SMR_Unf_Chi4].Fill(smrDijets.mass,genDijets.mass,weight)

            h["dijet_massgen_massSMR_1"].Fill(genDijets.mass,smrDijets.mass,weight)
            h["dijet_massgen_massSMR_2"].Fill(genDijets.mass,smrDijets.mass,weight)
            h["dijet_massgen_massSMR_1_nowt"].Fill(genDijets.mass,smrDijets.mass,1.)
            h["dijet_massgen_massSMR_2_nowt"].Fill(genDijets.mass,smrDijets.mass,1.)
            h["dijet_chigen_chiSMR"].Fill(genDijets.chi,smrDijets.chi,weight)
            h["dijet_chigen_chiSMR_nowt"].Fill(genDijets.chi,smrDijets.chi,1.)

        elif genDijets.dijetFlag:
            hRooUnf["response2dSMR"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m2c1"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m2c2"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m2c3"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m2c4"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m1c1"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m1c2"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m1c3"].Miss(genDijets.mass,genDijets.chi,weight)
            hRooUnf["response2dSMR_m1c4"].Miss(genDijets.mass,genDijets.chi,weight)
            if iChi1 == -1:
                print "%Troubles2 iChi1,chi,mass: ",iChi1,genDijets.chi,genDijets.mass
            else:
                hRooUnf[SMR_Unf_Chi1_GEN].Miss(genDijets.mass,weight)
            if iChi2 == -1:
                print "%Troubles2 iChi2,chi,mass: ",iChi2,genDijets.chi,genDijets.mass
            else:
                hRooUnf[SMR_Unf_Chi2_GEN].Miss(genDijets.mass,weight)
            if iChi3 == -1:
                print "%Troubles2 iChi3,chi,mass: ",iChi3,genDijets.chi,genDijets.mass
            else:
                hRooUnf[SMR_Unf_Chi3_GEN].Miss(genDijets.mass,weight)
            if iChi4 == -1:
                print "%Troubles2 iChi4,chi,mass: ",iChi4,genDijets.chi,genDijets.mass
            else:
                hRooUnf[SMR_Unf_Chi4_GEN].Miss(genDijets.mass,weight)
        elif smrDijets.dijetFlag:
            hRooUnf["response2dSMR"].Fake(smrDijets.mass,smrDijets.chi,weight)
            hRooUnf["response2dSMR_m1c1"].Fake(smrDijets.mass,smrDijets.chi,weight)
            hRooUnf["response2dSMR_m1c2"].Fake(smrDijets.mass,smrDijets.chi,weight)
            hRooUnf["response2dSMR_m1c3"].Fake(smrDijets.mass,smrDijets.chi,weight)
            hRooUnf["response2dSMR_m1c4"].Fake(smrDijets.mass,smrDijets.chi,weight)
            hRooUnf["response2dSMR_m2c1"].Fake(smrDijets.mass,smrDijets.chi,weight)
            hRooUnf["response2dSMR_m2c2"].Fake(smrDijets.mass,smrDijets.chi,weight)
            hRooUnf["response2dSMR_m2c3"].Fake(smrDijets.mass,smrDijets.chi,weight)
            hRooUnf["response2dSMR_m2c4"].Fake(smrDijets.mass,smrDijets.chi,weight)
            hRooUnf[SMR_Unf_Chi1].Fake(smrDijets.mass,weight)
            hRooUnf[SMR_Unf_Chi2].Fake(smrDijets.mass,weight)
            hRooUnf[SMR_Unf_Chi3].Fake(smrDijets.mass,weight)
            hRooUnf[SMR_Unf_Chi4].Fake(smrDijets.mass,weight)

    ###############################################################################################
    ###   done with event loop  ###################################################################
    ###############################################################################################

    outf.cd()

    for hname, h in h.iteritems():
        ## print h, hname
        outf.WriteTObject(h,hname)

    for hname, h in hRooUnf.iteritems():
        ## print h, hname
        outf.WriteTObject(h,hname)

    outf.Write();
    outf.Close();
