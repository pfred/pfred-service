#!/usr/bin/perl -w

use strict;

my ($inputfile, $line, @array, $chr, $name, $i, $start, $strand, $count, $cmd, $tmpSeq, $length, $tss, $size);

die "<usage>fasta2txt" unless $#ARGV<0;

$inputfile = '-';
open (IN, $inputfile);

$start=shift;
$length=shift;

$tmpSeq="";

$line = <IN>;
while ($line) {
  $line=~s/\s$//g;
  if ($line=~/^>/) {
    $line=~s/>//;
    if ($tmpSeq) {
      print STDOUT "\t$tmpSeq\n$line";
    }
    else {
      print STDOUT "$line";
    }
    $tmpSeq="";
  }
  else {
    $tmpSeq=$tmpSeq.$line;
    #print "$tmpSeq\n";
  }
  $line = <IN>;
}
#print out the last one
print STDOUT "\t$tmpSeq\n";


