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
# This function controls watering
#V1.0.3
#
# This functions execute with desired volume if using autowater or desired mm of rain if using autorain
# returns 0 on failure, 1 on success, 2 on low water
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
    
    except:
        return 0


def stopwater():  # define function to stop watering
    try:
        s1.value = False  # turns off pump
        return 1
    except:
        return 0
