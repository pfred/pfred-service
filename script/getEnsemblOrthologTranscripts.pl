#!/usr/bin/perl
#created on: July 15, 2010
#created by: Qing Cao
#usage: Taking an Ensemble Gene or Transcript ID of any species, Obtain transcripts for all othologs
#BEGIN{
#    push @INC,"/gridccs/vendor/rtc/rna/","/usr/local/share/applications/BioPerl/BioPerl-1.6.1","/usr/local/share/applications/ensemblAPI/ensembl/modules","/usr/local/share/applications/ensemblAPI/ensembl-compara/modules","/usr/local/share/applications/ensemblAPI/ensembl-variation/modules";
#    print @INC;
#}

use strict;
use Bio::EnsEMBL::Registry;
use Bio::EnsEMBL::Variation::DBSQL::DBAdaptor;
use Bio::EnsEMBL::DBSQL::DBAdaptor;
#use BIO::Species;
use Getopt::Long;
#use lib '/users/dcaffrey/bin';

use ensembl2;
use fasta2;

my $usage= "$0 -g GeneID -s speciesOfProvidedID -o output.txt -l requestedSpeciesList\n";
unless (@ARGV>0) { 
    &validSpecies(); 
    die $usage;
}

my ($id,$inputSpecies,$outfile,$requestedSpeciesList);
GetOptions( "g=s"=>\$id,
	    "s=s"=>\$inputSpecies,
	    "o=s"=>\$outfile,
	    "l=s"=>\$requestedSpeciesList
	    ); #= means mandatory, : means optional, s means string, i means int, b means binary

print STDERR "running $0 -g $id -s $inputSpecies -o $outfile\n";

my @speciesList=split /,\s*|\s+|;\s*/, $requestedSpeciesList;
my @requestedSpecies=grep {$_  ne "$inputSpecies"} @speciesList;
my ($inputSpecies)=&getFullNames(($inputSpecies));
#my %allSpecies=&getSpeciesSynonyms();

print STDERR "@speciesList : @requestedSpecies \n";

my @requestedSpeciesFullName=&getFullNames(@requestedSpecies);
print STDERR "@requestedSpeciesFullName\n";
&connect();

# my $inputdbA= &getDbAdaptor($inputSpecies,"core");
#print STDERR "inputdbA $inputdbA, $inputSpecies\n";

#my $inputga=$inputdbA->get_GeneAdaptor();
my $inputga =&getGeneAdaptorForSpecies($inputSpecies);
my $inputGene;
if($id=~ /EN.*G\d+/){
    $inputGene=$inputga->fetch_by_stable_id($id);
    print STDERR "input id is $inputSpecies $id; input type GeneID\n";
}elsif ($id=~ /EN.*T\d+/){
    $inputGene=$inputga->fetch_by_transcript_stable_id($id);
    print STDERR "input id is $inputSpecies $id; input type Transcript ID\n";
}else{
    die "input id is not recongnized as an Ensembl gene or transcript id.\n";
}

my $geneName=$inputGene->stable_id;
print STDERR "input Gene is $inputSpecies,$geneName\n";

#my $inputga=getGeneAdaptorForSpecies($inputSpecies);
#my $inputGene=

my $member_adaptor=&getComparaMemberAdaptor();
my $homology_adaptor=&getComparaHomologyAdaptor();
print STDERR "member adaptor: $member_adaptor; homology adaptor: $homology_adaptor\n";

my @orthologousGenes=&getAllOrthologousGenes($inputGene,$member_adaptor,$homology_adaptor,@requestedSpeciesFullName);
my @allTranscripts=();
my @fastaSeqs=();
my @allSpeciesList=();
my @boundaries=();
my @variationDetails=();
my @allTranscriptNames=();
my @speciesForGenes=&getSpeciesForGenes($member_adaptor,@orthologousGenes);
print STDERR "Ortholog Genes: ", scalar @orthologousGenes, "\n";

#iterate over all orthologous genes
for (my $l=0;$l<@orthologousGenes;$l++){
   my $tmpGeneName=$orthologousGenes[$l]->stable_id;
   print STDERR "Ortholog Gene $l: $tmpGeneName\n";
   #get transcripts for current gene
   my @transcripts=&getAllTranscriptsForGene($orthologousGenes[$l]); 
   push(@allTranscripts,@transcripts);
   my @transcriptNames=&getNamesForTranscripts(@transcripts);
   push(@allTranscriptNames,@transcriptNames);
   #make species list for genes and transcripts
   #print STDERR "SP $speciesForGenes[$l]\n";
   my @speciesList=&makeSpeciesList($speciesForGenes[$l],@transcripts);
   push (@allSpeciesList,@speciesList);
   #get utrs and exon
   my @fastaSeqsForTrans=&getUtrsPlusSplicedExonsForTranscriptsInFastaFormat(@transcripts);
   push(@fastaSeqs,@fastaSeqsForTrans);
   #get exon boundaries
   #my @tmpBoundaries=&getBoundariesForUtrsPlusExonsForTranscripts(@transcripts);
   #push (@boundaries,@tmpBoundaries);
   #get variation data for transcript
   #my @tmpVariationDetails=&getVariationDetailsForTranscripts($tmpGeneName,$member_adaptor,@transcripts);
   #push(@variationDetails,@tmpVariationDetails);
 } # next gene ortholog 

