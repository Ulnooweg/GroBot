#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under Québec Free and Open-Source Licence – Strong Reciprocity (LiLiQ-R+) Version 1.1
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
from multiprocessing import shared_memory
from time import sleep, monotonic
from diopinsetup import diopinset
import subprocess
from config import readcsv_waterparam, writecsv_mainflags, readcsv_mainflags

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
        #Read the debugstate for use as condition in printing debug statement
        ext_mem = shared_memory.SharedMemory(name='grobot_shared_mem')
        debugstate = ext_mem.buf[0]

        #Debug message
        print('watercontrol-wateringwithlogic: Defining parameters') if debugstate == 1 or debugstate == 2 else None

        # Define parameters used in logical calculation
        samplerate = (1/32) # Seconds
        counter = 0 # Seconds

        #Debug message
        print('watercontrol-wateringwithlogic: Starting watering routine') if debugstate == 1 or debugstate == 2 else None

        s1.value = True # Enables Pump MOSFET   
        while s1.value == True: # If MOSFET S1 is enabled
            if counter < timetowater: # If the counter is less than the user specified time
                Amps = ina.current # Measured in milliamps
                A_filtered = currentFilter.update(Amps) # Filtered Current measured in milliamps
                #Debug message
                print(f"watercontrol-wateringwithlogic: At time {counter} of {timetowater} Amps = {Amps} mA, A_filtered ={A_filtered} mA") if debugstate == 1 or debugstate == 2 else None
                if counter > 0 and counter % 2 == 0: # if counter is divisible by 2 and leaves a remainder of 0
                    #Debug message
                    print(f"watercontrol-wateringwithlogic: Counter of {counter} is divisible by 2") if debugstate == 1 or debugstate == 2 else None
                    if A_filtered >= 350: # if the filtered current is greater than 350 mA
                        #Debug message
                        print(f"watercontrol-wateringwithlogic: A_filtered of {A_filtered} >= 350 mA, water level OK, continuing") if debugstate == 1 or debugstate == 2 else None
                        pass # Current is at normal levels for normal 
                    elif A_filtered < 350: # if the filtered current is less than 350 mA
                        #Debug message
                        print(f"watercontrol-wateringwithlogic: A_filtered of {A_filtered} < 350 mA, pump dry, stopping") if debugstate == 1 or debugstate == 2 else None
                        s1.value = False # Turn off pump MOSFET
                        writecsv_mainflags("PumpRunDry","1") # Raise RunDry Flag
                    else:
                        raise RuntimeError('CURRENT VALUE IS INVALID') # Current should be a logical value
                else:
                    #Debug message
                    print(f"watercontrol-wateringwithlogic: Counter of {counter} is not divisible by 2") if debugstate == 1 or debugstate == 2 else None
                    pass
                sleep(samplerate) # Sleep for the specified sample rate
                counter = counter + (samplerate) # Increment counter by one samplerate 
            else:
                #Debug message
                print(f"watercontrol-wateringwithlogic: At time {counter} of {timetowater} watering completed") if debugstate == 1 or debugstate == 2 else None
                s1.value = False # Disable MOSFET
                break
    except Exception as errvar:
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

# Water cycle operation - when the pump runs dry, the current draw can trigger the dry pump flag shuting the pump down prematurely.
# When called, this function will cycle water through the pump until current reaches expected levels.

def pumprefillcycle():
    try:
        #Read the debugstate for use as condition in printing debug statement
        ext_mem = shared_memory.SharedMemory(name='grobot_shared_mem')
        debugstate = ext_mem.buf[0]

        #Debug message
        print('watercontrol-pumprefillcycle: Defining variables') if debugstate == 1 or debugstate == 2 else None

        samplerate = (1/32) # Seconds
        s1.value = True
        sleep(2)
        pumprefillcycle_timestart = monotonic(); #The start time recorded using monotonic clock
        while s1.value == True: # If MOSFET S1 is enabled

            #Debug message
            print('watercontrol-pumprefillcycle: Engaging current measurements') if debugstate == 1 or debugstate == 2 else None

            Amps = ina.current # Measured in milliamps
            A_filtered = currentFilter.update(Amps) # Filtered Current measured in milliamps
            pumprefillcycle_timediff = monotonic() - pumprefillcycle_timestart #Calculate time difference
            #Debug message
            print(f"watercontrol-pumprefillcycle: Time elapsed = {pumprefillcycle_timediff} seconds") if debugstate == 1 or debugstate == 2 else None

            if pumprefillcycle_timediff > 10: #Set an exit condition if time spent is greater than 10 seconds
                #Debug message
                print(f"watercontrol-pumprefillcycle: Time elapsed of {pumprefillcycle_timediff} exceeds 10s limit. Turning off pump and marking it as dry.") if debugstate == 1 or debugstate == 2 else None
                s1.value = False # Turn off pump MOSFET
                writecsv_mainflags("PumpRunDry","1") # Write RunDry Flag back to 1 if time runs out and current value still too low

            elif A_filtered < 350 and pumprefillcycle_timediff <= 10: # if the filtered current is less than 350 mA
                #Debug message
                print(f"watercontrol-pumprefillcycle: Amps = {Amps} mA, A_filtered = {A_filtered} mA") if debugstate == 1 or debugstate == 2 else None
                print(f"watercontrol-pumprefillcycle: Current value too low, sleeping for {samplerate} seconds") if debugstate == 1 or debugstate == 2 else None

                sleep(samplerate) # Sleep for the specified sample rate

            elif A_filtered >= 350 and pumprefillcycle_timediff <= 10: # if the filtered current is greater than 350 mA
                #Debug message
                print('watercontrol-pumprefillcycle: Current OK, turning off pump') if debugstate == 1 or debugstate == 2 else None

                s1.value = False # Turn off pump MOSFET
                writecsv_mainflags("PumpRunDry","0") # Write RunDry Flag back to 0

            else:
                raise RuntimeError('CURRENT OR TIME VALUE IS INVALID') # Current should be a logical value
            
        #Debug message
        print('watercontrol-pumprefillcycle: Pump cycling completed') if debugstate == 1 or debugstate == 2 else None
   
    except Exception as errvar:
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None
    

def autorain(mmrain):  # define autorain func with mm of water input as mm
    try:  # check water level
        #Read the debugstate for use as condition in printing debug statement
        ext_mem = shared_memory.SharedMemory(name='grobot_shared_mem')
        debugstate = ext_mem.buf[0]

        #Debug message
        print('watercontrol-autorain: Processing autorain parameters') if debugstate == 1 or debugstate == 2 else None

        # Calculations based on 28.5 mL/s of water through the squid yielding 60.0 mL of water delivered per millilitre of rain
        #Based on current growing area X-sec area and related calcs

        mmrate = 2.11  # rate of watering in seconds/mm_Water
        t = mmrain*mmrate  # time required to water in seconds

        #Debug message
        print('watercontrol-autorain: Reading current pump dryness status') if debugstate == 1 or debugstate == 2 else None

        PumpRunDry = int(readcsv_mainflags("PumpRunDry"))

        if PumpRunDry == 0:
            #Debug message
            print('watercontrol-autorain: Engaging logic-controlled watering') if debugstate == 1 or debugstate == 2 else None

            wateringwithlogic(t) #Hand off time to water variable

        elif PumpRunDry == 1:
            #Debug message
            print('watercontrol-autorain: Pump dry - skipping') if debugstate == 1 or debugstate == 2 else None
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