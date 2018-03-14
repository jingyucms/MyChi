from ROOT import *

#fil=TFile("Axial_Dijet_LO_Mphi_4000_1_1p0_1p0_Mar515.root")
fil=TFile("Axial_Dijet_LO_Mphi_4000_1_1p0_1p0_Mar515_smr_test.root")

#events=fil.Get("Events")
events=fil.Get("DijetTree")

nevents=0

weightname='gdmv_0_gdma_1p0_gv_0_ga_0p75'

for event in events:
#    xsec=event.LHEEventProduct_externalLHEProducer__GEN.product().originalXWGTUP()*1000. # convert to pb
#    print "xsec:",xsec
    #print event.LHEEventProduct_externalLHEProducer__GEN.product().weights()[0]
#    for w in event.LHEEventProduct_externalLHEProducer__GEN.product().weights():
#        print w.id, w.wgt
        #if weightname==w.id:
        #    print w.wgt
        #    break
    #print event.LHEEventProduct_externalLHEProducer__GEN.product().weights()[0].wgt
    print "xsec:", event.dmXsec
    for w in events.dmWeights:
        print w.first, w.second
    #try:
        #print [w.wgt for w in event.LHEEventProduct_externalLHEProducer__GEN.product().weights() if weightname==w.id][0]
	#weight=[w.wgt for w in event.LHEEventProduct_externalLHEProducer__GEN.product().weights() if weightname==w.id][0]/event.LHEEventProduct_externalLHEProducer__GEN.product().weights()[0].wgt
        #print weight
    #except:
	#print "error reading weight"
	#break
    nevents+=1
    if nevents==3: break

    
