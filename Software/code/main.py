#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: lcddispfunc
#Version: 2.0
#Description: LCD Module control code
#Function: Controls the workings of the LCD display and human interaction. Consult Info.md for more information
#Input: consult Info.md
#Output: consult Info.md
#Error Handling: consult Info.md
#This Python file uses the following encoding: utf-8
#
########################################
import sys
import os
import updatefw
import time
import board
import subprocess
import RPi.GPIO as GPIO
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLCDNumber, QMainWindow
from PySide6.QtCore import QDateTime, QTimer, Slot, Signal, QThreadPool, QRunnable, QObject, QTranslator, QCoreApplication
from PySide6.QtGui import *
from datetime import datetime, time as time2
from ui_form import Ui_Form
from timecheck import checktimebetween
from sensorfeed import feedread
from BoardMOSFETReset import grobotboot
from logoutput import logtofile
try:
    print('Writing log to file')
    logtofile() #Write log to file immediately after boot in case needed for debugging
except Exception as errvar:
    #Note: There is no force reboot yet here as logoutput should be the first thing imported and done
    #It's also already handled in the logoutput file itself.
    raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None
from watercontrol import autorain, pumprefillcycle
from fancontrol import fanmanon, fanoff, fanon
from lightcontrol import growlightoff, growlighton
from grobotpicam import picam_capture
from dataout import excelout
from diopinsetup import diopinset

# config.py is for linux.
import config
from config import (
    get_plant_settings, 
    readcsv,
    readlocal,
    readcsv_softver,
    readcsv_mainflags,
    writecsv_mainflags,
    readcsv_waterparam
)

##############################################
################# ON BOOTUP ##################
##############################################

if os.environ.get('DISPLAY','') == '': # Handles raspberry pi environment variable, for launching a python program on a display
    os.environ.__setitem__('DISPLAY', ':0.0')

print("Starting GUI...")

try:
    #Suppress traceback for cleaner error log
    #sys.tracebacklimit = 0 # Imported from main.py | cleans up the console of unessecary error messages

    # Virutally the same function as grobotboo(), but manages the GPIO pins through a separate library;
    # Whenever console commands attempted to start an instance of main.py through ssh, this error would occur
    # This fixes the "GPIO Busy" Error during GUI developement

    #Runs BoardMostfetReset
    grobotboot() #This force all pin reset

    # This only initialize once on bootup
    #LCD COLOUR HANDLING CODE (GREEN) HERE  # Set LCD color to green on bootup

    # Start the LCD menu thread immediately
except Exception as errvar:
    subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
    #LCD COLOUR HANDLING CODE (RED) HERE
    raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

# Starts with reading values from sensor
try:
    ReadVal = feedread() # T RH SRH in order
    
    # Now do an initial read of the configuration value
    settings = get_plant_settings()

    # Now check if light needs to be on or off
    if checktimebetween(time2(settings['sunrise'][0], settings['sunrise'][1]), time2(settings['sunset'][0], settings['sunset'][1])) == True:
        growlighton()
    elif checktimebetween(time2(settings['sunrise'][0], settings['sunrise'][1]), time2(settings['sunset'][0], settings['sunset'][1])) == False:
        growlightoff()
    else:
        raise RuntimeError('UNKNOWN FAILURE')

    # Check if internal humidity or temperature is too high and the fan needs to be on
    if ReadVal[0] > settings['maxTemp'] or ReadVal[1] > settings['maxHumid']:
        fanon(settings['fanTime'])
    elif ReadVal[0] <= settings['maxTemp'] and ReadVal[1] <= settings['maxHumid']:
        pass
    else:
        raise RuntimeError('UNKNOWN FAILURE')

except Exception as errvar:
    subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
    #LCD COLOUR HANDLING CODE (RED) HERE
    raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

##############################################
################# GUI CLASS ##################
##############################################

# Important notes for GUI buttons: when connecting a function to a QPushButton object, the function must be preceeded by
# "lambda:". Without this, any function placed inside the clicked.connect() method will be called on Grobot startup.

class Widget(QMainWindow): # Creates a class containing attributes imported from ui_form.py
    def __init__(self, parent=None): 
        super().__init__(parent) # Inherits class constructor from 'QWidget'
        self.resize(480, 640) # Sets resolution
        self.ui = Ui_Form() # defines UI
        self.ui.setupUi(self) # Imports setupUI from UI_Form which contains all objects such as QPushButtons, QSliders, QLabels, QCLD
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint) # Removes Title bar for a seamless window application

# Startup parameters

        # Toggle parameters
        self.togglewater = False # Initial Toggle state for waterpump
        self.togglelight = False # Initial Toggle state for UV growlamp
        self.togglefan = False # Intital Toggle state for enclosure fan

        # Start Threading
        self.thread_manager = QThreadPool() # Define QThreadPool
        thread_count = self.thread_manager.maxThreadCount() # Define Thread Count
        activethread_count = self.thread_manager.activeThreadCount()
        print(f"Multithreading with maximum {thread_count} threads") # Print Thread Count
        self.start_thread(self.schedule_routine) #Opens a new thread to begin scheduling
        print("Routine Running")
        print(f"Now running with {thread_count-activethread_count} threads") # Print Thread Count

        cfg = config.read_config()

