scriptdir=/local/PFRED/OPEN_SOURCE_TEST/SCRIPTS
#rnadir=/local/PFRED/OPEN_SOURCE_TEST/SCRIPTS/rna
rnadir=.
bioperldir=/gridccs/vendor/bioPerl/bioPerl/bioperl-live
ensembldir=/gridccs/vendor/ensemblApi/v52/
OligoWalk_root=/usr/local/oligowalk_src;

echo $rnadir

#PERL5LIB=${PERL5LIB}:$rnadir;
PERL5LIB="$scriptdir:$bioperldir:${ensembldir}/ensembl/modules:${ensembldir}/ensembl-compara/modules:${ensembldir}/ensembl-variation/modules:${rnadir}:."
export rnadir
export bioperldir 
export ensembldir
export PERL5LIB
export OligoWalk_root
export scriptdir
echo $bioperldir $ensembldir $PERL5LIB $OligoWalk_root

#BOWTIE="/gridccs/vendor/rtc/bowtie/bowtie";
#BOWTIE_INDEXES="/gridccs/vendor/rtc/bowtie/indexes";
#BOWTIE_BUILD="/gridccs/vendor/rtc/bowtie/bowtie-build";


#export BOWTIE BOWTIE_INDEXES BOWTIE_BUILD
#echo $BOWTIE $BOWTIE_INDEXES $BOWTIE_BUILD
#alias perl='/usr/bin/perl'
#alias python='/usr/bin/python'


#perl $rnadir/getEnsemblOrthologTranscripts.pl

