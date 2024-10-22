#Copyright 2023-2024 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/TNarakol-UEC/GroBot
#
########################################
#
#Contact: engineering@ulnooweg.ca
#Growth Enclosure 
#
#This function check if current time is between set time
#V1.0.3
#
#This functions execute with inputs start and end time. It can also handle time that crosses midnight
#returns True on current time in range, False on out of range
#Note: The time start and end input must be converted from tuple using time(hh,mm) outside the function first
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