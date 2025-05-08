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
import subprocess
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLCDNumber
from PySide6.QtCore import QDateTime, QTimer, Slot, SIGNAL
from PySide6.QtGui import *
from datetime import datetime
from ui_form import Ui_Form

# configwin.py is for windows testing ONLY!
# from configwin import (
#     get_plant_settings, 
#     readcsv,
#     readlocal,
#     readcsv_softver
# )

# config.py is for linux.
from config import (
   get_plant_settings, 
    readcsv,
    readlocal,
    readcsv_softver
)

#time.sleep(1)
#print("Hello world!")
#time.sleep(2)

if os.environ.get('DISPLAY','') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(480, 640)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    ### Button Functions & Label Logic ###

    # Progress Bar
        # Progress Bar Logic -------
        self.statusbar = self.findChild(QLabel, "statusbar_label")
        self.statusbar.setText("Welcome! :)")

    # Primary Menus --------------------------------------------------------------------------------------------------------------

        # Start
            # Buttons
        self.ui.continue_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page))
        self.ui.close_btn.clicked.connect(self.close_program)

        # Main Menu ----------------
                # Buttons
        self.ui.systeminfo_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.systeminfo_page))
        self.ui.editsettings_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.editsettings_page))
        self.ui.manualcontrols_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.manualcontrols_page))
        self.ui.monitordata_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.monitordata_page))
        self.ui.mainmenu_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.start_page)) #Back

        # System Info --------------
            # System Version Label
        self.systemversionlabel = self.findChild(QLabel, "systemversion_label")
        self.systemversionlabel.setText(f"{self.get_version_info()}") # Fetches system versions from config

            # Buttons
        self.ui.updatefirmware_page_btn.clicked.connect(self.update_firmware)
        self.ui.logexport_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.logexport_page))
        self.ui.systeminfo_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)) #Back

        # Edit Settings ------------
            # Buttons
        self.ui.irrigation_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.irrigation_page))
        self.ui.datetime_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.datetime_page))
        self.ui.editsettings_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)) #Back

        # Manual Controls -----------
            # Buttons
        self.ui.fanon_btn.clicked.connect(self.debug_press)
        self.ui.lightswitch_btn.clicked.connect(self.debug_press)
        self.ui.waternow_btn.clicked.connect(self.debug_press)
        self.ui.takepicture_btn.clicked.connect(self.debug_press)
        self.ui.recorddata_btn.clicked.connect(self.debug_press)
        self.ui.manualcontrols_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)) #Back

        # Monitor Data -------------
            # Buttons
        self.ui.monitordata_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page))

        # Irrigation ---------------
            # Buttons
        self.ui.irrigation_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.irrigation_page))
        self.ui.irrigation_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.editsettings_page)) #Back

        # Date/Time ----------------
            # Buttons
        self.ui.datetime_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.editsettings_page)) #Back

        # Moisture Display Logic ---
        sensor1 = self.findChild(QLCDNumber, "sensordisplay_1")
        sensor1.display(1)

        # Clock Logic --------------
        self.lcd = self.findChild(QLCDNumber, "clockdisplay")
        self.lcd.setDigitCount(12)
        
        # Timer --------------------
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_time)
        self.timer.start(1000)

    def display_time(self):
        time = datetime.now()
        formatted_time = time.strftime("%H:%M:%S")

        self.lcd.display(formatted_time)

    def debug_press(self):
        print("button pressed")

    def close_program(self):
        exit()

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
            self.statusbar.setText(f"{readlocal('173')}\n{readlocal('174')}") # Updating Firmware \n Please wait...
            print("Updating Firmware")
            time.sleep(2)
            # Call the firmware update function
            result = updatefw.grobotfwupdate()
            # Show result
            if result == 1:
                ###set_lcd_color("normal")  # Green for success
                self.statusbar.setText(f"{readlocal('175')}\n{readlocal('176')}") # Update success! \n Restart needed
                print("Updating Success!")
                time.sleep(2)
                while True:
                    ###set_lcd_color("error")
                    print("Restarting")
                    subprocess.run("echo grobot | sudo -S shutdown -r now", shell=True)
                    time.sleep(2)
                    pass
            else:
                ###set_lcd_color("error")  # Red for error
                self.statusbar.setText(f"{readlocal('179')}\n{readlocal('180')}") # Update failed! \n Press SELECT
                print("Update Failed")
                time.sleep(2)
                    
        except Exception as e:
            ###set_lcd_color("error")
            self.statusbar.setText(f"{readlocal('181')}\n{readlocal('182')}") # Error updating \n firmware
            print("Error Updating")
            time.sleep(2)
            ###set_lcd_color("normal")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