### Button Functions & Label Logic ###

    # Progress Bar
        # Progress Bar Logic -------
        self.statusbar = self.findChild(
            QLabel, "statusbar_label"
            ) # Finds object QLabel "statusbar_label" in Ui_Form
        self.statusbar.setText(
            self.welcome_message()
            ) # Sets text of "statusbar_label" to welcome_message function
        
        # Indicators
        self.waterstatuslabel = self.findChild(
            QLabel, "water_status_label"
        )
       
        # Set Text of Indicators
        PumpRunDry = (readcsv_mainflags("PumpRunDry"))
        if int(PumpRunDry) == 1:
            self.waterstatuslabel.setText("Pump Dry")
            self.waterstatuslabel.setStyleSheet("color: red;")
        else:
            self.waterstatuslabel.setText("Water Det.")
            self.waterstatuslabel.setStyleSheet("color: navy;")

    # Primary Menus --------------------------------------------------------------------------------------------------------------

        # Start
            # Buttons
        self.ui.continue_btn.clicked.connect(
            lambda: self.start_thread(self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page))
            ) # Button event when pressed: changes page to mainmenu_page

        #### Clock Logic ---------------

            # Clock Display ------------
        self.clockdisplay = self.findChild(
            QLabel, "clockdisplay"
            ) # Finds QLCDNumber object "clockdisplay" in Ui_Form
        self.clockdisplay.setText(
            QCoreApplication.tr("Loading...")
            )
        
            # Date Display -------------
        self.datedisplay = self.findChild(
            QLabel, "Datedisplay"
            ) # Finds QLabel object "Datedisplay" in Ui_Form
        self.datedisplay.setText(
            QCoreApplication.tr("Loading...")
            )
        
            # Timer --------------------
        self.timer = QTimer() # Defines QTimer
        self.timer.timeout.connect(
            self.display_time
            ) # Connects QTimer output to function display_time
        self.timer.timeout.connect(
            self.current_date
            ) # Connects QTimer output to function current_date
        #self.timer.timeout.connect(self.moisture_display) # Connects QTimer output to function moisture_display
        self.timer.start(
            (1000)
            )
        
        # Main Menu ----------------
            # Buttons
        self.ui.systeminfo_page_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.systeminfo_page)
            ) # Button event when pressed: changes page to systeminfo_page
        self.ui.editsettings_page_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.editsettings_page)
            ) # Button event when pressed: changes page to editsettings_page
        self.ui.manualcontrols_page_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.manualcontrols_page)
            ) # Button event when pressed: changes page to manualcontrols_page
        self.ui.monitordata_page_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.monitordata_page)
            ) # Button event when pressed: changes page to monitordata_page
        self.ui.mainmenu_back_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.start_page)
            ) # Back Button 

        # System Info --------------
            # System Version Label
        self.systemversionlabel = self.findChild(
            QLabel, "systemversion_label"
            ) # Finds QLabel object "systemversion_label" in Ui_Form
        self.systemversionlabel.setText(
            f"{self.get_version_info()}"
            ) # Changes QLabel text to version number; calls read_csv & readcsv_softver from config, which reads from softver

            # Buttons
        self.ui.updatefirmware_page_btn.clicked.connect(
            lambda: self.start_thread(self.update_firmware)
            ) # Button event when pressed: calls update_firmware
        self.ui.logexport_page_btn.clicked.connect(
            lambda: self.start_thread(self.export_log)
            ) # Button event when pressed: exports log
        self.ui.systeminfo_back_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)
            ) # Back Button
        self.ui.grand_debugger_btn.clicked.connect(
            lambda: self.start_thread(self.debug_press)
            ) # Back Button

        # Edit Settings ------------
            # Buttons
        self.ui.irrigation_page_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.irrigation_page)
            ) # Button event when pressed: changes page to irrigation_page
        self.ui.datetime_page_btn.clicked.connect(
            self.update_datetime_page
            ) # Button event when pressed: changes page to datetime_page
        self.ui.editsettings_back_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)
            ) # Back Button

            # Sliders
        self.brightnesschanger = self.findChild(
            QSlider, "brightness_slider"
            ) # Finds QSlider object "brighness_slider" in Ui_Form
        self.brightnesschanger.valueChanged.connect(
            lambda: self.start_thread(self.change_brightness)
            ) # On a changed value from QSlider, calls function that writes to backlight text file

            #Brightness Label
        self.brightnesslabel = self.findChild(
            QLabel, "brightness_label"
            ) # Finds QLabel object "brighness_label" in Ui_Form
        self.brightnesslabel.setText(
            str(self.brightnesschanger.value())
            ) # Sets text of "brightness_label" to the value of the QSlider object

        # Manual Controls -----------
            # Buttons
        self.ui.fanon_btn.clicked.connect(
            lambda: self.start_thread(self.fan_toggle)
            ) # Button event when pressed: Debug press prints to console
        self.ui.lightswitch_btn.clicked.connect(
            lambda: self.start_thread(self.light_toggle)
            ) # Button event when pressed: Debug press prints to console
        self.ui.waternow_btn.clicked.connect(
            lambda: self.start_thread(self.water_toggle)
            ) # Button event when pressed: Initiate watering
        self.ui.watercycle_btn.clicked.connect(
            lambda: self.start_thread(self.water_cycle)
            ) # Button event when pressed: Initiate watering
        self.ui.takepicture_btn.clicked.connect(
            lambda: self.start_thread(self.take_picture)
            ) # Button event when pressed: Debug press prints to console
        self.ui.recorddata_btn.clicked.connect(
            lambda: self.start_thread(self.record_data)
            ) # Button event when pressed: Debug press prints to console
        self.ui.manualcontrols_back_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(
                self.ui.mainmenu_page)
            ) # Back Button

        # Monitor Data -------------
            # Buttons
        self.ui.monitordata_back_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)
            ) # Back Button

        # Irrigation ---------------
            # Buttons
        self.ui.wateringtime_page_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.watertiming_page)
            )
        self.ui.irrigation_save_btn.clicked.connect(
            lambda: self.start_thread(self.save_irr_settings)
            ) # Saves options set by QSlider objects
        self.ui.irrigation_back_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.editsettings_page)
            ) # Back Button

            # Water Volume Slider
        self.watervolume_changer = self.findChild(
            QSlider, "watervol_slider"
            ) # Finds QSlider object "watervol_slider" in Ui_Form
        self.watervolume_changer.setValue(
            int(cfg['PLANTCFG']['waterVol'])
            ) # Sets displayed value of slider to stored cfg value
        self.watervolume_changer.valueChanged.connect(
            self.change_watervolume
            ) # On a changed value from QSlider, calls function that writes to cfg

            # Moist Thresh Slider
        self.moistthresh_changer = self.findChild(
            QSlider, "moistthresh_slider"
            ) # Finds QSlider object "moistthresh_slider" in Ui_Form
        self.moistthresh_changer.setValue(
            int(cfg['PLANTCFG']['dryValue'])
            ) # Sets displayed value of slider to stored cfg value
        self.moistthresh_changer.valueChanged.connect(
            self.change_moistthresh
            ) # On a changed value from QSlider, calls function that writes to cfg

            # Temperature Set Slider
        self.tempset_changer = self.findChild(
            QSlider, "tempset_slider")
         # Finds QSlider object "tempset_slider" in Ui_Form
        self.tempset_changer.setValue(
            int(cfg['PLANTCFG']['maxTemp'])
            ) # Sets displayed value of slider to stored cfg value
        self.tempset_changer.valueChanged.connect(
            self.change_tempset)
         # On a changed value from QSlider, calls function that writes to cfg

            # Humid Set Slider
        self.humidset_changer = self.findChild(
            QSlider, "humidset_slider"
            ) # Finds QSlider object "humidset_slider" in Ui_Form
        self.humidset_changer.setValue(
            int(cfg['PLANTCFG']['maxHumid'])
            ) # Sets displayed value of slider to stored cfg value
        self.humidset_changer.valueChanged.connect(
            self.change_humidset
            ) # On a changed value from QSlider, calls function that writes to cfg

            # Water Volume Label
        self.watervolume_label = self.findChild(
            QLabel, "watervol_indicator"
            ) # Finds QLabel object "watervol_indicator" in Ui_Form
        self.watervolume_label.setText(
            str(self.watervolume_changer.value())
            ) # Sets text of "watervol_indicator" to the value of the QSlider object "watervolume_changer"

            # Moisture Threshold Label
        self.moistthresh_label = self.findChild(
            QLabel, "moistthresh_idicator"
            ) # Finds QLabel object "moistthresh_indicator" in Ui_Form
        self.moistthresh_label.setText(
            str(self.moistthresh_changer.value())
            ) # Sets text of "moistthreh_indicator" to the value of the QSlider object "moistthresh_changer"

            # Temperature Set Label
        self.tempset_label = self.findChild(
            QLabel, "tempset_indicator"
            ) # Finds QLabel object "tempset_indicator" in Ui_Form
        self.tempset_label.setText(
            str(self.tempset_changer.value())
            ) # Sets text of "tempset_indicator" to the value of the QSlider object "tempset_changer"

            # Humid Set Label
        self.humidset_label = self.findChild(
            QLabel, "humidset_indicator"
            ) # Finds QLabel object "humidset_indicator" in Ui_Form
        self.humidset_label.setText(
            str(self.humidset_changer.value())
            ) # Sets text of "humidset_indicator" to the value of the QSlider object "humidset_changer"

        # Water Timing -------------

            # Hour Label
        self.waterhours_label = self.findChild(
            QLabel, "waterhours_label"
            ) # Finds QLabel object "waterhours_label" in Ui_Form
            # Minute Label
        self.waterminutes_label = self.findChild(
            QLabel, "waterminutes_label"
            ) # Finds QLabel object "waterminutes_label" in Ui_Form

            # Buttons
            # Hour Plus
        self.ui.hoursplus_btn.clicked.connect(
            lambda: self.watertime_hourinput('plus')
            ) # increments hour of selected config time by one
            # Hour Minus
        self.ui.hoursminus_btn.clicked.connect(
            lambda: self.watertime_hourinput('minus')
            ) # increments hour of selected config time by one
            # Minute Plus
        self.ui.minutesplus_btn.clicked.connect(
            lambda: self.watertime_minuteinput('plus')
            ) # increments minute of selected config time by one
            # Minute Minus
        self.ui.minutesminus_btn.clicked.connect(
            lambda: self.watertime_minuteinput('minus')
            ) # increments minute of selected config time by one
            # Watertime Save
        self.ui.watertiming_save_btn.clicked.connect(
            lambda: self.start_thread(self.watertime_save(currentwatersave))
            ) # Saves current time to config
            # Check Time Select
        self.ui.checktime_btn.clicked.connect(
            lambda: self.watertime_select('checkTime')
            ) # Selects 'checkTime' for changing 

        self.ui.sunrise_btn.clicked.connect(
            lambda: self.watertime_select('sunrise')
            ) # Selects 'sunrise' for changing 
        
        self.ui.sunset_btn.clicked.connect(
            lambda: self.watertime_select('sunset')
            ) # Selects 'sunset' for changing 
        
        self.ui.watertiming_back_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.irrigation_page)
            ) # Back Button

        # Date/Time ----------------

            # Labels
        self.systemminutes_label = self.findChild(
            QLabel, "systemminutes_label"
        ) # System minutes label for current time

        self.systemhours_label = self.findChild(
            QLabel, "systemhours_label"
        ) # System hours label for current time

        self.systemyear_label = self.findChild(
            QLabel, "systemyear_label"
        ) # System year for current time

        self.systemmonth_label = self.findChild(
            QLabel, "systemmonth_label"
        ) # System month for current time

        self.systemday_label = self.findChild(
            QLabel, "systemday_label"
        ) # System day for current time


            # Buttons
        self.ui.systemhoursplus_btn.clicked.connect(
            lambda: self.systemtime_hourinput('plus')
            ) # Increments the system hour by one
        
        self.ui.systemhoursminus_btn.clicked.connect(
            lambda: self.systemtime_hourinput('minus')
            ) # Decrememnts the system hour by one
        
        self.ui.systemminutesplus_btn.clicked.connect(
            lambda: self.systemtime_minuteinput('plus')
            ) # Increments the system minutes by one
        
        self.ui.systemminutesminus_btn.clicked.connect(
            lambda: self.systemtime_minuteinput('minus')
            ) # Decrements the system minutes by one
        
        self.ui.systemyearplus_btn.clicked.connect(
            lambda: self.systemtime_yearinput('plus')
            ) # Increments the system year by one 

        self.ui.systemyearminus_btn.clicked.connect(
            lambda: self.systemtime_yearinput('minus')
            ) # Decrements the system year by one
        
        self.ui.systemmonthplus_btn.clicked.connect(
            lambda: self.systemtime_monthinput('plus')
            ) # Increments the system month by one
        
        self.ui.systemmonthminus_btn.clicked.connect(
            lambda: self.systemtime_monthinput('minus')
            ) # Decrements the system month by one
        
        self.ui.systemdayplus_btn.clicked.connect(
            lambda: self.systemtime_dayinput('plus')
            ) # Increments the system day by one
        
        self.ui.systemdayminus_btn.clicked.connect(
            lambda: self.systemtime_dayinput('minus')
            ) # Decrements the system day by one
        
        self.ui.systemtiming_save_btn.clicked.connect(
            self.save_system_time
            ) # Saves the current system time displayed to config

        self.ui.datetime_back_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.editsettings_page)
            ) # Back Button
        

