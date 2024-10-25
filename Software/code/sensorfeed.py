#Copyright 2023-2024 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: sensorfeed
#Version: 1.0.4
#Description: This function read sensor feeds and return its value
#Function: feedread(), read sensor values and return it as a tuple of values
#Input: NONE
#Output: Returns value of temperature, relative humidity, and soil humidity in order as a tuple of numbers
#Error Handling: returns 0 on failure and output to log/terminal. The logs text out to terminal is:
#                RuntimeError: Failed to initialize pins and sensors
#
########################################
# MODULE IMPORTS
from diopinsetup import diopinset

##############################################
# Handle the pins definition and sensor definition
diop = diopinset()

if isinstance(diop, tuple):
    s1, s2, s3, s4, s5, s6, b1, ths, sms = diop
else:
    raise RuntimeError('Failed to initialize pins and sensors')

def feedread():  # define feedread function
    try:
        T = ths.temperature
        RH = ths.relative_humidity
        SRH = sms.moisture_read()

        return T, RH, SRH  # return tuple of all values
    except Exception as e:
        print(f"Error reading sensor values: {e}")
        return 0
