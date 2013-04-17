use Bio::EnsEMBL::Registry;
use Bio::EnsEMBL::Transcript;
use Bio::EnsEMBL::DBSQL::TranscriptAdaptor;
use Bio::EnsEMBL::Feature;
use Bio::EnsEMBL::Variation::DBSQL::DBAdaptor;
use Bio::EnsEMBL::DBSQL::DBAdaptor;

use fasta2;
use strict;

my $registry = 'Bio::EnsEMBL::Registry';
#my $host='pandora.pfizer.com'; 
my $host='ensembldb.ensembl.org';
my $port='5306';
sub connect{

$registry->load_registry_from_db(
#-host => 'pandora.pfizer.com',
-host => 'ensembldb.ensembl.org',
-port => '5306',
-user => 'anonymous',
#-verbose => '1'
);

#return $registry;
}

############################################################################
#will return a database adaptor for a specified
#species(latin format, e.g homo_sapiens) and group (e.g core or variation)
#No need to specifiy the database name as that is determined automatically
###########################################################################
sub getDbAdaptor{
my ($species,$group)=@_;
#print STDERR " SPEC: $species $group\n";
my $list=&getDbaseDetailsForSpeciesAndGroup($species,$group);
my $dbA;
if ($list!~/^$/){
my @cols=split(/\t/,$list);
#print STDERR "Getting db adaptor for 0: $cols[0] 1: $cols[1] 2: $cols[2] 3: $cols[3]\n";
$dbA = Bio::EnsEMBL::Variation::DBSQL::DBAdaptor->new(
    -host    => $host,
    -port    => $cols[4],
    -dbname  => $cols[2],
    -species => $species,
    -group   => $group,
    -user    => 'anonymous'
);

}
return $dbA;
}

###########################################
#returns a gene name stable id for
#a specified gene adaptor and transcript ID
#############################################

sub getGeneNameForTranscriptId{
my ($ga,$transcriptId)=@_;
my $gene=$ga->fetch_by_transcript_stable_id($transcriptId);
my $geneName=$gene->stable_id;
return $geneName;
}




########################################
#returns all database details for a 
#specified species and group
#########################################
sub getDbaseDetailsForSpeciesAndGroup{
my ($species,$group)=@_;
my $dbDetails="";
my @list =&listDatabases;
while (my $l=shift(@list)){
my @cols=split(/\t/,$l);
#print STDERR "does $cols[0] match $species \? does  $cols[1] match $group \?\n";
if ($cols[0]=~/$species/ && $cols[1]=~/$group/){
$dbDetails= $l;
}
}
return $dbDetails;
}




sub getHumanCore{
my $value="";
my @list=&listDatabases();
for (my $i=0;$i<@list;$i++){
my @cols=split(/\t/,$list[$i]);
if (($cols[1]=~/core/) && ($cols[0]=~/homo_sapiens/)){
$value=$list[$i];
}
}
return $value;
}

#######################################
#returns the proper species name for
#an alias. e.g. Homo sapiens is returned
#for human
########################################
sub getProperSpeciesName{
my ($alias)=@_;
my $sn=$registry->get_alias($alias);
return $sn;
}


sub getTranscriptVariationAdaptor{
my $tva=$registry->get_adaptor('human','variation');#,'TranscriptVariation');
return $tva;
}

###############################################
#Return Type: Bio::EnsEMBL::DBSQL::GeneAdaptor
###############################################
sub getHumanGeneAdaptor{
#my $reg=@_;
#my $ga = $registry->get_adaptor("human","core","Gene");
my $ga = $registry->get_adaptor("Homo sapiens","core","Gene");
return $ga;
}


sub getGeneAdaptorForSpecies{
my ($species)=@_;
#print "\nSpecies:$species\n";
my $ga = $registry->get_adaptor("$species","core","Gene");
if (!defined $ga){
print STDERR "Gene adaptor not defined for $species!\n";
}
return $ga;
}

