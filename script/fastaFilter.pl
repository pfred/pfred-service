#!/usr/bin/perl -w

use strict;

my ($inputfile, $filterfile, $line, $tmpSeq,  $size, $filter_line, %filter, $keep, $name, $length);

die "<usage>fastaFilter" unless ($#ARGV>=0);

$inputfile = '-';
$filterfile = $ARGV[0];
open (IN, $inputfile);
open (FILTER, $filterfile);

$filter_line=<FILTER>;
while ($filter_line) {
  $filter_line =~s/\s$//g;
  $filter_line =~s/\s//g;
  if (length($filter_line)>0){
    $filter{$filter_line}=1;
  }
  $filter_line=<FILTER>;
}

if (keys(%filter)>0){
  #don't filter anything
}


$line = <IN>;
if (keys(%filter)==0) {
  #don't filter anything\
   while ($line) {
      print STDOUT "$line";
      $line = <IN>;
   }
}
else {
  $keep=0;
  while ($line) {
    if ($line=~/^>/) {
      $name=$line;
      $name=~s/^>//;
      $name=~s/\s$//;
      $name=~s/\s//g;
      if ($filter{$name}) {
        print STDOUT "$line";
        $keep=1;
      } else {
        $keep=0;
      }
    } else {
      if ($keep==1) {
        print STDOUT "$line";
      }
    }
    $line = <IN>;
  }
}





