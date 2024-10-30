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
#Description: Code to read and manipulate configuration file grobot_cfg.ini
#Function: get_plant _settings(), read config and return plant settings as a tuple of data
#          read_config(), read config.ini and return a dictionary value of all data
#          update_config(section, parameter, value), write "value" to config file under "parameter" parameter in "section" section
#Input: update_config requires section and parameter in strings and value in any form convertible to strings. 
#Output: returns dictionary variable in string for read_config() and in integer for get_plant_settings(); output data to file for update_config(...)
#Error Handling: NONE
#
########################################

#Import important modules
import configparser

config = configparser.ConfigParser()
config.optionxform = str #Force keep case-sensititvity in config file

def read_config():
    config.read("grobot_cfg.ini")
    return config

def get_plant_settings(): #Define get_plant_settings which read config file and put them in a dictionaried variable
    config.read("grobot_cfg.ini")
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
    config.read("grobot_cfg.ini")
    config[section][parameter] = str(value)
    with open('grobot_cfg.ini', 'w') as configfile:
        config.write(configfile)
