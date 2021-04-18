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
        MainWindow.resize(649, 198)
        MainWindow.setMinimumSize(QSize(268, 167))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.wholeFrame = QFrame(self.centralwidget)
        self.wholeFrame.setObjectName(u"wholeFrame")
        self.wholeFrame.setGeometry(QRect(9, 10, 621, 151))
        self.wholeFrame.setFrameShape(QFrame.Box)
        self.wholeFrame.setFrameShadow(QFrame.Raised)
        self.reloadBtn = QPushButton(self.wholeFrame)
        self.reloadBtn.setObjectName(u"reloadBtn")
        self.reloadBtn.setGeometry(QRect(520, 110, 91, 28))
        font = QFont()
        font.setPointSize(11)
        self.reloadBtn.setFont(font)
        self.window_list = QComboBox(self.wholeFrame)
        self.window_list.setObjectName(u"window_list")
        self.window_list.setGeometry(QRect(9, 112, 501, 21))
        self.timeFrame = QFrame(self.wholeFrame)
        self.timeFrame.setObjectName(u"timeFrame")
        self.timeFrame.setGeometry(QRect(250, 16, 151, 31))
        self.timeFrame.setFrameShape(QFrame.Box)
        self.timeFrame.setFrameShadow(QFrame.Raised)
        self.sec = QLabel(self.timeFrame)
        self.sec.setObjectName(u"sec")
        self.sec.setGeometry(QRect(74, 1, 61, 31))
        self.trans_time = QLabel(self.timeFrame)
        self.trans_time.setObjectName(u"trans_time")
        self.trans_time.setGeometry(QRect(13, 1, 81, 31))
        self.frame = QFrame(self.wholeFrame)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(250, 63, 151, 31))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.show_status = QLabel(self.frame)
        self.show_status.setObjectName(u"show_status")
        self.show_status.setGeometry(QRect(46, 6, 101, 20))
        self.status_lbl = QLabel(self.frame)
        self.status_lbl.setObjectName(u"status_lbl")
        self.status_lbl.setGeometry(QRect(13, 8, 51, 16))
        self.btnFrame = QFrame(self.wholeFrame)
        self.btnFrame.setObjectName(u"btnFrame")
        self.btnFrame.setGeometry(QRect(10, 10, 231, 91))
        self.btnFrame.setFrameShape(QFrame.Box)
        self.btnFrame.setFrameShadow(QFrame.Raised)
        self.show_ori_btn = QPushButton(self.btnFrame)
        self.show_ori_btn.setObjectName(u"show_ori_btn")
        self.show_ori_btn.setGeometry(QRect(90, 5, 71, 31))
        font1 = QFont()
        font1.setFamily(u"Consolas")
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setWeight(50)
        self.show_ori_btn.setFont(font1)
        self.show_trans_btn = QPushButton(self.btnFrame)
        self.show_trans_btn.setObjectName(u"show_trans_btn")
        self.show_trans_btn.setGeometry(QRect(7, 5, 81, 31))
        self.show_trans_btn.setFont(font1)
        self.stop_trans_btn = QPushButton(self.btnFrame)
        self.stop_trans_btn.setObjectName(u"stop_trans_btn")
        self.stop_trans_btn.setGeometry(QRect(163, 5, 61, 31))
        font2 = QFont()
        font2.setPointSize(10)
        self.stop_trans_btn.setFont(font2)
        self.isPrintBoth = QCheckBox(self.btnFrame)
        self.isPrintBoth.setObjectName(u"isPrintBoth")
        self.isPrintBoth.setGeometry(QRect(10, 37, 151, 19))
        self.isPrintBoth.setFont(font2)
        self.isAutoTrans = QCheckBox(self.btnFrame)
        self.isAutoTrans.setObjectName(u"isAutoTrans")
        self.isAutoTrans.setGeometry(QRect(10, 54, 211, 19))
        self.isAutoTrans.setFont(font2)
        self.isPrintLog = QCheckBox(self.btnFrame)
        self.isPrintLog.setObjectName(u"isPrintLog")
        self.isPrintLog.setGeometry(QRect(10, 71, 211, 19))
        self.isPrintLog.setFont(font2)
        self.authorFrame = QFrame(self.wholeFrame)
        self.authorFrame.setObjectName(u"authorFrame")
        self.authorFrame.setGeometry(QRect(410, 10, 201, 91))
        self.authorFrame.setFrameShape(QFrame.Box)
        self.authorFrame.setFrameShadow(QFrame.Raised)
        self.dev_info = QLabel(self.authorFrame)
        self.dev_info.setObjectName(u"dev_info")
        self.dev_info.setGeometry(QRect(100, 10, 81, 71))
        self.dev_info.setFrameShape(QFrame.NoFrame)
        self.go_dev_page = QPushButton(self.authorFrame)
        self.go_dev_page.setObjectName(u"go_dev_page")
        self.go_dev_page.setGeometry(QRect(7, 5, 75, 81))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Ehnd \uc6f9 \ubc88\uc5ed", None))
        self.reloadBtn.setText(QCoreApplication.translate("MainWindow", u"\ub9ac\ub85c\ub4dc", None))
        self.sec.setText("")
        self.trans_time.setText(QCoreApplication.translate("MainWindow", u"\ubc88\uc5ed \uc2dc\uac04:", None))
        self.show_status.setText("")
        self.status_lbl.setText(QCoreApplication.translate("MainWindow", u"\uc0c1\ud0dc: ", None))
        self.show_ori_btn.setText(QCoreApplication.translate("MainWindow", u"\uc6d0\ubcf8 \ubcf4\uae30", None))
        self.show_trans_btn.setText(QCoreApplication.translate("MainWindow", u"\ubc88\uc5ed\ubcf8 \ubcf4\uae30", None))
        self.stop_trans_btn.setText(QCoreApplication.translate("MainWindow", u"\ubc88\uc5ed \uc911\uc9c0", None))
        self.isPrintBoth.setText(QCoreApplication.translate("MainWindow", u"\uc6d0\ubb38/\ubc88\uc5ed\ubb38 \ub3d9\uc2dc \ucd9c\ub825", None))
        self.isAutoTrans.setText(QCoreApplication.translate("MainWindow", u"\ud398\uc774\uc9c0 \ubc14\ub014 \ub54c\ub9c8\ub2e4 \uc790\ub3d9 \ubc88\uc5ed", None))
        self.isPrintLog.setText(QCoreApplication.translate("MainWindow", u"\ubc88\uc5ed \ub85c\uadf8 \ucd9c\ub825", None))
        self.dev_info.setText(QCoreApplication.translate("MainWindow", u"\uc81c\uc791\uc790: kdr \n"
"  V.210418", None))
        self.go_dev_page.setText(QCoreApplication.translate("MainWindow", u"\uc81c\uc791\uc790\n"
"\ud648\ud398\uc774\uc9c0", None))
    # retranslateUi

if __name__ == "__main__": 
    import sys 
    app = QApplication(sys.argv) 
    form = QMainWindow() 
    ui = Ui_MainWindow() 
    ui.setupUi(form) 
    form.show() 
    sys.exit(app.exec_()) 
