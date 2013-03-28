#!/usr/bin/perl 
#Author: Qing Ccao
#Created: Feb 02, 2009
#Usage: asOligoWalk.pl RNAsequence.seq [example.options]
#modified from the original siRNAWalk.pl script/
#===============================================================================
#
#         FILE:  siRNAWalk.pl
#
#        USAGE:  ./siRNAWalk.pl 
#
#  DESCRIPTION: Predicting siRNA automatically 
#
#      OPTIONS:  ---
# REQUIREMENTS:  libsvm: svm/svm-predict, svm/svm-scale
#         BUGS:  ---
#        NOTES:  ---
#       AUTHOR:  Zhi John Lu <urluzhi@gmail.com>
#      COMPANY:  University of Rochester, Medical Center
#      VERSION:  1.0
#      CREATED:  10/15/2007 15:33:11 EDT
#     REVISION:  1.0
#===============================================================================

use strict;
use warnings;

#set global variables
#############################
my $usage="asOligoWalk.pl RNAsequence.seq \[example.options\]\n";
my (%Form, $mainstring);
my (@position, @oligoseq,@length, @filter_score,@predict_prob);
my (@overall,@dup_break,@duplex,@Tm,@breaking,@intraoligo,@interoligo,@end_diff,@perBaseOverall,@perBaseDuplex,@perBaseInteroligo, @perBaseIntraoligo);
my (@targetRNAseq,@hybrid_DG,@DNAduplex);
my @negativeMotif=('GGGG','ACTG','TAA','CCGG','AAA');
my @positiveMotif=('CCAC','TCCC','ACTC','GCCA','CTCT');
my %count;

my %negativeFilters=('duplex>=',-15.0, 'perBaseDuplex>=', -1.0, 'GGGG>=',1 );
my %scoreWeight=('totalP',1, 'totalN', -1,'interoligo<-8.0', -0.5, 'interoligo<-16.0', -1, 'intraoligo<-4.0',-1, 'intraoligo<-2.0',-0.5,'negativeFilters',-5 );
my @score;

#my $OligoWalk_root= "/usr/local/oligowalk_src";
#my $OligoWalk_exe="$OligoWalk_root/exe/OligoWalk";
#my $NN_data="$OligoWalk_root/NN_data/";

#main flow
####################################
my $optionFile=$ARGV[3];
&read_options;
print STDERR "options are set: $mainstring \n";
&check_options;
#output energy talbes in simple text
&parse_energy ($ARGV[0]);
&calc_features(@oligoseq);
&calc_score (@oligoseq);
&output_energy($ARGV[1],$ARGV[2]) ;

exit;


#subroutines:
##########################################################
sub read_options {

    unless($ARGV[0]){
	print "Please type in the name of your sequence file like\n";
	print "$usage";
	exit ;
    }
    $Form{'seq'}=$Form{'energy'} = "$ARGV[0]"; #sequence of the target
    unless ($optionFile) {
	$Form{'energy'} =~ s/\.seq$//;
	$Form{'asDNA'} = "$Form{'energy'}.asDNA";    
	$Form{'energy'} .= '.energy';
	$Form{'type'} = 'd'; #r: rna; d: dna
	$Form{'mode'} = 3;	#0: break local structure,2: refold the structure, 3: disregard target structure
	$Form{'option'} = 2; #partition function when m=2 or m=0;
	$Form{'scanstart'} = 1; 
	$Form{'scanstop'} = 0; #end of the target
	$Form{'length'} = 19; #lengh of the siRNA
	$Form{'concentration'} = 1;
	$Form{'unit'} = -7;
	$Form{'prefilter'} = 0;
	$Form{'foldsize'} = 800;
	$Form{'score'} = 6; #cannot be re-defined yet
	print STDERR "The default options are used.\n"
	}
    else {
	open (IN,$optionFile) or die ("Cannot read option input file $optionFile $!");
	while (<IN>) {
		if ($_ =~ /^\w/) {
			$_=~ s/[=]//g;
			my @tabs=split " ",$_;
			$Form{$tabs[0]} = $tabs[1];
		}
	}
	close IN;
    }
    #set input options for oligowalk.exe
    $mainstring="-type  $Form{'type'} -seq  $Form{'seq'} -o nofile -m $Form{'mode'} -st 1 -en 0 -M  $Form{'scanstart'} -N  $Form{'scanstop'} -l  $Form{'length'} -co  $Form{'concentration'} -unit  $Form{'unit'} -fi  $Form{'prefilter'} -fold  $Form{'foldsize'} -score  ";
    if($Form{'mode'}!=3){
	$mainstring .= "-s $Form{'option'}";
    }
}

sub check_options {

	if ( $Form{'foldsize'} <= $Form{'length'}) {
		if($Form{'foldsize'}) {
			die("Folding size must be larger than oligo's length.");
		}
	}

}

