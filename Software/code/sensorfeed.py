#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under Québec Free and Open-Source Licence – Strong Reciprocity (LiLiQ-R+) Version 1.1
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: sensorfeed
#Version: 2.0
#Description: This function read sensor feeds and return its value
#Function: feedread(), read sensor values and return it as a tuple of values
#Input: NONE
#Output: Returns value of temperature, relative humidity, and soil humidity in order as a tuple of numbers
#Error Handling: Standard UEC Error Handling V1
#
########################################
# MODULE IMPORTS
from diopinsetup import diopinset
import subprocess
from multiprocessing import shared_memory

##############################################
def feedread():  # define feedread function
    try:
        #Read the debugstate for use as condition in printing debug statement
        ext_mem = shared_memory.SharedMemory(name='grobot_shared_mem')
        debugstate = ext_mem.buf[0]

        #Debug message
        print('sensorfeed-feedread: Defining sensors') if debugstate == 1 or debugstate == 2 else None

        # Handle the pins definition and sensor definition
        diop = diopinset()

        if isinstance(diop, tuple):
            s1, s2, s3, s4, s5, s6, b1, ths, sms, ina = diop
        else:
            raise RuntimeError('Failed to initialize pins and sensors')

        #Debug message
        print('sensorfeed-feedread: Assigning sensors') if debugstate == 1 or debugstate == 2 else None

        T = ths.temperature
        RH = ths.relative_humidity
        SRH = sms.moisture_read()

        #Debug message
        print('sensorfeed-feedread: Sensors assignment completed') if debugstate == 1 or debugstate == 2 else None

        return T, RH, SRH  # return tuple of all values
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None
