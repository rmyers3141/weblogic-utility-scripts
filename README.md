# weblogic-utility-scripts
A miscellaneous collection of `wlst` Jython scripts I have developed for configuring and managing [Oracle WebLogic Server](https://www.oracle.com/uk/java/weblogic/), (hereafter referred to as *WebLogic*).

## OVERVIEW
These are essentially *prototype* WLST (*WebLogic Scripting Tool*) scripts, all tested and working, that could be developed further for use in Production environments.

Before using the scripts, a strong familiarity with *WebLogic*, particularly running the *WebLogic* Jython command interpreter `wlst`, is assumed.

The scripts are grouped into the following folders: -

## start-stop
This folder contains a Jython script `WLS-server-init.py` to start, or stop, as managed WebLogic server using a Node Manager.  (Using a Node Manager for start/stop operations is a recommended "best practice" by Oracle).

It also contains an example "wrapper" `bash` script `WLS-server-init.py.sh` demonstrating how to use the `WLS-server-init.py` script in practice to start, stop, or check the status of a managed server using required environment variables and the necessary Node Manager SSL authentication credentials.

### WLS-server-init.py
As a prerequisite, the Node Manager must be running and the environment variables `WLST_USER_CONFIG_FILE` and `WLST_USER_KEY_FILE` need to specify the full path to the config and key files that store encrypted credential details for the Node Manager.  These files should have been created beforehand using the `storeUserConfig()` WLST command in the locations specified by the said environment variables.  The script checks for existence of these files.

The other environment variables the script needs defining before execution are:

| Variable | Description | 
| ------ | ------ |
| `WLS_NM_HOST` | Node Manager machine hostname. | 
| `WLS_NM_PORT` | Node Manager port.
| `WLS_NM_TYPE` | Node Manager type, e.g. **SSL** or **PLAIN**. |
| `WLS_DOMAIN` | Name of WebLogic domain. |
| `WLS_DOMAIN_DIR` | Path to WebLogic directory. |
| `WLS_SERVER` | Server on which to perform life cycle operations on. |

Assuming you've invoked the necessary environment variables to run WLST, the script can be run with syntax like the following:

```sh
java ${JAVA_OPTIONS} weblogic.WLST ./WLS-server-init.py start | stop | status
```
Where `${JAVA_OPTIONS}` specify the necessary Java options for running WLST, such as over SSL.

### cluster01-ms1_init.sh
This script is an example of how to use the above WLST Jython script in practice to start, stop, or check the status of a managed WebLogic Server called `cluster01-ms1`.

To use the script in practice, edit the `export` environment variables defined in the script appropriately, as well as the `$JAVA_OPTIONS` before executing it with syntax like the following:

```sh
./cluster01-ms1_init.sh start | stop | status
```

## ENDNOTES:
These scripts have been tested in both **WebLogic 12c** and **WebLogic 14c** domains.