sub parse_energy {
	my ($file)= @_;
		open (FILE,"$file" ) or  die("Can't open $file $!");
		my @outdata=<FILE>;
		close FILE;
		my $linei=0;#the flag for reading energy table
		foreach my $outline(@outdata) {
			if($outline=~/<\/table>/) {#check if line hit the end of energy table
				last;#break out of the loop
			} elsif ($linei <4 && $linei >=1) {#read from the 4th line of the table
				$linei++;
			} elsif($linei >=4)	{#read the energy talbe to find the oligo site
				$outline=~ s/<tr>//g;
				$outline=~ s/<td>//g;
				$outline=~ s/<\/tr>//g;
				$outline=~ s/<\/td>//g;
				print $outline;
				my @energies=split(" ",$outline);

				if (not defined $energies[0] ){
				   $energies[0]=0;
				}
				if (not defined $energies[1] ){
				   $energies[1]=0;
				}
				if (not defined $energies[2] ){
				   $energies[2]=0;
				}
				if (not defined $energies[3] ){
				   $energies[3]=0;
				}
				if (not defined $energies[4] ){
				   $energies[4]=0;
				}
				if (not defined $energies[5] ){
				   $energies[5]=0;
				}
				if (not defined $energies[6] ){
				   $energies[6]=0;
				}
				if (not defined $energies[7] ){
				   $energies[7]=0;
				}
				if (not defined $energies[8] ){
				   $energies[8]=0;
				}
				if (not defined $energies[9] ){
				   $energies[9]=0;
				}


				push(@position,$energies[0]);
				push(@oligoseq,$energies[1]);
				push(@overall, $energies[2]);
				push(@duplex,$energies[3]);
				push(@perBaseOverall,$energies[2]/19);
				push(@perBaseDuplex,$energies[3]/19);
				push(@Tm, $energies[4]);
				push(@breaking,$energies[5]);
				push(@intraoligo, $energies[6]);
				push(@perBaseIntraoligo,$energies[6]/19);
				push(@interoligo, $energies[7]);
				push(@perBaseInteroligo,$energies[7]/19);
				push(@end_diff, $energies[8]);
				push(@filter_score, $energies[9]);
				#print STDERR "@energies\n";
			}elsif($outline=~/<table>/) {#if line begins a energy table
				$linei=1;# set $linei flag and prepare to read next
			}	
		}
}

#write the energies read from oligowalk output files to the table
sub output_energy {
	print STDERR "OUTPUT\n";
	my ($walkStart,$step)=@_;
	print  "start\toverall\tduplex\tbreaking\tTm\tintraoligo\tinteroligo\tperBaseOverall\tperBaseDuplex\tperBaseIntraoligo\tperBaseInterOligo\t";
	print  "NegativeMotif_",join ("\tNegativeMotif_",@negativeMotif), "\tTotalNegativeMotif\t";
	print  "PositiveMotif_",join ("\tPositiveMotif_",@positiveMotif), "\tTotalPositiveMotif\tTp-Tn\t";
	print  "antisenseSeq5'-3'\ttargetSeq5'-3'\t";
	print  "score\n";
	my $num=@position;
	for(my $j=$walkStart-1; $j<$num; $j+=$step) {
		print  "$position[$j]\t";
		printf  "%.1f\t",$overall[$j];
		print  "$duplex[$j]\t$breaking[$j]\t$Tm[$j]\t";
		print  "$intraoligo[$j]\t$interoligo[$j]\t";
		print  "$perBaseOverall[$j]\t$perBaseDuplex[$j]\t$perBaseIntraoligo[$j]\t$perBaseInteroligo[$j]\t";
		foreach my $motif (@negativeMotif){
		    print  "$count{$motif}->[$j]\t";
		}
		print  "$count{'totalN'}->[$j]\t";
		foreach my $motif (@positiveMotif){
		    print "$count{$motif}->[$j]\t";
		}
		print "$count{'totalP'}->[$j]\t",$count{'totalP'}->[$j]-$count{'totalN'}->[$j], "\t";
		print  "$oligoseq[$j]\t$targetRNAseq[$j]\t";
		print  "$score[$j]\n";
	}
	
}

