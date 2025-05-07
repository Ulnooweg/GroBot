#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: fancontrol
#Version: 2.0
#Description: This function controls the growth chamber fan
#Function: fanon(t), turns the fan on for time "t"
#          fanmanon(), turns on the fan indefinitely
#          fanoff(), turns the fan off
#Input: fanon(...) requires time to turn fan on inputted in numerical form; fanoff() do not requires input
#Output: NONE
#Error Handling: Standard UEC Error Handling V1
#
########################################
# MODULE IMPORTS
import time  # need time for sleep function
from diopinsetup import diopinset
import subprocess

##############################################
# Handle the pins definition and sensor definition
diop = diopinset()
s1, s2, s3, s4, s5, s6, b1, ths, sms = diop[0], diop[1], diop[2], diop[3], diop[4], diop[5], diop[6], diop[7], diop[8]

# Note, fan circuit usually s3

def fanon(t):  # define function to turn on fan for t seconds as input
    try:
        s3.value = True  # turns on fan
        time.sleep(t)  # sleep for t seconds while fan is on
        s3.value = False  # turns off fan
        return 1
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None
    
def fanmanon():  # define function to turn on fan indefinitely for manual control. MUST BE USED WITH fanoff at the end always
    try:
        s3.value = True  # turns on fan
        return 1
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def fanoff():  # define function to turn off fan
    try:
        s3.value = False  # turns off fan
        return 1
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None
