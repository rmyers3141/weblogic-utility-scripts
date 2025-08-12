#------------------------------------------------------------------------------
#    NAME: WLS-server-init.py
# PURPOSE: Uses Node Manager to start/stop a specific WebLogic server instance. 
# VERSION: 2.0 - Updated for WebLogic 14c / Jython v2.7.1
#   NOTES: This script connects to a Node Manager (as specified by external
#          environment variables) and runs a choice of the following 
#          life cycle operations on a named WebLogic server instance: 'start',
#          'stop', or 'status'.
#
#          See the usage() function below to see how to run this script.
#
#          Also, see the get_envs() function below to see what variables 
#          the script needs to obtain from the environment; most of these 
#          relate to parameters for connecting to the Node Manager, as well
#          as which server to perform operations on.  
#        
#          As a prerequisite, Node Manager must be running and the environment   
#          variables WLST_USER_CONFIG_FILE and WLST_USER_KEY_FILE need to 
#          specify the full path to the config and key files that store
#          encrypted credential details for the Node Manager.  These files  
#          should have been created beforehand using the storeUserConfig() 
#          WLST command in the locations specified by the said environment
#          variables.  The script checks for existence of these files.
#
#   TO-DO: See if you can improve the excetion handling as functions like 
#          dumpStack() don't provide much useful info in most cases.  
#------------------------------------------------------------------------------


import sys
import os
import getopt


# Global constants used in this script:
scriptName = 'WLS-server-init.py'


# BEGIN SUPPORTING FUNCTION DEFINITIONS


def usage():
    "Function provides brief instructions on correct script usage."
    print
    print """This Jython script must be used with the command-line syntax: 
  
    """, scriptName, """ start | stop | status 

    """
#endDef


def get_args():
    "Function gets command-line arguments."
    # Initialise first argument value and make it available globally:
    global arg1
    arg1=""
    # First check the required number of command-line arguments exist:
    if len(sys.argv) != 2:
        print "ERROR - invalid number of command-line arguments."
        usage()
        os._exit(2)
    else:
        arg1=sys.argv[1]
    #endIf
#endDef


def get_envs():
    "Function get required environment variable values."
    global user_config_file, user_key_file, nm_host, nm_port, nm_type, domain_name, domain_path, server_name
    try:
        # Try to assign required vars from environment:
        user_config_file=os.environ['WLST_USER_CONFIG_FILE']
        user_key_file=os.environ['WLST_USER_KEY_FILE']
        nm_host=os.environ['WLS_NM_HOST']
        nm_port=os.environ['WLS_NM_PORT']
        nm_type=os.environ['WLS_NM_TYPE']
        domain_name=os.environ['WLS_DOMAIN']
        domain_path=os.environ['WLS_DOMAIN_DIR']
        server_name=os.environ['WLS_SERVER']
    except:
        print "AN EXCEPTION OCCURRED:"
        print "\tTYPE:", sys.exc_info()[0]
        print "\tVALUE:", sys.exc_info()[1]
        # print "\tTRACEBACK:", sys.exc_info()[2]
        print
        print """INFO - "THIS SCRIPT NEEDS THE FOLLOWING ENVIRONMENT VARIABLES PRE-DEFINED:
        WLST_USER_CONFIG_FILE = Config file for authentication to Node Manager.
        WLST_USER_KEY_FILE = Key file to obtain authentication info from WLST_USER_CONFIG_FILE.
        WLS_NM_HOST = Node Manager machine hostname.
        WLS_NM_PORT = Node Manager port.
        WLS_NM_TYPE = Node Manager type, e.g. SSL or PLAIN.
        WLS_DOMAIN = Name of WebLogic domain.
        WLS_DOMAIN_DIR = Path to WebLogic directory.
        WLS_SERVER = Server on which to perform life cycle operations on."""
        print
        print "EXITING..."
        os._exit(2)
    #endTry
#endDef


def file_path_check(filePath):
    "Function checks if a file exists, specify full path."
    if not os.path.isfile(filePath):
        print "FILE NOT FOUND: "+filePath
        print "EXITING..."
        os._exit(2)
    #endif
