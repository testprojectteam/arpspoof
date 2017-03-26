# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(785, 481)
        MainWindow.setMinimumSize(QtCore.QSize(444, 323))
        MainWindow.setMaximumSize(QtCore.QSize(785, 481))
        MainWindow.setWindowOpacity(0.5)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startDetect = QtWidgets.QPushButton(self.centralwidget)
        self.startDetect.setObjectName("startDetect")
        self.horizontalLayout.addWidget(self.startDetect)
        self.vhbutton = QtWidgets.QPushButton(self.centralwidget)
        self.vhbutton.setEnabled(False)
        self.vhbutton.setObjectName("vhbutton")
        self.horizontalLayout.addWidget(self.vhbutton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.stopDetect = QtWidgets.QPushButton(self.centralwidget)
        self.stopDetect.setEnabled(False)
        self.stopDetect.setObjectName("stopDetect")
        self.horizontalLayout_2.addWidget(self.stopDetect)
        self.ihbutton = QtWidgets.QPushButton(self.centralwidget)
        self.ihbutton.setEnabled(False)
        self.ihbutton.setObjectName("ihbutton")
        self.horizontalLayout_2.addWidget(self.ihbutton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.currpac = QtWidgets.QPushButton(self.centralwidget)
        self.currpac.setEnabled(False)
        self.currpac.setObjectName("currpac")
        self.verticalLayout.addWidget(self.currpac)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 28))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Arp Spoof Detection Engine"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600; text-decoration: underline;\">Cyber Eye</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Click Start Detection to start listening for arp packets</span></p></body></html>"))
        self.startDetect.setText(_translate("MainWindow", "Start Detection"))
        self.vhbutton.setText(_translate("MainWindow", "View Valid Hosts"))
        self.stopDetect.setText(_translate("MainWindow", "Stop Detection"))
        self.ihbutton.setText(_translate("MainWindow", "View Invalid Hosts"))
        self.currpac.setText(_translate("MainWindow", "View Currently Captured Packets"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Status : </span><span style=\" font-weight:600; color:#ef2929;\">Not listening</span></p></body></html>"))

