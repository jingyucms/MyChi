import os,subprocess

EXEC="xrdcp "

inPREFIX="root://eoscms.cern.ch/"
#inPREFIX=""
#inDir="/afs/cern.ch/work/z/zhangj/private/jetUnfold/data/hstsMCmadgraphMLM/"
inDir="/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/Jingyu/samples/DiJet/SMEAR/MCOutput/hstsMCmadgraphMLM_v5/"

## FNAL
outPREFIX="root://cmseos.fnal.gov/"
outDIR="/eos/uscms/store/user/jingyu/jetUnfold/MCNtuple/madgraphMLM_Moriond_v5/"

eosCommand="/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select"

searchString="GS"

def GetFileList(inDir,searchString):

    eosls=subprocess.Popen([eosCommand,"ls",inDir],shell=False,stdout=subprocess.PIPE)

    stdouts=[]
    while True:
        line = eosls.stdout.readline()
        stdouts.append(line)
        if line == '' and eosls.poll() != None:
            break

    files=[]
    for stdout in stdouts:
	if not '.root' in stdout: continue
        if not searchString in stdout: continue
	files.append(stdout.replace('\n',''))

    print files
    return files

if __name__ == '__main__':

    #files=os.listdir(inDir)
    files=GetFileList(inDir,searchString)

    print len(files)
    
    nfiles=0
    for file in files:
	file.replace(".root\n",".root")
	#print file
	nfiles+=1
	if nfiles%10==0: print "Copying...",nfiles,"file"
	#os.system("echo "+inPREFIX+inDir+file+" "+outPREFIX+outDIR+file)
	os.system(EXEC+inPREFIX+inDir+file+" "+outPREFIX+outDIR+file)
	    
