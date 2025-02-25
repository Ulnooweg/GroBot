#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: config
#Version: 1.2
#Description: Code to read and manipulate configuration file grobot_cfg.ini, read system info from ulnoowegdat csv
#Function: get_plant _settings(), read config and return plant settings as a tuple of data
#          read_config(), read config.ini and return a dictionary value of all data
#          update_config(section, parameter, value), write "value" to config file under "parameter" parameter in "section" section
#          readcsv(csventryname), read data from ulnoowegdat and return value for entry csventryname
#          writecsv(csventryname,csventryvalue), take strings entry name and entry value and write it to the appropriate entry columns in ulnoowegdat csv
#          writecsvnote(csventryname,csventryvalue,csventrynote) same as writecsv except also takes entry note and write that string also to the note column of the appropriate entry in ulnoowegdat csv
#          readcsv_softver(csventryname), same as readcsv except it reads the file/code/softver instead of /userdata/ulnoowegdat
#          writecsvnewrow(col1,col2,col3), append a new row to the end with column col1, col2, col3 inputted as string
#Input: update_config requires section and parameter in strings and value in any form convertible to strings. readcsv, writecsv, writecsvnote, readcsv_softver, and writecsvnewrow requires string inputs
#Output: returns dictionary variable in string for read_config() and in integer for get_plant_settings(); output data to file for update_config(...); output string for readcsv and readcsv_softver
#Error Handling: Standard UEC Error Handling V1
#
########################################

#Import important modules
import configparser
import csv
import threading
import subprocess
from lcddispfunc import set_lcd_color

config = configparser.ConfigParser()
config.optionxform = str #Force keep case-sensititvity in config file

#Define thread locks for use in multi-threading
#A single file should have a single threadlock variable for both read and write operations called using "with"
readconfigs_lock = threading.Lock() #Define a thread lock class
csv_ulnoodat_lock = threading.Lock() #Define a thread lock class
csv_softver_lock = threading.Lock() #Define a thread lock class
csv_mainflags_lock = threading.Lock() #Define a thread lock class as csv_mainflags_lock

def read_config():
    try:
        with readconfigs_lock: #Acquire thread lock before operation
            config.read("/mnt/grobotextdat/userdata/grobot_cfg.ini")
            return config
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def get_plant_settings(): #Define get_plant_settings which read config file and put them in a dictionaried variable
    try:
        with readconfigs_lock: #Acquire thread lock before operation
            config.read("/mnt/grobotextdat/userdata/grobot_cfg.ini")
            settings = {
                'sunrise': [int(x) for x in config['PLANTCFG']['sunrise'].split(",")],
                'sunset': [int(x) for x in config['PLANTCFG']['sunset'].split(",")],
                'checkTime': [int(x) for x in config['PLANTCFG']['checkTime'].split(",")],
                'dryValue': int(config['PLANTCFG']['dryValue']),
                'maxTemp': int(config['PLANTCFG']['maxTemp']),
                'maxHumid': int(config['PLANTCFG']['maxHumid']),
                'waterVol': int(config['PLANTCFG']['waterVol']),
                'fanTime': int(config['PLANTCFG']['fanTime'])
            }
            return settings #return variable as a dictionary
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def update_config(section, parameter, value): #Define function to write variable back to config file
    try:
        with readconfigs_lock: #Acquire thread lock before operation
            config.read("/mnt/grobotextdat/userdata/grobot_cfg.ini")
            config[section][parameter] = str(value)
            with open('/mnt/grobotextdat/userdata/grobot_cfg.ini', 'w') as configfile:
                config.write(configfile)
            return 1
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def readcsv(csventryname): #define a function to read csv file and return the value corresponding to entry
    #csv entry name must be a string
    try:
        csvdata = [] #define an empty list
        with csv_ulnoodat_lock: #Acquire thread lock before operation
            with open('/mnt/grobotextdat/userdata/ulnoowegdat', 'r') as csvfile: #open the csv file as csvfile object
                csvraw = csv.reader(csvfile) #read csvfile into csvraw using reader class from csv library
                for row in csvraw: #iterate through each row in cswraw
                    if row[0] == csventryname: #Check for row where the first column, name in the file, match desired csv entry
                        csventryvalue = row[1]  #read the value for row that matched the desired entry
                        return csventryvalue
                    else:
                        pass
            raise RuntimeError('CSV ENTRY NOT FOUND')
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None
    
