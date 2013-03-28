#! /bin/bash

perl getSeqForTranscriptIds.pl -l "$1" -f ./sequence.fa -a ./exonBoundaries.csv -v ./variationData.csv
perl RnaEnumeration.pl -p "$2" -l "$3" -f ./sequence.fa -o ./oligoOut.csv
perl joinOligoAnnotations.pl -l ./oligoOut.csv -j ./exonBoundaries.csv -v ./variationData.csv -o ./outputSummary_.csv



cat ./outputSummary_.csv | awk -F"," '{print ","$1}' | sed -e 's/name/oligoName/g'> ./name.txt
paste ./outputSummary_.csv ./name.txt > ./outputSummary.csv


#rev ./outputSummary_.csv |cut -f 3-999 -d ','|rev >./outputSummary.csv

#cat ./outputSummary.csv | cut -f 1-13 -d ',' > ./outputSummary.csv
