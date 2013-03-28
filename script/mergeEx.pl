#! /usr/bin/perl -w

use strict;


#usage: cat file1| perl merge.pl <idx1> <idx2> <file2> <keepAllInFile1>

my(@lines,@lines2, @lib, @tmp, %ref, $i, $j, $curr_id, $interval, $idx1, $idx2, $id, $line, $keepFile1, $numOfFields);

$idx1 = $ARGV[0];
$idx2 = $ARGV[1];
$keepFile1 = $ARGV[3];
$numOfFields=0;

open (FILE, "$ARGV[2]") || die "unable to open file $ARGV[2] \n";
@lines2 = <FILE>;
for ($i=0; $i<$#lines2+1; $i++) {
  $line = $lines2[$i];
  $line =~ s/\s$//g;
  #$line =~ s/^\s//;
  @tmp=split (/\t/, $line);
  if ($numOfFields==0){
    $numOfFields=$#tmp+1;
  }
  $id = $tmp[$idx2-1];
  cleanup(\$id);
  #print "$id\n";
  $ref{$id}= $lines2[$i];
}

@lines = <STDIN>;
$curr_id="";
for ($i = 0; $i < $#lines+1; $i++) {
  $line = $lines[$i];
  $line =~ s/\s$//g;
  @tmp=split (/\t/, $line);
  $id=$tmp[$idx1-1];
  cleanup(\$id);
  if ( $ref{$id} ){
    print "$line\t$ref{$id}";
  }
  elsif (defined ($keepFile1)) {
    print "$line";
    for ($j=0; $j<$numOfFields; $j++){
      print "\t ";
      if ($j==$idx2-1){
        print "$id";
      }
    }
    print "\n";
  }
}



sub cleanup {
  my ($string1);
  $string1 = shift;
  #print $$string1;

  #AnnArbor compounds here
  if ( $$string1 =~/(^\d{7})\d{4}/ ) {
    $$string1 = $1;
    #print "$$string1";
  }
  elsif ( $$string1 =~/(^\d{7})-\d{4}/ ) {
    $$string1 = $1;
    #print "$$string1";
  }
  #Pfizer old PF compounds
  #elsif ( $$string1 =~/^PF-(\d{6})-\d{2}/i ) {
  #  $$string1 = "PF-00".$1;
  #}
  #Pfizer old PF compounds
  #elsif ( $$string1 =~/PF-(\d{6}$)/i ) {
  #  $$string1 = "PF-00".$1;
  #}
  #pfizer new PF compounds
  elsif ( $$string1 =~/(^PF-\d{8})/i ) {
    $$string1 = $1;
  }
  #all other legacy pfizer compounds
  elsif ( $$string1 =~/(^\w{2}-\d{6})-\d{2}/i ) {
    $$string1 = $1;
  }
  #PHA cmpds
  elsif ( $$string1 =~/^PHA-00(\d{6})/i) {
    $$string1 = "PHA-00".$1;
  }
  #PNU cmpds
  elsif ( $$string1 =~/^PNU-0(\d{6})/i) {
    $$string1 = "PNU-0".$1;
  }
  #PNUL cmpds
  elsif ( $$string1 =~/^PNUL(\d{6})/i) {
    $$string1 = "PNUL".$1;
  }

}
