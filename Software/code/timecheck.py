#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: timecheck
#Version: 2.0
#Description: This function check if current time is between set time. It can handle time that crosses midnight
#Function: checktimebetween(starttime, endtime), check if current time falls between starttime and endtime and returns True/False
#Input: Start time and end time in proper time format by converting the tuple (hh,mm) using time(hh,mm) from datetime library
#Output: True or False
#Error Handling: Standard UEC Error Handling V1
#
########################################

#Module Imports
from datetime import datetime, time
import subprocess
from multiprocessing import shared_memory

##############################################

#Define a function to take in start and end time for comparison
def checktimebetween(starttime, endtime): #Define a function checktimebetween
    try:
        #Read the debugstate for use as condition in printing debug statement
        ext_mem = shared_memory.SharedMemory(name='grobot_shared_mem')
        debugstate = ext_mem.buf[0]

        #Debug message
        print('timecheck-checktimebetween: Getting current time') if debugstate == 1 or debugstate == 2 else None

        currtime = time(datetime.now().time().hour,datetime.now().time().minute) #Take current time hours and minutes using datetime and convert to proper time format

        #Debug message
        print('timecheck-checktimebetween: Initialising time check logic') if debugstate == 1 or debugstate == 2 else None        
        
        if starttime < endtime: #Check if it is proper time as if starttime < endtime it does not cross midnight assuming 24 hr format
            if starttime <= currtime and currtime <= endtime: #If start do not cross midnight into end, simple check
                #Debug message
                print('timecheck-checktimebetween: Time check succeeded') if debugstate == 1 or debugstate == 2 else None
                return True
            elif starttime > currtime or currtime > endtime: #Return false if time not within specified
                #Debug message
                print('timecheck-checktimebetween: Time check succeeded') if debugstate == 1 or debugstate == 2 else None
                return False
            else:
                raise RuntimeError('TIME COMPARE FAILURE') #Raise error on failure
        elif starttime > endtime: #this condition is crossing midnight
            if starttime <= currtime and currtime <= time(23,59): #If curr time is before midnight check if after starttime
                #Debug message
                print('timecheck-checktimebetween: Time check succeeded') if debugstate == 1 or debugstate == 2 else None
                return True
            elif time (0,0) <= currtime and currtime <= endtime: #If currtime after midnight check if before endtime
                #Debug message
                print('timecheck-checktimebetween: Time check succeeded') if debugstate == 1 or debugstate == 2 else None
                return True
            elif starttime > currtime and currtime <= time(23,59):  #Check false condition
                #Debug message
                print('timecheck-checktimebetween: Time check succeeded') if debugstate == 1 or debugstate == 2 else None
                return False
            elif time (0,0) <= currtime and currtime > endtime: #Check false condition
                #Debug message
                print('timecheck-checktimebetween: Time check succeeded') if debugstate == 1 or debugstate == 2 else None
                return False
            else:
                raise RuntimeError('TIME COMPARE FAILURE') #Raise error on failure
        else:
            raise RuntimeError('TIME COMPARE FAILURE') #Raise error on failure

    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None