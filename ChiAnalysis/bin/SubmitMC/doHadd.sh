#!/bin/sh

EOSDIR=/eos/cms/store/caf/user/apana/Chi_13TeV/ChiNtuples/MC/76x


## SMEARING=CB2_AK4SF_DataToMCSF
SMEARING=GS_AK4SF_DataToMCSF

## SMEARING=CB2_AK4SF
## SMEARING=GS_AK4SF

## SMEARING=CB2
## SMEARING=GS

EOS=/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select

TMPDIR=/tmp/apana

GENERATOR=Madgraph
## GENERATOR=Pythia8

if [[ "$GENERATOR" == "Pythia8" ]]
then
    ptBins="Pt_1000to1400 Pt_1400to1800 Pt_170to300 Pt_1800to2400 Pt_2400to3200 Pt_300to470 Pt_3200 Pt_470to600 Pt_600to800 Pt_800to1000"
    Range=Pt_170toInf
    generator=pythia8
else
    ptBins="HT300to500 HT500to700 HT700to1000 HT1000to1500 HT1500to2000 HT2000toInf"
    Range=Ht_300toInf
    generator=madgraphMLM
fi

filelist=""
nfiles=0
for file in `$EOS ls $EOSDIR/hsts`
do
    if [[ "$file" == chiNtuple_${generator}_*"${SMEARING}_"?".root" ]]; then
    ## if [[ "$file" == chiNtuple_*"${SMEARING}_"?".root" ]]; then
	# echo $file
	for ptBin in `echo $ptBins`
        do
	    # echo -e "\t"$file"\t"${ptBin}
	    if [[ "$file" == *"${ptBin}"* ]]; then
		fullfile="root://eoscms/$EOSDIR/hsts/$file"
		echo $fullfile
	
		$EOS cp $EOSDIR/hsts/$file $TMPDIR/$file
		filelist="$filelist $TMPDIR/$file"
		let "nfiles++"
	    fi
	done
    fi
done

basename="chiNtuple_${GENERATOR}_${Range}_${SMEARING}_noTrees.root"
target="root://eoscms/$EOSDIR/"${basename}
outfile=$TMPDIR/${basename}

echo "Number of files copied: $nfiles"
if [[ ${#filelist} -eq 0 ]]; then
    echo -e "\tNo files copied! -- exiting\n"
    exit 1
fi

echo ""
echo $outfile $filelist
### hadd -T $outfile $filelist  ## -T option does not add Trees, only hsts
echo ""

echo $EOS cp $outfile $target
$EOS cp $outfile $target

echo

