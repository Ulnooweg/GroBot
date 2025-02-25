#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: main
#Version: 1.2
#Description: This is the main function that's ran by systemd grobot service.
#Function: No callable function by itself but handles all the calling of other function and the main loop of GroBot. Consult Info.md for more information
#Input: NONE
#Output: NONE
#Error Handling: Standard UEC Error Handling V1
#
########################################
#Logging, immediately import the logging function and push it to file
from logoutput import logtofile
try:
    logtofile() #Write log to file immediately after boot in case needed for debugging
except Exception as errvar:
    raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

#MODULE IMPORTS
from datetime import time, datetime
import time as time2 #We already import time from datetime so time library is imported as time2
import threading
import sys
import subprocess

#Submodules import, these require files to be present in local dir
from BoardMOSFETReset import grobotboot
from sensorfeed import feedread
from watercontrol import autorain
from fancontrol import fanon
from lightcontrol import growlighton, growlightoff
from grobotpicam import picam_capture
from dataout import excelout
from timecheck import checktimebetween
from config import get_plant_settings, readcsv_mainflags, writecsv_mainflags
from lcddispfunc import lcd_menu_thread, set_lcd_color

##############################################
################# ON BOOTUP ##################
##############################################

try:
    #Suppress traceback for cleaner error log
    sys.tracebacklimit = 0

    #Runs BoardMostfetReset
    grobotboot() #This force all pin reset

    # This only initialize once on bootup
    set_lcd_color("normal")  # Set LCD color to green on bootup

    # Start the LCD menu thread immediately
    lcd_thread = threading.Thread(target=lcd_menu_thread)
    lcd_thread.daemon = True #Set the thread as a daemon so main can exit without waiting for lcddisp to quit first, and lcddisp exits when main exits.
    lcd_thread.start()
except Exception as errvar:
    subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
    set_lcd_color("error")
    raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

# Starts with reading values from sensor
try:
    ReadVal = feedread() # T RH SRH in order
    
    # Now do an initial read of the configuration value
    settings = get_plant_settings()

    # Now check if light needs to be on or off
    if checktimebetween(time(settings['sunrise'][0], settings['sunrise'][1]), time(settings['sunset'][0], settings['sunset'][1])) == True:
        growlighton()
    elif checktimebetween(time(settings['sunrise'][0], settings['sunrise'][1]), time(settings['sunset'][0], settings['sunset'][1])) == False:
        growlightoff()
    else:
        raise RuntimeError('UNKNOWN FAILURE')

    # Check if internal humidity or temperature is too high and the fan needs to be on
    if ReadVal[0] > settings['maxTemp'] or ReadVal[1] > settings['maxHumid']:
        fanon(settings['fanTime'])
    elif ReadVal[0] <= settings['maxTemp'] and ReadVal[1] <= settings['maxHumid']:
        pass
    else:
        raise RuntimeError('UNKNOWN FAILURE')

except Exception as errvar:
    subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
    set_lcd_color("error")
    raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

##############################################
##############   SCHEDULED CODE   ############
##############################################

def EveryXX15(): # This schedule grouping runs at every quarter of hour
    try:
        settings = get_plant_settings()
        set_lcd_color("in_progress")  # Set LCD color to blue when in progress

        # This should read value from sensor and turn fan on or off
        # Read value from sensor
        ReadVal = feedread() # T RH SRH in order

        # Turn on fan if temp or humidity exceeds the limit 
        if ReadVal[0] > settings['maxTemp'] or ReadVal[1] > settings['maxHumid']:
            fanon(settings['fanTime'])
        elif ReadVal[0] <= settings['maxTemp'] and ReadVal[1] <= settings['maxHumid']:
            pass
        else:
            raise RuntimeError('UKNOWN FAILURE')
        
        writecsv_mainflags("EveryXX15","0") #Set the execution flag for the function back to 0
        set_lcd_color("normal")  # Set LCD color to green when done

    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def EverySETTIME(): # This runs every settime read from grobot_cfg
    try:
        settings = get_plant_settings()
        set_lcd_color("in_progress")  # Set LCD color to blue when in progress

        # This should read value from sensor and autorain if Soil moisture too low
        # Read value from sensor
        ReadVal = feedread() # T RH SRH in order

        # Now water plant if soil too dry
        if ReadVal[2] <= settings['dryValue']:
            autorain(settings['waterVol'])
        elif ReadVal[2] > settings['dryValue']:
            pass
        else:
            raise RuntimeError('UKNOWN FAILURE')
        
        writecsv_mainflags("EverySETTIME","0") #Set the execution flag for the function back to 0
        set_lcd_color("normal")  # Set LCD color to green when done

    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def EveryXX25(): # This code runs at every 25 minute mark of the hour
    try:
        set_lcd_color("in_progress")  # Set LCD color to blue when in progress
        # Read value from sensor and write it out to excel
        # Read value from sensor
        ReadVal = feedread() # T RH SRH in order
        # Write data out to excel file
        excelout(ReadVal[0], ReadVal[1], ReadVal[2])

        writecsv_mainflags("EveryXX25","0") #Set the execution flag for the function back to 0
        set_lcd_color("normal")  # Set LCD color to green when done

    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def EveryXX35(): # Runs every 35 minute mark of the hour
    try:
        set_lcd_color("in_progress")  # Set LCD color to blue when in progress
        picam_capture() # Take picture with pi camera

        writecsv_mainflags("EveryXX35","0") #Set the execution flag for the function back to 0
        set_lcd_color("normal")  # Set LCD color to green when done

    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def EverySUNRISE(): # This should run every sunrise time to turn on the light
    try:
        set_lcd_color("in_progress")  # Set LCD color to blue when in progress
        growlighton()

        writecsv_mainflags("EverySUNRISE","0") #Set the execution flag for the function back to 0
        set_lcd_color("normal")  # Set LCD color to green when done

    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def EverySUNSET(): # This should run every sunset time to turn off light
    try:
        set_lcd_color("in_progress")  # Set LCD color to blue when in progress
        growlightoff()

        writecsv_mainflags("EverySUNSET","0") #Set the execution flag for the function back to 0
        set_lcd_color("normal")  # Set LCD color to green when done

    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