#endDef


def server_status(serverName):
    """Function determines state of server named serverName.
    Assumes connection to Node Manager."""
    global server_state
    server_state=""
    try:
        server_state=nmServerStatus(serverName)
    except:
        dumpStack()
        print "\nAN EXCEPTION OCCURRED DETERMINING STATE OF SERVER:", serverName
        exit_script(1)
#endDef


def server_start(serverName):
    """Function starts server specified by serverName.
    Assumes connection to Node Manager."""
    try:
        nmStart(serverName)
    except:
        dumpStack()
        print "\nAN EXCEPTION OCCURRED STARTING SERVER:", serverName
        exit_script(1)
    else:
        print "\nSERVER START COMPLETED."
#endDef


def server_stop(serverName):
    """Function stops server specified by serverName.
    Assumes connection to Node Manager."""
    try:
        nmKill(serverName)
    except:
        dumpStack()
        print "\nAN EXCEPTION OCCURRED STOPPING SERVER:", serverName
        exit_script(1)
    else:
        print "\nSERVER STOP COMPLETED."
#endDef


def exit_script(exitValue):
    """Function - disonnects from Node Manager (if connected)
    and WLST with a specified exit value, exitValue."""
    print "\nDISCONNECT FROM NODE MANAGER...",
    nmDisconnect()
    os._exit(exitValue)
#endDef

# END SUPPORTING FUNCTION DEFINITIONS


# MAIN FUNCTION
def main():
    "Function performs main program execution."
    get_args()
    get_envs()
    file_path_check(user_config_file)
    file_path_check(user_key_file)
    print "\nCONNECT TO NODE MANAGER...\n"
    try:
        nmConnect(userConfigFile=user_config_file, userKeyFile=user_key_file,
                  host=nm_host, port=nm_port,
                  domainName=domain_name, domainDir=domain_path,
                  nmType=nm_type)
    except:
        dumpStack()
        print "\nA PROBLEM OCCURRED CONNECTING TO NODE MANAGER, EXITING..."
        os._exit(1)
    else:
        print "\nCONNECTED TO NODE MANAGER."
    #endTry
    
    # Process command-line arguments:
    if arg1 == 'start':
        print "\nBEGIN SERVER", server_name, "START FROM STATE:"
        server_status(server_name)
        if server_state not in ["RUNNING", "STARTING", "RESUMING", "SUSPENDING", "FORCE_SUSPENDING", "SHUTTING_DOWN", "FAILED", "UNKNOWN"]:
            server_start(server_name)
            exit_script(0)
        else:
            print "\nSERVER", server_name, "IS IN STATE", server_state, "AND CANNOT CURRENTLY BE STARTED."
            print "EXITING..."
            exit_script(1)
        #endIf
    elif arg1 == 'stop':
        print "\nBEGIN SERVER", server_name, "STOP FROM STATE:"
        server_status(server_name)
        if server_state not in ["SHUTDOWN", "STARTING", "RESUMING", "SUSPENDING", "FORCE_SUSPENDING", "SHUTTING_DOWN", "FAILED", "UNKNOWN"]:
            server_stop(server_name)
            exit_script(0)
        else:
            print "\nSERVER", server_name, "IS IN STATE", server_state, "AND CANNOT CURRENTLY BE STOPPED."
            print "EXITING..."
            exit_script(1)
        #endIf
    elif arg1 == 'status':
        print "\nCURRENT STATE OF SERVER",server_name,"IS:"
        server_status(server_name)
        exit_script(0)
    else:
        print "\nUNRECOGNISED OPTION:", arg1
        usage()
        exit_script(2)
    #endIf
#endDef


# Ensure script is executed rather than imported:
if  __name__ == '__main__' or __name__ == 'main':
    main()
else:
    print 'ERROR: THIS SCRIPT MUST BE EXECUTED, NOT IMPORTED.'
    usage()
    os._exit(1)
#endIf
