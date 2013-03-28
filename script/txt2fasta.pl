#!/usr/bin/perl -w

use strict;

my ($inputfile, $line, @array, $chr, $name, $i, $start, $strand, $count, $cmd, $tmpSeq, $length, $tss, $size, $keepSize);

#die "<usage>txt2fasta" unless $#ARGV<0;

$inputfile = '-';
open (IN, $inputfile);

$keepSize="F";
if ($#ARGV==0){
  $keepSize="T";
}

$tmpSeq="";

$line = <IN>;
while ($line) {
  $line=~s/\s$//g;
  @array = split(/\s/, $line);
  $size=length($array[1]);
  if ($keepSize eq "T"){
    print STDOUT ">$array[0]|$size\n";
  }
  else {
    print STDOUT ">$array[0]\n";
  }

  print STDOUT "$array[1]\n";
  $line = <IN>;
}
#print out the last one


