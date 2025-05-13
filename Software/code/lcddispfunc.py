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
import adafruit_tca9548a    # Import the library for the Multiplexer board
from adafruit_seesaw.seesaw import Seesaw   # Import the library for the SEESAW capacitive moisture sensor
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLCDNumber
from PySide6.QtCore import QDateTime, QTimer, Slot, SIGNAL
from PySide6.QtGui import *
from datetime import datetime
from ui_form import Ui_Form
from logoutput import logtofile
from diopinsetup import diopinset
from watercontrol import autorain, stopwater, startwater

# configwin.py is for windows testing ONLY!
# from configwin import (
#     get_plant_settings, 
#     readcsv,
#     readlocal,
#     readcsv_softver
# )

# config.py is for linux.
import config
from config import (
   get_plant_settings, 
    readcsv,
    readlocal,
    readcsv_softver
)

diop = diopinset()
s1, s2, s3, s4, s5, s6, b1, ths, sms = diop[0], diop[1], diop[2], diop[3], diop[4], diop[5], diop[6], diop[7], diop[8]

# Global variables for manual override and watering state
manual_override = {
    "light": False,
    "fan": False,
    "watering": False
}

watering_active = False

if os.environ.get('DISPLAY','') == '': # Handles raspberry pi environment variable, for launching a python program on a display
    os.environ.__setitem__('DISPLAY', ':0.0')

class Widget(QWidget): # Creates a class containing attributes imported from ui_form.py
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(480, 640) # Sets resolution
        self.ui = Ui_Form() # defines UI
        self.ui.setupUi(self) # Imports setupUI from UI_Form which contains all objects such as QPushButtons, QSliders, QLabels, QCLD
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)

        self.toggle = False
        cfg = config.read_config()

    # Moisture Data Logic ------ Currently disabled

        #i2c_bus = board.I2C()  # uses board.SCL and board.SDA
        #i2c_bus = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

        #tca = adafruit_tca9548a.TCA9548A(i2c_bus)   # Initalizes Muxer board as the I2C Bus
        #self.ss1 = Seesaw(tca[0], addr=0x36) # Sets the first seesaw sensor address through the I2C Bus (TCA9548a), on channel 0
        #self.ss2 = Seesaw(tca[1], addr=0x36) # Sets the first seesaw sensor address through the I2C Bus (TCA9548a), on channel 1

### Button Functions & Label Logic ###

    # Progress Bar
        # Progress Bar Logic -------
        self.statusbar = self.findChild(
            QLabel, "statusbar_label"
            ) # Finds object QLabel "statusbar_label" in Ui_Form
        self.statusbar.setText(
            self.welcome_message()
            ) # Sets text of "statusbar_label" to welcome_message function

    # Primary Menus --------------------------------------------------------------------------------------------------------------

        # Start
            # Buttons
        self.ui.continue_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)
            ) # Button event when pressed: changes page to mainmenu_page
        self.ui.close_btn.clicked.connect(
            self.close_program
            ) # Button event when pressed: closes program

            # Moisture Display ---------
        #self.sensor1 = self.findChild(QLCDNumber, "sensordisplay_1") # Finds QLCDNumber object "sensordisplay_1" in Ui_Form
        #self.sensor1.setDigitCount(12) # Sets digit count to 12
        #self.sensor2 = self.findChild(QLCDNumber, "sensordisplay_2") # Finds QLCDNumber object "sensordisplay_2" in Ui_Form
        #self.sensor2.setDigitCount(12) # Sets digit count to 12

            # Clock Logic --------------
        self.clockdisplay = self.findChild(
            QLabel, "clockdisplay"
            ) # Finds QLCDNumber object "clockdisplay" in Ui_Form
        self.clockdisplay.setText(
            "Loading..."
            )
        
            # Timer --------------------
        self.timer = QTimer() # Defines QTimer
        self.timer.timeout.connect(
            self.display_time
            ) # Connects QTimer output to function display_time
        #self.timer.timeout.connect(self.moisture_display) # Connects QTimer output to function moisture_display
        self.timer.start(
            1000
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
            ) #Back

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
            self.update_firmware
            ) # Button event when pressed: calls update_firmware
        self.ui.logexport_page_btn.clicked.connect(
            self.export_log
            ) # Button event when pressed: exports log
        self.ui.systeminfo_back_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)
            ) #Back

        # Edit Settings ------------
            # Buttons
        self.ui.irrigation_page_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.irrigation_page)
            ) # Button event when pressed: changes page to irrigation_page
        self.ui.datetime_page_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.datetime_page)
            ) # Button event when pressed: changes page to datetime_page
        self.ui.editsettings_back_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)
            ) #Back

            # Sliders
        self.brightnesschanger = self.findChild(
            QSlider, "brightness_slider"
            ) # Finds QSlider object "brighness_slider" in Ui_Form
        self.brightnesschanger.valueChanged.connect(
            self.change_brightness
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
            self.debug_press
            ) # Button event when pressed: Debug press prints to console
        self.ui.lightswitch_btn.clicked.connect(
            self.debug_press
            ) # Button event when pressed: Debug press prints to console
        self.ui.waternow_btn.clicked.connect(
            self.water_toggle
            ) # Button event when pressed: Initiate watering
        self.ui.takepicture_btn.clicked.connect(
            self.debug_press
            ) # Button event when pressed: Debug press prints to console
        self.ui.recorddata_btn.clicked.connect(
            self.debug_press
            ) # Button event when pressed: Debug press prints to console
        self.ui.manualcontrols_back_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(
                self.ui.mainmenu_page)
            ) #Back

        # Monitor Data -------------
            # Buttons
        self.ui.monitordata_back_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)
            ) # Button event when pressed: changes page to mainmenu_page

        # Irrigation ---------------
            # Buttons
        self.ui.wateringtime_page_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.wateringtime_page)
            )
        self.ui.irrigation_save_btn.clicked.connect(
            self.save_irr_settings
            ) # Saves options set by QSlider objects
        self.ui.irrigation_back_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.editsettings_page)
            ) #Back

            # Sliders
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

            # Labels
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

        # Date/Time ----------------
            # Buttons
        self.ui.datetime_back_btn.clicked.connect(
            lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.editsettings_page)
            ) #Back

