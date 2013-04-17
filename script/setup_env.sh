# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
        . ~/.bashrc
fi

# User specific environment and startup programs
JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk.x86_64 export JAVA_HOME
CATALINA_HOME=/usr/share/tomcat7 export CATALINA_HOME
CATALINA_BASE=/usr/share/tomcat7 export CATALINA_BASE

PFRED_HOME=/home/ec2-user/pfred export PFRED_HOME
SCRIPTS_DIR=$PFRED_HOME/scripts export SCRIPTS_DIR
RUN_DIR=/media/ephemeral0/pfred export RUN_DIR

PERL_LIB=/usr/share/perl5:/usr/lib64/perl5/vendor_perl
BIOPERL_DIR=$PFRED_HOME/BioPerl-1.6.1 export BIOPERL_DIR
ENSEMBL_DIR=$PFRED_HOME/ensemblapi-v52 export ENSEMBL_DIR
PERL5LIB="$PERL_LIB:$SCRIPTS_DIR:$BIOPERL_DIR:$ENSEMBL_DIR/ensembl/modules:$ENSEMBL_DIR/ensembl-compara/modules:$ENSEMBL_DIR/ensembl-v
ariation/modules" export PERL5LIB

BOWTIE_HOME=$PFRED_HOME/bowtie-0.10.0.2 export BOWTIE_HOME
BOWTIE=$BOWTIE_HOME/bowtie export BOWTIE
BOWTIE_INDEXES=$BOWTIE_HOME/indexes export BOWTIE_INDEXES
BOWTIE_BUILD=$BOWTIE_HOME/bowtie-build export BOWTIE_BUILD


PATH=$JAVA_HOME/bin:/home/ec2-user/pfred/python-2.7.3/bin:/home/ec2-user/pfred/R-2.6.0/bin:$SCRIPTS_DIR:$PATH export PATH


alias python=/home/ec2-user/pfred/python-2.7.3/bin/python2.7

alias checklog='tail -n 100 -f $CATALINA_HOME/logs/catalina.out'

