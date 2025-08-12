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
#Version: 2.0
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
import csv
from multiprocessing import shared_memory

##############################################

dataoutcsv_lock = threading.Lock() #Define a thread lock class

def excelout(T,RH,SRH):
    try:
        #Read the debugstate for use as condition in printing debug statement
        ext_mem = shared_memory.SharedMemory(name='grobot_shared_mem')
        debugstate = ext_mem.buf[0]

        #Debug message
        print('dataout-excelout: Checking if output path exists') if debugstate == 1 or debugstate == 2 else None

        #First, check if the required path exists
        directory = "/mnt/grobotextdat/data" #This is the main external directory associated with USB
        if os.path.isdir(directory) == True: #check if exist
            pass #if it is pass
        else: #if not return error to force a code restart
            raise RuntimeError('FILE IO FAIL')

        #Debug message
        print('dataout-excelout: Checking if file already exist') if debugstate == 1 or debugstate == 2 else None

        #Now check if the output excel file exist, if it does not create it.
        filename = f"{directory}/datalog.csv"

        if os.path.isfile(filename) == True:
            pass
        else: #create the excel file
            #Debug message
            print('dataout-excelout: Creating datalog.csv') if debugstate == 1 or debugstate == 2 else None
            #All info must be strings
            csvinitdata = ['Time','Temp','%RH','Soil RH'] #define the row list
            with dataoutcsv_lock: #Acquire thread lock before operation
                with open('/mnt/grobotextdat/data/datalog.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(csvinitdata) #Use writerow not writerows as we only want to write a single row


        #Debug message
        print('dataout-excelout: Creating dataset to append') if debugstate == 1 or debugstate == 2 else None

        #Now we will append the data
        humantimestamp = datetime.datetime.now().strftime("%H:%M:%S %Y-%m-%d") #Current timestamp Canadian standard (ISO 8081 ref)
        #See: https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/enabling-interoperability/gc-enterprise-data-reference-standards/data-reference-standard-date-time-format.html

        csvdata = [str(humantimestamp), str(T), str(RH), str(SRH)] #data to write to csv, convert to string to make sure they are string


        #Debug message
        print('dataout-excelout: Writing data to file') if debugstate == 1 or debugstate == 2 else None

        #Now write the data back to file in line append mode
        with dataoutcsv_lock: #Acquire thread lock before operation
            with open('/mnt/grobotextdat/data/datalog.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(csvdata) #Use writerow not writerows as we only want to write a single row

            #Debug message
            print('dataout-excelout: Data written to file') if debugstate == 1 or debugstate == 2 else None

            return 1
        
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        #LCD COLOUR HANDLING CODE (RED) HERE
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None