#! /usr/bin/perl
# created: Qing Cao
# date:  Sept 28, 2009
# usage: siRNA_OffTargetSearch_bowtie -t inputType -s species -g GeneEnsemblID seqs.txt


use strict;
use Getopt::Std;
#use FileHandle;
use bowtie2;

undef my %opts;
my $usage="$0 [-t -s -g -v] seqs.txt (with compound names as first column and sequence in the  2nd column)\n -t inputType (sense/antisense)\n -s species (\"human,mouse,rat\")\n -g EnsemblID (gene or transcript Ensembl ID  of intended target, need to have the same order as species)\n-v number of mismatches to search for, should be an integer between [0-3]\n";
#defaults:
$opts{'s'}="HUMAN";
$opts{'t'}="sense";
$opts{'g'}="";  #on-target geneID
$opts{'v'}=2; #default mismatch for siRNA;

#my $BOWTIE="/CHEM/bowtie/bowtie";
#my $BOWTIE_BUILD="/CHEM/bowtie/bowtie-build";
#my $BOWTIE_INDEXES="/CHEM/bowtie/indexes";
my ($BOWTIE,$BOWTIE_BUILD,$BOWTIE_INDEXES)= & exportEnv();
my @BOWTIE_SearchList= & exportsiRNAIndexes("human");
#my @BOWTIE_SearchList=("HumancDNA.v56");
my $BOWTIE_option="-a";

Getopt::Std::getopt('stgvh', \%opts);
if($opts{'h'} || @ARGV<1 ){ die $usage;} # print help

#--------set bowtie mismatch ------------------------------------#
my $mismatch=($opts{'v'}=~ /[0-3]/)? $opts{'v'} : 2;
$BOWTIE_option .=" -v $mismatch -f";

#---------build bowtie search list--------------------------------#

if($opts{'s'} !~ /human/i){
    @BOWTIE_SearchList=();	
    print STDERR "not human\n";
}
if($opts{'s'} =~ /mouse/i){
    #push @BOWTIE_SearchList,"MousecDNA.v55";
	push @BOWTIE_SearchList, & exportsiRNAIndexes("mouse");
}
if($opts{'s'}=~ /rat/i){
    #push @BOWTIE_SearchList, "RatcDNA.v55";
	push @BOWTIE_SearchList, & exportsiRNAIndexes("rat");
}

#-----------------build bowtie input fasta file---------------------------#
my $seqfile = pop @ARGV;
my @names=();
my $bowtie_in="${seqfile}.fa";
my ($bowtie_out,$bowtie_noAlign);
my ($name,$seq,$rest);
if(-f $seqfile){
    open(TG,"<$seqfile") || die $usage;
    open(FA,">$bowtie_in") || die $usage;
    while (<TG>){
	$_=~ s/\s+$//g;
	($name,$seq,$rest)=split /\s+/,$_,3;
	push @names, $name;
	$seq=&toDNA($seq);
	print FA ">$name\n$seq\n";
    }
    close FA;
    close TG;
}elsif($seqfile=~ /^[ATUGC]+$/i){
    open (FA, ">$bowtie_in") || die $usage;
    $seq= &toDNA($seqfile);
    print FA ">$seqfile\n$seq\n";
    close FA;
    push @names,"$seqfile";
}else{
    die $usage;
}
    
#-------------------------------------------------------------------------#
#-----------------run bowtie search --------------------------------------#
my (%count,%record);
print "name";
for (my $i=0; $i< @BOWTIE_SearchList; $i++){
    my $db=$BOWTIE_SearchList[$i];
    my $target=$opts{'g'};
    $bowtie_out="${bowtie_in}_${db}.out";
    $bowtie_noAlign="${bowtie_in}_${db}.noAlign";
    print STDERR ("set BOWTIE_INDEXES $BOWTIE_INDEXES; $BOWTIE $BOWTIE_option --un $bowtie_noAlign $db $bowtie_in > $bowtie_out;\n");
    system ("set BOWTIE_INDEXES $BOWTIE_INDEXES; $BOWTIE $BOWTIE_option --un $bowtie_noAlign $db $bowtie_in > $bowtie_out;");
    if (-f $bowtie_noAlign){
	#append no match to bowtie_out;
	open("NA", "<$bowtie_noAlign");
	my $lines="";
	while(<NA>){
	    if(/^\>(.*)/){
		$lines .="$1\t \tNoMatch|NoMatch\t \t \n";
	    }
	}
        close NA;
	system ("echo \"$lines\" >> $bowtie_out");
    }
    #------parse bowtie out ------------#
    $count{$db} = &parseBowtieOutput ($bowtie_out,$target);
    for (my $j=0;$j<=$mismatch;$j++){
	print "\t${db}_${j}mismatch";
    }
}
print "\n";

#--------------print result----------------------#
foreach $name (@names){
    print "$name";
    for (my $i=0;$i<@BOWTIE_SearchList;$i++){
	my $db=$BOWTIE_SearchList[$i];
	for (my $j=0;$j<=$mismatch;$j++){
	    print "\t$count{$db}->{$name}->[$j]";
	}
    }
    print "\n";

}

#-----------------------------------------------------------------------------------------------------------#

sub parseBowtieOutput
{ 
    my ($bowtie_out,$targetGene,$type)=@_;
    my (%count,%record);
    my ($name,$transcript,$gene,$mismatch);
    open(OUT,"<$bowtie_out");
    while(<OUT>){
	$_=~ s/\s+$//g; 
	my @da=split /\s+/,$_;
	$name=$da[0];
	($transcript,$gene)=split /\|/,$da[2],2;
	($gene,$transcript)=split /\|/, $da[2],2 if($type=~ /unspliced/i);
	#print STDERR "$gene\n";
	$mismatch = ($da[7]=~ tr/>/>/);
	$targetGene=$gene if($da[2]=~ /$targetGene/);
	if($gene=~ /NoMatch/){
	    $count{$name}=[0,0,0,0];
	    next;
	}
        if (! defined $count{$name}){
	    $count{$name}=[0,0,0,0];
	    $record{"${name}_${gene}_$mismatch"}=1;
	    $count{$name}->[$mismatch]++;
	}else{
	    next if ($record{"${name}_${gene}_$mismatch"});
	    $record{"${name}_${gene}_$mismatch"}=1;
	    $count{$name}->[$mismatch]++;  
	}
	
    }
    foreach $name (keys %count){
	for (my $i=0;$i<3;$i++){
	    $count{$name}->[$i]-- if ($record{"${name}_${targetGene}_$i"});
	}
    }
    #print STDERR "$targetGene\n$count{$name}->[0]\n$count{$name}->[1]\n$count{$name}->[2]\n";
    return \%count;
}



#--------------------------------------------------------------------
#---------------------RNA.pm-----------------------------------------------
#sub readSeq(SequenceString): read in Sequence String, and trim off space, carriage returns etc.
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
#sub getReversComplement (Sequence)
sub getReversComplement
{
    my($str)=@_;
    my $compStr="";
    $str=&readSeq($str);
    $compStr=reverse($str);
    ($str=~ /U/)? $compStr=~tr/GCAU/CGUA/:$compStr=~tr/GCAT/CGTA/;
    #print STDERR $compStr;
    return $compStr;
}
sub toDNA
{
    my($seq)=@_;
    $seq = &readSeq($seq);
    $seq=~ tr/U/T/;
    return $seq;
}
sub toRNA
{
    my($seq)=@_;
    $seq=&readSeq($seq);
    $seq=~ tr /T/U/;
    return $seq;
}

