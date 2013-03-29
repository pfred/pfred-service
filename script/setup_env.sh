
JAVA_HOME=/usr/local/java/jdk1.6.0_30 export JAVA_HOME
CATALINA_HOME=/usr/local/tomcat/apache-tomcat-6.0.35 export CATALINA_HOME
CATALINA_OPTS="-Xms512m -Xmx1024m -XX:MaxPermSize=128m" export CATALINA_OPTS

BIOPERL_DIR=/usr/local/share/applications/BioPerl/BioPerl-1.6.1 export BIOPERL_DIR
ENSEMBL_DIR=/usr/local/share/applications/ensemblAPI export ENSEMBL_DIR
BOWTIE_HOME=/usr/local/share/applications/bowtie export BOWTIE_HOME
BOWTIE=$BOWTIE_HOME/bowtie export BOWTIE
BOWTIE_INDEXES=$BOWTIE_HOME/indexes export BOWTIE_INDEXES
BOWTIE_BUILD=$BOWTIE_HOME/bowtie-build export BOWTIE_BUILD

SCRIPTS_DIR=/home/pfred/scripts export SCRIPTS_DIR
RUNS_DIR=/home/pfred/runs export RUNS_DIR
PERL5LIB="$SCRIPTS_DIR:$BIOPERL_DIR:$ENSEMBL_DIR/ensembl/modules:$ENSEMBL_DIR/ensembl-compara/modules:$ENSEMBL_DIR/ensembl-variation/modules" export PERL5LIB


PATH=$JAVA_HOME/bin:$CATALINA_HOME/bin:$PERL5LIB:$PATH export PATH


