# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLCDNumber
from PySide6.QtCore import QDateTime, QTimer, Slot, SIGNAL
from PySide6.QtGui import *
from datetime import datetime
from ui_form import Ui_Form
from config import (
    get_plant_settings, 
    readcsv,
    readlocal,
    readcsv_softver
)

if os.environ.get('DISPLAY','') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(480, 640)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    ### Button Functions & Label Logic ###
    # Primary Menus --------------------------------------------------------------------------------------------------------------

        # Start
        self.ui.continue_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page))
        self.ui.close_btn.clicked.connect(self.close_program)

        # Main Menu ----------------
        self.ui.systeminfo_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.systeminfo_page))
        self.ui.editsettings_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.editsettings_page))
        self.ui.manualcontrols_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.manualcontrols_page))
        self.ui.monitordata_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.monitordata_page))
        self.ui.mainmenu_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.start_page)) #Back

        # System Info --------------

             # System Version Label
        systemversion = self.findChild(QLabel, "systemversion")
        systemversion.setText("Test")

        self.ui.updatefirmware_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.updatefirmware_page))
        self.ui.logexport_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.logexport_page))
        self.ui.systeminfo_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)) #Back

        # Edit Settings ------------
        self.ui.irrigation_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.irrigation_page))
        self.ui.datetime_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.datetime_page))
        self.ui.editsettings_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)) #Back

        # Manual Controls -----------
        self.ui.fanon_btn.clicked.connect(self.debug_press)
        self.ui.lightswitch_btn.clicked.connect(self.debug_press)
        self.ui.waternow_btn.clicked.connect(self.debug_press)
        self.ui.takepicture_btn.clicked.connect(self.debug_press)
        self.ui.recorddata_btn.clicked.connect(self.debug_press)
        self.ui.manualcontrols_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)) #Back

        # Monitor Data -------------
        self.ui.monitordata_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page))

        # Irrigation ---------------
        self.ui.irrigation_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.irrigation_page))
        self.ui.irrigation_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.editsettings_page)) #Back

        # Date/Time ----------------
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

    def get_version_info():
        """Get formatted version information string"""
        try:
            # Read from correct paths
            sw_version = readcsv_softver('software_version')  # From Software/code/softver
            fw_version = readcsv('fw_version')  # From Software/userdata/ulnoowegdat
            return f"SW Ver: {sw_version}\nFW Ver: {fw_version}"
        except Exception as e:
            return f"{readlocal('149')}\n{readlocal('160')}" # Error reading \n version info

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
