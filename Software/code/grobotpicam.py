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
#Version: 2.0
#Description: This function takes picture using pi camera
#Function: picam_capture(), capture image using rpi-still the using imagemagic convert to add annotations (timestamps)
#          checks if camera exists and if not, return 1 and do not take picture
#Input: NONE
#Output: Timestamped image from Pi Camera to fixed location
#Error Handling: Standard UEC Error Handling V1
#
########################################
#MODULE IMPORTS
import subprocess
import datetime
import os
from multiprocessing import shared_memory

#define function to take picture
#Note that we are using subprocess to allow python code to run command line command
def picam_capture():
    try:
        #Read the debugstate for use as condition in printing debug statement
        ext_mem = shared_memory.SharedMemory(name='grobot_shared_mem')
        debugstate = ext_mem.buf[0]

        #Debug message
        print('grobotpicam-picam_capture: Checking existence of camera') if debugstate == 1 or debugstate == 2 else None

        #First check if the camera exists or not
        gbpcresult = subprocess.run(['rpicam-still', 'list-cameras', '-v', '0'], capture_output=True) #run list-cameras to check if camera exists or not and use capture_output = True to capture output into gbpcresult for processing
        #-v specify verbosity to be none to not make the log file clutter, on error it will still return an output
        match gbpcresult.returncode: #match the return code with expected value
            case 0: #return code = 0 means successful execution
                pass
            case 255:  #Return code 255 is associated with no cameras detected for rpicam-still
                #gbpcstdout = gbpcresult.stdout.decode().strip() #Not used, no std output returned in this case
                gbpcerrout = gbpcresult.stderr.decode().strip() #decode the captured error and strip them of start/end empty space
                if "no cameras available" in gbpcerrout: #check if the error message actual contains there is no camera as expected
                    return 1 #Ends function and returns now, sending 1 as it successfully do not execute per config
                else:
                    raise RuntimeError('PICAM ERROR - ERROR MESSAGE DO NOT MATCH RETURN CODE')
            case _: #Any other case should raise an error
                raise RuntimeError('PICAM ERROR - NON STANDARD RETURN CODE') #If there is no proper match, raise an error

        #Debug message
        print('grobotpicam-picam_capture: Constructing timestamp') if debugstate == 1 or debugstate == 2 else None

        #This part takes an image    
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") #get current date and time
        humantimestamp = datetime.datetime.now().strftime("%H:%M:%S %Y-%m-%d") #Timestamp for image

        #Debug message
        print('grobotpicam-picam_capture: Checking existence of image output directory') if debugstate == 1 or debugstate == 2 else None

        #Now this part will determine what directory to use
        directory = "/mnt/grobotextdat/pictures" #This is the main external directory associated with USB
        if os.path.isdir(directory) == True: #check if exist
            pass #if it is pass
        else: #if not return error to force a code restart
            raise RuntimeError('FILE IO FAIL')

        #Debug message
        print('grobotpicam-picam_capture: Raking image') if debugstate == 1 or debugstate == 2 else None

        filename = f"{directory}/grobot-camera-image-{timestamp}.jpeg" #construct filename structure using f-string
        subprocess.run(['rpicam-still', '-o', filename, '-v', '0']) #capture to filename which already have directory specified using libcamera command line tool
        #-o specify output filename, -v specify verbosity to be none to not make the log file clutter

        #Debug message
        print('grobotpicam-picam_capture: Post-processing image') if debugstate == 1 or debugstate == 2 else None

        #Now this part adds the timestamp text
        fontsize = '150' #Set timestamp font size in points
        fontcolour = '#DEC305' #Set font colour
        XYpos = '+100+2500' #Set text XY position from top left corner
        outputsize = 'jpeg:extent=512kb' #Set the maximum size of the output jpeg that will be set by define
        #Not put it all together in a convert command
        #Note The command is 'convert filename -pointsize 150 -fill "#DEC035" -annotate +100+2500 'TIMESTAMP' filename'
        subprocess.run(['convert', filename, '-pointsize', fontsize, '-define', outputsize, '-fill', fontcolour, '-annotate', XYpos, humantimestamp, filename])

        #Debug message
        print('grobotpicam-picam_capture: Image capture completed') if debugstate == 1 or debugstate == 2 else None

        return 1
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None