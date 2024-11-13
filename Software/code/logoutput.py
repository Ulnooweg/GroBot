#Copyright 2023-2024 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: logoutput
#Version: 1.1
#Description: These functions write the log result of grobot process from journalctl to file
#Function: logtofile(), output the grobot log from journalctl output to a logfile in /mnt/grobotextdat/userdata
#Input: NONE
#Output: NONE
#Error Handling: Output to log/terminal "RuntimeError: LOG IO FAIL" if any uncatched failure occurs and "RuntimeError('FILE IO FAIL')" if output dir don't exist
#
########################################
#MODULE IMPORTS
import subprocess
import os

#Output log from journalctl to file
def logtofile():
    try: #Everything in try-except to catch errors
        #First, check if the directory in question exist
        directory = "/mnt/grobotextdat/userdata" #This is the main external directory associated with USB
        if os.path.isdir(directory) == True: #check if exist
            pass #if it is pass
        else: #if not return error to force a code restart
            raise RuntimeError('FILE IO FAIL')
        
        #Now run the log output using subprocess
        #This runs journalctl and force overwrite the output to the specified logfile.log using >|
        #We use shell=True to specify using system shell so the wildcard >| can be used
        subprocess.run('journalctl -u grobot.service -n 1000 -r --no-pager >| /mnt/grobotextdat/userdata/logfile.log', shell=True)
        
        return
    except:
        raise RuntimeError('LOG IO FAIL')