def writecsv(csventryname,csventryvalue): #define a function to write to csv file taking in name of entry and value of the entry to update to
    try:
        #csventryname and csventryvalue must be a string
        #First, read csv file (same as)
        csvdata = [] #define an empty list
        with csv_ulnoodat_lock: #Acquire thread lock before operation
            with open('/mnt/grobotextdat/userdata/ulnoowegdat', 'r') as csvfile: #open the csv file as csvfile object
                csvraw = csv.reader(csvfile) #read csvfile into csvraw using reader class from csv library
                for row in csvraw: #iterate through each row in cswraw
                    if row[0] == csventryname: #Check for row where the first column, name in the file, match desired csv entry
                        row[1] = csventryvalue #Change the value to desired value
                    else:
                        pass
                    csvdata.append(row) #for each row, append the data to the list
            #Now write the data back to file
            with open('/mnt/grobotextdat/userdata/ulnoowegdat', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerows(csvdata)

            return 1 #return the csv data in list form
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def writecsvnote(csventryname,csventryvalue,csventrynote): #define a function to write to csv file taking in name of entry, value of the entry, and value of note to update to
    try:
        #csventryname, csventryvalue, and csventrynote must be a string
        #First, read csv file (same as)
        csvdata = [] #define an empty list
        with csv_ulnoodat_lock: #Acquire thread lock before operation
            with open('/mnt/grobotextdat/userdata/ulnoowegdat', 'r') as csvfile: #open the csv file as csvfile object
                csvraw = csv.reader(csvfile) #read csvfile into csvraw using reader class from csv library
                for row in csvraw: #iterate through each row in cswraw
                    if row[0] == csventryname: #Check for row where the first column, name in the file, match desired csv entry
                        row[1] = csventryvalue #Change the value to desired value
                        row[2] = csventrynote #Change the note to desired note
                    else:
                        pass
                    csvdata.append(row) #for each row, append the data to the list
            #Now write the data back to file
            with open('/mnt/grobotextdat/userdata/ulnoowegdat', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerows(csvdata)

            return 1 #return the csv data in list form
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None
    
def readcsv_softver(csventryname): #define a function to read csv file and return the value corresponding to entry
    #csv entry name must be a string
    try:
        csvdata = [] #define an empty list
        with csv_softver_lock: #Acquire thread lock before operation
            with open('/mnt/grobotextdat/code/softver', 'r') as csvfile: #open the csv file as csvfile object
                csvraw = csv.reader(csvfile) #read csvfile into csvraw using reader class from csv library
                for row in csvraw: #iterate through each row in cswraw
                    if row[0] == csventryname: #Check for row where the first column, name in the file, match desired csv entry
                        csventryvalue = row[1]  #read the value for row that matched the desired entry
                        return csventryvalue
                    else:
                        pass
            raise RuntimeError('CSV ENTRY NOT FOUND') #If entry not found raise an error
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None
    
def writecsvnewrow(col1,col2,col3): #define a function to write a new row to csv file with 3 column
    try:
        #All input must be string
        csvdata = [col1,col2,col3] #define the row list
        #Now write the data back to file in line append mode
        with csv_ulnoodat_lock: #Acquire thread lock before operation
            with open('/mnt/grobotextdat/userdata/ulnoowegdat', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(csvdata) #Use writerow not writerows as we only want to write a single row

            return 1 #return the csv data in list form
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

def readcsv_mainflags(csventryname): #define a function to read csv file and return the value corresponding to entry
    #csv entry name must be a string
    try:
        csvdata = [] #define an empty list
        with csv_mainflags_lock: #Acquire thread lock before operation using csv_mainflags_lock. Any subsequent attempt to access will wait for with statement to release the lock
            with open('/mnt/grobotextdat/code/mainflags', 'r') as csvfile: #open the csv file as csvfile object
                csvraw = csv.reader(csvfile) #read csvfile into csvraw using reader class from csv library
                for row in csvraw: #iterate through each row in cswraw
                    if row[0] == csventryname: #Check for row where the first column, name in the file, match desired csv entry
                        csventryvalue = row[1]  #read the value for row that matched the desired entry
                        return csventryvalue
                    else:
                        pass
            raise RuntimeError('CSV ENTRY NOT FOUND')
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None
    
def writecsv_mainflags(csventryname,csventryvalue): #define a function to write to csv file taking in name of entry and value of the entry to update to
    try:
        #csventryname and csventryvalue must be a string
        #First, read csv file (same as)
        csvdata = [] #define an empty list
        with csv_mainflags_lock: #Acquire thread lock before operation using csv_mainflags_lock. Any subsequent attempt to access will wait for with statement to release the lock
            with open('/mnt/grobotextdat/code/mainflags', 'r') as csvfile: #open the csv file as csvfile object
                csvraw = csv.reader(csvfile) #read csvfile into csvraw using reader class from csv library
                for row in csvraw: #iterate through each row in cswraw
                    if row[0] == csventryname: #Check for row where the first column, name in the file, match desired csv entry
                        row[1] = csventryvalue #Change the value to desired value
                    else:
                        pass
                    csvdata.append(row) #for each row, append the data to the list
            #Now write the data back to file
            with open('/mnt/grobotextdat/code/mainflags', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerows(csvdata)

            return 1 #return the csv data in list form
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        set_lcd_color("error")
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None