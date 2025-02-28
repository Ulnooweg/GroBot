#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: grobotpicam
#Version: 1.2
#Description: This function takes picture using pi camera
#Function: picam_capture(), capture image using rpi-still the using imagemagic convert to add annotations (timestamps)
#Input: NONE
#Output: Timestamped image from Pi Camera to fixed location or fallback directory.
#Error Handling: Standard UEC Error Handling V1
#
########################################
#MODULE IMPORTS
import subprocess
import datetime
import os
import configparser
from lcdfuncdef import set_lcd_color

config = configparser.ConfigParser()

#define function to take picture
#Note that we are using subprocess to allow python code to run command line command
def picam_capture():
    try:
        #First check if the camera is configured to be on:
        config.read("/mnt/grobotextdat/userdata/grobot_cfg.ini") #Read the grobot config file
        match config['PICAMERA']['CameraSet']: #Configparser always parse as strings
            case '0': #0 is no camera attached
                return 1 #Ends function and returns now, sending 1 as it successfully do not execute per config
            case '1':
                pass
            case _:
                raise RuntimeError('PICAM CONFIG ERROR') #If there is no proper match, raise an error
        #This part takes an image    
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") #get current date and time
        humantimestamp = datetime.datetime.now().strftime("%H:%M:%S %Y-%m-%d") #Timestamp for image

        #Now this part will determine what directory to use
        directory = "/mnt/grobotextdat/pictures" #This is the main external directory associated with USB
        if os.path.isdir(directory) == True: #check if exist
            pass #if it is pass
        else: #if not return error to force a code restart
            raise RuntimeError('FILE IO FAIL')

        filename = f"{directory}/camera-image-{timestamp}.jpeg" #construct filename structure using f-string
        subprocess.run(['rpicam-still', '-o', filename]) #capture to filename which already have directory specified using libcamera command line tool

        #Now this part adds the timestamp text
        fontsize = '150' #Set timestamp font size in points
        fontcolour = '#DEC305' #Set font colour
        XYpos = '+100+2500' #Set text XY position from top left corner
        #Not put it all together in a convert command
        #Note The command is 'convert filename -pointsize 150 -fill "#DEC035" -annotate +100+2500 'TIMESTAMP' filename'
        subprocess.run(['convert', filename, '-pointsize', fontsize, '-fill', fontcolour, '-annotate', XYpos, humantimestamp, filename])

        return 1
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None