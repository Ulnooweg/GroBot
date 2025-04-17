# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
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
    QSizePolicy, QStackedWidget, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 480)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoHome))
        Widget.setWindowIcon(icon)
        Widget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pagelayoutwidget = QStackedWidget(Widget)
        self.pagelayoutwidget.setObjectName(u"pagelayoutwidget")
        self.pagelayoutwidget.setGeometry(QRect(0, 50, 800, 430))
        self.pagelayoutwidget.setStyleSheet(u"")
        self.mainmenu_page = QWidget()
        self.mainmenu_page.setObjectName(u"mainmenu_page")
        self.manualcontrol_page_btn = QPushButton(self.mainmenu_page)
        self.manualcontrol_page_btn.setObjectName(u"manualcontrol_page_btn")
        self.manualcontrol_page_btn.setGeometry(QRect(320, 250, 151, 51))
        self.systeminfo_page_btn = QPushButton(self.mainmenu_page)
        self.systeminfo_page_btn.setObjectName(u"systeminfo_page_btn")
        self.systeminfo_page_btn.setGeometry(QRect(320, 110, 151, 51))
        self.editsettings_page_btn = QPushButton(self.mainmenu_page)
        self.editsettings_page_btn.setObjectName(u"editsettings_page_btn")
        self.editsettings_page_btn.setGeometry(QRect(320, 180, 151, 51))
        self.editsettings_page_btn.setFlat(False)
        self.monitordata_page_btn = QPushButton(self.mainmenu_page)
        self.monitordata_page_btn.setObjectName(u"monitordata_page_btn")
        self.monitordata_page_btn.setGeometry(QRect(320, 320, 151, 51))
        self.mainmenu_label = QLabel(self.mainmenu_page)
        self.mainmenu_label.setObjectName(u"mainmenu_label")
        self.mainmenu_label.setGeometry(QRect(10, 10, 201, 20))
        self.lcdNumber = QLCDNumber(self.mainmenu_page)
        self.lcdNumber.setObjectName(u"lcdNumber")
        self.lcdNumber.setGeometry(QRect(10, 50, 151, 23))
        font = QFont()
        font.setFamilies([u"Sitka"])
        self.lcdNumber.setFont(font)
        self.lcdNumber.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lcdNumber.setStyleSheet(u"QLCDNumber {\n"
"\n"
"background-color: darkgreen;\n"
"\n"
"}")
        self.lcdNumber.setProperty(u"value", 5.000000000000000)
        self.pagelayoutwidget.addWidget(self.mainmenu_page)
        self.systeminfo_page = QWidget()
        self.systeminfo_page.setObjectName(u"systeminfo_page")
        self.systeminfo_label = QLabel(self.systeminfo_page)
        self.systeminfo_label.setObjectName(u"systeminfo_label")
        self.systeminfo_label.setGeometry(QRect(10, 10, 202, 20))
        self.systeminfo_back_btn = QPushButton(self.systeminfo_page)
        self.systeminfo_back_btn.setObjectName(u"systeminfo_back_btn")
        self.systeminfo_back_btn.setGeometry(QRect(630, 360, 151, 51))
        self.pagelayoutwidget.addWidget(self.systeminfo_page)
        self.monitordata_page = QWidget()
        self.monitordata_page.setObjectName(u"monitordata_page")
        self.monitordata_label = QLabel(self.monitordata_page)
        self.monitordata_label.setObjectName(u"monitordata_label")
        self.monitordata_label.setGeometry(QRect(10, 10, 202, 20))
        self.monitordata_back_btn = QPushButton(self.monitordata_page)
        self.monitordata_back_btn.setObjectName(u"monitordata_back_btn")
        self.monitordata_back_btn.setGeometry(QRect(630, 360, 151, 51))
        self.pagelayoutwidget.addWidget(self.monitordata_page)
        self.editsettings_page = QWidget()
        self.editsettings_page.setObjectName(u"editsettings_page")
        self.irrigation_page_btn = QPushButton(self.editsettings_page)
        self.irrigation_page_btn.setObjectName(u"irrigation_page_btn")
        self.irrigation_page_btn.setGeometry(QRect(320, 180, 151, 51))
        self.editsettings_back_btn = QPushButton(self.editsettings_page)
        self.editsettings_back_btn.setObjectName(u"editsettings_back_btn")
        self.editsettings_back_btn.setGeometry(QRect(630, 360, 151, 51))
        self.irrigation_label_2 = QLabel(self.editsettings_page)
        self.irrigation_label_2.setObjectName(u"irrigation_label_2")
        self.irrigation_label_2.setGeometry(QRect(10, 10, 201, 20))
        self.pagelayoutwidget.addWidget(self.editsettings_page)
        self.manualcontrol_page = QWidget()
        self.manualcontrol_page.setObjectName(u"manualcontrol_page")
        self.manualcontrol_back_btn = QPushButton(self.manualcontrol_page)
        self.manualcontrol_back_btn.setObjectName(u"manualcontrol_back_btn")
        self.manualcontrol_back_btn.setGeometry(QRect(630, 360, 151, 51))
        self.manualcontrol_label = QLabel(self.manualcontrol_page)
        self.manualcontrol_label.setObjectName(u"manualcontrol_label")
        self.manualcontrol_label.setGeometry(QRect(10, 10, 201, 20))
        self.pagelayoutwidget.addWidget(self.manualcontrol_page)
        self.irrigation_page = QWidget()
        self.irrigation_page.setObjectName(u"irrigation_page")
        self.humidsetpoint_btn = QPushButton(self.irrigation_page)
        self.humidsetpoint_btn.setObjectName(u"humidsetpoint_btn")
        self.humidsetpoint_btn.setGeometry(QRect(320, 180, 151, 51))
        self.irrigation_back_btn = QPushButton(self.irrigation_page)
        self.irrigation_back_btn.setObjectName(u"irrigation_back_btn")
        self.irrigation_back_btn.setGeometry(QRect(630, 360, 151, 51))
        self.irrigation_label = QLabel(self.irrigation_page)
        self.irrigation_label.setObjectName(u"irrigation_label")
        self.irrigation_label.setGeometry(QRect(10, 10, 201, 20))
        self.pagelayoutwidget.addWidget(self.irrigation_page)
        self.widget = QWidget(Widget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 800, 50))
        self.widget.setStyleSheet(u"QWidget {\n"
"\n"
"background-color: grey;\n"
"\n"
"}")
        self.lcdNumbertime = QLCDNumber(self.widget)
        self.lcdNumbertime.setObjectName(u"lcdNumbertime")
        self.lcdNumbertime.setGeometry(QRect(10, 10, 151, 23))
        self.lcdNumbertime.setFont(font)
        self.lcdNumbertime.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lcdNumbertime.setStyleSheet(u"QLCDNumber {\n"
"\n"
"background-color: darkgreen;\n"
"\n"
"}")
        self.lcdNumbertime.setProperty(u"value", 5.000000000000000)

        self.retranslateUi(Widget)

        self.editsettings_page_btn.setDefault(False)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.manualcontrol_page_btn.setText(QCoreApplication.translate("Widget", u"Manual Control", None))
        self.systeminfo_page_btn.setText(QCoreApplication.translate("Widget", u"System Info", None))
        self.editsettings_page_btn.setText(QCoreApplication.translate("Widget", u"Edit Settings", None))
        self.monitordata_page_btn.setText(QCoreApplication.translate("Widget", u"Monitor Data", None))
        self.mainmenu_label.setText(QCoreApplication.translate("Widget", u"Main Menu", None))
        self.systeminfo_label.setText(QCoreApplication.translate("Widget", u"System Info", None))
        self.systeminfo_back_btn.setText(QCoreApplication.translate("Widget", u"Back", None))
        self.monitordata_label.setText(QCoreApplication.translate("Widget", u"Monitor Data", None))
        self.monitordata_back_btn.setText(QCoreApplication.translate("Widget", u"Back", None))
        self.irrigation_page_btn.setText(QCoreApplication.translate("Widget", u"Irrigation", None))
        self.editsettings_back_btn.setText(QCoreApplication.translate("Widget", u"Back", None))
        self.irrigation_label_2.setText(QCoreApplication.translate("Widget", u"Edit Settings", None))
        self.manualcontrol_back_btn.setText(QCoreApplication.translate("Widget", u"Back", None))
        self.manualcontrol_label.setText(QCoreApplication.translate("Widget", u"Manual Control", None))
        self.humidsetpoint_btn.setText(QCoreApplication.translate("Widget", u"Humid Setpoint", None))
        self.irrigation_back_btn.setText(QCoreApplication.translate("Widget", u"Back", None))
        self.irrigation_label.setText(QCoreApplication.translate("Widget", u"Irrigation", None))
    # retranslateUi

