#Copyright 2023-2024 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: fancontrol
#Version: 1.0.4
#Description: This function controls the growth chamber fan
#Function: fanon(t), turns the fan on for time "t"
#          fanoff(), turns the fan off
#Input: fanon(...) requires time to turn fan on inputted in numerical form; fanoff() do not requires input
#Output: NONE
#Error Handling: returns 0 on failure, 1 on success
#
########################################
# MODULE IMPORTS
import time  # need time for sleep function
from diopinsetup import diopinset

##############################################
# Handle the pins definition and sensor definition
diop = diopinset()
s1, s2, s3, s4, s5, s6, b1, ths, sms = diop[0], diop[1], diop[2], diop[3], diop[4], diop[5], diop[6], diop[7], diop[8]

# Note, fan circuit usually s3

def fanon(t):  # define function to turn on fan for t seconds as input
    try:
        print(f"Turning on fan for {t} seconds")  # Debugging line
        s3.value = True  # turns on fan
        time.sleep(t)  # sleep for t seconds while fan is on
        s3.value = False  # turns off fan
        return 1
    except Exception as e:
        print(f"Error in fanon: {e}")  # Debugging line
        return 0

def fanoff():  # define function to turn off fan
    try:
        print("Turning off fan")  # Debugging line
        s3.value = False  # turns off fan
        return 1
    except Exception as e:
        print(f"Error in fanoff: {e}")  # Debugging line
        return 0
