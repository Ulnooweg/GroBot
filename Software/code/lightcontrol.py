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
#Version: 1.2
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
from lcdfuncdef import set_lcd_color

##############################################
#Handle the pins definition and sensor definition
diop = diopinset()
s1, s2, s3, s4, s5, s6, b1, ths, sms = diop[0], diop[1], diop[2], diop[3], diop[4], diop[5], diop[6], diop[7], diop[8]

#Note, light circuit usually s2

def growlighton(): #define function to turn on growlight
    try:
        s2.value = True #turns on fan
        return 1
    
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def growlightoff(): #define function to turn off growlight
    try:
        s2.value = False #turns on fan
        return 1
    
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None