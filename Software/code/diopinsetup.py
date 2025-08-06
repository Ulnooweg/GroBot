#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: diopinsetup
#Version: 2.0
#Description: This function setup digital IO pins, their directions and sensor objects
#Function: diopinset(), setup digitalIO pins and sensors and return them as object when called
#Input: NONE
#Output: returns a tuple of pins s1 thru s6, temp/humidity sensor, and soil moisture sensor objects
#Error Handling: Standard UEC Error Handling V1
#
########################################
#MODULE IMPORTS
#BLINKA
import board
import busio
import digitalio

#ADDITIONAL BLINKA
import adafruit_ahtx0
from adafruit_seesaw.seesaw import Seesaw
from adafruit_ina219 import INA219

import subprocess

##############################################

def diopinset(): #define diopinset function that takes no arguments
    print("diopinset called")
    try: #set up try except so it it successful return 1, if not return 0
        #Begin by defining pins
        #For Blinka, the pins are defined as DXX
        pins = {
            'S1' : board.D13, #This is MOSFET control pin 1 (System 1). Other S pin controls n MOSFET.
            'S2' : board.D16, #DXX Corresponds to GPIO pins XX
            'S3' : board.D19,
            'QWIIC_SCL' : board.SCL, #Define I2C pin CLOCK, use board.SCL in pi
            'QWIIC_SDA' : board.SDA #Define I2C pin DATA, use board.SDA in pi
            }
        
        #Define a function to capture current pin state from system using subprocess and pinctrl
        #Step 1: Capture the result
        pinctrlresult_s1 = subprocess.run(['pinctrl', 'get', '13'], capture_output=True)
        pinctrlresult_s2 = subprocess.run(['pinctrl', 'get', '16'], capture_output=True)
        pinctrlresult_s3 = subprocess.run(['pinctrl', 'get', '19'], capture_output=True)
        #Step 2: Decode the result stdout and strip them of extra star/end empty space
        s1_stdout = pinctrlresult_s1.stdout.decode().strip()
        s2_stdout = pinctrlresult_s2.stdout.decode().strip()
        s3_stdout = pinctrlresult_s3.stdout.decode().strip()
        #Check, for each pin stdout, the current value and assign original value accordingly
        if "lo" in s1_stdout: 
            s1_ori_val = False #If lo = False
        elif "hi" in s1_stdout:
            s1_ori_val = True #If hi = True
        else:
            raise RuntimeError('DIOPIN Match failed')
        
        if "lo" in s2_stdout: 
            s2_ori_val = False #If lo = False
        elif "hi" in s2_stdout:
            s2_ori_val = True #If hi = True
        else:
            raise RuntimeError('DIOPIN Match failed')
        
        if "lo" in s3_stdout: 
            s3_ori_val = False #If lo = False
        elif "hi" in s3_stdout:
            s3_ori_val = True #If hi = True
        else:
            raise RuntimeError('DIOPIN Match failed')

        #Setup Actuator circuts
        s1 = digitalio.DigitalInOut(pins['S1'])
        s2 = digitalio.DigitalInOut(pins['S2'])
        s3 = digitalio.DigitalInOut(pins['S3'])
        s4 = 'NaN' #For compat
        s5 = 'NaN' #For compat
        s6 = 'NaN' #For compat
        b1 = 'NaN' #For compat

        s1.switch_to_output(s1_ori_val,digitalio.DriveMode.PUSH_PULL) #This instead use switch to output to switch to output while keeping the MOSFEt status as-is and doing push-pull all in one step
        s2.switch_to_output(s2_ori_val,digitalio.DriveMode.PUSH_PULL) #This instead use switch to output to switch to output while keeping the MOSFEt status as-is and doing push-pull all in one step
        s3.switch_to_output(s3_ori_val,digitalio.DriveMode.PUSH_PULL) #This instead use switch to output to switch to output while keeping the MOSFEt status as-is and doing push-pull all in one step
        
        #for s in [s1, s2, s3]:
        #    #original_val = s.value #Reads current value the pin is defined as. DOESN'T WORK ANYMORE AS digitalio.DigitalInOut reset pin state
        #    s.switch_to_output(original_val,digitalio.DriveMode.PUSH_PULL) #This instead use switch to output to switch to output while keeping the MOSFEt status as-is and doing push-pull all in one step

        #B1 by default of digitalIO is set up as an input to the code (read from pin)
        #so we do not need to set it up further

        # Setup QWIIC Bus  
        qwiic = busio.I2C(scl=pins['QWIIC_SCL'], sda=pins['QWIIC_SDA'])

        #Setup the required sensors
        ths = adafruit_ahtx0.AHTx0(qwiic) # Temperature & Humidity Sensor
        sms = Seesaw(qwiic, addr=0x36) # Soil Moisture Sensor

        #Now because the current sensor may not be present, check if it is. if it is not don't initialize it but set it as a dummy value
        currsenspresent = False #Set the flag current sensor present default to false
        # First check if the INA219 high side current sensor exists and is plugged in, if not skip the water level check
        gbcsresult = subprocess.run(['i2cget', '-y', '1', '0x40'], capture_output=True) #run i2cget to check if current sensor exists or not and use capture_output = True to capture output into gbcsresult for processing
        #i2cget -y skips interactive mode, using the i2c bus "1" reads value from device at 0x40 address (current sensor), errors on not exists
        match gbcsresult.returncode: #match the return code with expected value
            case 0: #return code = 0 means successful execution
                ina = INA219(qwiic) #There is a current sensor
            case 2:  #Return code 2 is associated with Error: Read failed
                ina = 'NaN' #There is no current sensor
            case _: #Any other case should raise an error
                raise RuntimeError('CURRENT SENSOR CHECK ERROR - NON STANDARD RETURN CODE') #If there is no proper match, raise an error

        return s1, s2, s3, s4, s5, s6, b1, ths, sms, ina #return the pins and sensors as tuple of objects
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None