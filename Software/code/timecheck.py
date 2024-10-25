#Copyright 2023-2024 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: timecheck
#Version: 1.0.4
#Description: This function check if current time is between set time. It can handle time that crosses midnight
#Function: checktimebetween(starttime, endtime), check if current time falls between starttime and endtime and returns True/False
#Input: Start time and end time in proper time format by converting the tuple (hh,mm) using time(hh,mm) from datetime library
#Output: True or False
#Error Handling: Output to log/terminal. The logs text out to terminal is:
#                RuntimeError: TIME COMPARE FAILURE
#
########################################

#Module Imports
from datetime import datetime, time

##############################################

#Define a function to take in start and end time for comparison
def checktimebetween(starttime, endtime): #Define a function checktimebetween
    currtime = time(datetime.now().time().hour,datetime.now().time().minute) #Take current time hours and minutes using datetime and convert to proper time format
    if starttime < endtime: #Check if it is proper time as if starttime < endtime it does not cross midnight assuming 24 hr format
        if starttime <= currtime and currtime <= endtime: #If start do not cross midnight into end, simple check
            return True
        elif starttime > currtime or currtime > endtime: #Return false if time not within specified
            return False
        else:
            raise RuntimeError('TIME COMPARE FAILURE') #Raise error on failure
    elif starttime > endtime: #this condition is crossing midnight
        if starttime <= currtime and currtime <= time(23,59): #If curr time is before midnight check if after starttime
            return True
        elif time (0,0) <= currtime and currtime <= endtime: #If currtime after midnight check if before endtime
            return True
        elif starttime > currtime and currtime <= time(23,59):  #Check false condition
            return False
        elif time (0,0) <= currtime and currtime > endtime: #Check false condition
            return False
        else:
            raise RuntimeError('TIME COMPARE FAILURE') #Raise error on failure
    else:
        raise RuntimeError('TIME COMPARE FAILURE') #Raise error on failure