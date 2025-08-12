#!/bin/sh

# Script name: cluster01-ms1_init.sh
# Description: 'Wrapper' script for starting, stopping, or 
#              determining status of WebLogic server named
#              "cluster01-ms1".  This wrapper script provides 
#              the necessary parameters to the WLST Jython script 
#              (as specified by the ${WLST_SCRIPT}) which actually
#              performs the requested 'start', 'stop', or 'status' 
#              operations.
#
#              If desired, this script could be specified in a 
#              systemd unit file so it can be managed as a 
#              service.
# TO-DO:       Substitute the CustomTrustKeyStorePassPhrase clear-text
#              entry with an encrypted value using the WLST encrypt() function.
#
# Version:     1.0


# First ensure script is run as correct user:
RUNAS=oracle

if [ `/bin/whoami` != "${RUNAS}" ]
  then
    echo "ERROR: this script must run as be ${RUNAS} user, exiting..."
    exit 1
fi

# Jython script this script will run:
WLST_SCRIPT=/home/oracle/scripts/WLS-server-init.py

# Specify environment variables required by this Jython script:
export WLST_USER_CONFIG_FILE=/home/oracle/scripts/NMuser.properties
export WLST_USER_KEY_FILE=/home/oracle/scripts/NMuser.key
export WLS_NM_HOST=machine1.project14c.test
export WLS_NM_PORT=5556
export WLS_NM_TYPE=ssl
export WLS_DOMAIN=project14c
export WLS_DOMAIN_DIR=/apps/oracle/config/domains/project14c
export WLS_SERVER=cluster01-ms1



# Prepare environment to run WLST:
. /apps/oracle/products/fmw/wlserver/server/bin/setWLSEnv.sh > /dev/null 2>&1

# Provide necessary options for WLST connecting to the Node Manager over SSL:
#JAVA_OPTIONS="${JAVA_OPTIONS} -Dweblogic.security.SSL.ignoreHostnameVerification=true"
JAVA_OPTIONS="${JAVA_OPTIONS} -Dweblogic.security.TrustKeyStore=CustomTrust"
JAVA_OPTIONS="${JAVA_OPTIONS} -Dweblogic.security.CustomTrustKeyStoreFileName=/apps/oracle/config/domains/project14c/keystores/PRODtruststore.p12"
JAVA_OPTIONS="${JAVA_OPTIONS} -Dweblogic.security.TrustKeystoreType=pkcs12"
JAVA_OPTIONS="${JAVA_OPTIONS} -Dweblogic.security.CustomTrustKeyStorePassPhrase=change_me"
         


# Run WLST script with the desired option:
case "$1" in
        start)
		java ${JAVA_OPTIONS} weblogic.WLST ${WLST_SCRIPT} start
		;;

	stop)
		java ${JAVA_OPTIONS} weblogic.WLST ${WLST_SCRIPT} stop

		;;
	 
	status)
		java ${JAVA_OPTIONS} weblogic.WLST ${WLST_SCRIPT} status
		;;

	*)
	        echo "Usage: $0 {start|stop|status}"
	        exit 1
esac
