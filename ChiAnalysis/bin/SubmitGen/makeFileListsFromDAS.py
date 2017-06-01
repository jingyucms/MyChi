import os, time, math

HTBins=['300to500', '500to700', '700to1000','1000to1500','1500to2000','2000toInf']
#HTBins=['300to500']

for HTBin in HTBins:

    filenames=[]

    for version in ['v6','v6_ext1']:

        cmd='python das_client.py --query="file dataset=/QCD_HT'+HTBin+'_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_'+version+'-v1/MINIAODSIM" >list.txt'

        #print HTBin,version
        
        if HTBin=='500to700' and version=='v6_ext1':
            #print cmd
            #cmd.replace("v6_ext1-v1","v6_ext1-v2")
            cmd='python das_client.py --query="file dataset=/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM" >list.txt'

        print cmd
        
        os.system(cmd)

        with open('list.txt') as f:
            lines = f.readlines()

        for line in lines:
            if "QCD_HT" not in line: continue
            filename=line.replace("\n","")
            filenames.append(filename)

    #print filenames

    #continue

    size=5.
    nouts=math.ceil(len(filenames)/size)

    os.system('mkdir ./filelists/madgraphMLM_2017/ht'+HTBin)
    for nout in range(0,int(nouts)):
        out=open('./filelists/madgraphMLM_2017/ht'+HTBin+'/fileList_'+str(nout)+".txt","w")
        print "Writing:",'./filelists/madgraphMLM_2017/ht'+HTBin+'/fileList_'+str(nout)+".txt"
        for s in range(0,int(size)):
            if (nout*size+s)<len(filenames):
                out.write("root://cmsxrootd.fnal.gov/"+filenames[int(nout*size+s)]+'\n')

    print 'ht'+HTBin, "---done"
    time.sleep(3)
    #os.system("rm -rf list.txt")
    
