#!/usr/bin/perl -w

use strict;

my ($inputfile, @array, %counts, $max, @fields, $count, $oligo_field, $seq_name,$match_pct,$match_len, $oligo_name, $oligo_len, $line, $total_count, $v, %oligo_names);

#die "<usage>parseBLAST_bestMatch" unless $#ARGV<0;

$inputfile = '-';
open (IN, $inputfile);


$line = <IN>;
while ($line) {
  $line=~s/\s$//g;
  @array = split(/\s/, $line);
  if ($#array<3){
    $line=<IN>; #skip
    next;
  }

  $oligo_field=$array[0];
  $seq_name=$array[1];
  $match_pct=$array[2];
  $match_len=$array[3];

  #print STDERR "$match_pct\n";
  
  @fields=split(/\|/,$oligo_field);
  if ($#fields==1){
    $oligo_name=$fields[0];
    $oligo_names{$oligo_name}=1;
    $oligo_len=$fields[1];
    #print STDERR "$oligo_len\n";
  } else {
    print STDERR "incorrect formatted name: $oligo_field\n";
    $line=<IN>;
    next;
  }

  if ($match_pct==100 && $oligo_len==$match_len){
    if($counts{$seq_name}){
      $count=$counts{$seq_name};
      $count++;
    }else{
      $count=1;
    }
    $counts{$seq_name}=$count;
  }
  $line=<IN>;
}

#found out which ones are the largest
$max=0;
foreach my $key (keys %counts){
  #print "$key\n";
  $v=$counts{$key};
  if ($v>$max){
    $max=$v;
  }
}

$total_count= keys(%oligo_names);
print STDERR ("total_count=$total_count\n");
print STDERR ("max=$max\n");

if ($max<0.9*$total_count){
  print STDERR "no proper target found";
}


foreach my $key (keys %counts){
  $v=$counts{$key};
  if ($v==$max){
    print "$key\n";
  }
}