# Multithreading
def run_threaded(job_func): #Function that runs a given function input in a new thread using threading module
    try:
        #First, define job_thread object as a threading class targeting job_func function passed in
        #while also setting the thread name to be the same as job_func using __name__ attribute
        #Also want daemon=True so it does not block main from quitting and will exits if main no longer runs
        job_thread = threading.Thread(target=job_func,name=str(job_func.__name__),daemon=True)

        runthread_flag = True #set the default value of flag use to signal if thread should be ran to True as default
        #Now must check if a thread with the same name is already running using enumerate logic
        for i in threading.enumerate(): #Use enumerate to list all currently running thread
            if i.name == job_func.__name__:
                runthread_flag = False #if the name of any running thread matched the name of job_func passed in, set the flag to false
            else:
                pass #Do nothing and keep running flag to true if name doesn't match
        
        #Now check the flag and start the thread if the flag is True
        if runthread_flag == True:
            job_thread.start() #If nothing match, start the thread as normal
        elif runthread_flag == False:
            pass #Do not start the thread if the flag is false.
        else: #If there's an error
            raise RuntimeError('THREAD FLAG NOT BOOLEAN')
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

# This is now the main running thread, one while loop that spawns subthreads as needed.
while 1:
    try: #Put the entire try block under while loop. VERY IMPORTANT while must be the top level or it won't loop properly all the time
        settings = get_plant_settings() #Get plant settings so we have the proper set time to compare current time to

        #Get current time and put its component in separate variables
        currhour = datetime.now().hour
        currminute = datetime.now().minute
        currsecond = datetime.now().second

        #currtime = [datetime.now().hour, datetime.now().minute, datetime.now().second] #combine the variable together, not needed anymore

        # Now write the code to set execution flag for the appropriate function in mainflags file to 1 if the appropriate time is
        # reached such that the fuction will later be executed when mainflags is read back.
        # The first case only match function for minutes
        match currminute:
            case 15:
                writecsv_mainflags("EveryXX15","1")
            case 25:
                writecsv_mainflags("EveryXX25","1")
            case 35:
                run_threaded(logtofile) #Write log immediately every 35 minutes
                writecsv_mainflags("EveryXX35","1")
            case _:
                pass
        
        # This one requires matching both hour and minute
        if currhour == settings['sunset'][0] and currminute == settings['sunset'][1]:
            writecsv_mainflags("EverySUNSET","1")
        if currhour == settings['sunrise'][0] and currminute == settings['sunrise'][1]:
            writecsv_mainflags("EverySUNRISE","1")
        if currhour == settings['checkTime'][0] and currminute == settings['checkTime'][1]:
            writecsv_mainflags("EverySETTIME","1")

        # Now, read the mainflags file and execute any function that has its execution value = 1.
        # Make a list of functions. Need to use the actual function object such that they can be called later
        funcexecnamelist = [EveryXX15, EverySETTIME, EveryXX25, EveryXX35, EverySUNRISE, EverySUNSET]
        for funcexecname in funcexecnamelist: #iterate through the list funcexecnamelist using variable funcexecname
            tempflagvalue = readcsv_mainflags(str(funcexecname.__name__)) #Read flag value for current function from csv
            if tempflagvalue == '1': #Check if flag value corresponding to function name provided by funcexecname variable match 1, if it does start the thread
                run_threaded(funcexecname)
            elif tempflagvalue == '0':
                pass
            else:
                raise RuntimeError('FUNCTION EXEC FLAG COMPARISON ERROR')

        #Implement logic to sleep until next tick
        currtickminute = datetime.now().minute

        if currtickminute == currminute: #If we are still in the same minute as initial time check, sleep until minute change
            currticksecond = datetime.now().second #get current second
            tsleep = 61 - currticksecond #subtract current second from 61 to get seconds to sleep until next min
            time2.sleep(tsleep)
        elif currtickminute > currminute: #Immediately rerun loop if current tick is larger than initial time set during update
            pass
        else:
            raise RuntimeError('TIME EXCEPTION') #Time anomaly

    except Exception as errvar: #Catch any while loop exception
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None
