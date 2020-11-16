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
        MainWindow.setFixedSize(755, 584)
        MainWindow.setStyleSheet("background-color: rgb(26, 26, 26);\n")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AlarmClockBut = QtWidgets.QPushButton(self.centralwidget)
        self.AlarmClockBut.setStyleSheet("background-color: rgb(143, 143, 143);")
        self.AlarmClockBut.setObjectName("AlarmClockBut")
        self.horizontalLayout.addWidget(self.AlarmClockBut)
        self.StopWatchBut = QtWidgets.QPushButton(self.centralwidget)
        self.StopWatchBut.setStyleSheet("background-color: rgb(143, 143, 143);")
        self.StopWatchBut.setObjectName("StopWatchBut")
        self.horizontalLayout.addWidget(self.StopWatchBut)
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
        self.DateNow.setMinimumSize(QtCore.QSize(80, 30))
        self.DateNow.setMaximumSize(QtCore.QSize(80, 30))
        self.DateNow.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.DateNow.setStyleSheet("font: 9pt \"Myriad Variable Concept SemiExt\";\n"
                                   "color: rgb(255, 255, 255);\n""")
        self.DateNow.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.DateNow.setText("")
        self.DateNow.setObjectName("DateNow")
        self.verticalLayout.addWidget(self.DateNow)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.widget = QtWidgets.QWidget(self.centralwidget)
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
