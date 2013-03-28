# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs
JAVA_HOME=/usr/local/java/jdk1.6.0_30 export JAVA_HOME
CATALINA_HOME=/usr/local/tomcat/apache-tomcat-6.0.35 export CATALINA_HOME
CATALINA_OPTS="-Xms512m -Xmx1024m -XX:MaxPermSize=128m" export CATALINA_OPTS

PERL_HOME=/opt/ActivePerl-5.16  export PERL_HOME

SCRIPTS_DIR=/home/pfred/scripts export SCRIPTS_DIR
RUNS_DIR=/home/pfred/runs export RUNS_DIR
BOWTIE_HOME=/usr/local/share/applications/bowtie export BOWTIE_HOME
BOWTIE=$BOWTIE_HOME/bowtie export BOWTIE
BOWTIE_INDEXES=$BOWTIE_HOME/indexes export BOWTIE_INDEXES
BOWTIE_BUILD=$BOWTIE_HOME/bowtie-build export BOWTIE_BUILD
BIOPERL_DIR=/usr/local/share/applications/BioPerl/BioPerl-1.6.1 export BIOPERL_DIR
ENSEMBL_DIR=/usr/local/share/applications/ensemblAPI export ENSEMBL_DIR
OLIGOWALK_ROOT=/usr/local/share/applications/oligowalk export OLIGOWALK_ROOT
PERL5LIB="$SCRIPTS_DIR:$PERL_HOME/site/lib:$BIOPERL_DIR:$ENSEMBL_DIR/ensembl/modules:$ENSEMBL_DIR/ensembl-compara/modules:$ENSEMBL_DIR/ensembl-variation/modules" export PERL5LIB


PATH=$HOME/bin:$JAVA_HOME/bin:$PERL_HOME/bin:$CATALINA_HOME/bin:$PERL5LIB:$PATH export PATH




alias checklog='tail -n 100 -f $CATALINA_HOME/logs/catalina.out'

