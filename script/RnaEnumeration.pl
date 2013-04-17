#!/usr/bin/perl
#created on: July 15, 2010
#created by: Qing Cao
#usage: Take a primary ID, and multiple fasta files to enumerate into desired length.

use strict;
use Bio::EnsEMBL::Registry;
use Bio::EnsEMBL::Variation::DBSQL::DBAdaptor;
use Bio::EnsEMBL::DBSQL::DBAdaptor;
#use BIO::Species;
use Getopt::Long;

use ensembl2;
#use fasta2;
use bowtie2;

# incorrect order --dmitri
# my ($BOWTIE,$BOWTIE_BUILD,$BOWTIE_INDEXES)= & exportEnv();
my ($BOWTIE, $BOWTIE_INDEXES, $BOWTIE_BUILD) = exportEnv();

my $usage= "$0 -p primaryID -l oligoLength -f \"fastainputfile.fa containing transcript sequences any additional .fa files\" -o oligoOutFile \n";
@ARGV>1 || die $usage;


my $mismatch=2; # default to mismatch search
my ($primaryID,$oligoLen, $fastaFileList,$oligoOutFile);

GetOptions( "p=s"=>\$primaryID,
	    "l=i"=>\$oligoLen,
	    "f=s"=>\$fastaFileList,
	    "o=s"=>\$oligoOutFile,
	    ); #= means mandatory, : means optional, s means string, i means int, b means binary

my @fastaFiles=split /,|\s+|:/,$fastaFileList;  
print STDERR "Input : $primaryID\t$oligoLen\t@fastaFiles\n";
$oligoOutFile="oligoOut.csv" if (! defined $oligoOutFile);

#get Sequecne for primaryID
my %seqs = &loadSequences2 (@fastaFiles);
my $primarySeq = $seqs{$primaryID}->[1];
#print STDERR "$primarySeq\n";
#enumerate primarySeq
my @oligos= &enumerateSeq($primarySeq,$oligoLen);  #@oligo[dnaSense][rnaSense][rnaAntisense]

#onTargetMatch
my @transcriptNames= keys %seqs;
my $baseName = "onTarget$$";
my $bowtie_in= "$primaryID.dnaOligo.fa";
my $bowtie_out="";
my ($countHash,$posHash); # bowtie output, reference to hash
if(@transcriptNames > 1){ #do onTargetMatch with Bowtie if more than 1 sequence is provided.
    &buildBowtieIndex ( $baseName, @fastaFiles );
    #build bowtie_in fastafile
    open (FA,">$bowtie_in") || die "Can't write temperay file $bowtie_in\n$usage";
    for (my $i=1; $i<=@{$oligos[0]};$i++){
	print FA ">${primaryID}_$i\n$oligos[0]->[$i-1]\n";
    }
    close FA;
    $bowtie_out=&bowtieSearch ("sense",$mismatch,$bowtie_in, $baseName);
    
    ($countHash,$posHash) = &parseBowtieOutput($bowtie_out);
    print STDERR $countHash,$posHash;
}
#-------------- print result ------------#
open (OUT, ">$oligoOutFile")||die "Can't write to file $oligoOutFile\n$usage";
print OUT "name,start,end,length,parent_dna_oligo,parent_sense_oligo,parent_antisense_oligo,target_name";

foreach my $tr (@transcriptNames){
    print OUT ",${tr}_match",",${tr}_position";
}
print OUT "\n";
my ($name,$start,$end);
for (my $i=1; $i<=@{$oligos[0]};$i++){
    $name="${primaryID}_$i";
    $start=$i;
    $end=$i+$oligoLen-1;
    print OUT "$name,$start,$end,$oligoLen,$oligos[0]->[$i-1],$oligos[1]->[$i-1],$oligos[2]->[$i-1],$primaryID";
    for (my $j=0;$j<@transcriptNames; $j++){
	my $tr=$transcriptNames[$j];
	if (! defined $countHash->{$name}{$tr}){
	    $countHash->{$name}{$tr}=[">$mismatch"] ;
	    $posHash->{$name}{$tr}=["NA"];
	 }
	 print OUT ",@{$countHash->{$name}{$tr}},@{$posHash->{$name}{$tr}}";
    }
    print OUT "\n";
}
close OUT;
system ("rm *.ebwt");
#-----------------------------------------------------------------------------------------------------------#

#############################################################################################
#sub enumerateSeq($primarySeq,$oligoLen);  #@oligo[dnaSense][rnaSense][rnaAntisense]
sub enumerateSeq
{
    my ($pSeq,$ol)=@_;
    my $dnaSeq= &RNAtoDNA($pSeq);
    my (@dnaOligos,@rnaOligos,@rnaASOs);
    for (my $i=0;$i<=((length $dnaSeq) - $ol); $i++){
	my $dna=substr ($dnaSeq,$i,$ol);
	push @dnaOligos, $dna;
	push @rnaOligos, &cDNAtoRNA($dna);
	push @rnaASOs, &getReversComplement($dna,"RNA");
    }
    return (\@dnaOligos,\@rnaOligos,\@rnaASOs);
}
	

#sub buildBowtieIndex ($basename, @fastaFiles)
sub buildBowtieIndex
{
    my ($basename, @fastaFiles)=@_;
    #my $BOWTIE_BUILD="/usr/local/share/applications/bowtie/bowtie-build";
    my $basefiles=join ',',@fastaFiles;
    
    print STDERR "$BOWTIE_BUILD $basefiles $basename> dump\n";
    system ("$BOWTIE_BUILD $basefiles $basename > dump");
    return;
}

