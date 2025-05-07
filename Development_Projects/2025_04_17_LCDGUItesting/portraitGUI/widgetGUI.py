# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLCDNumber
from PySide6.QtCore import QDateTime, QTimer, Slot, SIGNAL
from PySide6.QtGui import *
from datetime import datetime

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Form

if os.environ.get('DISPLAY','') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(480, 640)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    ### Button Functions ###
    # Primary Menus --------------------------------------------------------------------------------------------------------------

        # Start
        self.ui.continue_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page))

        # Main Menu ----------------
        self.ui.systeminfo_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.systeminfo_page))
        self.ui.editsettings_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.editsettings_page))
        self.ui.manualcontrols_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.manualcontrols_page))
        self.ui.monitordata_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.monitordata_page))
        self.ui.mainmenu_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.start_page)) #Back

        # System Info --------------
        self.ui.systemversion_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.systemversion_page))
        self.ui.updatefirmware_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.updatefirmware_page))
        self.ui.logexport_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.logexport_page))
        self.ui.systeminfo_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)) #Back

        # Edit Settings ------------
        self.ui.irrigation_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.irrigation_page))
        self.ui.datetime_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.datetime_page))
        self.ui.editsettings_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page)) #Back

        # Manual Controls -----------
        #self.ui.fanon_btn.clicked.connect()
        #self.ui.lightswitch_btn.clicked.connect()
        #self.ui.waternow_btn.clicked.connect()
        #self.ui.takepicture_btn.clicked.connect()
        #self.ui.recorddata_btn.clicked.connect()
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
        
        # Global Clock -------------
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_time)
        self.timer.start(1000)

    def display_time(self):
        time = datetime.now()
        formatted_time = time.strftime("%H:%M:%S")

        self.lcd.display(formatted_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
