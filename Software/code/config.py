#Copyright 2023-2024 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/TNarakol-UEC/GroBot
#
########################################
#
#Contact: engineering@ulnooweg.ca
#Growth Enclosure 
#
#Config file readout code
#V1.0.3
#
#This code defines several important function to read config files including
#get_plant _settings() which read config and return plant settings as a tuple of data
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