##################################################
################# GUI FUNCTIONS ##################
##################################################

    def watertime_select(self, selection): # When a given time selection is requested for edit by the user, the corresponding label text changes
        global currentwatersave # Variable for interaction with watertime_save; whatever time is selected will be saved in that function
        cfg = config.read_config() # defines read_config
        currentwatersave = selection # Global variable is defined as the selection desired by the user
        try:
            if selection == 'checkTime':
                value = [int(x) for x in cfg['PLANTCFG']['checkTime'].split(",")] # Checks current value in PLANTCFG
                hour, minutes = value 
                self.ui.waterhours_label.setText(str(hour)) # Sets waterhours_label to hour found in config
                self.ui.waterminutes_label.setText(str(minutes)) # Sets waterminutes_label to hour found in config
                #self.debug_press
            elif selection == 'sunset':
                value = [int(x) for x in cfg['PLANTCFG']['sunset'].split(",")] # Checks current value in PLANTCFG
                hour, minutes = value
                self.ui.waterhours_label.setText(str(hour)) # Sets waterhours_label to hour found in config
                self.ui.waterminutes_label.setText(str(minutes)) # Sets waterminutes_label to hour found in config
                #self.debug_press
            elif selection == 'sunrise': 
                value = [int(x) for x in cfg['PLANTCFG']['sunrise'].split(",")] # Checks current value in PLANTCFG
                hour, minutes = value
                self.ui.waterhours_label.setText(str(hour)) # Sets waterhours_label to hour found in config
                self.ui.waterminutes_label.setText(str(minutes)) # Sets waterminutes_label to hour found in config
                #self.debug_press
            else:
                raise RuntimeError('UNKNOWN FAILURE') # If unknown option is selected
            
        except Exception as errvar:
            subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
            #LCD COLOUR HANDLING CODE (RED) HERE
            raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

    ### Water Timing

    @Slot()
    def watertime_save(self, currentwatersave): # Saves the current time 
        currenttime_str = f"{self.ui.waterhours_label.text()}, {self.ui.waterminutes_label.text()}" # Defines
        try:
            config.update_config('PLANTCFG', currentwatersave, currenttime_str)
            self.ui.statusbar_label.setText(
                QCoreApplication.tr("Water timing parameters saved!")
            )
            self.tasksleep(2)
            self.statusbar.setText(self.welcome_message())
        except Exception as errvar:
            subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
            #LCD COLOUR HANDLING CODE (RED) HERE
            raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

    def watertime_hourinput(self, increment): # Changes the hours in the watertime selection screen
        value = int(self.ui.waterhours_label.text())
        print(str(value))
        print(str(increment))
        if increment == 'plus':
            value = (value + 1) % 24
            print(str(value))
            self.ui.waterhours_label.setText(str(value))
        elif increment == 'minus':
            value = (value - 1) % 24
            print(str(value))
            self.ui.waterhours_label.setText(str(value))

    def watertime_minuteinput(self, increment): # Changes the minutes in the watertime selection screen
        value = int(self.ui.waterminutes_label.text())
        print(str(value))
        print(str(increment))
        if increment == 'plus':
            value = (value + 1) % 60
            print(str(value))
            self.ui.waterminutes_label.setText(str(value))
        elif increment == 'minus':
            value = (value - 1) % 60
            print(str(value))
            self.ui.waterminutes_label.setText(str(value))

    ### System Time

    def update_datetime_page(self):
        self.ui.pagelayoutwidget.setCurrentWidget(self.ui.datetime_page)
        now = datetime.now()
        self.systemminutes_label.setText(str(now.minute))
        self.systemhours_label.setText(str(now.hour))
        self.systemyear_label.setText(str(now.year))
        self.systemmonth_label.setText(str(now.month))
        self.systemday_label.setText(str(now.day))

    def systemtime_hourinput(self, increment): # Changes the hours in the watertime selection screen
        value = int(self.ui.systemhours_label.text())
        if increment == 'plus':
            value = (value + 1) % 24
            self.ui.systemhours_label.setText(str(value))
        elif increment == 'minus':
            value = (value - 1) % 24
            self.ui.systemhours_label.setText(str(value))

    def systemtime_minuteinput(self, increment): # Changes the hours in the watertime selection screen
        value = int(self.ui.systemminutes_label.text())
        if increment == 'plus':
            value = (value + 1) % 60
            self.ui.systemminutes_label.setText(str(value))
        elif increment == 'minus':
            value = (value - 1) % 60
            self.ui.systemminutes_label.setText(str(value))

    def systemtime_yearinput(self, increment): # Changes the hours in the watertime selection screen
        value = int(self.ui.systemyear_label.text())
        if increment == 'plus':
            value = min(value + 1, 2999)
            self.ui.systemyear_label.setText(str(value))
        elif increment == 'minus':
            value = max(value - 1, 2000) 
            self.ui.systemyear_label.setText(str(value))

    def systemtime_monthinput(self, increment): # Changes the hours in the watertime selection screen
        value = int(self.ui.systemmonth_label.text())
        if increment == 'plus':
            value = min(value + 1, 12)
            self.ui.systemmonth_label.setText(str(value))
        elif increment == 'minus':
            value = max(value - 1, 1) 
            self.ui.systemmonth_label.setText(str(value))

    def systemtime_dayinput(self, increment): # Changes the hours in the watertime selection screen
        value = int(self.ui.systemday_label.text())
        if increment == 'plus':
            value = min(value + 1, 31)
            self.ui.systemday_label.setText(str(value))
        elif increment == 'minus':
            value = max(value - 1, 1)
            self.ui.systemday_label.setText(str(value))

    def save_system_time(self):
        try:
            date_str = f"{self.ui.systemyear_label.text()}-{self.ui.systemmonth_label.text()}-{self.ui.systemday_label.text()}"
            time_str = f"{self.ui.systemhours_label.text()}:{self.ui.systemminutes_label.text()}"
            subprocess.run(f"echo grobot | sudo -S date -pyside6-lupdate main.py -ts example_de.tss \"{date_str} {time_str}\"", shell=True, check=True) #Needs \ to escape " as date and time string needs to be wrapped by "" for date -s
            subprocess.run("echo grobot | sudo -S hwclock -w", shell=True, check=True) #Write system date to RTC
            self.ui.statusbar_label.setText(
                QCoreApplication.tr("System Time Saved!")
            )
            self.tasksleep(2)
            self.statusbar.setText(self.welcome_message())

        except Exception as errvar:
            subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
            #LCD COLOUR HANDLING CODE (RED) HERE
            raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

    @Slot() # Decorator for multithreading
    def fan_toggle(self): # Function that toggles fan 
        if self.togglefan: # self.togglefan is False by default
            fanoff() # turns fan off
            print("Fan off") # prints to console
        else:
            fanmanon() # turns fan on (this is the manual variant, meaning it will stay on indefinetly)
            print("Fan on") # prints to console
        self.togglefan = not self.togglefan # resets self.togglefan to opposite of previous bool

    @Slot() # Decorator for multithreading
    def light_toggle(self): # Function that toggles growlight
        if self.togglelight: # self.togglefan is False by default
            growlightoff() # turns off growlight
            print("light off") # prints to console
        else:
            growlighton() # turns on fan
            print("Light on") # prints to console
        self.togglelight = not self.togglelight # resets self.togglelight to opposite of previous bool

    @Slot() # Decorator for multithreading
    def water_toggle(self): # Toggles whether the water pump is on indefinetly, or off
        self.statusbar.setText("Watering in Progress...") # changes text of statusbar to "Watering in Progress..."
        settings = get_plant_settings()
        mmrain = int(settings['waterVol'])
        autorain(mmrain)
        self.statusbar.setText("Stopped Watering!") # changes text of statusbar to "Stopped Watering"
        PumpRunDry = (readcsv_mainflags("PumpRunDry"))
        if int(PumpRunDry) == 1:
            self.waterstatuslabel.setText("Pump Dry")
            self.waterstatuslabel.setStyleSheet("color: red;")
        else:
            self.waterstatuslabel.setText("Water Det.")
            self.waterstatuslabel.setStyleSheet("color: navy;")
        self.tasksleep(2) # sleeps for 2 seconds
        self.statusbar.setText(self.welcome_message()) # resets statubsbar to default statusbar message

    @Slot() # Decorator for multithreading
    def water_cycle(self):
        self.statusbar.setText("Cycling Pump...")
        pumprefillcycle()
        self.statusbar.setText("Pump cycled!")
        PumpRunDry = (readcsv_mainflags("PumpRunDry"))
        if int(PumpRunDry) == 1:
            self.waterstatuslabel.setText("Pump Dry")
            self.waterstatuslabel.setStyleSheet("color: red;")
        else:
            self.waterstatuslabel.setText("Water Det.")
            self.waterstatuslabel.setStyleSheet("color: navy;")
        self.tasksleep(2)
        self.statusbar.setText(self.welcome_message())
        pass


    ### Time Display    

    def display_time(self): # Sets time from library datetime, and alters QLCD clock for time
        time = datetime.now() # time variable equal to a set datetime
        formatted_time = time.strftime("%H:%M:%S") # format of desired time
        self.clockdisplay.setText(str(formatted_time)) # changes QLCD to format of desired time

    def current_date(self):
        time = datetime.now()
        formatted_time = time.strftime("%Y/%m/%d")
        self.datedisplay.setText(str(formatted_time))

    ### Brightness Change    

    def change_brightness(self): # When called, changes brightness value of the touchscreen
        lumos_maxima = str(self.brightnesschanger.value()) # Defines "lumos_maxima" as string of QSlider value
        self.brightnesslabel.setText(lumos_maxima) # Sets text of "brightness_label" to lumos_maxima
        brightness_dir = '/sys/devices/platform/soc/3f205000.i2c/i2c-11/i2c-10/10-0045/backlight/10-0045/brightness' # Defines directory of brightness value in raspberry pi
        try:
            with open(brightness_dir, 'w') as csvfile: # Opens brightness directory to write
                csvfile.write(lumos_maxima) # Writes brightness value to directory
        except Exception as errvar:
            subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
            #LCD COLOUR HANDLING CODE (RED) HERE
            raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None
        
    def change_watervolume(self): # This function changes the text of the watervolume label to the value of the QSlider
        volume = str(self.watervolume_changer.value()) # Defines variable as QSlider value
        self.watervolume_label.setText(volume) # Sets text to QSlider value

    def change_moistthresh(self): # This function changes the text of the moistthresh label to the value of the QSlider
        moisture = str(self.moistthresh_changer.value()) # Defines variable as QSlider value
        self.moistthresh_label.setText(moisture) # Sets text to QSlider value

    def change_humidset(self): # This function changes the text of the humidset label to the value of the QSlider
        humidity = str(self.humidset_changer.value()) # Defines variable as QSlider value
        self.humidset_label.setText(humidity) # Sets text to QSlider value
         
    def change_tempset(self): # This function changes the text of the tempset label to the value of the QSlider
        temp = str(self.tempset_changer.value()) # Defines variable as QSlider value
        self.tempset_label.setText(temp) # Sets text to QSlider value

    @Slot()
    def save_irr_settings(self): # Saves values of QSlider object(s) to PLANTCFG
        try:
            config.update_config('PLANTCFG', 'waterVol', str(self.watervolume_changer.value())) # updates config with new value of watervolume slider
            config.update_config('PLANTCFG', 'dryValue', str(self.moistthresh_changer.value())) # updates config with new value of moisture threshold slider
            config.update_config('PLANTCFG', 'maxHumid', str(self.humidset_changer.value())) # updates config with new value of humid set slider
            config.update_config('PLANTCFG', 'maxTemp', str(self.tempset_changer.value())) # updates config with new value of temperature set slider
            self.statusbar.setText(
                QCoreApplication.tr("New Config Parameters Saved!")
             ) # changes text of statubs bar to "New Config Parameters Saved!"
            self.tasksleep(2) # sleeps for 2 seconds
            self.statusbar.setText(self.welcome_message()) # resets statubsbar to default statusbar message
        except Exception as errvar:
            subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True) # if there is an error writing to config, automatically reboots Grobot
            #LCD COLOUR HANDLING CODE (RED) HERE
            raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

    def tasksleep(self, duration): # Adds pause to a given process
        QApplication.processEvents() # Prompts the application to scan for events currently being processed
        time.sleep(duration) # Sleeps for a given duration