#&getSpeciesForTranscript($member_adaptor,@allTranscripts);
my @lengths=&getLengths(@fastaSeqs);
#print STDERR "LEN:$lengths[0]\n";
&printAnnotation($outfile,\@allTranscriptNames,\@allSpeciesList,\@lengths);
#&printFastaSeqs($fastaFile,@fastaSeqs);
#&printBoundaries($exonJunctionFile,@boundaries);
#&printVariation($variationFile,@variationDetails);
exit;

############################################################################################################
############################################################################################################

sub makeSpeciesList{
#my @transcripts=@_;
#my $species="ASS";
my ($species,@transcripts)=@_;
#my (@transcripts,$species)=@_;
my (@list)=();
while (my $tran=shift(@transcripts)){
        my $name=$tran->stable_id;
        my $line=$species;
        push(@list,$line);
    }

return @list;

}


sub printAnnotation{
my ($speciesFile,$names,$speciesDetails,$lengths)=@_;
open (SP,">$speciesFile");
print SP ("name\,species\,length\,source\n");
for (my $i=0;$i<@$speciesDetails;$i++){
   $speciesDetails->[$i]=~s/\s/\_/;
   print SP "$names->[$i]\,$speciesDetails->[$i]\,$lengths->[$i]\,ENSEMBL\n";
   }
close(SP);
}

sub printVariation{
my ($variationFile,@variationDetails)=@_;
open (VAR,">$variationFile");
print VAR ("sequenceName\,columnNumber\,residueNumber\,number\,".
 "RCOL\,GCOL\,BCOL\,SYMBOL\,name\,snpId\,allele\,snpType\n");
for (my $i=0;$i<@variationDetails;$i++){
   print VAR  "$variationDetails[$i]";
   }
close(VAR);
}

sub printFastaSeqs{
my ($fastaFile,@fastaSeqs)=@_;
open (FA,">$fastaFile"); 
for (my $i=0;$i<@fastaSeqs;$i++){
   print FA "$fastaSeqs[$i]";
    }
close(FA);
}

sub printBoundaries{
my ($exonJunctionFile,@boundaries)=@_;
open (BO,">$exonJunctionFile");
print BO ("sequenceName\,columnNumber\,residueNumber\,number\,".
          "RCOL\,GCOL\,BCOL\,SYMBOL\,name\,5utrEnd\,exonEnd\n");
for (my $i=0;$i<@boundaries;$i++){
   print BO  "$boundaries[$i]";
   }
close(BO);
}


sub printHumanTranscripts{
my ($gene)=@_;
my @primaryTranscripts=&getAllTranscriptsForGene($gene);
my @primaryFastaSeqs=&getUtrsPlusSplicedExonsForTranscriptsInFastaFormat(@primaryTranscripts);
for (my $i=0;$i<@primaryFastaSeqs;$i++){
     print FA "$primaryFastaSeqs[$i]";
    }
}


####################################
#converts common names into full names
####################################
sub getFullNames{
my (@requestedSpecies)=@_;
my %fullSpecies=&getSpeciesSynonyms();
my @requestedSpeciesFullName=();
for (my $i=0;$i<@requestedSpecies;$i++){
   if(!$fullSpecies{$requestedSpecies[$i]}){
      print STDERR "$requestedSpecies[$i] is not a valid species name\n";
      &validSpecies();
      exit;


     }
   $requestedSpeciesFullName[$i]=$fullSpecies{$requestedSpecies[$i]};
  }
return @requestedSpeciesFullName;
}


sub validSpecies{
my %speciesSyn=&getSpeciesSynonyms();
print "Valid species are:\n";
  while (my($key,$value)=each %speciesSyn){
     print STDERR "$key\n";
    }
print STDERR "\n\n";
}



sub getSpeciesSynonyms{
my %species=();
$species{"mouse"}="Mus musculus";
$species{"rat"}="rattus norvegicus";
$species{"human"}="Homo sapiens";
$species{"dog"}="canis familiaris";
$species{"chimp"}="pan troglodytes";
$species{"macaque"}="macaca mulatta";
return %species;
}