sub getTranscriptAdaptorForSpecies{
my ($species)=@_;
#print "\nSpecies:$species\n";
my $ta = $registry->get_adaptor("$species","core","Transcript");
if (!defined $ta){
print STDERR "Not DEFINED!\n";
}
return $ta;
}



sub getVariationFeatureAdaptor{
my $vfa = $registry->get_adaptor('human', 'Variation', 'VariationFeature');
return $vfa;
}




###############################################
#Return Type:Bio::EnsEMBL::DBSQL::SliceAdaptor 
###############################################
sub getHumanSliceAdaptor{
my $sa = $registry->get_adaptor("human","core","slice");
return $sa;
}

sub getComparaDBAdaptor{
my $cdba=$registry->get_DBAdaptor('compara', 'compara');
return $cdba;
}

sub getComparaMemberAdaptor{
my $ma=$registry->get_adaptor('compara', 'compara', 'Member');
return $ma;
}

sub getComparaHomologyAdaptor{
my $ha=$registry->get_adaptor("Compara", "compara", "Homology");
return $ha;
}

sub getComparaProteinTreeAdaptor{
my $ta=$registry->get_adaptor("Compara", "compara", "ProteinTree");
return $ta;
}

sub getComparaMethodLinkSpeciesSetAdaptor{
my $ss=$registry->get_adaptor("Compara", "compara", "MethodLinkSpeciesSet");
return $ss;
}



###############################################
#Return GenomeDB adaptor for multispecies
###############################################
sub getComparaGenomeDBAdaptor{
my $gd=$registry->get_adaptor("Compara", "compara","GenomeDB");
return $gd;
}


##############################################
#Return DnaAlignFeatureAdaptor for multispecies
##############################################


sub getDnaAlignFeatureAdaptor {
my $daf=$registry->get_adaptor('Multi', 'compara', 'DnaDnaAlignFeature');
return $daf;
}


sub getGenomicAlignBlockAdaptor{
my $gaba=$registry->get_adaptor('Multi', 'compara', 'GenomicAlignBlock');
return $gaba;
} 


sub getSliceForChromosome{
my ($chromosome,$sa)=@_;
my $slice = $sa->fetch_by_region( 'chromosome', $chromosome );
return $slice;
}

#####################################################
#Return type: An array od slices. Each slice contains
#a chromosome
######################################################
sub getAllChromosomes{
my($sa)=@_;
my @chromosomes = @{$sa->fetch_all('chromosome') };
return @chromosomes;
}


sub getAllGenes{
my($sa)=@_;
my @chromosomes =&getAllChromosomes($sa);
my @genes=();
while (my $cSome=shift @chromosomes){
my @tmpGenes=@{$cSome->get_all_Genes()};
push(@genes,@tmpGenes);
}
return @genes;
}




sub getAllGenesForChromosome{
my ($chromosome,$sa)=@_;
my $slice =&getSliceForChromosome($chromosome,$sa);
my @genes=@{$slice->get_all_Genes()};
return @genes;
}

sub getGeneIdsForUniprot{
my($ga,$uniprot)=@_;
my @gene_names = @{$ga->fetch_all_by_external_name($uniprot)};
my @ids=();
foreach my $gn (@gene_names){
push(@ids,$gn->display_id());
#print "GENENAME:".$gn->display_id()."\n";
}

return @ids;
}

sub getGeneIdsForRefseq{
my($ga,$refseq)=@_;
my @gene_names = @{$ga->fetch_all_by_external_name($refseq)};
my @ids=();
foreach my $gn (@gene_names){
push(@ids,$gn->display_id());
#print "GENENAME:".$gn->display_id()."\n";
}

return @ids;
}

sub getGeneIdsForExternalId{
my($ga,$id)=@_;
my @gene_names = @{$ga->fetch_all_by_external_name($id)};
my @ids=();
#foreach my $gn (@gene_names){
# push(@ids,$gn->display_id());
#}
#return @ids;
my $id="";
if (defined $gene_names[0]){
$id=$gene_names[0]->display_id();
}
return $id;
}