####################################################
################# DEBUG FUNCTIONS ##################
####################################################

    # def moisture_display(self): # Handles moisture output from adafruit SEESAW capacitive moisture sensors
    #     data1 = self.ss1.moisture_read() # defines "data1" as the output from I2C bus channel [0] and calls moisture detection
    #     data2 = self.ss2.moisture_read() # defines "data2" as the output from I2C bus channel [1] and calls moisture detection
    #     print("Moisture1:" + str(data1) + " Moisture2:" + str(data2)) # Prints moisture values
    #     self.sensor1.display(data1) # Sets value of "sensordisplay_1" to moisture value from channel [0]
    #     self.sensor2.display(data2) # Sets value of "sensordisplay_1" to moisture value from channel [1]

    def debug_press(self): # Simple function that prints to console if a button was pressed
        print("button pressed")
        self.ui.statusbar_label.setText("button pressed")
        diopinset()
        self.ui.statusbar_label.setText(
            QCoreApplication.tr("Button Pressed!")
        )
        self.tasksleep(2)
        self.ui.statusbar_label.setText(str(self.welcome_message()))

    def welcome_message(self): # Welcome message on status bar
        welcome_text = QCoreApplication.tr("Welcome!")
        return welcome_text

#######################################################
################# IMPORTED FUNCTIONS ##################
#######################################################

    @Slot()
    def record_data(self):
        try:
            #LCD COLOUR HANDLING CODE (BLUE) HERE  # Set LCD color to blue when in progress
            # Read value from sensor and write it out to excel
            # Read value from sensor
            ReadVal = feedread() # T RH SRH in order
            # Write data out to excel file
            excelout(ReadVal[0], ReadVal[1], ReadVal[2])
            self.ui.statusbar_label.setText(
                QCoreApplication.tr("Datapoint Taken!")
            )
            self.tasksleep(1)
            self.ui.statusbar_label.setText(self.welcome_message())
            
        except Exception as e:
            ###set_lcd_color("error")
            self.ui.statusbar_label.setText(
                QCoreApplication.tr("Error Reading Data")
            ) # Error Recording \n data
            self.tasksleep(2)
            ###set_lcd_color("normal")

    @Slot()
    def take_picture(self):
        try:
            ###set_lcd_color("in_progress")
            self.ui.statusbar_label.setText(
                QCoreApplication.tr("Taking Picture")
            ) # Taking Picture...
            # Don't check buttons during picture capture
            result = picam_capture()
            ###set_lcd_color("normal")
            self.tasksleep(2)
            if result:
                self.ui.statusbar_label.setText(
                    QCoreApplication.tr("Picture Taken!")
                )
            else:
                self.ui.statusbar_label.setText(
                    QCoreApplication.tr("Picture Failed")
                ) # Picture Taken, Picture Failed
            self.tasksleep(2)
            self.ui.statusbar_label.setText(self.welcome_message())
        except Exception as e:
            ###set_lcd_color("error")
            self.ui.statusbar_label.setText(f"Error: {e}") #Error:
            self.tasksleep(2)
            self.ui.statusbar_label.setText(self.welcome_message())
            ###set_lcd_color("normal")

    def get_version_info(self):
        """Get formatted version information string"""
        try:
            # Read from correct paths
            sw_version = readcsv_softver('software_version')  # From Software/code/softver
            fw_version = readcsv('fw_version')  # From Software/userdata/ulnoowegdat
            return f"SW Ver: {sw_version}\nFW Ver: {fw_version}"
        except Exception as e:
            return f"Error reading version info" # Error reading \n version info
   
    def update_firmware(self):
        """Handle firmware update process"""
        try:
            ###set_lcd_color("in_progress")  # Blue while updating
            self.statusbar.setText(
                QCoreApplication.tr("Updating Firmware")
            ) # Updating Firmware \n Please wait...
            print("Updating Firmware")
            self.tasksleep(2)
            # Call the firmware update function
            result = updatefw.grobotfwupdate()
            # Show result
            if result == 1:
                ###set_lcd_color("normal")  # Green for success
                self.statusbar.setText(
                    QCoreApplication.tr("Update Success! Restart Needed")
                ) # Update success! \n Restart needed
                self.tasksleep(2)
                while True:
                    ###set_lcd_color("error")
                    subprocess.run("echo grobot | sudo -S shutdown -r now", shell=True)
                    self.tasksleep(2)
                    pass
            else:
                ###set_lcd_color("error")  # Red for error
                self.statusbar.setText(
                    QCoreApplication.tr("Update Failed!")
                ) # Update failed! \n Press SELECT
                self.tasksleep(2)
                    
        except Exception as e:
            ###set_lcd_color("error")
            self.statusbar.setText(
                QCoreApplication.tr("Error Updating Firmware")
            ) # Error updating \n firmware
            self.tasksleep(2)
            ###set_lcd_color("normal")

    def export_log(self):
        """Handle log export process"""
        try:
            ###set_lcd_color("in_progress")  # Blue while exporting
            self.statusbar.setText(
                QCoreApplication.tr("Exporting Log...")
            ) # Exporting Log... \n Please Wait
            self.tasksleep(2)
            # Call logtofile function
            from logoutput import logtofile
            result = logtofile()
            feedread() # JUXTAPOSITION #### THIS IS A DEBUG CODE LINE
            
            # Show result
            if result == 1:
                ###set_lcd_color("normal")  # Green for success
                self.statusbar.setText(f"{readlocal('167')}\n{readlocal('168')}") # Log Exported \n successfully!
                self.tasksleep(2)
                self.statusbar.setText(self.welcome_message())
            else:
                ###set_lcd_color("error")  # Red for error
                self.statusbar.setText(f"{readlocal('169')}\n{readlocal('170')}") # Export failed! \n Try again
                self.tasksleep(2)
                self.statusbar.setText(self.welcome_message())
                
            self.tasksleep(2)  # Show result message
            ###set_lcd_color("normal")  # Return to normal color
            
        except Exception:
            ###set_lcd_color("error")
            self.statusbar.setText(f"{readlocal('171')}\n{readlocal('172')}") # Error exporting \n log file
            self.tasksleep(2)
            self.statusbar.setText(self.welcome_message())
            ###set_lcd_color("normal")

