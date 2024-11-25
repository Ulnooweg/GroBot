#Copyright 2023-2024 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: watercontrol
#Version: 1.1
#Description: This function controls watering
#Function: autorain(mmrain), turns on the pump for a time such that the water delivered is "mmrain" mm of rain
#          stopwater(), turns of the pump upon being called
#Input: autorain(...) requires mmrain as a numerical input, stopwater() requires no input
#Output: NONE
#Error Handling: Standard UEC Error Handling V1
#
#POST-SCRIPT: Water level check in autorain is currently turned off pending further investigation to make it more consistent.
#
########################################
# MODULE IMPORTS
import time  # need time for sleep function
from diopinsetup import diopinset

##############################################
# Handle the pins definition and sensor definition
diop = diopinset()
s1, s2, s3, s4, s5, s6, b1, ths, sms = diop[0], diop[1], diop[2], diop[3], diop[4], diop[5], diop[6], diop[7], diop[8]

# Note, pump circuit usually s1

def autorain(mmrain):  # define autorain func with mm of water input as mm
    try:  # check water level
        # Note that the float switch's reed switch is open in the bottom float position (low water) and closed when in the top position (high water)
        # Note that b1 (GPIO10 / Pin 19) is set with a pull-up resistor

        #### REQUIRES FURTHER INVESTIGATION - NOT WORKING CONSISTENTLY ####

        #if b1.value == False:
        #    pass 
        #elif b1.value == True:  # if the water level is low
        #    return 2
        #else:
        #    return 0
    
        ###################

        # Calculations based on 28.5 mL/s of water through the squid yielding 60.0 mL of water delivered per millilitre of rain
        #Based on current growing area X-sec area and related calcs

        mmrate = 2.11  # rate of watering in seconds/mm_Water
        t = mmrain*mmrate  # time required to water in seconds
        s1.value = True  # turns on pump
        time.sleep(t)  # sleep for t seconds while pump is on
        s1.value = False  # turns off pump
        return 1
    
    except Exception as errvar:
        s1.value = False  # Make sure pump is off on error
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None


def stopwater():  # define function to stop watering
    try:
        s1.value = False  # turns off pump
        return 1
    except Exception as errvar:
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def test_status_light():
    """Simple test function for status light"""
    print("Testing status light...")
    lcddispfunc.display_status("Test action...", action=True)
    time.sleep(3)  # Wait 3 seconds
    lcddispfunc.clear_action_status()
    print("Test complete - light should be white now")

# Run test with:
# python3 -c "import watercontrol; watercontrol.test_status_light()"
