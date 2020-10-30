# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\gnebe\Desktop\Python\YandexWatchProgect\UI\UniversalWatch.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(767, 784)
        MainWindow.setStyleSheet("background-color: rgb(13, 22, 75);\n"
"gridline-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 155, 155));")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AlarmClockBut = QtWidgets.QPushButton(self.centralwidget)
        self.AlarmClockBut.setStyleSheet("background-color: #3b408a")
        self.AlarmClockBut.setObjectName("AlarmClockBut")
        self.horizontalLayout.addWidget(self.AlarmClockBut)
        self.StopWatchBut = QtWidgets.QPushButton(self.centralwidget)
        self.StopWatchBut.setStyleSheet("background-color: #3b408a")
        self.StopWatchBut.setObjectName("StopWatchBut")
        self.horizontalLayout.addWidget(self.StopWatchBut)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setStyleSheet("background-color: #3b408a")
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.TimeNow = QtWidgets.QLCDNumber(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TimeNow.sizePolicy().hasHeightForWidth())
        self.TimeNow.setSizePolicy(sizePolicy)
        self.TimeNow.setMinimumSize(QtCore.QSize(40, 30))
        self.TimeNow.setStyleSheet("")
        self.TimeNow.setObjectName("TimeNow")
        self.verticalLayout.addWidget(self.TimeNow)
        self.DateNow = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DateNow.sizePolicy().hasHeightForWidth())
        self.DateNow.setSizePolicy(sizePolicy)
        self.DateNow.setMinimumSize(QtCore.QSize(70, 30))
        self.DateNow.setMaximumSize(QtCore.QSize(70, 30))
        self.DateNow.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.DateNow.setStyleSheet("font: 8pt \"Myriad Variable Concept SemiExt\";\n"
"color: rgb(255, 239, 240);\n"
"")
        self.DateNow.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.DateNow.setText("")
        self.DateNow.setObjectName("DateNow")
        self.verticalLayout.addWidget(self.DateNow)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setStyleSheet("background-color: rgb(5, 20, 90);")
        self.widget.setObjectName("widget")
        self.gridLayout_2.addWidget(self.widget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Универсальные часы"))
        self.AlarmClockBut.setText(_translate("MainWindow", "Будильник"))
        self.StopWatchBut.setText(_translate("MainWindow", "Секундамер"))
        self.pushButton_4.setText(_translate("MainWindow", "Таймер"))