##############################################
################# MAIN.PY ####################
##############################################

    def EveryXX15(*args, **kwargs): # This schedule grouping runs at every quarter of hour
        try:
            settings = get_plant_settings()
            #LCD COLOUR HANDLING CODE (BLUE) HERE  # Set LCD color to blue when in progress

            # This should read value from sensor and turn fan on or off
            # Read value from sensor
            ReadVal = feedread() # T RH SRH in order

            # Turn on fan if temp or humidity exceeds the limit 
            if ReadVal[0] > settings['maxTemp'] or ReadVal[1] > settings['maxHumid']:
                fanon(settings['fanTime'])
            elif ReadVal[0] <= settings['maxTemp'] and ReadVal[1] <= settings['maxHumid']:
                pass
            else:
                raise RuntimeError('UKNOWN FAILURE')
            
            writecsv_mainflags("EveryXX15","0") #Set the execution flag for the function back to 0
            #LCD COLOUR HANDLING CODE (GREEN) HERE  # Set LCD color to green when done

        except Exception as errvar:
            subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
            #LCD COLOUR HANDLING CODE (RED) HERE
            raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

    def EverySETTIME(*args, **kwargs): # This runs every settime read from grobot_cfg
        try:
            settings = get_plant_settings()
            #LCD COLOUR HANDLING CODE (BLUE) HERE  # Set LCD color to blue when in progress

            # This should read value from sensor and autorain if Soil moisture too low
            # Read value from sensor
            ReadVal = feedread() # T RH SRH in order

            # Now water plant if soil too dry
            if ReadVal[2] <= settings['dryValue']:
                autorain(settings['waterVol'])
            elif ReadVal[2] > settings['dryValue']:
                pass
            else:
                raise RuntimeError('UKNOWN FAILURE')
            
            writecsv_mainflags("EverySETTIME","0") #Set the execution flag for the function back to 0
            #LCD COLOUR HANDLING CODE (GREEN) HERE  # Set LCD color to green when done

        except Exception as errvar:
            subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
            #LCD COLOUR HANDLING CODE (RED) HERE
            raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

    def EveryXX25(*args, **kwargs): # This code runs at every 25 minute mark of the hour
        try:
            #LCD COLOUR HANDLING CODE (BLUE) HERE  # Set LCD color to blue when in progress
            # Read value from sensor and write it out to excel
            # Read value from sensor
            ReadVal = feedread() # T RH SRH in order
            # Write data out to excel file
            excelout(ReadVal[0], ReadVal[1], ReadVal[2]) 

            writecsv_mainflags("EveryXX25","0") #Set the execution flag for the function back to 0
            #LCD COLOUR HANDLING CODE (GREEN) HERE  # Set LCD color to green when done

        except Exception as errvar:
            subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
            #LCD COLOUR HANDLING CODE (RED) HERE
            raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

    def EveryXX35(*args, **kwargs): # Runs every 35 minute mark of the hour
        try:
            #LCD COLOUR HANDLING CODE (BLUE) HERE  # Set LCD color to blue when in progress
            picam_capture() # Take picture with pi camera

            writecsv_mainflags("EveryXX35","0") #Set the execution flag for the function back to 0
            #LCD COLOUR HANDLING CODE (GREEN) HERE  # Set LCD color to green when done

        except Exception as errvar:
            subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
            #LCD COLOUR HANDLING CODE (RED) HERE
            raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

    def EverySUNRISE(*args, **kwargs): # This should run every sunrise time to turn on the light
        try:
            #LCD COLOUR HANDLING CODE (BLUE) HERE  # Set LCD color to blue when in progress
            growlighton()

            writecsv_mainflags("EverySUNRISE","0") #Set the execution flag for the function back to 0
            #LCD COLOUR HANDLING CODE (GREEN) HERE  # Set LCD color to green when done

        except Exception as errvar:
            subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
            #LCD COLOUR HANDLING CODE (RED) HERE
            raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

    def EverySUNSET(*args, **kwargs): # This should run every sunset time to turn off light
        try:
            #LCD COLOUR HANDLING CODE (BLUE) HERE  # Set LCD color to blue when in progress
            growlightoff()

            writecsv_mainflags("EverySUNSET","0") #Set the execution flag for the function back to 0
            #LCD COLOUR HANDLING CODE (GREEN) HERE  # Set LCD color to green when done

        except Exception as errvar:
            subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
            #LCD COLOUR HANDLING CODE (RED) HERE
            raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