### GUI Functions

    def water_toggle(self): # Toggles whether the water pump is on indefinetly, or off
        if self.toggle:
            stopwater()
            self.statusbar.setText("Stopped Watering")
            self.tasksleep(2)
            self.statusbar.setText(self.welcome_message())
        else:
            self.statusbar.setText("Watering in Progress...")
            startwater()
        self.toggle = not self.toggle

    def display_time(self): # Sets time from library datetime, and alters QLCD clock for time
        time = datetime.now() # time variable equal to a set datetime
        formatted_time = time.strftime("%H:%M:%S") # format of desired time
        self.clockdisplay.setText(str(formatted_time)) # changes QLCD to format of desired time

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
    
    def save_irr_settings(self): # Saves values of QSlider object(s) to PLANTCFG
        try:
            config.update_config('PLANTCFG', 'waterVol', str(self.watervolume_changer.value()))
            config.update_config('PLANTCFG', 'dryValue', str(self.moistthresh_changer.value()))
            config.update_config('PLANTCFG', 'maxHumid', str(self.humidset_changer.value()))
            config.update_config('PLANTCFG', 'maxTemp', str(self.tempset_changer.value()))
            self.statusbar.setText("New Config Parameters Saved!")
            self.tasksleep(2)
            self.statusbar.setText(self.welcome_message())
        except Exception as errvar:
            subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
            #LCD COLOUR HANDLING CODE (RED) HERE
            raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None

    def tasksleep(self, duration): # Adds pause to a given process
        QApplication.processEvents() # Prompts the application to scan for events currently being processed
        time.sleep(duration) # Sleeps for a given duration

    def close_program(self): # Simple function to close the program
        exit()

    def adjust_system_time(self):
        pass

### Debug functions ------------------

    # def moisture_display(self): # Handles moisture output from adafruit SEESAW capacitive moisture sensors
    #     data1 = self.ss1.moisture_read() # defines "data1" as the output from I2C bus channel [0] and calls moisture detection
    #     data2 = self.ss2.moisture_read() # defines "data2" as the output from I2C bus channel [1] and calls moisture detection
    #     print("Moisture1:" + str(data1) + " Moisture2:" + str(data2)) # Prints moisture values
    #     self.sensor1.display(data1) # Sets value of "sensordisplay_1" to moisture value from channel [0]
    #     self.sensor2.display(data2) # Sets value of "sensordisplay_1" to moisture value from channel [1]

    def debug_press(self): # Simple function that prints to console if a button was pressed
        print("button pressed")

    def welcome_message(self): # Welcome message on status bar
        return str("Welcome!")

### Imported functions ---------------

    def get_version_info(self):
        """Get formatted version information string"""
        try:
            # Read from correct paths
            sw_version = readcsv_softver('software_version')  # From Software/code/softver
            fw_version = readcsv('fw_version')  # From Software/userdata/ulnoowegdat
            return f"SW Ver: {sw_version}\nFW Ver: {fw_version}"
        except Exception as e:
            return f"{readlocal('149')}\n{readlocal('160')}" # Error reading \n version info
   
    def update_firmware(self):
        """Handle firmware update process"""
        try:
            ###set_lcd_color("in_progress")  # Blue while updating
            self.statusbar.setText("Updating Firmware") # Updating Firmware \n Please wait...
            print("Updating Firmware")
            self.tasksleep(2)
            # Call the firmware update function
            result = updatefw.grobotfwupdate()
            # Show result
            if result == 1:
                ###set_lcd_color("normal")  # Green for success
                self.statusbar.setText(f"{readlocal('175')}\n{readlocal('176')}") # Update success! \n Restart needed
                print("Updating Success!")
                self.tasksleep(2)
                while True:
                    ###set_lcd_color("error")
                    print("Restarting")
                    subprocess.run("echo grobot | sudo -S shutdown -r now", shell=True)
                    self.tasksleep(2)
                    pass
            else:
                ###set_lcd_color("error")  # Red for error
                self.statusbar.setText(f"{readlocal('179')}\n{readlocal('180')}") # Update failed! \n Press SELECT
                print("Update Failed")
                self.tasksleep(2)
                    
        except Exception as e:
            ###set_lcd_color("error")
            self.statusbar.setText(f"{readlocal('181')}\n{readlocal('182')}") # Error updating \n firmware
            print("Error Updating")
            self.tasksleep(2)
            ###set_lcd_color("normal")

    def export_log(self):
        """Handle log export process"""
            
        try:
            ###set_lcd_color("in_progress")  # Blue while exporting
            self.statusbar.setText(f"{readlocal('165')}\n{readlocal('166')}") # Exporting Log... \n Please Wait
            self.tasksleep(2)
            # Call logtofile function
            from logoutput import logtofile
            result = logtofile()
            
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
            
        except Exception as e:
            ###set_lcd_color("error")
            self.statusbar.setText(f"{readlocal('171')}\n{readlocal('172')}") # Error exporting \n log file
            self.tasksleep(2)
            self.statusbar.setText(self.welcome_message())
            ###set_lcd_color("normal")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
