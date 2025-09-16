# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formtiVMiV.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QPushButton,
    QSizePolicy, QSlider, QStackedWidget, QWidget)

from pyqtgraph import PlotWidget

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(484, 647)
        font = QFont()
        font.setFamilies([u"TikTok Sans 28pt"])
        Form.setFont(font)
        self.pagelayoutwidget = QStackedWidget(Form)
        self.pagelayoutwidget.setObjectName(u"pagelayoutwidget")
        self.pagelayoutwidget.setGeometry(QRect(0, 70, 480, 570))
        font1 = QFont()
        font1.setFamilies([u"TikTok Sans 28pt"])
        font1.setBold(False)
        self.pagelayoutwidget.setFont(font1)
        self.pagelayoutwidget.setStyleSheet(u"QStackedWidget{\n"
"	background-color: rgb(226, 255, 229);\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.start_page = QWidget()
        self.start_page.setObjectName(u"start_page")
        self.continue_btn = QPushButton(self.start_page)
        self.continue_btn.setObjectName(u"continue_btn")
        self.continue_btn.setGeometry(QRect(130, 380, 221, 170))
        font2 = QFont()
        font2.setFamilies([u"TikTok Sans 28pt"])
        font2.setPointSize(18)
        font2.setBold(False)
        self.continue_btn.setFont(font2)
        self.continue_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: white;\n"
"}")
        self.clockdisplay = QLabel(self.start_page)
        self.clockdisplay.setObjectName(u"clockdisplay")
        self.clockdisplay.setGeometry(QRect(0, 50, 471, 131))
        font3 = QFont()
        font3.setFamilies([u"TikTok Sans 28pt"])
        font3.setPointSize(47)
        font3.setBold(True)
        self.clockdisplay.setFont(font3)
        self.clockdisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label = QLabel(self.start_page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(170, 176, 151, 31))
        self.label.setFont(font2)
        self.Datedisplay = QLabel(self.start_page)
        self.Datedisplay.setObjectName(u"Datedisplay")
        self.Datedisplay.setGeometry(QRect(0, 196, 471, 131))
        font4 = QFont()
        font4.setFamilies([u"Myriad Pro"])
        font4.setPointSize(47)
        font4.setBold(True)
        self.Datedisplay.setFont(font4)
        self.Datedisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pagelayoutwidget.addWidget(self.start_page)
        self.mainmenu_page = QWidget()
        self.mainmenu_page.setObjectName(u"mainmenu_page")
        self.systeminfo_page_btn = QPushButton(self.mainmenu_page)
        self.systeminfo_page_btn.setObjectName(u"systeminfo_page_btn")
        self.systeminfo_page_btn.setGeometry(QRect(10, 10, 201, 151))
        self.systeminfo_page_btn.setFont(font2)
        self.systeminfo_page_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.editsettings_page_btn = QPushButton(self.mainmenu_page)
        self.editsettings_page_btn.setObjectName(u"editsettings_page_btn")
        self.editsettings_page_btn.setGeometry(QRect(260, 10, 201, 151))
        self.editsettings_page_btn.setFont(font2)
        self.editsettings_page_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.mainmenu_back_btn = QPushButton(self.mainmenu_page)
        self.mainmenu_back_btn.setObjectName(u"mainmenu_back_btn")
        self.mainmenu_back_btn.setGeometry(QRect(10, 330, 201, 151))
        self.mainmenu_back_btn.setFont(font2)
        self.mainmenu_back_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-3, y1:0, x2:2, y2:0, stop:0 white, stop:1 #ed7a2a);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.manualcontrols_page_btn = QPushButton(self.mainmenu_page)
        self.manualcontrols_page_btn.setObjectName(u"manualcontrols_page_btn")
        self.manualcontrols_page_btn.setGeometry(QRect(10, 170, 201, 151))
        self.manualcontrols_page_btn.setFont(font2)
        self.manualcontrols_page_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.monitordata_page_btn = QPushButton(self.mainmenu_page)
        self.monitordata_page_btn.setObjectName(u"monitordata_page_btn")
        self.monitordata_page_btn.setGeometry(QRect(260, 170, 201, 151))
        self.monitordata_page_btn.setFont(font2)
        self.monitordata_page_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.pagelayoutwidget.addWidget(self.mainmenu_page)
        self.monitordata_page = QWidget()
        self.monitordata_page.setObjectName(u"monitordata_page")
        self.monitordata_back_btn = QPushButton(self.monitordata_page)
        self.monitordata_back_btn.setObjectName(u"monitordata_back_btn")
        self.monitordata_back_btn.setGeometry(QRect(315, 450, 151, 101))
        self.monitordata_back_btn.setFont(font2)
        self.monitordata_back_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-3, y1:0, x2:2, y2:0, stop:0 white, stop:1 #ed7a2a);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.graphwindow = PlotWidget(self.monitordata_page)
        self.graphwindow.setObjectName(u"graphwindow")
        self.graphwindow.setGeometry(QRect(0, 5, 241, 218))
        self.monitordata_update_btn = QPushButton(self.monitordata_page)
        self.monitordata_update_btn.setObjectName(u"monitordata_update_btn")
        self.monitordata_update_btn.setGeometry(QRect(5, 450, 151, 101))
        self.monitordata_update_btn.setFont(font2)
        self.monitordata_update_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-3, y1:0, x2:2, y2:0, stop:0 white, stop:1 #ed7a2a);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.graphwindow_2 = PlotWidget(self.monitordata_page)
        self.graphwindow_2.setObjectName(u"graphwindow_2")
        self.graphwindow_2.setGeometry(QRect(240, 5, 231, 218))
        self.graphwindow_3 = PlotWidget(self.monitordata_page)
        self.graphwindow_3.setObjectName(u"graphwindow_3")
        self.graphwindow_3.setGeometry(QRect(0, 220, 241, 218))
        self.monitordata_data_label = QLabel(self.monitordata_page)
        self.monitordata_data_label.setObjectName(u"monitordata_data_label")
        self.monitordata_data_label.setGeometry(QRect(250, 230, 211, 111))
        font5 = QFont()
        font5.setFamilies([u"TikTok Sans 28pt"])
        font5.setPointSize(13)
        self.monitordata_data_label.setFont(font5)
        self.monitordata_data_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.graphdomain_slider = QSlider(self.monitordata_page)
        self.graphdomain_slider.setObjectName(u"graphdomain_slider")
        self.graphdomain_slider.setGeometry(QRect(250, 370, 211, 68))
        self.graphdomain_slider.setStyleSheet(u".QSlider {\n"
"    min-height: 68px;\n"
"    max-height: 68px;\n"
"}\n"
"\n"
".QSlider::groove:horizontal {\n"
"	border-radius: 5px;\n"
"    border: 3px solid #262626;\n"
"    height: 5px;\n"
"    margin: 0 12px;\n"
"}\n"
"\n"
".QSlider::handle:horizontal {\n"
"    background: Grey;\n"
"	border-radius: 10px;\n"
"    width: 46px;\n"
"    height: 100px;\n"
"	margin: -24px -12px\n"
"}")
        self.graphdomain_slider.setMinimum(10)
        self.graphdomain_slider.setMaximum(100)
        self.graphdomain_slider.setOrientation(Qt.Orientation.Horizontal)
        self.graphdomain_label = QLabel(self.monitordata_page)
        self.graphdomain_label.setObjectName(u"graphdomain_label")
        self.graphdomain_label.setGeometry(QRect(250, 350, 211, 21))
        font6 = QFont()
        font6.setFamilies([u"TikTok Sans"])
        font6.setPointSize(13)
        self.graphdomain_label.setFont(font6)
        self.graphdomain_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitordata_live_btn = QPushButton(self.monitordata_page)
        self.monitordata_live_btn.setObjectName(u"monitordata_live_btn")
        self.monitordata_live_btn.setGeometry(QRect(160, 450, 151, 101))
        self.monitordata_live_btn.setFont(font2)
        self.monitordata_live_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-3, y1:0, x2:2, y2:0, stop:0 white, stop:1 #ed7a2a);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.pagelayoutwidget.addWidget(self.monitordata_page)
        self.manualcontrols_page = QWidget()
        self.manualcontrols_page.setObjectName(u"manualcontrols_page")
        self.waternow_btn = QPushButton(self.manualcontrols_page)
        self.waternow_btn.setObjectName(u"waternow_btn")
        self.waternow_btn.setGeometry(QRect(10, 10, 141, 151))
        self.waternow_btn.setFont(font2)
        self.waternow_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 rgb(170, 255, 255));\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.lightswitch_btn = QPushButton(self.manualcontrols_page)
        self.lightswitch_btn.setObjectName(u"lightswitch_btn")
        self.lightswitch_btn.setGeometry(QRect(320, 10, 141, 151))
        self.lightswitch_btn.setFont(font2)
        self.lightswitch_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 #f7b329);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.fanon_btn = QPushButton(self.manualcontrols_page)
        self.fanon_btn.setObjectName(u"fanon_btn")
        self.fanon_btn.setGeometry(QRect(10, 170, 201, 151))
        self.fanon_btn.setFont(font2)
        self.fanon_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.takepicture_btn = QPushButton(self.manualcontrols_page)
        self.takepicture_btn.setObjectName(u"takepicture_btn")
        self.takepicture_btn.setGeometry(QRect(260, 170, 201, 151))
        self.takepicture_btn.setFont(font2)
        self.takepicture_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.recorddata_btn = QPushButton(self.manualcontrols_page)
        self.recorddata_btn.setObjectName(u"recorddata_btn")
        self.recorddata_btn.setGeometry(QRect(10, 330, 201, 151))
        self.recorddata_btn.setFont(font2)
        self.recorddata_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.manualcontrols_back_btn = QPushButton(self.manualcontrols_page)
        self.manualcontrols_back_btn.setObjectName(u"manualcontrols_back_btn")
        self.manualcontrols_back_btn.setGeometry(QRect(260, 330, 201, 151))
        self.manualcontrols_back_btn.setFont(font2)
        self.manualcontrols_back_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-3, y1:0, x2:2, y2:0, stop:0 white, stop:1 #ed7a2a);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.watercycle_btn = QPushButton(self.manualcontrols_page)
        self.watercycle_btn.setObjectName(u"watercycle_btn")
        self.watercycle_btn.setGeometry(QRect(160, 10, 151, 151))
        self.watercycle_btn.setFont(font2)
        self.watercycle_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.pagelayoutwidget.addWidget(self.manualcontrols_page)
        self.systeminfo_page = QWidget()
        self.systeminfo_page.setObjectName(u"systeminfo_page")
        self.updatefirmware_page_btn = QPushButton(self.systeminfo_page)
        self.updatefirmware_page_btn.setObjectName(u"updatefirmware_page_btn")
        self.updatefirmware_page_btn.setGeometry(QRect(10, 10, 201, 151))
        self.updatefirmware_page_btn.setFont(font2)
        self.updatefirmware_page_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.logexport_page_btn = QPushButton(self.systeminfo_page)
        self.logexport_page_btn.setObjectName(u"logexport_page_btn")
        self.logexport_page_btn.setGeometry(QRect(260, 10, 201, 151))
        self.logexport_page_btn.setFont(font2)
        self.logexport_page_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.systeminfo_back_btn = QPushButton(self.systeminfo_page)
        self.systeminfo_back_btn.setObjectName(u"systeminfo_back_btn")
        self.systeminfo_back_btn.setGeometry(QRect(10, 170, 201, 151))
        self.systeminfo_back_btn.setFont(font2)
        self.systeminfo_back_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-3, y1:0, x2:2, y2:0, stop:0 white, stop:1 #ed7a2a);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.systemversion_label = QLabel(self.systeminfo_page)
        self.systemversion_label.setObjectName(u"systemversion_label")
        self.systemversion_label.setGeometry(QRect(10, 330, 451, 61))
        font7 = QFont()
        font7.setFamilies([u"TikTok Sans 28pt"])
        font7.setPointSize(17)
        font7.setBold(False)
        self.systemversion_label.setFont(font7)
        self.pagelayoutwidget.addWidget(self.systeminfo_page)
        self.editsettings_page = QWidget()
        self.editsettings_page.setObjectName(u"editsettings_page")
        self.irrigation_page_btn = QPushButton(self.editsettings_page)
        self.irrigation_page_btn.setObjectName(u"irrigation_page_btn")
        self.irrigation_page_btn.setGeometry(QRect(260, 10, 201, 151))
        self.irrigation_page_btn.setFont(font2)
        self.irrigation_page_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.editsettings_back_btn = QPushButton(self.editsettings_page)
        self.editsettings_back_btn.setObjectName(u"editsettings_back_btn")
        self.editsettings_back_btn.setGeometry(QRect(260, 170, 201, 151))
        self.editsettings_back_btn.setFont(font2)
        self.editsettings_back_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-3, y1:0, x2:2, y2:0, stop:0 white, stop:1 #ed7a2a);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: white;\n"
