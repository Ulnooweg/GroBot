#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: firmware V1.1 update script
#Version: [NOT TRACKED]
#Description: This code, once executed, update GroBot firmware to the latest version. Checking if it needs intermediate update sequentially
#Function: NONE
#Input: NONE
#Output: NONE
#Error Handling: Standard UEC Error Handling V1
#
########################################
#MODULE IMPORTS
import subprocess
from config import readcsv, writecsvnote
from lcddispfunc import set_lcd_color

#Define a function to update the firmware
def grobotfwupdate():
    try:
        #Check individually for each step of the firmware update process

        ###############################################################################
        #Version 1.1 update#
        #Copy this entire block until Version update end to reuse it for later version
        #Remember to change:
        #                   The header and footer block
        #                   fw_update_version ... #Define what version this is
        #                   Anything inside #### FW UPDATE CODE ####
        ###############################################################################
        
        #Read current firmware version as string as defined by readcsv
        fw_version = readcsv('fw_version')

        fw_update_version = 1.1 #Define what version this is

        if float(fw_version) >= fw_update_version: #Checks, if current fw version already up to date or newer do nothing
            pass
        elif float(fw_version) < fw_update_version: #If version is less do the update
            #If needs to run as sudo, we need to echo the password as standrd input and use -S flag to have sudo use password from standard input
            #If command contains #, wrap it all in "COMMAND_HERE" to ensure it is not processed as comment
            #Source command is echo $PSSWD | sudo -S command 

            #### FW UPDATE CODE ####

            #Update 1, ensure systemmaxuse is commented out
            subprocess.run("echo grobot | sudo -S sed -i '/^[^#]*SystemMaxUse=/s/^/#/' /etc/systemd/journald.conf", shell=True)

            #Update 2, turn off wifi to strengthen security
            subprocess.run("echo grobot | sudo -S rfkill block wifi", shell=True)

            #Update 3, turn off bluetooth to strengthen security
            subprocess.run("echo grobot | sudo -S rfkill block bluetooth", shell=True)

            #Update 4, disable grobotboot and remove its service unit file
            subprocess.run("echo grobot | sudo -S systemctl stop grobotboot", shell=True)
            subprocess.run("echo grobot | sudo -S systemctl disable grobotboot", shell=True)
            subprocess.run("echo grobot | sudo -S rm /lib/systemd/system/grobotboot.service", shell=True)

            #Update 5, update grobot main service file to implement restart count control
            subprocess.run("echo grobot | sudo -S cp /mnt/grobotextdat/code/grobot.service /lib/systemd/system/grobot.service", shell=True)

            #### FW UPDATE CODE END ####

            #Write the updated firmware version
            writecsvnote('fw_version',str(fw_update_version),f"#Firmware Version: {fw_update_version}")            
        else: #Else raise an error
            raise RuntimeError('FW UPDATE VERSION CHECK FAILURE')
        
        #Read current firmware version as string as defined by readcsv (Done after every update block)
        fw_version = readcsv('fw_version')

        ###############################################################################
        #Version 1.1 update end#
        ###############################################################################

        #End of updates, return a success
        return 1
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None