##############################################
################# THREADING ##################
##############################################

    @Slot()
    def start_thread(self, fn):
        try:
            worker = Thread(fn)
            self.thread_manager.start(worker)
            activethreads = self.thread_manager.activeThreadCount()
            print(f"Current active threads:{activethreads}")
        except Exception as errvar:
            subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
            #LCD COLOUR HANDLING CODE (RED) HERE
            raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

    @Slot()
    def schedule_routine(self):
        while 1:
            try: #Put the entire try block under while loop. VERY IMPORTANT while must be the top level or it won't loop properly all the time
                settings = get_plant_settings() #Get plant settings so we have the proper set time to compare current time to

                #Get current time and put its component in separate variables
                currhour = datetime.now().hour
                currminute = datetime.now().minute
                currsecond = datetime.now().second
                print(f"Current time: (h:{currhour} m:{currminute})")

                #currtime = [datetime.now().hour, datetime.now().minute, datetime.now().second] #combine the variable together, not needed anymore

                # Now write the code to set execution flag for the appropriate function in mainflags file to 1 if the appropriate time is
                # reached such that the fuction will later be executed when mainflags is read back.
                # The first case only match function for minutes
                match currminute:
                    case 15:
                        writecsv_mainflags("EveryXX15","1")
                    case 25:
                        writecsv_mainflags("EveryXX25","1")
                    case 35:
                        self.start_thread(logtofile) #Write log immediately every 35 minutes
                        writecsv_mainflags("EveryXX35","1")
                    case _:
                        pass
                
                print("Wrote mainflags")
                
                # This one requires matching both hour and minute
                if currhour == settings['sunset'][0] and currminute == settings['sunset'][1]:
                    writecsv_mainflags("EverySUNSET","1")
                if currhour == settings['sunrise'][0] and currminute == settings['sunrise'][1]:
                    writecsv_mainflags("EverySUNRISE","1")
                if currhour == settings['checkTime'][0] and currminute == settings['checkTime'][1]:
                    writecsv_mainflags("EverySETTIME","1")

                # Now, read the mainflags file and execute any function that has its execution value = 1.
                # Make a list of functions. Need to use the actual function object such that they can be called later
                funcexecnamelist = [self.EveryXX15, self.EverySETTIME, self.EveryXX25, self.EveryXX35, self.EverySUNRISE, self.EverySUNSET]
                for funcexecname in funcexecnamelist: #iterate through the list funcexecnamelist using variable funcexecname
                    tempflagvalue = readcsv_mainflags(str(funcexecname.__name__)) #Read flag value for current function from csv
                    print("---------------------------")
                    if tempflagvalue == '1': #Check if flag value corresponding to function name provided by funcexecname variable match 1, if it does start the thread
                        print(f"Starting thread for {funcexecname.__name__}")
                        self.start_thread(funcexecname)
                    elif tempflagvalue == '0':
                        print(f"No current schedule for {funcexecname.__name__}")
                        pass
                    else:
                        raise RuntimeError('FUNCTION EXEC FLAG COMPARISON ERROR')

                #Implement logic to sleep until next tick
                currtickminute = datetime.now().minute
                print("---------------------------")

                if currtickminute == currminute: #If we are still in the same minute as initial time check, sleep until minute change
                    currticksecond = datetime.now().second #get current second
                    print("Datetime seconds defined")
                    tsleep = 61 - currticksecond #subtract current second from 61 to get seconds to sleep until next min
                    print(f"Sleeping for {tsleep} seconds...")
                    time.sleep(tsleep)
                elif currtickminute > currminute: #Immediately rerun loop if current tick is larger than initial time set during update
                    print("Current tick is larger than initial. Rerunning loop")
                    pass
                else:
                    raise RuntimeError('TIME EXCEPTION') #Time anomaly

            except Exception as errvar: #Catch any while loop exception
                subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
                #LCD COLOUR HANDLING CODE (RED) HERE
                raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

class Thread(QRunnable): # Thread class for creating an instance of QRunnable within QThreadpool
    def __init__(self, fn, *args, **kwargs): # Specifies an arbitrary number of positional and conditional arguments
        super().__init__() # Invokes constructor of the parent class
        self.fn = fn # Defines desired function to be run
        self.args = args # Defines arbitary positional arguments
        self.kwargs = kwargs # Defines arbitary named arguements
        # Listing arbitray number of arguments makes it easier for managing functions in the long term

    @Slot() # Decorator for multithreading
    def run(self): # Runs the aquired function from start_thread
        self.fn(*self.args, **self.kwargs) # Calls the function within the QRunnable instance

if __name__ == "__main__":
    app = QApplication(sys.argv)

    path = "/mnt/grobotextdat/code/fr.qm"
    translator = QTranslator(app)
    translator.load(path)
    app.installTranslator(translator)

    widget = Widget()
    widget.show()
    sys.exit(app.exec())