"}")
        self.editsettings_back_btn.setFlat(False)
        self.datetime_page_btn = QPushButton(self.editsettings_page)
        self.datetime_page_btn.setObjectName(u"datetime_page_btn")
        self.datetime_page_btn.setGeometry(QRect(10, 10, 201, 151))
        self.datetime_page_btn.setFont(font2)
        self.datetime_page_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.brightness_slider = QSlider(self.editsettings_page)
        self.brightness_slider.setObjectName(u"brightness_slider")
        self.brightness_slider.setGeometry(QRect(20, 330, 441, 68))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.brightness_slider.sizePolicy().hasHeightForWidth())
        self.brightness_slider.setSizePolicy(sizePolicy)
        font8 = QFont()
        font8.setFamilies([u"TikTok Sans 28pt"])
        font8.setPointSize(10)
        font8.setBold(False)
        self.brightness_slider.setFont(font8)
        self.brightness_slider.setStyleSheet(u".QSlider {\n"
"    min-height: 68px;\n"
"    max-height: 68px;\n"
"}\n"
"\n"
".QSlider::groove:horizontal {\n"
"	border-radius: 5px;\n"
"    border: 3px solid #262626;\n"
"    height: 5px;\n"
"    margin: 0 12px;\n"
"}\n"
"\n"
".QSlider::handle:horizontal {\n"
"    background: Grey;\n"
"	border-radius: 10px;\n"
"    width: 46px;\n"
"    height: 100px;\n"
"	margin: -24px -12px\n"
"}")
        self.brightness_slider.setMinimum(25)
        self.brightness_slider.setMaximum(255)
        self.brightness_slider.setValue(150)
        self.brightness_slider.setOrientation(Qt.Orientation.Horizontal)
        self.brightness_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.brightness_slider.setTickInterval(10)
        self.brightness_label = QLabel(self.editsettings_page)
        self.brightness_label.setObjectName(u"brightness_label")
        self.brightness_label.setGeometry(QRect(170, 380, 201, 61))
        font9 = QFont()
        font9.setFamilies([u"TikTok Sans 28pt"])
        font9.setPointSize(20)
        font9.setBold(False)
        self.brightness_label.setFont(font9)
        self.brightness_label_2 = QLabel(self.editsettings_page)
        self.brightness_label_2.setObjectName(u"brightness_label_2")
        self.brightness_label_2.setGeometry(QRect(30, 380, 201, 61))
        self.brightness_label_2.setFont(font9)
        self.pagelayoutwidget.addWidget(self.editsettings_page)
        self.datetime_page = QWidget()
        self.datetime_page.setObjectName(u"datetime_page")
        self.datetime_page.setStyleSheet(u"")
        self.datetime_back_btn = QPushButton(self.datetime_page)
        self.datetime_back_btn.setObjectName(u"datetime_back_btn")
        self.datetime_back_btn.setGeometry(QRect(260, 450, 201, 91))
        self.datetime_back_btn.setFont(font2)
        self.datetime_back_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-3, y1:0, x2:2, y2:0, stop:0 white, stop:1 #ed7a2a);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.systemhours_label = QLabel(self.datetime_page)
        self.systemhours_label.setObjectName(u"systemhours_label")
        self.systemhours_label.setGeometry(QRect(130, 80, 91, 111))
        font10 = QFont()
        font10.setFamilies([u"Myriad Pro"])
        font10.setPointSize(50)
        font10.setBold(True)
        self.systemhours_label.setFont(font10)
        self.systemhours_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timesep_label_2 = QLabel(self.datetime_page)
        self.timesep_label_2.setObjectName(u"timesep_label_2")
        self.timesep_label_2.setGeometry(QRect(220, 80, 21, 111))
        self.timesep_label_2.setFont(font10)
        self.timesep_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.systemminutes_label = QLabel(self.datetime_page)
        self.systemminutes_label.setObjectName(u"systemminutes_label")
        self.systemminutes_label.setGeometry(QRect(240, 80, 121, 111))
        self.systemminutes_label.setFont(font10)
        self.systemminutes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.systemhoursplus_btn = QPushButton(self.datetime_page)
        self.systemhoursplus_btn.setObjectName(u"systemhoursplus_btn")
        self.systemhoursplus_btn.setGeometry(QRect(140, 30, 75, 51))
        font11 = QFont()
        font11.setFamilies([u"TikTok Sans 28pt"])
        font11.setPointSize(20)
        font11.setBold(True)
        self.systemhoursplus_btn.setFont(font11)
        self.systemhoursplus_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 10px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.systemhoursminus_btn = QPushButton(self.datetime_page)
        self.systemhoursminus_btn.setObjectName(u"systemhoursminus_btn")
        self.systemhoursminus_btn.setGeometry(QRect(140, 190, 75, 51))
        self.systemhoursminus_btn.setFont(font11)
        self.systemhoursminus_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 10px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.systemminutesminus_btn = QPushButton(self.datetime_page)
        self.systemminutesminus_btn.setObjectName(u"systemminutesminus_btn")
        self.systemminutesminus_btn.setGeometry(QRect(260, 190, 75, 51))
        self.systemminutesminus_btn.setFont(font11)
        self.systemminutesminus_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 10px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.systemminutesplus_btn = QPushButton(self.datetime_page)
        self.systemminutesplus_btn.setObjectName(u"systemminutesplus_btn")
        self.systemminutesplus_btn.setGeometry(QRect(260, 30, 75, 51))
        self.systemminutesplus_btn.setFont(font11)
        self.systemminutesplus_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 10px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.systemtiming_save_btn = QPushButton(self.datetime_page)
        self.systemtiming_save_btn.setObjectName(u"systemtiming_save_btn")
        self.systemtiming_save_btn.setGeometry(QRect(10, 450, 201, 91))
        self.systemtiming_save_btn.setFont(font2)
        self.systemtiming_save_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.systemyear_label = QLabel(self.datetime_page)
        self.systemyear_label.setObjectName(u"systemyear_label")
        self.systemyear_label.setGeometry(QRect(20, 300, 171, 91))
        self.systemyear_label.setFont(font10)
        self.systemyear_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.systemmonthplus_btn = QPushButton(self.datetime_page)
        self.systemmonthplus_btn.setObjectName(u"systemmonthplus_btn")
        self.systemmonthplus_btn.setGeometry(QRect(194, 250, 111, 51))
        font12 = QFont()
        font12.setFamilies([u"TikTok Sans 28pt"])
        font12.setPointSize(18)
        font12.setBold(True)
        self.systemmonthplus_btn.setFont(font12)
        self.systemmonthplus_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 10px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.systemmonthminus_btn = QPushButton(self.datetime_page)
        self.systemmonthminus_btn.setObjectName(u"systemmonthminus_btn")
        self.systemmonthminus_btn.setGeometry(QRect(194, 390, 111, 51))
        self.systemmonthminus_btn.setFont(font12)
        self.systemmonthminus_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 10px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.systemdayplus_btn = QPushButton(self.datetime_page)
        self.systemdayplus_btn.setObjectName(u"systemdayplus_btn")
        self.systemdayplus_btn.setGeometry(QRect(340, 250, 75, 51))
        self.systemdayplus_btn.setFont(font12)
        self.systemdayplus_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 10px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.systemdayminus_btn = QPushButton(self.datetime_page)
        self.systemdayminus_btn.setObjectName(u"systemdayminus_btn")
        self.systemdayminus_btn.setGeometry(QRect(340, 390, 75, 51))
        self.systemdayminus_btn.setFont(font12)
        self.systemdayminus_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 10px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.systemyearminus_btn = QPushButton(self.datetime_page)
        self.systemyearminus_btn.setObjectName(u"systemyearminus_btn")
        self.systemyearminus_btn.setGeometry(QRect(70, 390, 75, 51))
        self.systemyearminus_btn.setFont(font12)
        self.systemyearminus_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 10px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.systemyearplus_btn = QPushButton(self.datetime_page)
        self.systemyearplus_btn.setObjectName(u"systemyearplus_btn")
        self.systemyearplus_btn.setGeometry(QRect(70, 250, 75, 51))
        self.systemyearplus_btn.setFont(font12)
        self.systemyearplus_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 10px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.systemmonth_label = QLabel(self.datetime_page)
        self.systemmonth_label.setObjectName(u"systemmonth_label")
        self.systemmonth_label.setGeometry(QRect(170, 300, 171, 91))
        self.systemmonth_label.setFont(font10)
        self.systemmonth_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.systemday_label = QLabel(self.datetime_page)
        self.systemday_label.setObjectName(u"systemday_label")
        self.systemday_label.setGeometry(QRect(290, 300, 171, 91))
        self.systemday_label.setFont(font10)
        self.systemday_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pagelayoutwidget.addWidget(self.datetime_page)
        self.irrigation_page = QWidget()
        self.irrigation_page.setObjectName(u"irrigation_page")
        self.irrigation_back_btn = QPushButton(self.irrigation_page)
        self.irrigation_back_btn.setObjectName(u"irrigation_back_btn")
        self.irrigation_back_btn.setGeometry(QRect(270, 440, 191, 111))
        self.irrigation_back_btn.setFont(font2)
        self.irrigation_back_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-3, y1:0, x2:2, y2:0, stop:0 white, stop:1 #ed7a2a);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.wateringtime_page_btn = QPushButton(self.irrigation_page)
        self.wateringtime_page_btn.setObjectName(u"wateringtime_page_btn")
        self.wateringtime_page_btn.setGeometry(QRect(10, 20, 191, 131))
        self.wateringtime_page_btn.setFont(font9)
        self.wateringtime_page_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.irrigation_save_btn = QPushButton(self.irrigation_page)
        self.irrigation_save_btn.setObjectName(u"irrigation_save_btn")
        self.irrigation_save_btn.setGeometry(QRect(10, 440, 201, 111))
        self.irrigation_save_btn.setFont(font2)
        self.irrigation_save_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.watervol_slider = QSlider(self.irrigation_page)
        self.watervol_slider.setObjectName(u"watervol_slider")
        self.watervol_slider.setGeometry(QRect(120, 170, 331, 68))
        sizePolicy.setHeightForWidth(self.watervol_slider.sizePolicy().hasHeightForWidth())
        self.watervol_slider.setSizePolicy(sizePolicy)
        self.watervol_slider.setStyleSheet(u".QSlider {\n"
"    min-height: 68px;\n"
"    max-height: 68px;\n"
"}\n"
"\n"
".QSlider::groove:horizontal {\n"
"	border-radius: 5px;\n"
"    border: 3px solid #262626;\n"
"    height: 5px;\n"
"    margin: 0 12px;\n"
"}\n"
"\n"
".QSlider::handle:horizontal {\n"
"    background: Grey;\n"
"	border-radius: 10px;\n"
"    width: 46px;\n"
"    height: 100px;\n"
"	margin: -24px -12px\n"
"}")
        self.watervol_slider.setMinimum(1)
        self.watervol_slider.setMaximum(20)
        self.watervol_slider.setOrientation(Qt.Orientation.Horizontal)
        self.watervol_slider.setInvertedAppearance(False)
        self.watervol_label = QLabel(self.irrigation_page)
        self.watervol_label.setObjectName(u"watervol_label")
        self.watervol_label.setGeometry(QRect(30, 190, 71, 16))
        font13 = QFont()
        font13.setFamilies([u"TikTok Sans 28pt"])
        font13.setBold(False)
        font13.setUnderline(True)
        self.watervol_label.setFont(font13)
        self.watervol_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.moistthresh_label = QLabel(self.irrigation_page)
        self.moistthresh_label.setObjectName(u"moistthresh_label")
        self.moistthresh_label.setGeometry(QRect(30, 250, 71, 16))
        self.moistthresh_label.setFont(font13)
        self.moistthresh_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.moistthresh_slider = QSlider(self.irrigation_page)
        self.moistthresh_slider.setObjectName(u"moistthresh_slider")
        self.moistthresh_slider.setGeometry(QRect(120, 230, 331, 68))
        self.moistthresh_slider.setStyleSheet(u".QSlider {\n"
"    min-height: 68px;\n"
"    max-height: 68px;\n"
"}\n"
"\n"
".QSlider::groove:horizontal {\n"
"	border-radius: 5px;\n"
"    border: 3px solid #262626;\n"
"    height: 5px;\n"
"    margin: 0 12px;\n"
"}\n"
"\n"
".QSlider::handle:horizontal {\n"
"    background: Grey;\n"
"	border-radius: 10px;\n"
"    width: 46px;\n"
"    height: 100px;\n"
"	margin: -24px -12px\n"
"}")
        self.moistthresh_slider.setMinimum(300)
        self.moistthresh_slider.setMaximum(1000)
        self.moistthresh_slider.setOrientation(Qt.Orientation.Horizontal)
        self.tempset_slider = QSlider(self.irrigation_page)
        self.tempset_slider.setObjectName(u"tempset_slider")
        self.tempset_slider.setGeometry(QRect(120, 290, 331, 68))
        self.tempset_slider.setStyleSheet(u".QSlider {\n"
"    min-height: 68px;\n"
"    max-height: 68px;\n"
"}\n"
"\n"
".QSlider::groove:horizontal {\n"
"	border-radius: 5px;\n"
"    border: 3px solid #262626;\n"
"    height: 5px;\n"
"    margin: 0 12px;\n"
"}\n"
"\n"
".QSlider::handle:horizontal {\n"
"    background: Grey;\n"
"	border-radius: 10px;\n"
"    width: 46px;\n"
"    height: 100px;\n"
"	margin: -24px -12px\n"
"}")
        self.tempset_slider.setMinimum(5)
        self.tempset_slider.setMaximum(30)
        self.tempset_slider.setOrientation(Qt.Orientation.Horizontal)
        self.humidset_slider = QSlider(self.irrigation_page)
        self.humidset_slider.setObjectName(u"humidset_slider")
        self.humidset_slider.setGeometry(QRect(120, 350, 331, 68))
        self.humidset_slider.setStyleSheet(u".QSlider {\n"
"    min-height: 68px;\n"
"    max-height: 68px;\n"
"}\n"
"\n"
".QSlider::groove:horizontal {\n"
"	border-radius: 5px;\n"
"    border: 3px solid #262626;\n"
"    height: 5px;\n"
"    margin: 0 12px;\n"
"}\n"
"\n"
".QSlider::handle:horizontal {\n"
"    background: Grey;\n"
"	border-radius: 10px;\n"
"    width: 46px;\n"
"    height: 100px;\n"
"	margin: -24px -12px\n"
"}")
        self.humidset_slider.setMinimum(1)
        self.humidset_slider.setMaximum(100)
        self.humidset_slider.setOrientation(Qt.Orientation.Horizontal)
        self.tempset_label = QLabel(self.irrigation_page)
        self.tempset_label.setObjectName(u"tempset_label")
        self.tempset_label.setGeometry(QRect(20, 310, 91, 16))
        self.tempset_label.setFont(font13)
        self.tempset_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.humidset_label = QLabel(self.irrigation_page)
        self.humidset_label.setObjectName(u"humidset_label")
        self.humidset_label.setGeometry(QRect(30, 370, 71, 16))
        self.humidset_label.setFont(font13)
        self.humidset_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.irrigation_description_label = QLabel(self.irrigation_page)
        self.irrigation_description_label.setObjectName(u"irrigation_description_label")
        self.irrigation_description_label.setGeometry(QRect(210, 20, 161, 161))
        font14 = QFont()
        font14.setFamilies([u"TikTok Sans 28pt"])
        font14.setPointSize(12)
        font14.setBold(True)
        self.irrigation_description_label.setFont(font14)
        self.irrigation_description_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.irrigation_description_label.setWordWrap(True)
        self.irrigation_description_label_2 = QLabel(self.irrigation_page)
        self.irrigation_description_label_2.setObjectName(u"irrigation_description_label_2")
        self.irrigation_description_label_2.setGeometry(QRect(380, 20, 91, 161))
        self.irrigation_description_label_2.setFont(font14)
        self.irrigation_description_label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.irrigation_description_label_2.setWordWrap(True)
        self.watervol_indicator = QLabel(self.irrigation_page)
        self.watervol_indicator.setObjectName(u"watervol_indicator")
        self.watervol_indicator.setGeometry(QRect(20, 210, 91, 20))
        font15 = QFont()
        font15.setFamilies([u"TikTok Sans 28pt"])
        font15.setPointSize(13)
        font15.setBold(False)
        font15.setUnderline(False)
        self.watervol_indicator.setFont(font15)
        self.watervol_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.moistthresh_idicator = QLabel(self.irrigation_page)
        self.moistthresh_idicator.setObjectName(u"moistthresh_idicator")
        self.moistthresh_idicator.setGeometry(QRect(20, 270, 91, 20))
        font16 = QFont()
        font16.setFamilies([u"TikTok Sans 28pt"])
        font16.setPointSize(13)
        font16.setBold(False)
        self.moistthresh_idicator.setFont(font16)
        self.moistthresh_idicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tempset_indicator = QLabel(self.irrigation_page)
        self.tempset_indicator.setObjectName(u"tempset_indicator")
        self.tempset_indicator.setGeometry(QRect(20, 330, 91, 20))
        self.tempset_indicator.setFont(font16)
        self.tempset_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.humidset_indicator = QLabel(self.irrigation_page)
        self.humidset_indicator.setObjectName(u"humidset_indicator")
        self.humidset_indicator.setGeometry(QRect(20, 390, 91, 20))
        self.humidset_indicator.setFont(font16)
        self.humidset_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.groupBox = QGroupBox(self.irrigation_page)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 160, 451, 271))
        self.groupBox.setStyleSheet(u"QGroupBox{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.pagelayoutwidget.addWidget(self.irrigation_page)
        self.groupBox.raise_()
        self.irrigation_back_btn.raise_()
        self.wateringtime_page_btn.raise_()
        self.irrigation_save_btn.raise_()
        self.watervol_slider.raise_()
        self.watervol_label.raise_()
        self.moistthresh_label.raise_()
        self.moistthresh_slider.raise_()
        self.tempset_slider.raise_()
        self.humidset_slider.raise_()
        self.tempset_label.raise_()
        self.humidset_label.raise_()
        self.irrigation_description_label.raise_()
        self.irrigation_description_label_2.raise_()
        self.watervol_indicator.raise_()
        self.moistthresh_idicator.raise_()
        self.tempset_indicator.raise_()
        self.humidset_indicator.raise_()
        self.watertiming_page = QWidget()
        self.watertiming_page.setObjectName(u"watertiming_page")
        self.waterhours_label = QLabel(self.watertiming_page)
        self.waterhours_label.setObjectName(u"waterhours_label")
        self.waterhours_label.setGeometry(QRect(120, 110, 91, 111))
        self.waterhours_label.setFont(font10)
        self.waterhours_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.waterminutes_label = QLabel(self.watertiming_page)
        self.waterminutes_label.setObjectName(u"waterminutes_label")
        self.waterminutes_label.setGeometry(QRect(230, 110, 121, 111))
        self.waterminutes_label.setFont(font10)
        self.waterminutes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timesep_label = QLabel(self.watertiming_page)
        self.timesep_label.setObjectName(u"timesep_label")
        self.timesep_label.setGeometry(QRect(210, 110, 21, 111))
        self.timesep_label.setFont(font10)
        self.timesep_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hoursplus_btn = QPushButton(self.watertiming_page)
        self.hoursplus_btn.setObjectName(u"hoursplus_btn")
        self.hoursplus_btn.setGeometry(QRect(130, 60, 75, 51))
        self.hoursplus_btn.setFont(font11)
        self.hoursplus_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 10px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.minutesplus_btn = QPushButton(self.watertiming_page)
        self.minutesplus_btn.setObjectName(u"minutesplus_btn")
        self.minutesplus_btn.setGeometry(QRect(250, 60, 75, 51))
        self.minutesplus_btn.setFont(font11)
        self.minutesplus_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 10px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.minutesminus_btn = QPushButton(self.watertiming_page)
        self.minutesminus_btn.setObjectName(u"minutesminus_btn")
        self.minutesminus_btn.setGeometry(QRect(250, 220, 75, 51))
        self.minutesminus_btn.setFont(font11)
        self.minutesminus_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 10px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.hoursminus_btn = QPushButton(self.watertiming_page)
        self.hoursminus_btn.setObjectName(u"hoursminus_btn")
        self.hoursminus_btn.setGeometry(QRect(130, 220, 75, 51))
        self.hoursminus_btn.setFont(font11)
        self.hoursminus_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 10px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.watertiming_back_btn = QPushButton(self.watertiming_page)
        self.watertiming_back_btn.setObjectName(u"watertiming_back_btn")
        self.watertiming_back_btn.setGeometry(QRect(260, 430, 201, 121))
        self.watertiming_back_btn.setFont(font2)
        self.watertiming_back_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-3, y1:0, x2:2, y2:0, stop:0 white, stop:1 #ed7a2a);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.watertiming_back_btn.setFlat(False)
        self.watertiming_save_btn = QPushButton(self.watertiming_page)
        self.watertiming_save_btn.setObjectName(u"watertiming_save_btn")
        self.watertiming_save_btn.setGeometry(QRect(10, 430, 201, 121))
        self.watertiming_save_btn.setFont(font2)
        self.watertiming_save_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.checktime_btn = QPushButton(self.watertiming_page)
        self.checktime_btn.setObjectName(u"checktime_btn")
        self.checktime_btn.setGeometry(QRect(10, 290, 141, 131))
        self.checktime_btn.setFont(font2)
        self.checktime_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.sunrise_btn = QPushButton(self.watertiming_page)
        self.sunrise_btn.setObjectName(u"sunrise_btn")
        self.sunrise_btn.setGeometry(QRect(160, 290, 151, 131))
        self.sunrise_btn.setFont(font2)
        self.sunrise_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.sunset_btn = QPushButton(self.watertiming_page)
        self.sunset_btn.setObjectName(u"sunset_btn")
        self.sunset_btn.setGeometry(QRect(320, 290, 141, 131))
        self.sunset_btn.setFont(font2)
        self.sunset_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: qlineargradient(x1:-1, y1:0, x2:2, y2:0, stop:0 white, stop:1 gray);\n"
"	border-radius: 25px;\n"
"	border: 5px solid rgb(120, 120, 120);\n"
"}")
        self.pagelayoutwidget.addWidget(self.watertiming_page)
        self.humidtempset_page = QWidget()
        self.humidtempset_page.setObjectName(u"humidtempset_page")
        self.pagelayoutwidget.addWidget(self.humidtempset_page)
        self.humidset_page = QWidget()
        self.humidset_page.setObjectName(u"humidset_page")
        self.pagelayoutwidget.addWidget(self.humidset_page)
        self.statusbar = QWidget(Form)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setGeometry(QRect(0, 0, 480, 80))
        self.statusbar.setStyleSheet(u"background-color: rgb(120, 120, 120)\n"
"")
        self.statusbar_label = QLabel(self.statusbar)
        self.statusbar_label.setObjectName(u"statusbar_label")
        self.statusbar_label.setGeometry(QRect(20, 10, 361, 61))
        font17 = QFont()
        font17.setFamilies([u"Myriad Pro"])
        font17.setPointSize(15)
        self.statusbar_label.setFont(font17)
        self.water_status_label = QLabel(self.statusbar)
        self.water_status_label.setObjectName(u"water_status_label")
        self.water_status_label.setGeometry(QRect(390, 10, 81, 16))
        font18 = QFont()
        font18.setFamilies([u"TikTok Sans 28pt"])
        font18.setBold(True)
        self.water_status_label.setFont(font18)
        self.water_status_label_2 = QLabel(self.statusbar)
        self.water_status_label_2.setObjectName(u"water_status_label_2")
        self.water_status_label_2.setGeometry(QRect(390, 30, 81, 16))
        self.water_status_label_2.setFont(font18)
        self.water_status_label_3 = QLabel(self.statusbar)
        self.water_status_label_3.setObjectName(u"water_status_label_3")
        self.water_status_label_3.setGeometry(QRect(390, 50, 81, 16))
        self.water_status_label_3.setFont(font18)

        self.retranslateUi(Form)

        self.pagelayoutwidget.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.continue_btn.setText(QCoreApplication.translate("Form", u"Continue", None))
        self.clockdisplay.setText(QCoreApplication.translate("Form", u"<<Clock>>", None))
        self.label.setText(QCoreApplication.translate("Form", u"Current Date:", None))
        self.Datedisplay.setText(QCoreApplication.translate("Form", u"<<Date>>", None))
        self.systeminfo_page_btn.setText(QCoreApplication.translate("Form", u"System Info", None))
        self.editsettings_page_btn.setText(QCoreApplication.translate("Form", u"Edit Settings", None))
        self.mainmenu_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.manualcontrols_page_btn.setText(QCoreApplication.translate("Form", u"Manual Controls", None))
        self.monitordata_page_btn.setText(QCoreApplication.translate("Form", u"Monitor Data", None))
        self.monitordata_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.monitordata_update_btn.setText(QCoreApplication.translate("Form", u"Update", None))
        self.monitordata_data_label.setText(QCoreApplication.translate("Form", u"<<Data Label>>", None))
        self.graphdomain_label.setText(QCoreApplication.translate("Form", u"<<Graph Domain>>", None))
        self.monitordata_live_btn.setText(QCoreApplication.translate("Form", u"Live", None))
        self.waternow_btn.setText(QCoreApplication.translate("Form", u"Water\n"
"Toggle", None))
        self.lightswitch_btn.setText(QCoreApplication.translate("Form", u"Light\n"
"Switch", None))
        self.fanon_btn.setText(QCoreApplication.translate("Form", u"Fan Toggle", None))
        self.takepicture_btn.setText(QCoreApplication.translate("Form", u"Take Picture", None))
        self.recorddata_btn.setText(QCoreApplication.translate("Form", u"Record Data", None))
        self.manualcontrols_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.watercycle_btn.setText(QCoreApplication.translate("Form", u"Cycle\n"
"Pump", None))
        self.updatefirmware_page_btn.setText(QCoreApplication.translate("Form", u"Update Firmware", None))
        self.logexport_page_btn.setText(QCoreApplication.translate("Form", u"Log Export", None))
        self.systeminfo_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.systemversion_label.setText(QCoreApplication.translate("Form", u"<<System Version>>", None))
        self.irrigation_page_btn.setText(QCoreApplication.translate("Form", u"Irrigation", None))
        self.editsettings_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.datetime_page_btn.setText(QCoreApplication.translate("Form", u"Date/Time", None))
        self.brightness_label.setText(QCoreApplication.translate("Form", u"<<Brightness>>", None))
        self.brightness_label_2.setText(QCoreApplication.translate("Form", u"Brightness:", None))
        self.datetime_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.systemhours_label.setText(QCoreApplication.translate("Form", u"9", None))
        self.timesep_label_2.setText(QCoreApplication.translate("Form", u":", None))
        self.systemminutes_label.setText(QCoreApplication.translate("Form", u"30", None))
        self.systemhoursplus_btn.setText(QCoreApplication.translate("Form", u"+", None))
        self.systemhoursminus_btn.setText(QCoreApplication.translate("Form", u"-", None))
        self.systemminutesminus_btn.setText(QCoreApplication.translate("Form", u"-", None))
        self.systemminutesplus_btn.setText(QCoreApplication.translate("Form", u"+", None))
        self.systemtiming_save_btn.setText(QCoreApplication.translate("Form", u"Save", None))
        self.systemyear_label.setText(QCoreApplication.translate("Form", u"2025", None))
        self.systemmonthplus_btn.setText(QCoreApplication.translate("Form", u"Month+", None))
        self.systemmonthminus_btn.setText(QCoreApplication.translate("Form", u"Month-", None))
        self.systemdayplus_btn.setText(QCoreApplication.translate("Form", u"Day+", None))
        self.systemdayminus_btn.setText(QCoreApplication.translate("Form", u"Day-", None))
        self.systemyearminus_btn.setText(QCoreApplication.translate("Form", u"Year-", None))
        self.systemyearplus_btn.setText(QCoreApplication.translate("Form", u"Year+", None))
        self.systemmonth_label.setText(QCoreApplication.translate("Form", u"5", None))
        self.systemday_label.setText(QCoreApplication.translate("Form", u"23", None))
        self.irrigation_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.wateringtime_page_btn.setText(QCoreApplication.translate("Form", u"Time\n"
"Parameters", None))
        self.irrigation_save_btn.setText(QCoreApplication.translate("Form", u"Save", None))
        self.watervol_label.setText(QCoreApplication.translate("Form", u"Water Vol", None))
        self.moistthresh_label.setText(QCoreApplication.translate("Form", u"Moist Thresh", None))
        self.tempset_label.setText(QCoreApplication.translate("Form", u"Temperature Set", None))
        self.humidset_label.setText(QCoreApplication.translate("Form", u"Humid Set", None))
        self.irrigation_description_label.setText(QCoreApplication.translate("Form", u"Description:\n"
"Water Vol: (1-20) [mm of rain]\n"
"Moist Thresh: (%)\n"
"Temp Set: (\u00b0C)\n"
"Humid Set: (%) ", None))
        self.irrigation_description_label_2.setText(QCoreApplication.translate("Form", u"Default:\n"
"[1 mm]\n"
"\n"
"[750]\n"
"[25\u00b0C]\n"
"[90%]", None))
        self.watervol_indicator.setText(QCoreApplication.translate("Form", u"<<value>>", None))
        self.moistthresh_idicator.setText(QCoreApplication.translate("Form", u"<<value>>", None))
        self.tempset_indicator.setText(QCoreApplication.translate("Form", u"<<value>>", None))
        self.humidset_indicator.setText(QCoreApplication.translate("Form", u"<<value>>", None))
        self.groupBox.setTitle("")
        self.waterhours_label.setText(QCoreApplication.translate("Form", u"9", None))
        self.waterminutes_label.setText(QCoreApplication.translate("Form", u"30", None))
        self.timesep_label.setText(QCoreApplication.translate("Form", u":", None))
        self.hoursplus_btn.setText(QCoreApplication.translate("Form", u"+", None))
        self.minutesplus_btn.setText(QCoreApplication.translate("Form", u"+", None))
        self.minutesminus_btn.setText(QCoreApplication.translate("Form", u"-", None))
        self.hoursminus_btn.setText(QCoreApplication.translate("Form", u"-", None))
        self.watertiming_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.watertiming_save_btn.setText(QCoreApplication.translate("Form", u"Save", None))
        self.checktime_btn.setText(QCoreApplication.translate("Form", u"Check Time", None))
        self.sunrise_btn.setText(QCoreApplication.translate("Form", u"Sunrise", None))
        self.sunset_btn.setText(QCoreApplication.translate("Form", u"Sunset", None))
        self.statusbar_label.setText(QCoreApplication.translate("Form", u"<<Status Bar>> ", None))
        self.water_status_label.setText(QCoreApplication.translate("Form", u"Water Status", None))
        self.water_status_label_2.setText(QCoreApplication.translate("Form", u"------", None))
        self.water_status_label_3.setText(QCoreApplication.translate("Form", u"------", None))
    # retranslateUi

