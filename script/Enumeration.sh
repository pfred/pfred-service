#! /bin/bash

getSeqForTranscriptIds.pl -l "$1" -f sequence.fa -a exonBoundaries.csv -v variationData.csv
RnaEnumeration.pl -p "$2" -l "$3" -f sequence.fa -o oligoOut.csv
joinOligoAnnotations.pl -l oligoOut.csv -j exonBoundaries.csv -v variationData.csv -o outputSummary_.csv



cat outputSummary_.csv | awk -F"," '{print ","$1}' | sed -e 's/name/oligoName/g'> name.txt
paste outputSummary_.csv name.txt > EnumerationResult.csv