##################################
#Returns a gene for a specified ID
#Arg[1]:ID
#Return type: Bio::EnsEMBL::Gene
#
##################################
sub getGeneForStableId{
my ($ga,$stable_id)=@_;
my $gene = $ga->fetch_by_stable_id($stable_id);
return $gene;
}


sub getTranscriptForStableId{
my ($ta,$stable_id)=@_;
my $transcript = $ta->fetch_by_stable_id($stable_id);
return $transcript;
}


###################################
#Returns all transcripts for the 
#gene specified as a argument
#Arg[1]: Bio::EnsEMBL::Gene
#Return type: array of Bio::EnsEMBL::Transcript
###################################
sub getAllTranscriptsForGene{
my ($gene)=@_;
my @transcripts=();
if (defined $gene){
@transcripts = @{$gene->get_all_Transcripts()};
}
return @transcripts;
} 



###################################
#
#Arg[1]: Bio::EnsEMBL::Gene
#Return type: array of fasta seqs
####################################
sub getAllTranscriptsForGeneInFastaFormat{
my ($gene)=@_;
my @transcripts=&getAllTranscriptsForGene($gene);
my @fastaSeqs=();
foreach my $tran (@transcripts){
my $seq="\>".$tran->display_id() ."\n".$tran->seq()->seq()."\n";
push(@fastaSeqs,$seq);
}
@fastaSeqs=&formatNumberOfLetters(60,@fastaSeqs);
return @fastaSeqs;
}





##################################
#
#Arg[1]: array of Bio::EnsEMBL::Transcript
#Return type: array of fasta seqs
##################################
sub getAllTranslatedRegionsForTranscriptsInFastaFormat{
my @transcripts=@_;
my @translated=();
foreach my $tran (@transcripts){
if($tran->translateable_seq()){
my $seq="\>".$tran->display_id()."\n".$tran->translateable_seq()."\n";
push(@translated,$seq);
}
}
@translated=&formatNumberOfLetters(60,@translated);
return @translated;
}

###############################
#Arg[1]: array of Bio::EnsEMBL::Transcript
#Return type: array of translates fasta seqs
##################################
sub getTranslationsForTranscriptsInFastaFormat{
my @transcripts=@_;
my @translated=();

foreach my $tran (@transcripts){
if($tran->translateable_seq()){
my $seq=$tran->translate();
my $n=$seq->display_id();
my $s=$seq->seq();
my $f="\>".$n."\n".$s;
push(@translated,$f);
}
}
@translated=&formatNumberOfLetters(60,@translated);
return @translated;
}  


##################################
#Returns all 3'UTRs for all transcripts
#passed as an argument
#Arg[1]: array of Bio::EnsEMBL::Transcript
#Return type: array of fasta seqs
##################################
sub getThreePrimeUtrTranscriptsInFastaFormat{
my @transcripts=@_;
my @fastaSeqs=();
foreach my $tran (@transcripts){
my $three_utr=$tran->three_prime_utr();
if(defined $three_utr){
my $seq="\>".$tran->display_id()."\n".$three_utr->seq()."\n";
push(@fastaSeqs,$seq);
}
}
@fastaSeqs=&formatNumberOfLetters(60,@fastaSeqs);
return @fastaSeqs;
}



