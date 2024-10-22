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
# This function read sensor feeds
#V1.0.3
#
# This function executes without input and returns Temp, %RH, and soilRH to main in raw form
# returns single number 0 on failure
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
