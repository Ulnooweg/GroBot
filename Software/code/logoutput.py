#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
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
#Error Handling: Standard UEC Error Handling V1
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
        #Here the -r flag is used so most recent is on top as in terminal recent on bottom is more convenient but a file open top down
        #while terminal stops at bottom so when writing to file makes the top the most recent entry
        subprocess.run('journalctl -u grobot.service -n 1000 -r --no-pager >| /mnt/grobotextdat/userdata/logfile.log', shell=True)
        
        return 1
    except Exception as errvar:
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None