#######################################
#For each transcript returns the 5'UTR
#the spliced exons and the 
#3' UTR in fasta format.
#####################################
sub getUtrsPlusSplicedExonsForTranscriptsInFastaFormat
{
my @transcripts=@_;
my @fastaSeqs=();

while (my $tran= shift(@transcripts)){
my $three="";
my $five="";
my $translated="";
my $three_utr=$tran->three_prime_utr();
my $five_utr=$tran->five_prime_utr();
if(defined $three_utr) {
$three=$three_utr->seq();
#  $three=~tr/[A-Z]/[a-z]/; #to lowercase
}
if (defined $five_utr) {
$five=$five_utr->seq();
#  $five=~tr/[A-Z]/[a-z]/; #to lowercase
}
if($tran->translateable_seq()){
$translated=$tran->translateable_seq();
$translated=~tr/[a-z]/[A-Z]/; #to highercase
my $seq="\>".$tran->display_id()."\n".
$five.$translated.$three."\n";
push(@fastaSeqs,$seq);
}
}
@fastaSeqs=&formatNumberOfLetters(60,@fastaSeqs);
return @fastaSeqs;
}


#############################################
#For each transcript, return 5'UTR(lowercase),
#Exons(uppercase), Introns(lowercase),3'UTR
#in the order that they appear on the genome
#############################################
#?? comment by Qing: the assumption of 3'UTR only spans 1 exon can be a problem??
#############################################
sub getUtrsPlusExonsPlusIntronsForTranscriptsInFastaFormat{
my @transcripts=@_;
my @fastaSeqs=();
while (my $tran= shift(@transcripts)){
my $seq="";
my $three="";
my $five="";
my $intron="";
my $exon="";   
my $three_utr=$tran->three_prime_utr();
my $five_utr=$tran->five_prime_utr();
if(defined $three_utr) {
$three=$three_utr->seq();
#$three=~tr/[A-Z]/[a-z]/; #to lowercase
}
if (defined $five_utr) {
$five=$five_utr->seq();
#$five=~tr/[A-Z]/[a-z]/; #to lowercase
}
if($tran->translateable_seq()){
my @exons=@{$tran->get_all_Exons()};
my @introns=@{$tran->get_all_Introns()};
$seq="\>".$tran->display_id()."\n".$five;
for (my $i=0;$i<@exons;$i++){
 $exon=$exons[$i]->seq->seq;
 $exon=~tr/[a-z]/[A-Z]/; #to highercase
 if ($i==0){
    my $ut=$five;
    $ut=~tr/[a-z]/[A-Z]/;
    $exon=~s/$ut//; #remove 5UTR that is included in 1st exon
   }
 if ($i==@exons-1){
    my $ut=$three;
    $ut=~tr/[a-z]/[A-Z]/;
    $exon=~s/$ut//; #remove 3UTR that is included in last exon
   }
 $seq=$seq.$exon;
 if ($i<@exons-1){
    $intron=$introns[$i]->seq();
    $intron=~tr/[A-Z]/[a-z]/; #to lowercase
    $seq=$seq.$intron;
   }
 }  
$seq=$seq.$three."\n";
push(@fastaSeqs,$seq);
}
}
@fastaSeqs=&formatNumberOfLetters(60,@fastaSeqs);
return @fastaSeqs; 
}

sub getAllFirstIntronsInFastaFormat{
my @transcripts=@_;
my @fastaSeqs=();
my $seq="";
while (my $tran= shift(@transcripts)){
if($tran->translateable_seq()){
my @introns=@{$tran->get_all_Introns()};
$seq="\>".$tran->display_id()."\n";
$seq=$seq.$introns[0]->seq();
push(@fastaSeqs,$seq);
}
}
@fastaSeqs=&formatNumberOfLetters(60,@fastaSeqs);
return @fastaSeqs;
}


#################################################
#return an array of genes that are orthologous
#to the specified $gene. The array includes the 
#specieified gene
#################################################

