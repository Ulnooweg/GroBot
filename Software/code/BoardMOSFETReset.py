#Copyright 2023-2024 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: BoardMOSFETReset
#Version: 1.1
#Description: Code to set all MOSFET gate to False (open circuit). Used on startup with grobotboot.
#Function: grobotboot(), force all MOSFET gate to False (open circuit) when called
#Input: NONE
#Output: NONE
#Error Handling: NONE
#
########################################

#import important library
#All these are part of Blinka
import board
import busio
import digitalio

def grobotboot(): #Define a callable function by main
    #Setup pinouts for hardware used
    #Current: Raspberry Pi 3 A+ with BCRobotics Irrigation Hat V2
    #For Blinka, the pins are defined as DXX
    pins = {
        'S1' : board.D13, #This is MOSFET control pin 1 (System 1). Other S pin controls n MOSFET.
        'S2' : board.D16, #DXX Corresponds to GPIO pins XX
        'S3' : board.D19,
        'S4' : board.D20,
        'S5' : board.D26,
        'S6' : board.D21,
        'B1' : board.D12, #This is button input pin 1. Other B pin receive n button command
        'B2' : board.D6,
        'B3' : board.D5,
        'B4' : board.D25,
        #'B5' : board.GP15, #Comment out any B5 or GP15 as there's currently only 4 analog control
        'QWIIC_SCL' : board.SCL, #Define I2C pin CLOCK, use board.SCL in pi
        'QWIIC_SDA' : board.SDA #Define I2C pin DATA, use board.SDA in pi
        }

    #Setup Actuator circuts
    print("initalizing actuator circuits on boot")

    s1 = digitalio.DigitalInOut(pins['S1'])
    s2 = digitalio.DigitalInOut(pins['S2'])
    s3 = digitalio.DigitalInOut(pins['S3'])
    s4 = digitalio.DigitalInOut(pins['S4'])
    s5 = digitalio.DigitalInOut(pins['S5'])
    s6 = digitalio.DigitalInOut(pins['S6'])

    for s in [s1, s2, s3, s4, s5, s6]:
        s.direction = digitalio.Direction.OUTPUT
        s.drive_mode = digitalio.DriveMode.PUSH_PULL
        s.value = False
    
    return