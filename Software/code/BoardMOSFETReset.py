#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under Québec Free and Open-Source Licence – Strong Reciprocity (LiLiQ-R+) Version 1.1
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: BoardMOSFETReset
#Version: 2.0
#Description: Code to set all MOSFET gate to False (open circuit). Used on startup with grobotboot.
#Function: grobotboot(), force all MOSFET gate to False (open circuit) when called
#Input: NONE
#Output: NONE
#Error Handling: Standard UEC Error Handling V1
#
########################################

#import important library
#All these are part of Blinka
import board
import digitalio
import subprocess
from multiprocessing import shared_memory

def grobotboot(): #Define a callable function by main
    try:
        #Read the debugstate for use as condition in printing debug statement
        ext_mem = shared_memory.SharedMemory(name='grobot_shared_mem')
        debugstate = ext_mem.buf[0]

        #Debug message
        print('BoardMOSFETReset-grobotboot: Defining pins') if debugstate == 1 or debugstate == 2 else None

        #Setup pinouts for hardware used
        #Current: Raspberry Pi 3 A+ with BCRobotics Irrigation Hat V2
        #For Blinka, the pins are defined as DXX

        pins = {
            'S1' : board.D13, #This is MOSFET control pin 1 (System 1). Other S pin controls n MOSFET.
            'S2' : board.D16, #DXX Corresponds to GPIO pins XX
            'S3' : board.D19,
            }
        
        #Debug message
        print('BoardMOSFETReset-grobotboot: Defining Digital I/O objects') if debugstate == 1 or debugstate == 2 else None

        #Setup Actuator circuts
        #print("initalizing actuator circuits on boot")

        s1 = digitalio.DigitalInOut(pins['S1'])
        s2 = digitalio.DigitalInOut(pins['S2'])
        s3 = digitalio.DigitalInOut(pins['S3'])

        #Debug message
        print('BoardMOSFETReset-grobotboot: Setting all pin to False') if debugstate == 1 or debugstate == 2 else None

        for s in [s1, s2, s3]:
            s.direction = digitalio.Direction.OUTPUT
            s.drive_mode = digitalio.DriveMode.PUSH_PULL
            s.value = False

        #Debug message
        print('BoardMOSFETReset-grobotboot: Set all pin to False') if debugstate == 1 or debugstate == 2 else None
        
        return 1
    
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None