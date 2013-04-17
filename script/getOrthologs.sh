#! /bin/bash
echo "runing getEnsemblOrthologTranscripts.pl"
getEnsemblOrthologTranscripts.pl -g "$1 " -s "$2" -l "$3" -o seqAnnotation.csv;
echo "runing getEnsemblOrthologTranscripts.pl ... done"

