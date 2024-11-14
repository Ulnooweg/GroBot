#Copyright 2023-2024 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: config
#Version: 1.1
#Description: Code to read and manipulate configuration file grobot_cfg.ini, read system info from ulnoowegdat csv
#Function: get_plant _settings(), read config and return plant settings as a tuple of data
#          read_config(), read config.ini and return a dictionary value of all data
#          update_config(section, parameter, value), write "value" to config file under "parameter" parameter in "section" section
#          readcsv(), read data from ulnoowegdat and return it as a list
#Input: update_config requires section and parameter in strings and value in any form convertible to strings. 
#Output: returns dictionary variable in string for read_config() and in integer for get_plant_settings(); output data to file for update_config(...); output list of data for readcsv
#Error Handling: NONE
#
########################################

#Import important modules
import configparser
import csv

config = configparser.ConfigParser()
config.optionxform = str #Force keep case-sensititvity in config file

def read_config():
    config.read("/mnt/grobotextdat/userdata/grobot_cfg.ini")
    return config

def get_plant_settings(): #Define get_plant_settings which read config file and put them in a dictionaried variable
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

def update_config(section, parameter, value): #Define function to write variable back to config file
    config.read("/mnt/grobotextdat/userdata/grobot_cfg.ini")
    config[section][parameter] = str(value)
    with open('/mnt/grobotextdat/userdata/grobot_cfg.ini', 'w') as configfile:
        config.write(configfile)

def readcsv(): #define a function to read csv file
    csvdata = [] #define an empty list
    with open('/mnt/grobotextdat/userdata/ulnoowegdat', 'r') as csvfile: #open the csv file as csvfile object
        csvraw = csv.reader(csvfile) #read csvfile into csvraw using reader class from csv library
        for row in csvraw: #iterate through each row in cswraw
            csvdata.append(row) #for each row, append the data to the list

    return csvdata #return the csv data in list form