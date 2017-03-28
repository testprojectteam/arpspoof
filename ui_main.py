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
        MainWindow.resize(575, 500)
        MainWindow.setMinimumSize(QtCore.QSize(575, 475))
        MainWindow.setMaximumSize(QtCore.QSize(600, 500))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../Downloads/eye.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(0.5)
        MainWindow.setStyleSheet("border-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.19397 rgba(0, 0, 0, 255), stop:0.202312 rgba(122, 97, 0, 255), stop:0.495514 rgba(76, 58, 0, 255), stop:0.504819 rgba(255, 255, 255, 255), stop:0.79 rgba(255, 255, 255, 255), stop:1 rgba(255, 158, 158, 255));\n"
"color: rgb(0, 0, 0);\n"
"font: 16pt \"Cantarell\";\n"
"background-color: rgba(255, 255, 255);\n"
"")
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.ihbutton = QtWidgets.QPushButton(self.centralwidget)
        self.ihbutton.setEnabled(False)
        self.ihbutton.setObjectName("ihbutton")
        self.gridLayout.addWidget(self.ihbutton, 7, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(563, 113))
        self.label.setMaximumSize(QtCore.QSize(16777215, 127))
        self.label.setStyleSheet("image: url(:/img/Downloads/WhatsApp Image 2017-03-27 at 23.31.53.jpeg);")
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 28))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 10, 0, 1, 1)
        self.helpButton = QtWidgets.QToolButton(self.centralwidget)
        self.helpButton.setObjectName("helpButton")
        self.gridLayout.addWidget(self.helpButton, 10, 1, 1, 1, QtCore.Qt.AlignRight)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setEnabled(True)
        self.tableView.setMaximumSize(QtCore.QSize(16777215, 200))
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 3, 0, 1, 2)
        self.startDetect = QtWidgets.QPushButton(self.centralwidget)
        self.startDetect.setStyleSheet("background-color: rgb(115, 210, 22);\n"
"color: rgb(0, 0, 0);\n"
"\n"
"")
        self.startDetect.setObjectName("startDetect")
        self.gridLayout.addWidget(self.startDetect, 9, 0, 1, 2)
        self.vhbutton = QtWidgets.QPushButton(self.centralwidget)
        self.vhbutton.setEnabled(False)
        self.vhbutton.setObjectName("vhbutton")
        self.gridLayout.addWidget(self.vhbutton, 7, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 13))
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("font: 11pt \"Cantarell\";")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Arp Spoof Detection Engine"))
        self.ihbutton.setText(_translate("MainWindow", "View Invalid Hosts"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Status : </span><span style=\" font-weight:600; color:#ef2929;\">Not listening</span></p></body></html>"))
        self.helpButton.setText(_translate("MainWindow", "?"))
        self.startDetect.setText(_translate("MainWindow", "Start Detection"))
        self.vhbutton.setText(_translate("MainWindow", "View Valid Hosts"))
        self.label_3.setText(_translate("MainWindow", "Sniffed Packets :"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

import img_rc
