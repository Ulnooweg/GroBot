#Copyright 2023-2024 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: main
#Version: 1.0.4
#Description: This is the main function that's ran by systemd grobot service.
#Function: No callable function by itself but handles all the calling of other function and the main loop of GroBot. Consult Info.md for more information
#Input: NONE
#Output: NONE
#Error Handling: Built-in, output to log/terminal. The logs text out to terminal is:
#                RuntimeError: SENSOR FAIL
#                RuntimeError: UKNOWN FAILURE
#                RuntimeError: LIGHT FAIL
#                RuntimeError
#                RuntimeError: WATER FAIL
#                RuntimeError: DATAOUT FAIL
#                RuntimeError: PICAMERA FAIL
#                RuntimeError: TIME EXCEPTION
#
########################################
#MODULE IMPORTS
from datetime import time, datetime
import time as time2 #We already import time from datetime so time library is imported as time2
import threading

#Submodules import, these require files to be present in local dir
from BoardMOSFETReset import grobotboot
from sensorfeed import feedread
from watercontrol import autorain
from fancontrol import fanon
from lightcontrol import growlighton, growlightoff
from picamera import picam_capture
from dataout import excelout
from timecheck import checktimebetween
from config import get_plant_settings
from lcddispfunc import lcd_menu_thread, set_lcd_color

##############################################
################# ON BOOTUP ##################
##############################################

#Runs BoardMostfetReset
grobotboot() #This force all pin reset

# This only initialize once on bootup
set_lcd_color("normal")  # Set LCD color to green on bootup

# Start the LCD menu thread immediately
lcd_thread = threading.Thread(target=lcd_menu_thread)
lcd_thread.daemon = True
lcd_thread.start()

# Starts with reading values from sensor
try:
    ReadVal = feedread() # T RH SRH in order
    if isinstance(ReadVal, tuple) == True: # Check if there is an actual value from feedread
        pass
    elif ReadVal == 0: # If returns 0 there is a failure in feedread
        set_lcd_color("error")  # Set LCD color to red on error
        raise RuntimeError('SENSOR FAIL') # Force code to quit and systemd will force it to restart
    else: # For any unknown error
        set_lcd_color("error")  # Set LCD color to red on error
        raise RuntimeError('UKNOWN FAILURE')
    
    # Now do an initial read of the configuration value
    settings = get_plant_settings()

    # Now check if light needs to be on or off
    if checktimebetween(time(settings['sunrise'][0], settings['sunrise'][1]), time(settings['sunset'][0], settings['sunset'][1])) == True:
        grstatus = growlighton()
        if grstatus == 1:
            pass
        elif grstatus == 0:
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('LIGHT FAIL') # Force code to quit and systemd will force it to restart
        else: # For any unknown error
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('UKNOWN FAILURE')
    elif checktimebetween(time(settings['sunrise'][0], settings['sunrise'][1]), time(settings['sunset'][0], settings['sunset'][1])) == False:
        grstatus = growlightoff()
        if grstatus == 1:
            pass
        elif grstatus == 0:
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('LIGHT FAIL') # Force code to quit and systemd will force it to restart
        else: # For any unknown error
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('UKNOWN FAILURE')
    else:
        set_lcd_color("error")  # Set LCD color to red on error
        raise RuntimeError('UKNOWN FAILURE')

    # Check if internal humidity or temperature is too high and the fan needs to be on
    if ReadVal[0] > settings['maxTemp'] or ReadVal[1] > settings['maxHumid']:
        fanstatus = fanon(settings['fanTime'])
        if fanstatus == 1:
            pass
        elif fanstatus == 0:
            set_lcd_color("error")  # Set LCD color to red on error
            pass
        else:
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('UKNOWN FAILURE')
    elif ReadVal[0] <= settings['maxTemp'] and ReadVal[1] <= settings['maxHumid']:
        pass
    else:
        set_lcd_color("error")  # Set LCD color to red on error
        raise RuntimeError('UKNOWN FAILURE')

except RuntimeError as e:
    set_lcd_color("error")  # Set LCD color to red on error
    raise e

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
        if isinstance(ReadVal, tuple) == True: # Check if there is an actual value from feedread
            pass
        elif ReadVal == 0: # If returns 0 there is a failure in feedread
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('SENSOR FAIL') # Force code to quit and systemd will force it to restart
        else: # For any unknown error
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('UKNOWN FAILURE')

        # Turn on fan if temp or humidity exceeds the limit 
        if ReadVal[0] > settings['maxTemp'] or ReadVal[1] > settings['maxHumid']:
            fanstatus = fanon(settings['fanTime'])
            if fanstatus == 1:
                pass
            elif fanstatus == 0:
                set_lcd_color("error")  # Set LCD color to red on error
                pass
            else:
                set_lcd_color("error")  # Set LCD color to red on error
                raise RuntimeError('UKNOWN FAILURE')
        elif ReadVal[0] <= settings['maxTemp'] and ReadVal[1] <= settings['maxHumid']:
            pass
        else:
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('UKNOWN FAILURE')

        set_lcd_color("normal")  # Set LCD color to green when done

    except RuntimeError as e:
        set_lcd_color("error")  # Set LCD color to red on error
        raise e

