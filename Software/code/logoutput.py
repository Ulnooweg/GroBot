#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under Québec Free and Open-Source Licence – Strong Reciprocity (LiLiQ-R+) Version 1.1
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: logoutput
#Version: 2.0
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
from multiprocessing import shared_memory

#Output log from journalctl to file
def logtofile():
    try: #Everything in try-except to catch errors
        #Read the debugstate for use as condition in printing debug statement
        ext_mem = shared_memory.SharedMemory(name='grobot_shared_mem')
        debugstate = ext_mem.buf[0]
		
        #Debug message
        print('logoutput-logtofile: Checking existence of log directory') if debugstate == 1 or debugstate == 2 else None

        #First, check if the directory in question exist
        directory = "/mnt/grobotextdat/userdata" #This is the main external directory associated with USB
        if os.path.isdir(directory) == True: #check if exist
            pass #if it is pass
        else: #if not return error to force a code restart
            raise RuntimeError('FILE IO FAIL')

        #Debug message
        print('logoutput-logtofile: Purging old logs') if debugstate == 1 or debugstate == 2 else None

        #Now run the log output using subprocess
        #This runs journalctl and force overwrite the output to the specified logfile.log using >|
        #We use shell=True to specify using system shell so the wildcard >| can be used
        #Here the -r flag is used so most recent is on top as in terminal recent on bottom is more convenient but a file open top down
        #while terminal stops at bottom so when writing to file makes the top the most recent entry
        subprocess.run('echo grobot | sudo -S journalctl --vacuum-time=30d', shell=True) #Added a vacuum code to make sure that logs older than 30 days are vacuum as they are so old they are useless
        
        #Debug message
        print('logoutput-logtofile: Writing log to file') if debugstate == 1 or debugstate == 2 else None
        
        subprocess.run('journalctl -u grobot.service -n 1000000000 -r --no-pager >| /mnt/grobotextdat/userdata/logfile.log', shell=True)

        #Debug message
        print('logoutput-logtofile: Log output to file completed') if debugstate == 1 or debugstate == 2 else None

        return 1
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None