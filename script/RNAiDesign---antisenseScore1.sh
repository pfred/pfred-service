#! /bin/bash
echo "line1"
source env.sh
echo "line2"

###temporary out put files###
tempfile="energy.htm"
tempfile2="tmp.txt"
OFILE="antisensescoreOut.txt";
#parse input if not in correct format#
test=`grep -c ';' target.seq`
echo $test
if [ "$test" -lt 1 ]; then
    echo ";target">$tempfile2
    echo "target">>$tempfile2
    cat  target.seq >> $tempfile2
   cat $tempfile2 > target.seq
    echo " 1" >> target.seq
fi

cat target.seq
echo "Running OLIGO_WALK"

#OligoWalk_exe=${OligoWalk_root}/exe/OligoWalk;
OligoWalk_exe=$OLIGOWALK_ROOT/exe/OligoWalk;
NN_data=$OLIGOWALK_ROOT/NN_data/;
#NN_data=/usr/local/oligowalk_src/NN_data/;
DATAPATH=${NN_data};
export DATAPATH
echo $DATAPATH


$OligoWalk_exe -type  d -seq  target.seq -o nofile -m 3 -st 1 -en 0 -M  1 -N  0 -l  $1 -co  1 -unit  -7 -fi 0 -fold  800 -score > $tempfile

echo "Parse OLIGO_WALK output"
perl asOligoWalk.pl $tempfile 1 1 > $OFILE
echo "Done"
echo $1


mv $OFILE output.txt
cat output.txt|awk '{ if(NR==1) printf("__MOL_ID__\t%s\n",$0); else printf("%s\t%s\n",NR-2,$0);}'>$OFILE
head $OFILE


cp outputSummary.csv outputSummaryBeforeMerge.csv
cat outputSummaryBeforeMerge.csv|tr ',' '\t' |perl mergeEx.pl 2 1 output.txt keepAll 1|tr '\t' ','>outputSummary.csv

 

