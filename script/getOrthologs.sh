#! /bin/bash
echo "runing getEnsemblOrthologTranscripts.pl"
perl getEnsemblOrthologTranscripts.pl -g "$1 " -s "$2" -o seqAnnotation.csv -l "$3";
echo "runing getEnsemblOrthologTranscripts.pl ... done"

