#! /bin/bash
#echo "line1"
#source env.sh
#echo "line2"

echo "run input test.txt"

cat EnumerationResult.csv | cut -f 1,5 -d ','>foo.csv
sed '1d' foo.csv |tr ',' '\t'> test.txt

IFILE="test.txt"
cat $IFILE
species="human"
targetGene="ENSG00000113580"
type="sense"
mismatch="1"
OFILE="antisenseOffTarget.out"

asDNA_OffTargetSearch_bowtie.pl -s "$1" -g "$2" -t $type  -v "$3" $IFILE > $OFILE

echo "result:"
#head $OFILE
############## always add this for RNAi design protocols ##########################
#mv $OFILE output.txt
#cat output.txt|awk '{ if(NR==1) printf("__MOL_ID__\t%s\n",$0); else printf("%s\t%s\n",NR-2,$0);}'>$OFILE
head $OFILE


cp EnumerationResult.csv outputSummaryBeforeMerge.csv
cat outputSummaryBeforeMerge.csv|tr ',' '\t' |mergeEx.pl 1 1 antisenseOffTarget.out keepAll 1|tr '\t' ','>ASOOffTargetSearchResult.csv