def EverySETTIME(): # This runs every settime read from grobot_cfg
    try:
        settings = get_plant_settings()
        set_lcd_color("in_progress")  # Set LCD color to blue when in progress

        # This should read value from sensor and autorain if Soil moisture too low
        # Read value from sensor
        ReadVal = feedread() # T RH SRH in order
        if isinstance(ReadVal, tuple) == True: # Check if there is an actual value from feedread
            pass
        elif ReadVal == 0: # If returns 0 there is a failure in feedread
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('SENSOR FAIL') # Force code to quit and systemd will force it to restart
        else: # For any unknown error
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('UKNOWN FAILURE')

        # Now water plant if soil too dry
        if ReadVal[2] <= settings['dryValue']:
            wtrstatus = autorain(settings['waterVol'])
            if wtrstatus == 1:
                pass
            elif wtrstatus == 2:        # Low water level
                set_lcd_color("error")  # Set LCD color to red on error
                pass
            elif wtrstatus == 0:
                set_lcd_color("error")  # Set LCD color to red on error
                raise RuntimeError('WATER FAIL')
            else:
                set_lcd_color("error")  # Set LCD color to red on error
                raise RuntimeError('UKNOWN FAILURE')
        elif ReadVal[2] > settings['dryValue']:
            pass
        else:
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('UKNOWN FAILURE')

        set_lcd_color("normal")  # Set LCD color to green when done

    except RuntimeError as e:
        set_lcd_color("error")  # Set LCD color to red on error
        raise e

def EveryXX25(): # This code runs at every 25 minute mark of the hour
    try:
        set_lcd_color("in_progress")  # Set LCD color to blue when in progress

        # Read value from sensor and write it out to excel
        # Read value from sensor
        ReadVal = feedread() # T RH SRH in order
        if isinstance(ReadVal, tuple) == True: # Check if there is an actual value from feedread
            pass
        elif ReadVal == 0: # If returns 0 there is a failure in feedread
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('SENSOR FAIL') # Force code to quit and systemd will force it to restart
        else: # For any unknown error
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('UKNOWN FAILURE')

        # Write data out to excel file
        excelstatus = excelout(ReadVal[0], ReadVal[1], ReadVal[2])
        if excelstatus == 1:
            pass
        elif excelstatus == 2:      #Alternative directory used
            set_lcd_color("error")  # Set LCD color to red on error
            pass
        elif excelstatus == 0:
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('DATAOUT FAIL')
        else: # For any unknown error
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('UKNOWN FAILURE')

        set_lcd_color("normal")  # Set LCD color to green when done

    except RuntimeError as e:
        set_lcd_color("error")  # Set LCD color to red on error
        raise e

def EveryXX35(): # Runs every 35 minute mark of the hour
    try:
        set_lcd_color("in_progress")  # Set LCD color to blue when in progress

        # Take picture with pi camera
        pcamstatus = picam_capture()
        if pcamstatus == 1:
            pass
        elif pcamstatus == 2:       #Alternate directory used
            set_lcd_color("error")  # Set LCD color to red on error
            pass
        elif pcamstatus == 0:
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('PICAMERA FAIL')
        else: # For any unknown error
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('UKNOWN FAILURE')

        set_lcd_color("normal")  # Set LCD color to green when done

    except RuntimeError as e:
        set_lcd_color("error")  # Set LCD color to red on error
        raise e

def EverySUNRISE(): # This should run every sunrise time to turn on the light
    try:
        set_lcd_color("in_progress")  # Set LCD color to blue when in progress

        grstatus = growlighton()
        if grstatus == 1:
            pass
        elif grstatus == 0:
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('LIGHT FAIL') # Force code to quit and systemd will force it to restart
        else: # For any unknown error
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('UKNOWN FAILURE')

        set_lcd_color("normal")  # Set LCD color to green when done

    except RuntimeError as e:
        set_lcd_color("error")  # Set LCD color to red on error
        raise e

def EverySUNSET(): # This should run every sunset time to turn off light
    try:
        set_lcd_color("in_progress")  # Set LCD color to blue when in progress

        grstatus = growlightoff()
        if grstatus == 1:
            pass
        elif grstatus == 0:
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('LIGHT FAIL') # Force code to quit and systemd will force it to restart
        else: # For any unknown error
            set_lcd_color("error")  # Set LCD color to red on error
            raise RuntimeError('UKNOWN FAILURE')

        set_lcd_color("normal")  # Set LCD color to green when done

    except RuntimeError as e:
        set_lcd_color("error")  # Set LCD color to red on error
        raise e

# Multithreading
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

# This is now the main running thread, one while loop that spawns subthreads as needed.
while 1:
    settings = get_plant_settings()
    currhour = datetime.now().hour
    currminute = datetime.now().minute
    currsecond = datetime.now().second

    currtime = [datetime.now().hour, datetime.now().minute, datetime.now().second]

    # The first case only match function for minutes
    match currminute:
        case 15:
            run_threaded(EveryXX15)
        case 25:
            run_threaded(EveryXX25)
        case 35:
            run_threaded(EveryXX35)
        case _:
            pass
    
    # This one requires matching both hour and minute
    if currhour == settings['sunset'][0] and currminute == settings['sunset'][1]:
        run_threaded(EverySUNSET)
    if currhour == settings['sunrise'][0] and currminute == settings['sunrise'][1]:
        run_threaded(EverySUNRISE)
    if currhour == settings['checkTime'][0] and currminute == settings['checkTime'][1]:
        run_threaded(EverySETTIME)

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
