# This Python file uses the following encoding: utf-8
import sys
import os
from datetime import datetime
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLCDNumber
from PySide6.QtCore import QTime, QTimer, Slot
from PySide6.QtGui import *

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

if os.environ.get('DISPLAY','') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(800, 480)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

    ### Button Functions ###
    # Primary Menus --------------------------------------------------------------------------------------------------------------

        # Main Menu ----------------
        self.ui.systeminfo_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.systeminfo_page))
        self.ui.editsettings_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.editsettings_page))
        self.ui.manualcontrol_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.manualcontrol_page))
        self.ui.monitordata_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.monitordata_page))

        # System Info --------------
        self.ui.systeminfo_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page))

        # Edit Settings ------------
        self.ui.irrigation_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.irrigation_page))
        self.ui.editsettings_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page))

        # Manual Control -----------
        self.ui.manualcontrol_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page))

        # Monitor Data -------------
        self.ui.monitordata_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.mainmenu_page))

    ### Sub Menus -------------------------------------------------------------------------------------------------------------------

        # Irrigation ---------------
        self.ui.irrigation_page_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.irrigation_page))
        self.ui.irrigation_back_btn.clicked.connect(lambda: self.ui.pagelayoutwidget.setCurrentWidget(self.ui.editsettings_page))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