sub getAllOrthologousGenes{
my ($gene,$member_adaptor,$homology_adaptor,@requestedSpeciesFullName)=@_;
my @allGenes=();
push(@allGenes,$gene);
my $member = $member_adaptor->fetch_by_source_stable_id("ENSEMBLGENE",$gene->stable_id);
my $db=$member->genome_db->name;
my $all_homologies = $homology_adaptor->fetch_by_Member($member);
#print STDERR "homology: ",scalar @$all_homologies, "\n";
foreach my $this_homology (@$all_homologies) {
my $desc=$this_homology->description();
if ($desc=~/ortholog.*/){
#print STDERR "DESC: $desc\n";
my $all_member_attributes =
$this_homology->get_all_Member_Attribute();
#print STDERR "memberAttribute: ",scalar @$all_member_attributes,"\n";
foreach my $ma (@$all_member_attributes) {
	my ($mb, $attr) = @$ma;
	my $label =$mb->stable_id;
	my $name=$mb->genome_db->name;
	#print STDERR "$name\n";
	if(&speciesMatch($name,@requestedSpeciesFullName)){
		my $sga=&getGeneAdaptorForSpecies($name);
		my $orthologGene=&getGeneForStableId($sga,$label);
		push(@allGenes,$orthologGene);
	}
}	
}#end if ortholog
}
return @allGenes;
}

###################################
#returns the species for one or 
#more genes
sub getSpeciesForGenes{
my($member_adaptor,@genes)=@_;
my @species=();
foreach my $g (@genes){
my $stableId=$g->stable_id();
my $mb=$member_adaptor->fetch_by_source_stable_id("ENSEMBLGENE",$stableId);
my $name=$mb->genome_db->name;
#print STDERR "found $name for $stableId\n";
push (@species,$name);
}
return @species;
}
####################################
#Checks if the query species matches
#one the requested species 
####################################
sub speciesMatch{
my($querySpecies,@requestedSpecies)=@_;
(my $altName=$querySpecies)=~ s/\s/_/g;
#print STDERR "$altName\t";
for (my $i=0;$i<@requestedSpecies;$i++){
    #print "comapring to $requestedSpecies[$i]\n";
    if (($querySpecies=~/$requestedSpecies[$i]/i)){#||($altName=~/$requestedSpecies[$i]/i)){
      return 1;
      }
  }
return 0;
}



sub getVariationDetailsForTranscripts{
my ($tmpGeneName,$member_adaptor,@transcripts)=@_;
my @variationDetails=();
my $member = $member_adaptor->fetch_by_source_stable_id("ENSEMBLGENE",$tmpGeneName);
my $db=$member->genome_db->name;
$db=~s/\s/\_/;
$db=~tr/A-Z/a-z/;
#print STDERR "GETTING variation for $db\n";
my $humanDbVariation  = &getDbAdaptor($db,'variation');
if (defined $humanDbVariation){
my $trv_adaptor = $humanDbVariation->get_TranscriptVariationAdaptor;
for (my $m=0;$m<@transcripts;$m++){
     my $trvs = $trv_adaptor->fetch_all_by_Transcripts([$transcripts[$m]]);
     foreach my $tv (@{$trvs}){
         #my $var=$tv->variation_feature->variation();
         #my $varGenomicStart=$tv->variation_feature->start;
         #my $varGenomicEnd=$tv->variation_feature->end;
         #my $varStrand=$tv->variation_feature->strand;
         #4 lines above are not efficient as multiple mysql connections made
         my $tvf=$tv->variation_feature; 
         my $varGenomicStart=$tvf->start;
         my $varGenomicEnd=$tvf->end;
         my $varStrand=$tvf->strand;

         my @coords= $transcripts[$m]->genomic2cdna($varGenomicStart,$varGenomicEnd,$varStrand);
         my $varCdnaStart=$coords[0]->start();
         my $transcriptId=$transcripts[$m]->display_id();
         #my $snpId=$tv->variation_feature->variation_name;
         #my $alleles=$tv->variation_feature->allele_string;
         my $snpId=$tvf->variation_name;
         my $alleles=$tvf->allele_string;
         my @consequences=@{$tv->consequence_type};
         my $addSnp=0;
         my  $snpType="";
         for (my $n=0;$n<@consequences;$n++){
             #print "$consequences[$n] ";
             if (($consequences[$n]=~/NON_SYNONYMOUS_CODING/) ||
                 ($consequences[$n]=~/SYNONYMOUS_CODING/)||
                 ($consequences[$n]=~/5PRIME_UTR/)||
                 ($consequences[$n]=~/3PRIME_UTR/) ){
                 $addSnp =1;
                 $snpType=$consequences[$n];
               }
          }
         if ($addSnp==1){
            my $tmpVarDetails=$transcriptId."\,-1\,".$varCdnaStart.
                           "\,-1\,0.21\,0.49\,0.84\,\*\,untitled\,".
                           $snpId. "\,".$alleles."\,". $snpType."\n";
           push (@variationDetails,$tmpVarDetails);
         }
     }
 }
}
return @variationDetails;
}

