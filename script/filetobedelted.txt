#dcaffrey
#parses blast files
#save this file in /path/bin
#and use as follows:
#use lib '/path/bin';
#use fasta
use strict;
#################
#Load the sequence
###################
sub loadSequences2
{
    my (@fileNames)=@_;
    my %fastaSeqs;  #% $fastaSeq{$shortname}[longname,sequence]
    while (my $fileName=shift @fileNames){
	open (FH,"<$fileName")||print STDERR "fasta2.pm: loadSequences2(): Can not open file $fileName\n";
	print STDERR "Loading sequenses from file $fileName\n";
	my ($empty,$shortname,$other);
	my $l="";
	while ($l=<FH>){
		$l=~ s/^\s+|\s+$//g;
#		print STDERR "$l\n";
		if($l=~/^\>/){
			($empty, $shortname,$other)=split />|,|\s|\|/,$l;
#			print STDERR "ShortName $shortname\n";
			$fastaSeqs{$shortname}=[$l,""];	
#			print STDERR "$shortname\n$fastaSeqs{$shortname}->[1]\n";

		}
		else{
			$fastaSeqs{$shortname}->[1] .=$l;
		}
	}
	close FH;
    }
	return %fastaSeqs;
}

#write to fastafile



sub loadSequences
{
my ($fileName)=@_;
open (FH,$fileName);
my @file=<FH>;
my @fastaSeqs=();
my $currSeq="";
my $line="";
my $seq="";
for (my $i=0;$i<@file;$i++){
    $line=$file[$i];
    if ($i==0){
      $seq=$line;
     }
    elsif ($i!=0 && $line=~/^\>/){
      push(@fastaSeqs,$seq);
      $seq="";
      $seq=$line;
    }
   else{
       $seq=$seq.$line;
     }
}
push(@fastaSeqs,$seq);
close(FH);
return(@fastaSeqs);
}


###################
#For a single sequence
#Return the sequence portion 
#as a string
##########################
sub getSequence{
my (@seq)=@_;
shift(@seq);
my $fullSeq=join("",@seq);
return $fullSeq;
}

########################3
#get sequence for a specified name
###################################
sub getSequenceByName{
my ($name,@sequences)=@_;
my $index=&getIndexForSequenceName($name,@sequences);
my @fasta=split(/\n/,$sequences[$index]);

}

##############################
#return index position for a
#sequence name
##############################
sub getIndexForSequenceName{
my ($name,@fastaSeqs)=@_;
my @names=&getNames(@fastaSeqs);
my $index=-1;
for (my $i=0;$i<@names;$i++){
    if($names[$i]=~/$name/){
     $index=$i;
     $i=@names;
    }
 }
return $index;
}


#################
#@seq is a single fasta seq where
#each line is assigned to an element
sub subStrOfSeq
{
my($start,$stop,@seq)=@_;
$stop=$stop-$start;
$start--;
$stop++;
#print STDERR "$start\,*$stop* $seq[0]\n";
my $header=$seq[0];
shift(@seq);
my $fullSeq=join("",@seq);
$fullSeq=~s/\s//g;
my $subSeq=substr($fullSeq,$start,$stop);
my (@newSeq)=($header,$subSeq);

return @newSeq;
}


#################
#get length for a single seq where
#@seq is a single fasta seq where
#each line is assigned to an element
sub getLength
{
my (@seq)=@_;
shift(@seq);
my $fullSeq=join("",@seq);
$fullSeq=~s/\s//g;
my $len=length($fullSeq);
return($len);
}

#####################################
#for each fastaseq in the array
#return the lengths of the sequences

sub getLengths{
my (@fastaSeqs)=@_;
my @lengths=();
for (my $i=0;$i<@fastaSeqs;$i++){
  my @lines=split(/\n/,$fastaSeqs[$i]);
  my $seq="";
  my $header="";
  for (my $j=0;$j<@lines;$j++){
     if($lines[$j]=~/^>/){
       $header=$lines[$j]."\n";
      }
     else{
      $seq=$seq.$lines[$j];
     }
    }
 $lengths[$i]=length($seq);
# print STDERR "$lengths[$i]\n";
 }
return @lengths;
}

