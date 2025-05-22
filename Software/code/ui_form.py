# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formwnZUMi.ui'
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
from PySide6.QtWidgets import (QApplication, QLCDNumber, QLabel, QPushButton,
    QSizePolicy, QSlider, QStackedWidget, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(484, 648)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        Form.setFont(font)
        self.pagelayoutwidget = QStackedWidget(Form)
        self.pagelayoutwidget.setObjectName(u"pagelayoutwidget")
        self.pagelayoutwidget.setGeometry(QRect(0, 70, 480, 560))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setBold(False)
        self.pagelayoutwidget.setFont(font1)
        self.start_page = QWidget()
        self.start_page.setObjectName(u"start_page")
        self.continue_btn = QPushButton(self.start_page)
        self.continue_btn.setObjectName(u"continue_btn")
        self.continue_btn.setGeometry(QRect(10, 290, 221, 170))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(30)
        font2.setBold(False)
        self.continue_btn.setFont(font2)
        self.sensordisplay_1 = QLCDNumber(self.start_page)
        self.sensordisplay_1.setObjectName(u"sensordisplay_1")
        self.sensordisplay_1.setGeometry(QRect(0, 150, 230, 100))
        self.sensordisplay_1.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.clockdisplay = QLabel(self.start_page)
        self.clockdisplay.setObjectName(u"clockdisplay")
        self.clockdisplay.setGeometry(QRect(0, 14, 471, 131))
        font3 = QFont()
        font3.setFamilies([u"Comic Sans MS"])
        font3.setPointSize(47)
        font3.setBold(True)
        self.clockdisplay.setFont(font3)
        self.clockdisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sensordisplay_1_label = QLabel(self.start_page)
        self.sensordisplay_1_label.setObjectName(u"sensordisplay_1_label")
        self.sensordisplay_1_label.setGeometry(QRect(90, 260, 71, 16))
        font4 = QFont()
        font4.setFamilies([u"Comic Sans MS"])
        font4.setPointSize(13)
        font4.setBold(True)
        self.sensordisplay_1_label.setFont(font4)
        self.close_btn = QPushButton(self.start_page)
        self.close_btn.setObjectName(u"close_btn")
        self.close_btn.setGeometry(QRect(240, 290, 221, 170))
        self.close_btn.setFont(font2)
        self.sensordisplay_2 = QLCDNumber(self.start_page)
        self.sensordisplay_2.setObjectName(u"sensordisplay_2")
        self.sensordisplay_2.setGeometry(QRect(250, 150, 230, 100))
        self.sensordisplay_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.sensordisplay_1_label_2 = QLabel(self.start_page)
        self.sensordisplay_1_label_2.setObjectName(u"sensordisplay_1_label_2")
        self.sensordisplay_1_label_2.setGeometry(QRect(350, 260, 71, 16))
        self.sensordisplay_1_label_2.setFont(font4)
        self.pagelayoutwidget.addWidget(self.start_page)
        self.mainmenu_page = QWidget()
        self.mainmenu_page.setObjectName(u"mainmenu_page")
        self.systeminfo_page_btn = QPushButton(self.mainmenu_page)
        self.systeminfo_page_btn.setObjectName(u"systeminfo_page_btn")
        self.systeminfo_page_btn.setGeometry(QRect(10, 10, 201, 151))
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setPointSize(18)
        font5.setBold(False)
        self.systeminfo_page_btn.setFont(font5)
        self.editsettings_page_btn = QPushButton(self.mainmenu_page)
        self.editsettings_page_btn.setObjectName(u"editsettings_page_btn")
        self.editsettings_page_btn.setGeometry(QRect(270, 10, 201, 151))
        self.editsettings_page_btn.setFont(font5)
        self.mainmenu_back_btn = QPushButton(self.mainmenu_page)
        self.mainmenu_back_btn.setObjectName(u"mainmenu_back_btn")
        self.mainmenu_back_btn.setGeometry(QRect(10, 310, 201, 151))
        self.mainmenu_back_btn.setFont(font5)
        self.manualcontrols_page_btn = QPushButton(self.mainmenu_page)
        self.manualcontrols_page_btn.setObjectName(u"manualcontrols_page_btn")
        self.manualcontrols_page_btn.setGeometry(QRect(10, 160, 201, 151))
        self.manualcontrols_page_btn.setFont(font5)
        self.monitordata_page_btn = QPushButton(self.mainmenu_page)
        self.monitordata_page_btn.setObjectName(u"monitordata_page_btn")
        self.monitordata_page_btn.setGeometry(QRect(270, 160, 201, 151))
        self.monitordata_page_btn.setFont(font5)
        self.pagelayoutwidget.addWidget(self.mainmenu_page)
        self.monitordata_page = QWidget()
        self.monitordata_page.setObjectName(u"monitordata_page")
        self.monitordata_back_btn = QPushButton(self.monitordata_page)
        self.monitordata_back_btn.setObjectName(u"monitordata_back_btn")
        self.monitordata_back_btn.setGeometry(QRect(250, 360, 201, 151))
        self.monitordata_back_btn.setFont(font5)
        self.pagelayoutwidget.addWidget(self.monitordata_page)
        self.manualcontrols_page = QWidget()
        self.manualcontrols_page.setObjectName(u"manualcontrols_page")
        self.waternow_btn = QPushButton(self.manualcontrols_page)
        self.waternow_btn.setObjectName(u"waternow_btn")
        self.waternow_btn.setGeometry(QRect(10, 10, 201, 151))
        self.waternow_btn.setFont(font5)
        self.lightswitch_btn = QPushButton(self.manualcontrols_page)
        self.lightswitch_btn.setObjectName(u"lightswitch_btn")
        self.lightswitch_btn.setGeometry(QRect(270, 10, 201, 151))
        self.lightswitch_btn.setFont(font5)
        self.fanon_btn = QPushButton(self.manualcontrols_page)
        self.fanon_btn.setObjectName(u"fanon_btn")
        self.fanon_btn.setGeometry(QRect(10, 160, 201, 151))
        self.fanon_btn.setFont(font5)
        self.takepicture_btn = QPushButton(self.manualcontrols_page)
        self.takepicture_btn.setObjectName(u"takepicture_btn")
        self.takepicture_btn.setGeometry(QRect(270, 160, 201, 151))
        self.takepicture_btn.setFont(font5)
        self.recorddata_btn = QPushButton(self.manualcontrols_page)
        self.recorddata_btn.setObjectName(u"recorddata_btn")
        self.recorddata_btn.setGeometry(QRect(10, 310, 201, 151))
        self.recorddata_btn.setFont(font5)
        self.manualcontrols_back_btn = QPushButton(self.manualcontrols_page)
        self.manualcontrols_back_btn.setObjectName(u"manualcontrols_back_btn")
        self.manualcontrols_back_btn.setGeometry(QRect(270, 310, 201, 151))
        self.manualcontrols_back_btn.setFont(font5)
        self.pagelayoutwidget.addWidget(self.manualcontrols_page)
        self.systeminfo_page = QWidget()
        self.systeminfo_page.setObjectName(u"systeminfo_page")
        self.updatefirmware_page_btn = QPushButton(self.systeminfo_page)
        self.updatefirmware_page_btn.setObjectName(u"updatefirmware_page_btn")
        self.updatefirmware_page_btn.setGeometry(QRect(10, 10, 201, 151))
        self.updatefirmware_page_btn.setFont(font5)
        self.logexport_page_btn = QPushButton(self.systeminfo_page)
        self.logexport_page_btn.setObjectName(u"logexport_page_btn")
        self.logexport_page_btn.setGeometry(QRect(270, 10, 201, 151))
        self.logexport_page_btn.setFont(font5)
        self.systeminfo_back_btn = QPushButton(self.systeminfo_page)
        self.systeminfo_back_btn.setObjectName(u"systeminfo_back_btn")
        self.systeminfo_back_btn.setGeometry(QRect(10, 160, 201, 151))
        self.systeminfo_back_btn.setFont(font5)
        self.systemversion_label = QLabel(self.systeminfo_page)
        self.systemversion_label.setObjectName(u"systemversion_label")
        self.systemversion_label.setGeometry(QRect(10, 320, 451, 61))
        font6 = QFont()
        font6.setFamilies([u"Segoe UI"])
        font6.setPointSize(17)
        font6.setBold(False)
        self.systemversion_label.setFont(font6)
        self.pagelayoutwidget.addWidget(self.systeminfo_page)
        self.editsettings_page = QWidget()
        self.editsettings_page.setObjectName(u"editsettings_page")
        self.irrigation_page_btn = QPushButton(self.editsettings_page)
        self.irrigation_page_btn.setObjectName(u"irrigation_page_btn")
        self.irrigation_page_btn.setGeometry(QRect(270, 10, 201, 151))
        font7 = QFont()
        font7.setFamilies([u"Segoe UI"])
        font7.setPointSize(25)
        font7.setBold(False)
        self.irrigation_page_btn.setFont(font7)
        self.editsettings_back_btn = QPushButton(self.editsettings_page)
        self.editsettings_back_btn.setObjectName(u"editsettings_back_btn")
        self.editsettings_back_btn.setGeometry(QRect(270, 160, 201, 151))
        self.editsettings_back_btn.setFont(font7)
        self.datetime_page_btn = QPushButton(self.editsettings_page)
        self.datetime_page_btn.setObjectName(u"datetime_page_btn")
        self.datetime_page_btn.setGeometry(QRect(10, 10, 201, 151))
        self.datetime_page_btn.setFont(font7)
        self.cameratoggle_btn = QPushButton(self.editsettings_page)
        self.cameratoggle_btn.setObjectName(u"cameratoggle_btn")
        self.cameratoggle_btn.setGeometry(QRect(10, 160, 201, 151))
        self.cameratoggle_btn.setFont(font5)
        self.cameratoggle_btn.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.brightness_slider = QSlider(self.editsettings_page)
        self.brightness_slider.setObjectName(u"brightness_slider")
        self.brightness_slider.setGeometry(QRect(20, 330, 441, 68))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.brightness_slider.sizePolicy().hasHeightForWidth())
        self.brightness_slider.setSizePolicy(sizePolicy)
        font8 = QFont()
        font8.setFamilies([u"Segoe UI"])
        font8.setPointSize(10)
        font8.setBold(False)
        self.brightness_slider.setFont(font8)
        self.brightness_slider.setStyleSheet(u".QSlider {\n"
"    min-height: 68px;\n"
"    max-height: 68px;\n"
"}\n"
"\n"
".QSlider::groove:horizontal {\n"
"    border: 1px solid #262626;\n"
"    height: 5px;\n"
"    margin: 0 12px;\n"
"}\n"
"\n"
".QSlider::handle:horizontal {\n"
"    background: Grey;\n"
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
        self.brightness_label.setGeometry(QRect(140, 380, 201, 61))
        font9 = QFont()
        font9.setFamilies([u"Segoe UI"])
        font9.setPointSize(20)
        font9.setBold(False)
        self.brightness_label.setFont(font9)
        self.pagelayoutwidget.addWidget(self.editsettings_page)
        self.datetime_page = QWidget()
        self.datetime_page.setObjectName(u"datetime_page")
        self.datetime_back_btn = QPushButton(self.datetime_page)
        self.datetime_back_btn.setObjectName(u"datetime_back_btn")
        self.datetime_back_btn.setGeometry(QRect(260, 410, 201, 151))
        self.datetime_back_btn.setFont(font5)
        self.pagelayoutwidget.addWidget(self.datetime_page)
        self.irrigation_page = QWidget()
        self.irrigation_page.setObjectName(u"irrigation_page")
        self.irrigation_back_btn = QPushButton(self.irrigation_page)
        self.irrigation_back_btn.setObjectName(u"irrigation_back_btn")
        self.irrigation_back_btn.setGeometry(QRect(270, 430, 201, 131))
        self.irrigation_back_btn.setFont(font7)
        self.wateringtime_page_btn = QPushButton(self.irrigation_page)
        self.wateringtime_page_btn.setObjectName(u"wateringtime_page_btn")
        self.wateringtime_page_btn.setGeometry(QRect(10, 10, 191, 151))
        self.wateringtime_page_btn.setFont(font9)
        self.irrigation_save_btn = QPushButton(self.irrigation_page)
        self.irrigation_save_btn.setObjectName(u"irrigation_save_btn")
        self.irrigation_save_btn.setGeometry(QRect(10, 430, 201, 131))
        self.irrigation_save_btn.setFont(font7)
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
"    border: 1px solid #262626;\n"
"    height: 5px;\n"
"    margin: 0 12px;\n"
"}\n"
"\n"
".QSlider::handle:horizontal {\n"
"    background: Grey;\n"
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
        self.watervol_label.setGeometry(QRect(20, 190, 71, 16))
        font10 = QFont()
        font10.setFamilies([u"Segoe UI"])
        font10.setBold(False)
        font10.setUnderline(True)
        self.watervol_label.setFont(font10)
        self.watervol_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.moistthresh_label = QLabel(self.irrigation_page)
        self.moistthresh_label.setObjectName(u"moistthresh_label")
        self.moistthresh_label.setGeometry(QRect(20, 250, 71, 16))
        self.moistthresh_label.setFont(font10)
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
"    border: 1px solid #262626;\n"
"    height: 5px;\n"
"    margin: 0 12px;\n"
"}\n"
"\n"
".QSlider::handle:horizontal {\n"
"    background: Grey;\n"
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
"    border: 1px solid #262626;\n"
"    height: 5px;\n"
"    margin: 0 12px;\n"
"}\n"
"\n"
".QSlider::handle:horizontal {\n"
"    background: Grey;\n"
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
"    border: 1px solid #262626;\n"
"    height: 5px;\n"
"    margin: 0 12px;\n"
"}\n"
"\n"
".QSlider::handle:horizontal {\n"
"    background: Grey;\n"
"    width: 46px;\n"
"    height: 100px;\n"
"	margin: -24px -12px\n"
"}")
        self.humidset_slider.setMinimum(1)
        self.humidset_slider.setMaximum(100)
        self.humidset_slider.setOrientation(Qt.Orientation.Horizontal)
        self.tempset_label = QLabel(self.irrigation_page)
        self.tempset_label.setObjectName(u"tempset_label")
        self.tempset_label.setGeometry(QRect(10, 310, 91, 16))
        self.tempset_label.setFont(font10)
        self.tempset_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.humidset_label = QLabel(self.irrigation_page)
        self.humidset_label.setObjectName(u"humidset_label")
        self.humidset_label.setGeometry(QRect(20, 370, 71, 16))
        self.humidset_label.setFont(font10)
        self.humidset_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.irrigation_description_label = QLabel(self.irrigation_page)
        self.irrigation_description_label.setObjectName(u"irrigation_description_label")
        self.irrigation_description_label.setGeometry(QRect(210, 20, 161, 161))
        font11 = QFont()
        font11.setFamilies([u"Segoe UI"])
        font11.setPointSize(12)
        font11.setBold(True)
        self.irrigation_description_label.setFont(font11)
        self.irrigation_description_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.irrigation_description_label.setWordWrap(True)
        self.irrigation_description_label_2 = QLabel(self.irrigation_page)
        self.irrigation_description_label_2.setObjectName(u"irrigation_description_label_2")
        self.irrigation_description_label_2.setGeometry(QRect(380, 20, 91, 161))
        self.irrigation_description_label_2.setFont(font11)
        self.irrigation_description_label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.irrigation_description_label_2.setWordWrap(True)
        self.watervol_indicator = QLabel(self.irrigation_page)
        self.watervol_indicator.setObjectName(u"watervol_indicator")
        self.watervol_indicator.setGeometry(QRect(20, 210, 91, 20))
        font12 = QFont()
        font12.setFamilies([u"Segoe UI"])
        font12.setPointSize(13)
        font12.setBold(False)
        font12.setUnderline(False)
        self.watervol_indicator.setFont(font12)
        self.watervol_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.moistthresh_idicator = QLabel(self.irrigation_page)
        self.moistthresh_idicator.setObjectName(u"moistthresh_idicator")
        self.moistthresh_idicator.setGeometry(QRect(20, 270, 91, 20))
        font13 = QFont()
        font13.setFamilies([u"Segoe UI"])
        font13.setPointSize(13)
        font13.setBold(False)
        self.moistthresh_idicator.setFont(font13)
        self.moistthresh_idicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tempset_indicator = QLabel(self.irrigation_page)
        self.tempset_indicator.setObjectName(u"tempset_indicator")
        self.tempset_indicator.setGeometry(QRect(20, 330, 91, 20))
        self.tempset_indicator.setFont(font13)
        self.tempset_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.humidset_indicator = QLabel(self.irrigation_page)
        self.humidset_indicator.setObjectName(u"humidset_indicator")
        self.humidset_indicator.setGeometry(QRect(20, 390, 91, 20))
        self.humidset_indicator.setFont(font13)
        self.humidset_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pagelayoutwidget.addWidget(self.irrigation_page)
        self.watertiming_page = QWidget()
        self.watertiming_page.setObjectName(u"watertiming_page")
        self.waterhours_label = QLabel(self.watertiming_page)
        self.waterhours_label.setObjectName(u"waterhours_label")
        self.waterhours_label.setGeometry(QRect(120, 110, 91, 111))
        font14 = QFont()
        font14.setFamilies([u"Comic Sans MS"])
        font14.setPointSize(50)
        font14.setBold(True)
        self.waterhours_label.setFont(font14)
        self.waterhours_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.waterminutes_label = QLabel(self.watertiming_page)
        self.waterminutes_label.setObjectName(u"waterminutes_label")
        self.waterminutes_label.setGeometry(QRect(230, 110, 121, 111))
        self.waterminutes_label.setFont(font14)
        self.waterminutes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timesep_label = QLabel(self.watertiming_page)
        self.timesep_label.setObjectName(u"timesep_label")
        self.timesep_label.setGeometry(QRect(210, 110, 21, 111))
        self.timesep_label.setFont(font14)
        self.timesep_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hoursplus_btn = QPushButton(self.watertiming_page)
        self.hoursplus_btn.setObjectName(u"hoursplus_btn")
        self.hoursplus_btn.setGeometry(QRect(130, 60, 75, 51))
        font15 = QFont()
        font15.setFamilies([u"Segoe UI"])
        font15.setPointSize(20)
        font15.setBold(True)
        self.hoursplus_btn.setFont(font15)
        self.minutesplus_btn = QPushButton(self.watertiming_page)
        self.minutesplus_btn.setObjectName(u"minutesplus_btn")
        self.minutesplus_btn.setGeometry(QRect(250, 60, 75, 51))
        self.minutesplus_btn.setFont(font15)
        self.minutesminus_btn = QPushButton(self.watertiming_page)
        self.minutesminus_btn.setObjectName(u"minutesminus_btn")
        self.minutesminus_btn.setGeometry(QRect(250, 220, 75, 51))
        self.minutesminus_btn.setFont(font15)
        self.hoursminus_btn = QPushButton(self.watertiming_page)
        self.hoursminus_btn.setObjectName(u"hoursminus_btn")
        self.hoursminus_btn.setGeometry(QRect(130, 220, 75, 51))
        self.hoursminus_btn.setFont(font15)
        self.watertiming_back_btn = QPushButton(self.watertiming_page)
        self.watertiming_back_btn.setObjectName(u"watertiming_back_btn")
        self.watertiming_back_btn.setGeometry(QRect(270, 430, 201, 131))
        self.watertiming_back_btn.setFont(font9)
        self.watertiming_save_btn = QPushButton(self.watertiming_page)
        self.watertiming_save_btn.setObjectName(u"watertiming_save_btn")
        self.watertiming_save_btn.setGeometry(QRect(10, 430, 201, 131))
        self.watertiming_save_btn.setFont(font7)
        self.checktime_btn = QPushButton(self.watertiming_page)
        self.checktime_btn.setObjectName(u"checktime_btn")
        self.checktime_btn.setGeometry(QRect(10, 290, 151, 131))
        font16 = QFont()
        font16.setFamilies([u"Segoe UI"])
        font16.setPointSize(22)
        font16.setBold(False)
        self.checktime_btn.setFont(font16)
        self.sunrise_btn = QPushButton(self.watertiming_page)
        self.sunrise_btn.setObjectName(u"sunrise_btn")
        self.sunrise_btn.setGeometry(QRect(160, 290, 151, 131))
        self.sunrise_btn.setFont(font7)
        self.sunset_btn = QPushButton(self.watertiming_page)
        self.sunset_btn.setObjectName(u"sunset_btn")
        self.sunset_btn.setGeometry(QRect(310, 290, 151, 131))
        self.sunset_btn.setFont(font7)
        self.pagelayoutwidget.addWidget(self.watertiming_page)
        self.humidtempset_page = QWidget()
        self.humidtempset_page.setObjectName(u"humidtempset_page")
        self.pagelayoutwidget.addWidget(self.humidtempset_page)
        self.humidset_page = QWidget()
        self.humidset_page.setObjectName(u"humidset_page")
        self.humidset_back_btn = QPushButton(self.humidset_page)
        self.humidset_back_btn.setObjectName(u"humidset_back_btn")
        self.humidset_back_btn.setGeometry(QRect(250, 360, 201, 151))
        self.humidset_back_btn.setFont(font7)
        self.pagelayoutwidget.addWidget(self.humidset_page)
        self.statusbar = QWidget(Form)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setGeometry(QRect(0, 0, 480, 80))
        self.statusbar.setStyleSheet(u"background-color: gray\n"
"")
        self.statusbar_label = QLabel(self.statusbar)
        self.statusbar_label.setObjectName(u"statusbar_label")
        self.statusbar_label.setGeometry(QRect(20, 10, 441, 61))
        font17 = QFont()
        font17.setFamilies([u"Comic Sans MS"])
        font17.setPointSize(15)
        self.statusbar_label.setFont(font17)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.continue_btn.setText(QCoreApplication.translate("Form", u"Continue", None))
        self.clockdisplay.setText(QCoreApplication.translate("Form", u"<<Clock>>", None))
        self.sensordisplay_1_label.setText(QCoreApplication.translate("Form", u"sensor 1", None))
        self.close_btn.setText(QCoreApplication.translate("Form", u"Close", None))
        self.sensordisplay_1_label_2.setText(QCoreApplication.translate("Form", u"sensor 2", None))
        self.systeminfo_page_btn.setText(QCoreApplication.translate("Form", u"System Info", None))
        self.editsettings_page_btn.setText(QCoreApplication.translate("Form", u"Edit Settings", None))
        self.mainmenu_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.manualcontrols_page_btn.setText(QCoreApplication.translate("Form", u"Manual Controls", None))
        self.monitordata_page_btn.setText(QCoreApplication.translate("Form", u"Monitor Data", None))
        self.monitordata_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.waternow_btn.setText(QCoreApplication.translate("Form", u"Water\n"
"Toggle", None))
        self.lightswitch_btn.setText(QCoreApplication.translate("Form", u"Light Switch", None))
        self.fanon_btn.setText(QCoreApplication.translate("Form", u"Fan Toggle", None))
        self.takepicture_btn.setText(QCoreApplication.translate("Form", u"Take Picture", None))
        self.recorddata_btn.setText(QCoreApplication.translate("Form", u"Record Data", None))
        self.manualcontrols_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.updatefirmware_page_btn.setText(QCoreApplication.translate("Form", u"Update Firmware", None))
        self.logexport_page_btn.setText(QCoreApplication.translate("Form", u"Log Export", None))
        self.systeminfo_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.systemversion_label.setText(QCoreApplication.translate("Form", u"<<System Version>>", None))
        self.irrigation_page_btn.setText(QCoreApplication.translate("Form", u"Irrigation", None))
        self.editsettings_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.datetime_page_btn.setText(QCoreApplication.translate("Form", u"Date/Time", None))
        self.cameratoggle_btn.setText(QCoreApplication.translate("Form", u"Camera Toggle", None))
        self.brightness_label.setText(QCoreApplication.translate("Form", u"<<Brightness>>", None))
        self.datetime_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
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
        self.waterhours_label.setText(QCoreApplication.translate("Form", u"9", None))
        self.waterminutes_label.setText(QCoreApplication.translate("Form", u"30", None))
        self.timesep_label.setText(QCoreApplication.translate("Form", u":", None))
        self.hoursplus_btn.setText(QCoreApplication.translate("Form", u"+", None))
        self.minutesplus_btn.setText(QCoreApplication.translate("Form", u"+", None))
        self.minutesminus_btn.setText(QCoreApplication.translate("Form", u"-", None))
        self.hoursminus_btn.setText(QCoreApplication.translate("Form", u"-", None))
        self.watertiming_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.watertiming_save_btn.setText(QCoreApplication.translate("Form", u"Save", None))
        self.checktime_btn.setText(QCoreApplication.translate("Form", u"checktime", None))
        self.sunrise_btn.setText(QCoreApplication.translate("Form", u"sunrise", None))
        self.sunset_btn.setText(QCoreApplication.translate("Form", u"sunset", None))
        self.humidset_back_btn.setText(QCoreApplication.translate("Form", u"Back", None))
        self.statusbar_label.setText(QCoreApplication.translate("Form", u"<<Status Bar>> ", None))
    # retranslateUi

