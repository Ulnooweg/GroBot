#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: dataout
#Version: 1.2
#Description: Code to write data to output excel file
#Function: excelout(T,RH,SRH), write timestamp, "T" temperature, "RH" relative humidity, "SRH" soil humidity to excel file once called
#Input: excelout(...) requires Temperature, Relative Humidity, Soil humidity as a numerical input
#Output: data output to excel file in fixed directory or fallback location for excelout(...)
#Error Handling: Standard UEC Error Handling V1
#
########################################
#MODULE IMPORTS
import os
import datetime
import threading
import subprocess
from lcdfuncdef import set_lcd_color
import csv

##############################################

dataoutcsv_lock = threading.Lock() #Define a thread lock class

def excelout(T,RH,SRH):
    try:
        #First, check if the required path exists
        directory = "/mnt/grobotextdat/data" #This is the main external directory associated with USB
        if os.path.isdir(directory) == True: #check if exist
            pass #if it is pass
        else: #if not return error to force a code restart
            raise RuntimeError('FILE IO FAIL')

        #Now check if the output excel file exist, if it does not create it.
        filename = f"{directory}/datalog.csv"

        if os.path.isfile(filename) == True:
            pass
        else: #create the excel file
            #All info must be strings
            csvinitdata = ['Time','Temp','%RH','Soil RH'] #define the row list
            with dataoutcsv_lock: #Acquire thread lock before operation
                with open('/mnt/grobotextdat/data/datalog.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(csvinitdata) #Use writerow not writerows as we only want to write a single row

        #Now we will append the data
        humantimestamp = datetime.datetime.now().strftime("%H:%M:%S %Y-%m-%d") #Current timestamp Canadian standard (ISO 8081 ref)
        #See: https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/enabling-interoperability/gc-enterprise-data-reference-standards/data-reference-standard-date-time-format.html

        csvdata = [str(humantimestamp), str(T), str(RH), str(SRH)] #data to write to csv, convert to string to make sure they are string

        #Now write the data back to file in line append mode
        with dataoutcsv_lock: #Acquire thread lock before operation
            with open('/mnt/grobotextdat/data/datalog.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(csvdata) #Use writerow not writerows as we only want to write a single row

            return 1
        
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None