sub getVariationDetailsForTranscripts2{
my ($inputSpecies,$inputTranscripts)=@_;
my @transcripts=@$inputTranscripts;
my @variationDetails=();
my @db_adaptors=();
my @trv_adaptors=();
my %dba;
my %trva;
foreach my $species (@$inputSpecies){
	$species=~ s/\s+/_/;
	if(! defined $dba{$species}){
		$dba{$species}= & getDbAdaptor("$species",'variation');
		print STDERR "GETTING variation for $species\n";
		$trva{$species}=$dba{$species}->get_TranscriptVariationAdaptor;
	}
	push @trv_adaptors,$trva{$species};
}
	
for (my $m=0;$m<@transcripts;$m++){
     my $trvs = $trv_adaptors[$m]->fetch_all_by_Transcripts([$transcripts[$m]]);
     foreach my $tv (@{$trvs}){
         #my $var=$tv->variation_feature->variation();
         #my $varGenomicStart=$tv->variation_feature->start;
         #my $varGenomicEnd=$tv->variation_feature->end;
         #my $varStrand=$tv->variation_feature->strand;
         #4 lines above are not efficient as multiple mysql connections made
         my $tvf=$tv->variation_feature;
         my $varGenomicStart=$tvf->start;
         my $varGenomicEnd=$tvf->end;
         my $varStrand=$tvf->strand;

         my @coords= $transcripts[$m]->genomic2cdna($varGenomicStart,$varGenomicEnd
,$varStrand);
         my $varCdnaStart=$coords[0]->start();
         my $transcriptId=$transcripts[$m]->display_id();
         #my $snpId=$tv->variation_feature->variation_name;
         #my $alleles=$tv->variation_feature->allele_string;
         my $snpId=$tvf->variation_name;
         my $alleles=$tvf->allele_string;
         my @consequences=@{$tv->consequence_type};
         my $addSnp=0;
         my  $snpType="";
         for (my $n=0;$n<@consequences;$n++){
             #print "$consequences[$n] ";
             if (($consequences[$n]=~/NON_SYNONYMOUS_CODING/) ||
                 ($consequences[$n]=~/SYNONYMOUS_CODING/)||
                 ($consequences[$n]=~/5PRIME_UTR/)||
                 ($consequences[$n]=~/3PRIME_UTR/) ){
                 $addSnp =1;
                 $snpType=$consequences[$n];
               }
          }
         if ($addSnp==1){
            my $tmpVarDetails=$transcriptId."\,-1\,".$varCdnaStart.
                           "\,-1\,0.21\,0.49\,0.84\,\*\,untitled\,".
                           $snpId. "\,".$alleles."\,". $snpType."\n";
           push (@variationDetails,$tmpVarDetails);
         }
     }
 }

return @variationDetails;
}


sub getNamesForTranscripts{
my @transcripts=@_;
my @transcriptNames=();
my $i=0;
while (my $tran= shift(@transcripts)){
       $transcriptNames[$i]=$tran->display_id();
       $i++;
      }
return @transcriptNames;
}


