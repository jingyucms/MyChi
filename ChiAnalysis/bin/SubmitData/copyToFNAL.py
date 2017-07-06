import os,subprocess,sys

## if len(sys.argv)>=2:
##     dirNames=[sys.argv[1]]
## else:
##     dirNames=["pythia8_ci_CrystalBall","pythia8_ci_Gaussian"]
## 
## #print len(sys.argv)
## print dirNames
    
baseDir='/afs/cern.ch/work/z/zhangj/private/jetUnfold/data/hstsData_vReReco_v3'

outDir='/eos/uscms/store/user/jingyu/jetUnfold/DataNtuple/2017ReReco'

cmd='ls '+baseDir
#print cmd
ls = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE)

stdouts=[]
while True:
    line = ls.stdout.readline()
    stdouts.append(line)
    if line == '' and ls.poll() != None:
        break

print stdouts
    
files=[]
for stdout in stdouts:
    if "chiNtuple" not in stdout: continue
    file=stdout.replace("\n","")
    files.append(file)
    
print files

for f in files:

    print "Copying",f
    os.system("xrdcp "+baseDir+"/"+f+" root://cmseos.fnal.gov/"+outDir+"/"+f)