sub calc_features
{
    my @oligos =@_;
    foreach my $asDNA (@oligos){
	my $rna =&getComplementaryRNA ($asDNA);	
	#my $dG=&Calc_DG_RNA_DNA ($rna);
	#my $dG_dup=&Calc_DG_DNAduplex ($asDNA);
	push @targetRNAseq, $rna;
	#push @hybrid_DG,$dG;
	#push @DNAduplex,$dG_dup;

	#sequence filter according to Matveeva O.V., Nucleic Acids Research, 2000 Vol28, No.15
	my $totalN=0;
	my $totalP=0;
	foreach my $motif (@negativeMotif){
	    my $c=0;
	    while ($asDNA =~ /$motif/g){
		$c++ ;
	    }
	    push @{$count{$motif}},$c;
	    $totalN +=$c;
	}
	push @{$count{'totalN'}},$totalN;
	
	foreach my $motif (@positiveMotif){
	    my $c=0;
	    while ($asDNA =~ /$motif/g){
		$c++ ;
	    }
	    push @{$count{$motif}},$c;
	    $totalP +=$c;
	}
	push @{$count{'totalP'}},$totalP;
    }
}
#make recommendation based on the parameters calculated for each antisense seq
sub calc_score
{
    my @position=@_;
    my $iscore=0;
    my $i=0;

    for ($i=0;$i<=$#position;$i++) {
	$iscore=0;
	$iscore += $scoreWeight{'negativeFilters'} * (($duplex[$i]>= $negativeFilters{'duplex>='}) or ($perBaseDuplex[$i]>= $negativeFilters{'perBaseDuplex>='}));
	$iscore += $scoreWeight{'negativeFilters'} * ($count{'GGGG'}->[$i] >= $negativeFilters{'GGGG>='});
	$iscore += $scoreWeight{'totalP'}*$count{'totalP'}->[$i];
	$iscore += $scoreWeight{'totalN'}*$count{'totalN'}->[$i];
	$iscore += $scoreWeight{'interoligo<-16.0'} * ($interoligo[$i]< -16.0);
	$iscore +=$scoreWeight{'interoligo<-8.0'} * ($interoligo[$i]>=-16.0 and ($interoligo[$i]<-8.0));
	$iscore += $scoreWeight{'intraoligo<-4.0'} * ($intraoligo[$i]< -4.0);
	$iscore +=$scoreWeight{'intraoligo<-2.0'} * ($intraoligo[$i]>=-4.0 and ($intraoligo[$i]<-2.0));
	#print STDERR "$i\t$iscore\n";
	$score[$i]=$iscore;
    }
   
}
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

#sub getComplementRNA (SequenceString): take sequence 5'-3', convert to complementary string, and report back in 5'-3' order
sub getComplementaryRNA
{
    my ($str)=@_;
    my $compStr="";
    $str=&readSeq($str);
  #  print "$str\t";
    $compStr=reverse($str);
    $compStr=~ tr/GCAUT/CGUAA/;
  #  print "$compStr\n";
    return $compStr;
}
#sub Calc_DG_RNA_DNA ($RNAseq)  Given the RNA sequence 5'-3' calculate dG of the RNA and its complementary DNA hybrid, return dG at 37C, in Kcal/mol.
sub Calc_DG_RNA_DNA
{
    my ($seq)=@_;
    my $init =3.1;
    my %stack =('AA',-1.0,'AC',-2.1,'AG',-1.8,'AU',-0.9,
		'CA',-0.9,'CC',-2.1,'CG',-1.7,'CU',-0.9,
		'GA',-1.3,'GC',-2.7,'GG',-2.9,'GU',-1.1,
		'UA',-0.6,'UC',-1.5,'UG',-1.6,'UU',-0.2,
	       );
    
    $seq = &readSeq ($seq);
    my @bases = split '',$seq;
    my $i=0;
    my $DG=$init;
    foreach ($i=0;$i < $#bases;$i++){
	$DG+=$stack{"$bases[$i]$bases[$i+1]"};
    }
    return $DG;
}

#sub Calc_DG_DNAduplex ($DNAseq)  Given the DNA sequence 5'-3' calculate dG of the DNA duplex with its complementary DNA with perfect match, no self-complementary check, return dG at 37C, in Kcal/mol.
#reference: Sugimoto, Nucleic Acids Research 1996, Vol24, No 22, 4501-4505
sub Calc_DG_DNAduplex
{
    my ($seq)=@_;
    my $init =3.4;
    my $self_complementary=0;
    my $self_complementaryEnergy =0.4;
    my %stack =('AA',-1.2,'AC',-1.5,'AG',-1.5,'AT',-0.9,
		'CA',-1.7,'CC',-2.1,'CG',-2.8,'CT',-1.5,
		'GA',-1.5,'GC',-2.3,'GG',-2.1,'GT',-1.5,
		'TA',-0.9,'TC',-1.5,'TG',-1.7,'TT',-1.2,
	       );
    
    $seq = &readSeq ($seq);
    my @bases = split '',$seq;
    my $i=0;
    my $DG=$init;
    foreach ($i=0;$i < $#bases;$i++){
	$DG+=$stack{"$bases[$i]$bases[$i+1]"};
    }
    return $DG;
}
