#!/usr/bin/perl
#created on: Nov 15, 2010
#created by: Qing Cao
#usage: joinOligoAnnotations.pl -l oligo.csv -j junction.csv -v variation.csv;  
#       join results from RnaEnumeration.pl and getSeqForTranscriptIds.pl.
#BEGIN{
#    push @INC,"/gridccs/vendor/rtc/rna/","/gridccs/vendor/bioPerl/bioPerl/bioperl-live","/gridccs/vendor/ensemblApi/v52/ensembl/modules","/gridccs/vendor/ensemblApi/v52/ensembl-compara/modules","/gridccs/vendor/ensemblApi/v52/ensembl-variation/modules";
  # print @INC;
#}
use strict;
#use Bio::EnsEMBL::Registry;
#use Bio::EnsEMBL::Variation::DBSQL::DBAdaptor;
#use Bio::EnsEMBL::DBSQL::DBAdaptor;
#use BIO::Species;
use Getopt::Long;

#use ensembl2;
#use fasta2;

my $usage= "$0 -l oligo.csv -j junction.csv -v variation.csv -o outputFile\n";
@ARGV>1 || die $usage;


my ($oligoFile,$exonFile, $variationFile,$oligoOutFile);

GetOptions( "l=s"=>\$oligoFile,
            "j=s"=>\$exonFile,
            "v=s"=>\$variationFile,
            "o=s"=>\$oligoOutFile,
            ); #= means mandatory, : means optional, s means string, i means int, b means binary

my @junctions = &readAnnotationFile ($exonFile);
my @variations = &readAnnotationFile ($variationFile);
  
my ($exonPositions,$exonNames)= &assignExons(\@junctions);
#my @names=keys %$exonPositions;
#print STDERR "@names\n";
my %snp =&assignSNPs(\@variations);

open (OLIGO,"<$oligoFile") || die "Can't open oligoFile $oligoFile\n$usage";
open (OUT,">$oligoOutFile") || die "Can't write to file $oligoOutFile\n$usage";

$_=<OLIGO>;
$_=~ s/^\s+|\s+$//g;
my @headers= split /,/,$_;
push @headers,"transcriptLocation";

#process Targetlist from header
my %transcriptCols;
my @transcripts=();
for (my $n=8;$n<@headers;$n++){
  if($headers[$n]=~/(.*)_position/){
      $transcriptCols{$1}=$n ;
      push @transcripts, $1;
      push @headers, "$1_snp";
  }
}
print STDERR "Transcripts: @transcripts\n";
print OUT join "," ,@headers;
print OUT "\n";

while (<OLIGO>){
    $_=~ s/^\s+|\s+$//g;
    my @cols= split /,/,$_; #name,start,end,length,parent_dna_oligo,parent_sense_oligo,parent_antisense_oligo,target_name,ENSRNOT00000046811_match,ENSRNOT00000046811_position,ENST00000399256_match,ENST00000399256_position

##############Assign Exons for the primary target#############
    my $target=$cols[7];
    my $start=$cols[1];
    my $end=$cols[2];
    my $oligoLen=$cols[3];
 #   print STDERR "$target,";
    if(defined $exonNames->{$target}){
	my $exons=@{$exonNames->{$target}};
	for (my $i=0;$i<$exons;$i++){
	    if($start <= $exonPositions->{$target}->[$i]){
		push @cols, $exonNames->{$target}->[$i];
		last;
	    }
	}
	if($start>$exonPositions->{$target}->[$exons-1]){
	    push @cols, "3UTR";
	}
    }else{
	push @cols, "NA";
    }
    
    #assign SNP for primary and other targets#################
 
    for (my $i=0;$i<@transcripts;$i++){
	my $snpline="";
	my $transcript=$transcripts[$i];
	my $matchPosition=$cols[$transcriptCols{$transcript}];
	if($matchPosition !~ /NA/){
	    my @positions=split ' ',$matchPosition;
	    if (defined $snp{$transcript}){
		foreach my $residue (keys %{$snp{$transcript}}){
		    for (my $j=0;$j<@positions;$j++){
			if (($residue>=$positions[$j]) && ($residue<$positions[$j]+$oligoLen)){ 
			    $snpline .= "$snp{$target}{$residue} ";
			}
		    }
		}
		$snpline=~ s/\s+$//g;
	    }
	}
	push @cols,$snpline;
    }
    print OUT join ',',@cols ;
    print OUT "\n";
}
close OLIGO;
close OUT;

#####################################################################################################
#sub readAnnotationFile ($filename)
sub readAnnotationFile
{
    my ($file)=@_;
    open (ANN,"<$file") || print STDERR "Can't open annotation files $file\n";
    my @lines=<ANN>;
    my @annotations=();
    for (my $i=1;$i<@lines;$i++){
	$lines[$i]=~ s/\s+$//g;
	my @cols=split /,/,$lines[$i];
	@{$annotations[$i-1]}=@cols;
    }
    close ANN;
#   print STDERR "@annotations\n";
    return @annotations;
}

#sub assignExons(\@junctions)
sub assignExons
{
    my ($junct)=@_;
#    print STDERR "@$junct\n";
    my %exonNames;
    my %exonPositions;
    my %UTR;
    for(my $i=0; $i<@$junct;$i++){
	my $target= "$junct->[$i][0]";
	my $residue= $junct->[$i][2];
	if (! defined $exonPositions{$target}){
	    $exonPositions{$target}=[];
	    $exonNames{$target}=[];
	    $UTR{$target}= 0;
	}
	if($junct->[$i][9]=~/true/i){
	    $UTR{$target}=1;
	}
	push @{$exonPositions{$target}}, $residue;
	push @{$exonNames{$target}},("exon".($i+1));
    }
    foreach my $target (keys %exonNames){
	if ($UTR{$target}==1){
	    unshift @{$exonNames{$target}}, "5UTR";
	    pop @{$exonNames{$target}};
	}
	@{$exonPositions{$target}}= sort {$a<=>$b}@{$exonPositions{$target}};
	print STDERR "$target @{$exonPositions{$target}}\n@{$exonNames{$target}}\n";
    }
    return (\%exonPositions,\%exonNames);
}

#sub assignSNPs(\@variations)
sub assignSNPs
{
    my ($lines)=@_;
    my %snp;
    for(my $i=0; $i<@$lines;$i++){
	my $target=$lines->[$i][0];
	my $residue=$lines->[$i][2];
	$snp{$target}{$residue}="$lines->[$i][9]($residue $lines->[$i][10])";
    }
    return %snp;
}
