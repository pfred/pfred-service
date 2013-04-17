#!/usr/bin/perl

#created on: July 15, 2010
#created by: Qing Cao
#usage: Take a list of Transcript IDs of any species, Obtain sequences and and transcript structure. The first ID is primaryID to be enumerate.
use strict;
use Bio::EnsEMBL::Registry;
use Bio::EnsEMBL::Variation::DBSQL::DBAdaptor;
use Bio::EnsEMBL::DBSQL::DBAdaptor;
#use BIO::Species;
use Getopt::Long;

use ensembl2;
#use fasta2;

my $usage= "$0 -l [list of EnsemblTranscripts \"ID1,ID2,ID3...\"] -f fasta output file -a sequence annotation.csv -v variationdata.csv\n";
@ARGV>0 || die $usage;

my ($tIDs, $fastaFile,$exonJunctionFile,$variationFile);

GetOptions( "l=s"=>\$tIDs,
	    "f=s"=>\$fastaFile,
	    "a=s"=>\$exonJunctionFile,
	    "v=s"=>\$variationFile
	    ); #= means mandatory, : means optional, s means string, i means int, b means binary

my @transcriptList=split /,|\s+|:/,$tIDs;  #primary ID is the first in the array
$fastaFile="test.fa" if (! defined $fastaFile);
$exonJunctionFile="test.junct" if(!defined $exonJunctionFile);
$variationFile="test.var" if(! defined $variationFile);
print STDERR "transcripts: @transcriptList\n";
foreach my $id (@transcriptList){
    $id=~ /^ENS/ || die "Transcript ID error: Requires Ensembl Transcript IDs as input : $id is not recongnized as ENSEMBL Transcript ID\n";
}
&connect();

my %allSpecies=&getSpeciesSynonyms();
my %taForSpecies;
foreach my $species (keys %allSpecies){
    my $ta=&getTranscriptAdaptorForSpecies($allSpecies{$species});
    print STDERR "TA $ta \n";
    $taForSpecies{${allSpecies{$species}}}=$ta;
}


my @transcripts=();
my @inputSpecies=();
foreach my $id (@transcriptList){
    my $species =& getSpeciesForTranscriptId($id);
    my $transcript= & getTranscriptForStableId($taForSpecies{$species}, $id);
    push @transcripts, $transcript;
    push @inputSpecies, $species;
}   

my @fastaSeqs=&getUtrsPlusSplicedExonsForTranscriptsInFastaFormat(@transcripts);
#push(@fastaSeqs,@fastaSeqsForTrans);
   #get exon boundaries
 my @boundaries=&getBoundariesForUtrsPlusExonsForTranscripts(@transcripts);
   #push (@boundaries,@tmpBoundaries);
   #get variation data for transcript
   #my @tmpVariationDetails=&getVariationDetailsForTranscripts($tmpGeneName,$member_adaptor,@transcripts);
   #my @variationDetails=&getVariationDetailsForTranscripts2(\@inputSpecies,\@transcripts);

#&getSpeciesForTranscript($member_adaptor,@allTranscripts);
my @lengths=&getLengths(@fastaSeqs);
#print STDERR "LEN:$lengths[0]\n";
#&printAnnotation($outfile,\@allTranscriptNames,\@allSpeciesList,\@lengths);
&printFastaSeqs($fastaFile,@fastaSeqs);
&printBoundaries($exonJunctionFile,@boundaries);

my @variationDetails=&getVariationDetailsForTranscripts2(\@inputSpecies,\@transcripts);
&printVariation($variationFile,@variationDetails);
print STDERR "files: $fastaFile, $exonJunctionFile,$variationFile\n";
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
$species{"mouse"}="mus musculus";
$species{"rat"}="rattus norvegicus";
$species{"human"}="homo sapiens";
$species{"dog"}="canis familiaris";
$species{"chimp"}="pan troglodytes";
$species{"macaque"}="macaca mulatta";
return %species;
}

sub getSpeciesForTranscriptId{
    my ($id)=@_;
    my %species= &getSpeciesSynonyms();
    my %transcriptSpecies=("ENSMUST" => "mouse",
			   "ENSMMUT" => "macaque",
			   "ENSCAFT" => "dog",
			   "ENST"=> "human",
			   "ENSPTRT"=> "chimp",
			   "ENSRNOT"=> "rat");
    foreach my $header (keys %transcriptSpecies){
	if($id=~ /$header/){
	    return $species{$transcriptSpecies{$header}}; 
	    print STDERR "species found for transcript $id: $species{$transcriptSpecies{$header}}\n";
	    print STDERR "species found for transcript $id: $species{$transcriptSpecies{$header}}\n";
        }
    }
    return;
}

sub getExonBoundariesForTranscript{
    my @transcripts=@_;
    my @fastaSeqs=();
    
    while(my $tran=shift(@transcripts)){
	my $three="";
	my $five="";
	my $translated="";
	my $three_utr=$tran->three_prime_utr();
	my $five_utr=$tran->five_prime_utr();
	if(defined $three_utr) {
	    $three=$three_utr->seq();
	}
	if (defined $five_utr) {
	    $five=$five_utr->seq();
	}
	if($tran->translateable_seq()){
	    $translated=$tran->translateable_seq();
	    $translated=~tr/[a-z]/[A-Z]/; #to highercase
	    my $seq="\>".$tran->display_id()."\n".
		$five.$translated.$three."\n";
	    push(@fastaSeqs,$seq);
	}
	my $exons=$tran->get_all_Exons;
	foreach my $exon (@$exons){
	    my $supporting_features=$exon->get_all_supporting_features;
	    foreach my $feature (@$supporting_features){
		print "Evidence ". $feature->gffstring ."\n";
	    }
	}
    }
}
