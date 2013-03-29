pfred-service
=============

Source codes to setup PFRED service. There are two major components for this project:
* Perl, Python and Shell scripts that performs the actual computational tasks
* [XFire] (http://www.xfire.org) based soap service that wraps these tasks and exposes them via WSDL

Setup 
---------
In order to run these scripts on your platform, you need to make sure all software packages listed in setup_env.sh 
are installed and environment variables are setup

Compiling
---------

You can use the provided ant Build.xml file to build the PFREDService-x.y.war, wher x.y is the version number.

* build war file - `ant publish`

Deploying
--------

The war file contains the version number (x.y), and you need to rename it to PFREDService.war, then
move it to the webapps folder of your Tomcat instance.
