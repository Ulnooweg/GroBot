#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: lightcontrol
#Version: 2.0
#Description: These functions controls the growlight
#Function: growlighton(), turns growlight on
#          growlightoff(), turns growlight off
#Input: NONE
#Output: NONE
#Error Handling: Standard UEC Error Handling V1
#
########################################
#MODULE IMPORTS
from diopinsetup import diopinset
import subprocess
from multiprocessing import shared_memory

##############################################
#Handle the pins definition and sensor definition
diop = diopinset()
s1, s2, s3, s4, s5, s6, b1, ths, sms, ina = diop[0], diop[1], diop[2], diop[3], diop[4], diop[5], diop[6], diop[7], diop[8], diop[9]

#Note, light circuit usually s2

def growlighton(): #define function to turn on growlight
    try:
        #Read the debugstate for use as condition in printing debug statement
        ext_mem = shared_memory.SharedMemory(name='grobot_shared_mem')
        debugstate = ext_mem.buf[0]

        #Debug message
        print('lightcontrol-growlighton: Turning light on') if debugstate == 1 or debugstate == 2 else None

        s2.value = True #turns on fan

        #Debug message
        print('lightcontrol-growlighton: Light on completed') if debugstate == 1 or debugstate == 2 else None

        return 1
    
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def growlightoff(): #define function to turn off growlight
    try:
        #Read the debugstate for use as condition in printing debug statement
        ext_mem = shared_memory.SharedMemory(name='grobot_shared_mem')
        debugstate = ext_mem.buf[0]

        #Debug message
        print('lightcontrol-growlightoff: Turning light off') if debugstate == 1 or debugstate == 2 else None

        s2.value = False #turns on fan

        #Debug message
        print('lightcontrol-growlightoff: Light off completed') if debugstate == 1 or debugstate == 2 else None

        return 1
    
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None