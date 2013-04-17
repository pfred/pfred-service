use strict;

#my $BOWTIE="/gridccs/vendor/rtc/bowtie/bowtie";
#my $BOWTIE_INDEXES="/gridccs/vendor/rtc/bowtie/indexes";
#my $BOWTIE_BUILD="/gridccs/vendor/rtc/bowtie/bowtie-build";


#get bowtie info from environment variables
my $BOWTIE="$ENV{BOWTIE}";
my $BOWTIE_INDEXES="$ENV{BOWTIE_INDEXES}";
my $BOWTIE_BUILD="$ENV{BOWTIE_BUILD}";

#my ($BOWTIE,$BOWTIE_BUILD,$BOWTIE_INDEXES)= & exportEnv();

my %AntisenseIndex=("human" => ["HumancDNA.v56", "allHumanUnsplicedGene.v55"],
			"mouse"=>["MousecDNA.v55","allMouseUnsplicedGene.v55"],
			"rat"=>["RatcDNA.v55","allRatUnsplicedGene.v55"],
			);
			
my %siRNAIndex=("human" => ["HumancDNA.v56"],
                        "mouse"=>["MousecDNA.v55"],
                        "rat"=>["RatcDNA.v55"],
                        );

sub exportEnv
{
	print STDERR "ENV: $BOWTIE\n";
        print STDERR "*** ['$BOWTIE', '$BOWTIE_INDEXES', '$BOWTIE_BUILD'] ***\n";
	return ($BOWTIE,$BOWTIE_INDEXES,$BOWTIE_BUILD);
}

sub exportAntisenseIndexes
{
	my ($species)=@_;
	#my $indexlist=join ",", @{$AntisenseIndex{"$species"}};
	print STDERR "AntisenseIndexList: @{$AntisenseIndex{$species}}\n";
	return (@{$AntisenseIndex{"$species"}});
}

sub exportsiRNAIndexes
{
	my ($species)=@_;
	print STDERR "siRNAIndex: @{$siRNAIndex{$species}}\n";
	return (@{$siRNAIndex{"$species"}});
}
