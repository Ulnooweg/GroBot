#Copyright 2023-2024 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: picamera
#Version: 1.1
#Description: This function takes picture using pi camera
#Function: picam_capture(), capture image using rpi-still the using imagemagic convert to add annotations (timestamps)
#Input: NONE
#Output: Timestamped image from Pi Camera to fixed location or fallback directory.
#Error Handling: returns 0 on failure, 1 on success, 2 on usage of fallback directory
#
########################################
#MODULE IMPORTS
import subprocess
import datetime
import os
import configparser

config = configparser.ConfigParser()

#define function to take picture
#Note that we are using subprocess to allow python code to run command line command
def picam_capture():
    try:
        #First check if the camera is configured to be on:
        config.read("grobot_cfg.ini") #Read the grobot config file
        match config['PICAMERA']['CameraSet']: #Configparser always parse as strings
            case '0': #0 is no camera attached
                return 1 #Ends function and returns now, sending 1 as it successfelly do not execute per config
            case '1':
                pass
            case _:
                return 0 #If there is no proper match, return an error 
        #This part takes an image    
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") #get current date and time
        humantimestamp = datetime.datetime.now().strftime("%H:%M %d/%B/%Y") #Timestamp for image

        #Now this part will determine what directory to use
        directory = "/mnt/grobotextdat/pictures" #This is the main external directory associated with USB
        if os.path.isdir(directory) == True: #check if exist
            returnvar = 1 #set variable to return = 1
            pass #if it is pass
        else: #if not set directory to alternative directory
            returnvar = 2 #set variable to return = 2
            directory = "/home/grobot/code/pictures"  # specify your directory here

        filename = f"{directory}/camera-image-{timestamp}.jpeg" #construct filename structure using f-string
        subprocess.run(['rpicam-still', '-o', filename]) #capture to filename which already have directory specified using libcamera command line tool

        #Now this part adds the timestamp text
        fontsize = '150' #Set timestamp font size in points
        fontcolour = '#DEC305' #Set font colour
        XYpos = '+100+2500' #Set text XY position from top left corner
        #Not put it all together in a convert command
        #Note The command is 'convert filename -pointsize 150 -fill "#DEC035" -annotate +100+2500 'TIMESTAMP' filename'
        subprocess.run(['convert', filename, '-pointsize', fontsize, '-fill', fontcolour, '-annotate', XYpos, humantimestamp, filename])

        return returnvar #return success or failure variables
    except:
        return 0