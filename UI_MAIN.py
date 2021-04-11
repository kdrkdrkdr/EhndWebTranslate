# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UI_MAIN.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(272, 242)
        MainWindow.setMinimumSize(QSize(268, 167))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.btnFrame = QFrame(self.centralwidget)
        self.btnFrame.setObjectName(u"btnFrame")
        self.btnFrame.setGeometry(QRect(9, 10, 251, 101))
        self.btnFrame.setFrameShape(QFrame.Box)
        self.btnFrame.setFrameShadow(QFrame.Raised)
        self.go_dev_page = QPushButton(self.btnFrame)
        self.go_dev_page.setObjectName(u"go_dev_page")
        self.go_dev_page.setGeometry(QRect(163, 10, 75, 81))
        self.show_ori_btn = QPushButton(self.btnFrame)
        self.show_ori_btn.setObjectName(u"show_ori_btn")
        self.show_ori_btn.setGeometry(QRect(13, 60, 131, 31))
        font = QFont()
        font.setFamily(u"Consolas")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.show_ori_btn.setFont(font)
        self.show_trans_btn = QPushButton(self.btnFrame)
        self.show_trans_btn.setObjectName(u"show_trans_btn")
        self.show_trans_btn.setGeometry(QRect(13, 10, 131, 31))
        self.show_trans_btn.setFont(font)
        self.timeFrame = QFrame(self.centralwidget)
        self.timeFrame.setObjectName(u"timeFrame")
        self.timeFrame.setGeometry(QRect(9, 120, 251, 31))
        self.timeFrame.setFrameShape(QFrame.Box)
        self.timeFrame.setFrameShadow(QFrame.Raised)
        self.sec = QLabel(self.timeFrame)
        self.sec.setObjectName(u"sec")
        self.sec.setGeometry(QRect(83, 1, 81, 31))
        self.trans_time = QLabel(self.timeFrame)
        self.trans_time.setObjectName(u"trans_time")
        self.trans_time.setGeometry(QRect(13, 1, 61, 31))
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(9, 160, 251, 31))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.show_status = QLabel(self.frame)
        self.show_status.setObjectName(u"show_status")
        self.show_status.setGeometry(QRect(50, 8, 191, 16))
        self.status_lbl = QLabel(self.frame)
        self.status_lbl.setObjectName(u"status_lbl")
        self.status_lbl.setGeometry(QRect(13, 8, 31, 16))
        self.dev_info = QLabel(self.centralwidget)
        self.dev_info.setObjectName(u"dev_info")
        self.dev_info.setGeometry(QRect(13, 202, 251, 21))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Ehnd \uc6f9 \ubc88\uc5ed", None))
        self.go_dev_page.setText(QCoreApplication.translate("MainWindow", u"\uc81c\uc791\uc790\n"
"\ud648\ud398\uc774\uc9c0", None))
        self.show_ori_btn.setText(QCoreApplication.translate("MainWindow", u"\uc6d0\ubcf8 \ubcf4\uae30", None))
        self.show_trans_btn.setText(QCoreApplication.translate("MainWindow", u"\ubc88\uc5ed\ubcf8 \ubcf4\uae30", None))
        self.sec.setText("")
        self.trans_time.setText(QCoreApplication.translate("MainWindow", u"\ubc88\uc5ed \uc2dc\uac04:", None))
        self.show_status.setText("")
        self.status_lbl.setText(QCoreApplication.translate("MainWindow", u"\uc0c1\ud0dc: ", None))
        self.dev_info.setText(QCoreApplication.translate("MainWindow", u"\uc81c\uc791\uc790: kdr             \ub9c8\uc9c0\ub9c9 \uc5c5\ub370\uc774\ud2b8: 210411", None))
    # retranslateUi