sub getGeneStructureForTranscripts{
my @transcripts=@_;
my @geneStructure=();
my $exSeq="";
#my $exon="";
#push(@boundaries,"sequenceName\,columnNumber\,residueNumber\,number\,RCOL\,GCOL\,BCOL\,SYMBOL\,name\,geneLocation End\n");
while (my $tran= shift(@transcripts)){
       my $transcriptName=$tran->display_id();
       my $nucCount=1;
       my $five_utr=$tran->five_prime_utr();
       my $fiveSeq="";
       my $three_utr=$tran->three_prime_utr();
       my $threeSeq="";
       if (defined $five_utr){
           $fiveSeq= $five_utr->seq();
          }
       if (defined $three_utr){
           $threeSeq=$three_utr->seq();
          }

       if (defined $five_utr) {
           my $fiveLength=length($fiveSeq);
           for (my $i=0;$i<$fiveLength;$i++){
               my $line=$transcriptName."\,-1\,".$nucCount.
                        "\,-1\,0.21\,0.7\,0.59\,\*\,untitled\,".
                        "5UTR\n";
               push(@geneStructure,$line); 
               $nucCount++;
            }
       }
      if($tran->translateable_seq()){
         my @exons=@{$tran->get_all_translateable_Exons()};
           for (my $i=0;$i<@exons;$i++){
              my $exon=$exons[$i]->seq->seq;
              my $exonLength=length($exon);
              for (my $j=0;$j<$exonLength;$j++){
                  my $k=$i+1;
                  my $exonNumber="Exon".$k;
                  my $line=$transcriptName."\,-1\,".$nucCount.
                           "\,-1\,0.21\,0.7\,0.59\,\*\,untitled\,".
                           "$exonNumber\n";
                  push(@geneStructure,$line);
                  $nucCount++;
                 }
           }
    }
    #     my @exons=@{$tran->get_all_Exons()};
    #     my @introns=@{$tran->get_all_Introns()};
    #     for (my $i=0;$i<@exons;$i++){
    #         my $exon=$exons[$i]->seq->seq;
    #         $exon=~s/$fiveSeq//; #FIRST exon contains 5 utr so must remove 
    #         $exon=~s/$threeSeq//; #LAST exon contains 3' UTR so must remove
    #         my $exonLength=length($exon);
    #         for (my $j=0;$j<$exonLength;$j++){
    #             my $k=$i+1;
    #             my $exonNumber="Exon".$k;
    #             my $line=$transcriptName."\,-1\,".$nucCount.
    #                     "\,-1\,0.21\,0.7\,0.59\,\*\,untitled\,".
    #                      "$exonNumber\n";
    #             push(@geneStructure,$line);
    #             $nucCount++;
    #            }
    #        }
    #    }
      my $three_utr=$tran->three_prime_utr();
      if (defined $three_utr){
           my $threeLength=length($threeSeq);
           for (my $i=0;$i<$threeLength;$i++){
               my $line=$transcriptName."\,-1\,".$nucCount.
                        "\,-1\,0.21\,0.7\,0.59\,\*\,untitled\,".
                        "3UTR\n";
               push(@geneStructure,$line);
               $nucCount++;
            }
       }
  } #next transcript
return @geneStructure;
}