#####################################
#get names for each sequence
#####################################
sub getNames{
my (@fastaSeqs)=@_;
my $header="";
my @names=();
for (my $i=0;$i<@fastaSeqs;$i++){
  my @lines=split(/\n/,$fastaSeqs[$i]);
  for (my $j=0;$j<@lines;$j++){
     if($lines[$j]=~/^>/){
       $header=$lines[$j];
       $header=~s/\>//g;
       push(@names,$header);
      }
   }
}
return @names;
}
################################
#for each sequence, 
#reverse the sequence without complementing
################################
sub reverseSequences{
my (@fastaSeqs)=@_;
my @newFasta=();
for (my $i=0;$i<@fastaSeqs;$i++){
    my @lines=split(/\n/,$fastaSeqs[$i]);
    my $seq="";
    my $header="";
    for (my $j=0;$j<@lines;$j++){
      if($lines[$j]=~/^>/){
        $header=$lines[$j]."\n";
       }
      else{
       $seq=$seq.$lines[$j];
      }
     }
   my $newSeq=reverse($seq);
   push(@newFasta,$header.$newSeq);
  }
@newFasta=&formatNumberOfLetters(60,@newFasta);
return @newFasta;
}

sub getGcContentOverWindow{
my ($winSize,@fastaSeqs)=@_;
my @lengths=&getLengths(@fastaSeqs);
my @names=&getNames(@fastaSeqs);
my @gc=();
for (my $i=0;$i<@names;$i++){
     #$gc[0][$i+1]=$names[$i];
     $gc[$i+1][0]=$names[$i];
  }
my $maxCols=0;
for (my $i=0;$i<@fastaSeqs;$i++){
   my @lines=split(/\n/,$fastaSeqs[$i]);
   my $seq="";
   for (my $j=0;$j<@lines;$j++){
     if ($lines[$j]!~/^>/){
        $seq=$seq.$lines[$j];
       }
    }
   for (my $k=0;$k<$lengths[$i]-$winSize+1;$k++){
        my $end=$k+$winSize;
        my $cnt=0;
        for (my $j=$k;$j<$end;$j++){
          my $letter=substr($seq,$j,1);
          $letter=~tr/a-z/A-Z/;
          if( ($letter=~/G/) || ($letter=~/C/)){
            $cnt++
            }
         }#next window
          my $first=substr($seq,$k,1);
          #$gc[$k+1][0]=$k+1;
          $gc[0][$k+1]=$k+1;
          $gc[0][$k+1]="cols".$gc[0][$k+1];
          #$gc[$k+1][0]=$gc[$k+1][0];#.$first;
          #$gc[$k+1][$i+1]=$cnt/$winSize;
          $gc[$i+1][$k+1]=$cnt/$winSize;
          if ($k+1>$maxCols){
             $maxCols=$k+1;
            }
   }#next col
 }#next seq 
for (my $i=0;$i<@fastaSeqs;$i++){
  for (my $k=0;$k<=$maxCols;$k++){ 
      if (!defined $gc[$i][$k]){
         $gc[$i][$k]="NA";
       }
     }
 }
$gc[0][0]="";
return @gc;
}

######################################
#for each fastaseq in the the array,
#set the number of letters in each
#line of sequence to that specied
##################################### 
sub formatNumberOfLetters{
my ($numOfLettersPerLine,@fastaSeqs)=@_;
my @newFasta=();
for (my $i=0;$i<@fastaSeqs;$i++){
  my @lines=split(/\n/,$fastaSeqs[$i]);
  my $seq="";
  my $header="";
  for (my $j=0;$j<@lines;$j++){
     if($lines[$j]=~/^>/){
       $header=$lines[$j]."\n";
      }
     else{
      $seq=$seq.$lines[$j];
     }
    }
  my $numOfLetters=length($seq);
  my $skip=0;
  my $newSeq="";
  while($skip<$numOfLetters){
   my $line=substr($seq,$skip,$numOfLettersPerLine);
   $newSeq=$newSeq.$line."\n";
   $skip=$skip+length($line);
   }
  push(@newFasta,$header.$newSeq);
 } #next fasta entry
return @newFasta;
}

1;
