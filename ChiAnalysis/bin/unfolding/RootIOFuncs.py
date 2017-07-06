from ROOT import TF1, TFile, TH1F, TH2F, TH3F, TTree, TChain, SetOwnership
import os.path,sys

def isEOS( path ):
    """Tests whether this path is a CMS EOS (name starts with /eos...)"""
    ## return path.startswith('/eos') or path.startswith('root://eoscms.cern.ch//eos/cms')
    return path.startswith('/eos')

def getRootChain(jobpar,treeName):

    import glob
    # print infiles
    InputRootFiles = glob.glob (jobpar.inputFiles)

    nStep1=0
    nStep1WithPU=0
    tr = TChain(treeName)    
    trFR = TChain("treeFriend")
    for rootfile in InputRootFiles:
        basename=os.path.basename(rootfile)
        print "Adding to chain: ",rootfile,rootfile.find("pnfs")
        if rootfile.find("pnfs")>-1:
            rootfile="dcache:" + rootfile

        ## print "XXX: ", rootfile

        f=TFile.Open(rootfile)
        h1=f.Get('Count')  # get histogram with Step 1 event count
        # print h.GetEntries()
        nStep1 = nStep1 + h1.GetBinContent(1)

        h2=f.Get('CountWithPU')  # get histogram with Step 1 event count
        # print h.GetEntries()
        nStep1WithPU = nStep1WithPU + h2.GetBinContent(1)
        f.Close()

        tr.AddFile(rootfile)

        ## now get friends
        FriendDir=os.path.join(os.path.dirname(rootfile),"NewFriends")
        if jobpar.isData:
            if os.environ.has_key('DATAFRIEND'):
                FriendDir=os.environ['DATAFRIEND']
        else:
            if os.environ.has_key('MCFRIEND'):
                FriendDir=os.environ['MCFRIEND']

        ## if jobpar.ApplyBJetRegressionSubjets:
        friendName=basename[:basename.find(".root")] + "_Friend.root"
        rootFriend=os.path.join(FriendDir,friendName)
            #if not os.path.isfile(rootFriend):
            #    print "Could not find Friend " + rootFriend+ " -- Exiting"
            #    sys.exit(1)

        print "Adding friend ",rootFriend
        trFR.AddFile(rootFriend)


    if (tr.GetEntries() != trFR.GetEntries()):
        print "Number of entries on Main and Friend chains differ -- exiting program"
        sys.exit(1)

    tr.AddFriend(trFR)
    SetOwnership( tr, False )

    print "Number of Step1 events: ", nStep1
    print "Number of Step1 events (pileup weighted): ", nStep1WithPU

    return tr, nStep1, nStep1WithPU

def Book1D(cname,ctitle,nbins,xmin,xmax,doSumw2=True):
    h=TH1F(cname,ctitle,nbins,xmin,xmax)
    if doSumw2: h.Sumw2()
    return h

def Book2D(cname,ctitle,nxbins,xmin,xmax,nybins,ymin,ymax,doSumw2=True):
    h=TH2F(cname,ctitle,nxbins,xmin,xmax,nybins,ymin,ymax)
    if doSumw2: h.Sumw2()
    return h

def Book3D(cname,ctitle,nxbins,xmin,xmax,nybins,ymin,ymax,nzbins,zmin,zmax,doSumw2=True):
    h=TH2F(cname,ctitle,nxbins,xmin,xmax,nybins,ymin,ymax,nzbins,zmin,zmax)
    if doSumw2: h.Sumw2()
    return h

def Book1DwithVarBins(cname,ctitle,xbins,doSumw2=True):
    from array import array

    xb=array('d', xbins)

    nbins=len(xbins)-1
    h=TH1F(cname,ctitle,nbins,xb)
    if doSumw2: h.Sumw2()
    return h

def Book2DwithVarBins(cname,ctitle,xbins,ybins,doSumw2=True):
    from array import array

    xb=array('d', xbins)
    yb=array('d', ybins)

    nxbins=len(xbins)-1
    nybins=len(ybins)-1
    h=TH2F(cname,ctitle,nxbins,xb,nybins,yb)
    if doSumw2: h.Sumw2()
    return h

def OutputRootFile(outfile):

    o = TFile(outfile,"RECREATE");
    print "Output written to: ", outfile
    SetOwnership( o, False )   # tell python not to take ownership

    return o

def printLeaves(leaves):

    leafEnts=leaves.GetSize();
    print "\nNumber of leaves: ", leafEnts
    for i in range(0,leafEnts):
        leafName = leaves[i].GetName();
        print "\t",leafName


def OpenFile(file_in,iodir):
    """  file_in -- Input file name
         iodir   -- 'r' readonly  'r+' read+write """
    try:
        ifile=open(file_in, iodir)
        # print "Opened file: ",file_in," iodir ",iodir
    except:
        print "Could not open file: ",file_in
        sys.exit(1)
    return ifile

def CloseFile(ifile):
    ifile.close()

def ReadFilesFromList(infile):

    ifile=OpenFile(infile,'r')
    iline=0

    x = ifile.readline()

    filelist=[]
    while x != "":
        iline+=1
        filename=x.rstrip()

        if len(filename)>0 and filename[0] != "#":
            # print filename
            filelist.append(filename)

        x = ifile.readline()

    return filelist