sub getBoundariesForUtrsPlusExonsForTranscripts{
my @transcripts=@_;
my @boundaries=();
#push(@boundaries,"sequenceName\,columnNumber\,residueNumber\,number\,RCOL\,GCOL\,BCOL\,SYMBOL\,name\,5utrEnd\,exonEnd\n");
while (my $tran= shift(@transcripts)){
    my $seq=""; my $three=""; my $five=""; my $exon=""; 
    my $annotLine="";
    my $fiveLength=0;
    my $threeLength=0;
    my $diff=0;
    my $exLength=0;
    my $start=0;
    my $end=0;
    my $three_utr=$tran->three_prime_utr();
    my $five_utr=$tran->five_prime_utr();
    if (defined $five_utr) {
      $five=$five_utr->seq();
      $seq=$five;
      $fiveLength=length($seq);
      $annotLine= $tran->display_id();
      $annotLine=$annotLine."\,-1\,".$fiveLength.
                 "\,-1\,0.21\,0.7\,0.59\,\*\,untitled\,true\,false\n";
      push(@boundaries,$annotLine);
      $exLength=$fiveLength; #### added line by Qing so that the output number matches the residue number of the enxons. ###
    }
    # not reported as end of 3utr is also end of seq
    if(defined $three_utr) {
      #my $d=$tran->display_id();
      #print STDERR "three prime defined $d !!\n";
      $three=$three_utr->seq();
      $threeLength=length($three);
      #$annotLine= $tran->display_id();
      #$annotLine=$annotLine."\,-1\,".$threeLength.
      #           "\,-1\,0.21\,0.7\,0.59\,\*\,untitled\,false\,true\,false\n";
      #push(@boundaries,$annotLine);
     }

   #if we hav a translateable sequence
   #then there will be exons
   # the end of the last exon will be
   #the start-1 of the three prime UTR
   if($tran->translateable_seq()){
     my @exons=@{$tran->get_all_translateable_Exons()};
     my @introns=@{$tran->get_all_Introns()};
     $seq="\>".$tran->display_id()."\n".$five;
     for (my $i=0;$i<@exons;$i++){
         $exon=$exons[$i]->seq->seq;
         $start=$exons[$i]->start();
         $end=$exons[$i]->end();
         $diff=$end-$start;
         if ($diff<0){
            $diff=$diff*$diff;
            $diff=sqrt($diff);
           }
         $diff++;
         $exLength=$exLength+$diff; 
         #print STDERR "$start $end $diff $exLength\n";
         $seq=$seq.$exon;
         $annotLine=$tran->display_id();
         # if not the last exon
         #if ($i!=@exons-1){
             $annotLine=$annotLine.
                        "\,-1\,".$exLength.
                        "\,-1\,0.21\,".
                        "0.7\,0.59\,\*\,".
                        "untitled\,false".
                        "\,true\n";
             push(@boundaries,$annotLine);
         #   }
          #if at the last exon
       #   if ($i==@exons-1){
       #      $exLength=$exLength-$threeLength;
       #      $annotLine=$annotLine.
       #                "\,-1\,".$exLength.
       #                "\,-1\,0.21\,".
       #                 "0.7\,0.59\,\*\,".
       #                 "untitled\,false".
       #                 "\,true\n";
       #      push(@boundaries,$annotLine);
       #      }
    } #end for all exons
  } #end if translatable
 }#end while transcripts
return @boundaries;
}





##################################
#Returns all 5'UTRs for all transcripts
#passed as an argument
#Arg[1]: array of Bio::EnsEMBL::Transcript
#Return type: array of fasta seqs
##################################
sub getFivePrimeUtrTranscriptsInFastaFormat{
my @transcripts=@_;
my @fastaSeqs=();
foreach my $tran (@transcripts){
  my $five_utr=$tran->five_prime_utr();
  if(defined $five_utr){
    my $seq="\>".$tran->display_id()."\n".$five_utr->seq()."\n";
    push(@fastaSeqs,$seq);
   }
  }
@fastaSeqs=&formatNumberOfLetters(60,@fastaSeqs);
return @fastaSeqs;
}


#####################################
#Lists databases avaiable in database
#####################################
sub listDatabases{
my @list=();
my @db_adaptors = @{ $registry->get_all_DBAdaptors() };
foreach my $db_adaptor (@db_adaptors) {
    my $db_connection = $db_adaptor->dbc();
    my $db=$db_adaptor->species()."\t".
           $db_adaptor->group(). "\t".
           $db_connection->dbname()."\t".
           $db_connection->host().
       "\t".$db_connection->port();
    push(@list,$db);

 }
return @list;
}
1;
