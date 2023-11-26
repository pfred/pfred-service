#! /usr/bin/perl -w

use strict;

my ($filterfile, $inputfile, $idx, $filter_line, $input_line, %filter, @fields, $key);

die "<usage>cp-filter.pl filterfile column_idx" unless @ARGV;
$filterfile = $ARGV[0];
$inputfile = '-';
$idx=$ARGV[1]-1;

open (FILTER, $filterfile);
open (IN, $inputfile);

$filter_line=<FILTER>;
while ($filter_line) {
  $filter_line =~s/\s$//g;
  $filter_line=cleanup(\$filter_line);
  $filter{$filter_line}=1;
  $filter_line=<FILTER>;
}


$input_line=<IN>;
while ($input_line){
  if ($input_line=~/^\s*$/){#empty line
     $input_line=<IN>;
     next;
  }
  $input_line=~s/\s$//g;
  @fields = split (/\t/, $input_line);
  $key=$fields[$idx];
  $key=cleanup(\$key);
  #print "$key\n";
  if ($filter{$key}) {
    print STDERR "$input_line\n";
  }
  else {
    print STDOUT "$input_line\n";
  }
  $input_line=<IN>;
}


sub cleanup {
  my $string1=shift;
  $$string1 = uc($$string1);

  if ( $$string1 =~/^PF-(\d{6})-\d{2}/i ) {
    $$string1 = "PF-00".$1;
  }

  elsif ( $$string1 =~/PF-(\d{6}$)/i ) {
    $$string1 = "PF-00".$1;
  }

  elsif ( $$string1 =~/(^PF-\d{8})/i ) {
    $$string1 = $1;
  }
}
