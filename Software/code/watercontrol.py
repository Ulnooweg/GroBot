#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: watercontrol
#Version: 2.0
#Description: This function controls watering, including logic that monitor the current as read by the current sensor and detect 
#             whether or not the pump is pumping air too or not by measuring current, applying processing, and measure it against 
#             known current draw.
#Function: autorain(mmrain), turns on the pump for a time such that the water delivered is "mmrain" mm of rain
#          startwater(), turns on pump indefinitely after being called
#          stopwater(), turns off the pump upon being called
#          wateringwithlogic(), TBD
#Input: autorain(...) requires mmrain as a numerical input, stopwater() requires no input
#Output: NONE
#Error Handling: Standard UEC Error Handling V1
#
#POST-SCRIPT: Water level check in autorain is currently turned off pending further investigation to make it more consistent.
#
########################################
# MODULE IMPORTS
import time  # need time for sleep function
from time import sleep
from diopinsetup import diopinset
import subprocess
from config import readcsv_waterparam, writecsv_mainflags, readcsv_mainflags
from datetime import datetime
import csv
import os

##############################################
# Handle the pins definition and sensor definition
diop = diopinset()
s1, s2, s3, s4, s5, s6, b1, ths, sms, ina = diop[0], diop[1], diop[2], diop[3], diop[4], diop[5], diop[6], diop[7], diop[8], diop[9]

# Note, pump circuit usually s1

filterWindowSize = int(readcsv_waterparam('filterWindowSize'))

#Now define the filter as a class
class MovingMax:
    def __init__(self, window_size=20, startVal=0):
        """
        implements a moving-window maximum filter to detect peak current draw in a very noisy signal
        """
        self.window_size = window_size
        self.ring = [startVal] * window_size
        self.index = 0

    def update(self, newVal):
        self.ring[self.index] = newVal
        self.index += 1
        if self.index >= self.window_size:
            self.index = 0
        return max(self.ring)
    
currentFilter = MovingMax(10)

def wateringwithlogic(timetowater): #Define a func that handles the run-dry detection logic
    try:
        ##### FOR CHIRS - TO DO #####
        #Should take timetowater as an input time to turn pump on in seconds
        #if there is no water skips watering and returns 2, if there is water water for timetowater seconds and return 1
        ##### FOR CHIRS - TO DO #####
        # Define parameters used in logical calculation
        print("Watering with logic")
        samplerate = (1/32) # Seconds
        counter = 0 # Seconds
        # Amps = ina.current # Measured in milliamps
        # A_filtered = currentFilter.update(Amps)
        #writecsv_mainflags("PumpRunDry","0") # Case for new mainflag: 0 means pump resevoir is full, 1 means resevoir is dry
        s1.value = True # Enables Pump MOSFET   
        while s1.value == True: # If MOSFET S1 is enabled
            if counter < timetowater: # If the counter is less than the user specified time
                Amps = ina.current # Measured in milliamps
                A_filtered = currentFilter.update(Amps) # Filtered Current measured in milliamps
                #print(Amps, A_filtered) # Print the filtered and unfiltered current
                if counter > 0 and counter % 2 == 0: # if counter is divisible by 2 and leaves a remainder of 0
                    # print("Counter is divisible by 2")
                    # print(str(counter))
                    if A_filtered >= 350: # if the filtered current is greater than 350 mA
                        # print("Current is greater than 350 mA")
                        pass # Current is at normal levels for normal 
                    elif A_filtered < 350: # if the filtered current is less than 350 mA
                        s1.value = False # Turn off pump MOSFET
                        writecsv_mainflags("PumpRunDry","1") # Raise RunDry Flag
                        print("Pump is dry")
                        # print("MOSFET disabled due to dry resevoir")
                    else:
                        raise RuntimeError('CURRENT VALUE IS INVALID') # Current should be a logical value
                else:
                    # print("Counter is not divisible by 2")
                    # print(str(counter))
                    pass
                sleep(samplerate) # Sleep for the specified sample rate
                counter = counter + (samplerate) # Increment counter by one samplerate 
            else:
                print("Watering has ended") # 
                s1.value = False # Disable MOSFET
                break
    except Exception as errvar:
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

# Water cycle operation - when the pump runs dry, the current draw can trigger the dry pump flag shuting the pump down prematurely.
# When called, this function will cycle water through the pump until current reaches expected levels.

def pumprefillcycle():
    try:

        print("Cycling water through pump")
        samplerate = (1/32) # Seconds
        s1.value = True
        sleep(2)

        while s1.value == True: # If MOSFET S1 is enabled

            Amps = ina.current # Measured in milliamps
            A_filtered = currentFilter.update(Amps) # Filtered Current measured in milliamps

            if A_filtered < 350: # if the filtered current is greater than 350 mA

                #print(f"{A_filtered}, {Amps}") # DEBUGGERLINE
                sleep(samplerate) # Sleep for the specified sample rate

            elif A_filtered >= 350: # if the filtered current is less than 350 mA

                s1.value = False # Turn off pump MOSFET
                writecsv_mainflags("PumpRunDry","0") # Raise RunDry Flag
                print("Pump has cycled")

            else:

                raise RuntimeError('CURRENT VALUE IS INVALID') # Current should be a logical value
   
    except Exception as errvar:
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None
    

def autorain(mmrain):  # define autorain func with mm of water input as mm
    try:  # check water level
        # Calculations based on 28.5 mL/s of water through the squid yielding 60.0 mL of water delivered per millilitre of rain
        #Based on current growing area X-sec area and related calcs

        mmrate = 2.11  # rate of watering in seconds/mm_Water
        t = mmrain*mmrate  # time required to water in seconds
        PumpRunDry = int(readcsv_mainflags("PumpRunDry"))

        if PumpRunDry == 0:
            wateringwithlogic(t) #Hand off time to water variable

        elif PumpRunDry == 1:
            pass
        else:
            raise RuntimeError('INVALID RUNDRY FLAG')

    except Exception as errvar:
        s1.value = False  # Make sure pump is off on error
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

# Unused Pump Scripts

# def startwater(): #define function to start watering indefinitely for manual control. MUST BE USED WITH stopwater at the end ALWAYS
#     try:
#         s1.value = True
#         return 1
#     except Exception as errvar:
#         s1.value = False  # Make sure pump is off on error
#         subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
#         #LCD COLOUR HANDLING CODE (RED) HERE
#         raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None    

# def stopwater():  # define function to stop watering
#     try:
#         s1.value = False  # turns off pump
#         return 1
#     except Exception as errvar:
#         s1.value = False  # Make sure pump is off on error
#         subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
#         #LCD COLOUR HANDLING CODE (RED) HERE
#         raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None