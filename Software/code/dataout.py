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
#Version: 1.1
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
import pandas as pd #import panda module as pd for easier call

##############################################

def excelout(T,RH,SRH):
    try:
        directory = "/mnt/grobotextdat/data" #This is the main external directory associated with USB
        if os.path.isdir(directory) == True: #check if exist
            pass #if it is pass
        else: #if not return error to force a code restart
            raise RuntimeError('FILE IO FAIL')

        #Now check if the output excel file exist, if it does not create it.
        filename = f"{directory}/datalog.xlsx"

        if os.path.isfile(filename) == True:
            xlsx_sheet_name = 'datatable' #also define sheet name here
            pass
        else: #create the excel file
            dfcolumns = ['Time', 'Temp', '%RH', 'Soil RH'] #Define columns name
            xlsx_sheet_name = 'datatable' #Excel sheet name

            df = pd.DataFrame(columns=dfcolumns) #create empty dataframe with only columns

            #Write dataframe to file with specified parameters, output header info and set index to False so we do not output row number as first data column
            df.to_excel(filename, sheet_name=xlsx_sheet_name, index=False, header=True)

        #Now we will append the data
        humantimestamp = datetime.datetime.now().strftime("%H:%M %d/%B/%Y") #Current timestamp 

        writedata = [humantimestamp, T, RH, SRH] #data to write to excel in tuple

        current_df = pd.read_excel(filename) #read the excel file into a dataframe
        new_df = pd.DataFrame([writedata], columns= current_df.columns) #create a new dataframe with same columns as existing df
        combined_df = pd.concat([current_df, new_df])

        with pd.ExcelWriter(filename) as writer:
            combined_df.to_excel(writer, sheet_name = xlsx_sheet_name, index = False)
        return 1
    except Exception as errvar:
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None
