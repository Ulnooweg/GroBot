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
from diopinsetup import diopinset
import subprocess
from config import readcsv_waterparam


##############################################
# Handle the pins definition and sensor definition
diop = diopinset()
s1, s2, s3, s4, s5, s6, b1, ths, sms, ina = diop[0], diop[1], diop[2], diop[3], diop[4], diop[5], diop[6], diop[7], diop[8], diop[9]

# Note, pump circuit usually s1

def wateringwithlogic(timetowater): #Define a func that handles the run-dry detection logic

    ##### FOR CHIRS - TO DO #####
    #Should take timetowater as an input time to turn pump on in seconds
    #if there is no water skips watering and returns 2, if there is water water for timetowater seconds and return 1
    ##### FOR CHIRS - TO DO #####

    # Define parameters used in logical calculation
    pumpTime = float(readcsv_waterparam('pumpTime'))
    settleTime = float(readcsv_waterparam('settleTime'))
    sampleRate = float(readcsv_waterparam('sampleRate'))
    filterWindowSize = float(readcsv_waterparam('filterWindowSize'))
    filterStartVal = float(readcsv_waterparam('filterStartVal'))
    P_dry = (float(readcsv_waterparam('P_dry_1')), float(readcsv_waterparam('P_dry_2')))
    t_rampUp = float(readcsv_waterparam('t_rampUp'))
    adc2volts = 3.30 / 65536 #A constant

    sampleTime = 1/sampleRate #Calculate some parameters from defined parameters

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

    powerFilter = MovingMax(filterWindowSize)

def autorain(mmrain):  # define autorain func with mm of water input as mm
    try:  # check water level
        currsenspresent = False #Set the flag current sensor present default to false
        # First check if the INA219 high side current sensor exists and is plugged in, if not skip the water level check
        gbcsresult = subprocess.run(['i2cget', '-y', '1', '0x40'], capture_output=True) #run i2cget to check if current sensor exists or not and use capture_output = True to capture output into gbcsresult for processing
        #i2cget -y skips interactive mode, using the i2c bus "1" reads value from device at 0x40 address (current sensor), errors on not exists
        match gbcsresult.returncode: #match the return code with expected value
            case 0: #return code = 0 means successful execution
                currsenspresent = True #There is a current sensor
            case 2:  #Return code 2 is associated with Error: Read failed
                currsenspresent = False #There is no current sensor
            case _: #Any other case should raise an error
                raise RuntimeError('CURRENT SENSOR CHECK ERROR - NON STANDARD RETURN CODE') #If there is no proper match, raise an error

        # Calculations based on 28.5 mL/s of water through the squid yielding 60.0 mL of water delivered per millilitre of rain
        #Based on current growing area X-sec area and related calcs

        mmrate = 2.11  # rate of watering in seconds/mm_Water
        t = mmrain*mmrate  # time required to water in seconds
        if currsenspresent == True: #If current sensor is present hand over watering to wateringwithlogic to integrate run-dry detection with watering
            wateringwithlogic(t) #Hand off time to water variable
        elif currsenspresent == False: #If no current sensor present use the standard logic and don't check water level, simply turns pump on or off
            s1.value = True  # turns on pump
            time.sleep(t)  # sleep for t seconds while pump is on
            s1.value = False  # turns off pump
        else:
            raise RuntimeError('CURRENT SENSOR PRESENT VALUE NOT LOGICAL') #If currensoresent is neither true or false raise an error
        
        return 1
    
    except Exception as errvar:
        s1.value = False  # Make sure pump is off on error
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def startwater(): #define function to start watering indefinitely for manual control. MUST BE USED WITH stopwater at the end ALWAYS
    try:
        s1.value = True  # turns on pump
        return 1
    except Exception as errvar:
        s1.value = False  # Make sure pump is off on error
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None    

def stopwater():  # define function to stop watering
    try:
        s1.value = False  # turns off pump
        return 1
    except Exception as errvar:
        s1.value = False  # Make sure pump is off on error
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None