#sub bowtieSearch($type,$mismatch,$fastaInput,$baseName)
sub bowtieSearch
{
    my($type,$mismatch,$bowtie_in,$db)=@_;
#    my $BOWTIE="/CHEM/bowtie/bowtie";
#    my $BOWTIE_INDEXES="/CHEM/bowtie/indexes";
    my $BOWTIE_option="-a --best";
    $mismatch=($mismatch =~ /[0-3]/)? $mismatch : 2;
    $BOWTIE_option .=" -v $mismatch";
    $BOWTIE_option .=(($type=~ /antisense/i))? " --nofw -f":" --norc -f";
    
    my $bowtie_out="${bowtie_in}_${db}.out";
    my $bowtie_noAlign="${bowtie_in}_${db}.noAlign";
    print STDERR ("set BOWTIE_INDEXES $BOWTIE_INDEXES; $BOWTIE $BOWTIE_option --un $bowtie_noAlign $db $bowtie_in > $bowtie_out;\n");
    system ("set BOWTIE_INDEXES $BOWTIE_INDEXES; $BOWTIE $BOWTIE_option --un $bowtie_noAlign $db $bowtie_in > $bowtie_out;");
    return $bowtie_out;
}


sub parseBowtieOutput
{ 
    my ($bowtie_out)=@_;
    #default type is cDNA #
    my (%count,%position);
    my ($name,$transcript,$gene,$mismatch);
    open(OUT,"<$bowtie_out");
    while(<OUT>){
	$_=~ s/\s+$//g; 
	my @da=split /\s+/,$_;
	$name=$da[0];
	($transcript,$gene)=split /\|/,$da[2],2;
#	print STDERR "$type:$targetGene:$da[2]:$gene\n";
	$mismatch = ($da[7]=~ tr/>/>/);
	if(! defined $count{$name}{$transcript}){
	    $count{$name}{$transcript}=[$mismatch];
	    $position{$name}{$transcript}=[$da[3]+1]; # bowtie reported position starting at 0
#	    print STDERR "$name,$transcript,@{$count{$name}{$transcript}}\n";
	}else{
	    push @{$count{$name}{$transcript}},$mismatch;
	    push @{$position{$name}{$transcript}},$da[3]+1;
#	    print STDERR "$name,$transcript,@{$count{$name}{$transcript}},@{$position{$name}{$transcript}}\n";
	}
    }
    return (\%count,\%position);
}

sub buildBowtieInputFastaFile{
    my ($seqfile,$format)=@_;
    my @names=();
    my $bowtie_in="${seqfile}.fa";
    my ($bowtie_out,$bowtie_noAlign);
    my ($name,$seq,$rest);
    open(OLIGO,"<$seqfile") || die "buildBowtieInputFastaFile() error: can't open  oligo input file $seqfile\n\n$usage";
    open(FA,">$bowtie_in") || die "buildBowtieInputFastaFile() error: can't write file $bowtie_in\n\n$usage";
    if($format=~ /tab/){
	while (<OLIGO>){
	    $_=~ s/\s+$//g;
	    ($name,$seq,$rest)=split /\s+/,$_,3;
	    push @names, $name;
	    $seq=&toDNA($seq);
	    print FA ">$name\n$seq\n";
	}

    }elsif($format=~ /fasta/){
	while (<OLIGO>){
	    if($_=~ /^>/){
	       $_=~ s/^>|\s+$//g;
	       ($name,$rest)=split /\||\s+/, $_;
	       $_=<OLIGO>;
	       $_=~ s/\s+$//g;
	       $seq= &toDNA($_);
	       print FA ">$name\n$seq\n";
	       push @names,$name;
	    }else{
	       print STDERR "Error from buildBowtieInputFastaFile: $seqfile not in right format\n";
	    }
	 }
    }
    close FA;
    close TG;
    return ($bowtie_in,@names);
}
    
#--------------------RNA.pm-------------------------------------#

sub readSeq
{
    my ($str)=@_;
    #$str=~ s/^\s+|^,|\s+$|,$//g;
    $str=~ s/\s+|\W//g;
    $str=~ tr/a-z/A-Z/;
    if($str !~ /^\s*[AUCGTX\s]+\s*$/i){
        print STDERR "Warning Sequence contains nonstandard (AUCGTX) residues:\n$str\n";
    }
    return $str;
}

sub RNAtoDNA
{
    my ($str)=@_;
    $str=readSeq($str);
    $str =~s /U/T/g;
    return $str;
}
#sub cDNAtoRNA(SequenceString): read in sequence string, replace Ts with Ussub DNAtoRNA
sub cDNAtoRNA
{
    my ($str)=@_;
    $str= &readSeq ($str);
    $str=~ s/T/U/g;
    return $str;
}

#sub getReversComplement (Sequence, type "DNA or RNA")
sub getReversComplement
{
    my($str, $type)=@_;
    $type = (defined $type)? $type:"DNA"; #default to DNA
#   print STDERR "$type\n";
    my $compStr="";
    $str=&readSeq($str);
    $compStr=reverse($str);
    ($type=~ /DNA/i )? $compStr=~ tr/CGAUT/GCTAA/ : $compStr=~ tr/CGAUT/GCUAA/;
#   $compStr=~ tr/CGAUT/GC\${type}AA/;
#   $compStr=~ ($str=~ /U/)? tr/GCAU/CGUA/, tr/GCAT/CGTA/;
    return $compStr;
}
