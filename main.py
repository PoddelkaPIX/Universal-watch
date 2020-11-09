import os
import sys
import datetime
import time

import pygame
from pygame.locals import *
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTime, QTimer, QUrl
from PyQt5.QtWidgets import QMainWindow, QLCDNumber, QPushButton, QWidget, QLineEdit, QStackedWidget, QGridLayout, \
    QComboBox, QFileDialog, QMessageBox, QLabel, QListWidget, QFormLayout, QHBoxLayout, QVBoxLayout
from pygame.mixer import Sound

from AppInterface import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.FileName = 'C:/Users/gnebe/Desktop/Python/Universal-watch/Sounds/5Sta Family - Первый снег.mp3'

        # Подключение к кнопкам функционал
        self.AlarmClockBut.clicked.connect(self.OpenAlarmClock)
        self.StopWatchBut.clicked.connect(self.OpenStopWatch)

        # Создание таймера
        timer = QTimer(self)
        timer.timeout.connect(self.showDateTime)
        timer.start(1000)

        # Выравникание виджетов под размер окна
        self.MainLayout = QGridLayout(self.widget)
        self.ClockWidget = QWidget()
        self.StopWatchWidget = QWidget()

        # Интерфейс будильника

        self.AddAlarmButton = QtWidgets.QPushButton('ДОБАВИТЬ', self.ClockWidget)
        self.AddAlarmButton.clicked.connect(self.AddAlarmsComboBoxItem)

        self.StartAlarmButton = QtWidgets.QPushButton('----------', self.ClockWidget)

        self.StopAlarmButton = QtWidgets.QPushButton('СТОП', self.ClockWidget)
        self.StopAlarmButton.clicked.connect(self.StopCountTime)
        self.StopAlarmButton.hide()

        self.PauseButton = QtWidgets.QPushButton('ПАУЗА', self.ClockWidget)
        self.PauseButton.hide()

        self.AddMusicButton = QtWidgets.QPushButton('Добавить свою музыку', self.ClockWidget)
        self.AddMusicButton.clicked.connect(self.DialogAddMusic)
        self.AddressMusicLine = QtWidgets.QLineEdit(self.ClockWidget)

        self.MinutesComboBox = QComboBox(self.ClockWidget)
        self.MinutesComboBox.setMinimumWidth(200)
        for i in range(0, 60):
            if i < 10:
                self.MinutesComboBox.addItem('0' + str(i))
            else:
                self.MinutesComboBox.addItem(str(i))

        self.HoursComboBox = QComboBox(self.ClockWidget)
        self.HoursComboBox.setMinimumWidth(100)
        for i in range(0, 24):
            self.HoursComboBox.addItem(str(i))

        self.MusicListComboBox = QComboBox(self.ClockWidget)
        self.MusicListComboBox.addItem('<Не выбрано>')

        self.ListOfAlarmClocks = QListWidget(self.ClockWidget)
        self.ListOfAlarmClocks.setMinimumWidth(350)

        self.ListOfPastAlarmClocks = QListWidget(self.ClockWidget)
        self.ListOfPastAlarmClocks.itemActivated.connect(self.DeletePastClock)

        self.formLayout = QFormLayout()
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.MinutesComboBox)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.HoursComboBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.StartAlarmButton)
        self.horizontalLayout.addWidget(self.StopAlarmButton)
        self.horizontalLayout.addWidget(self.PauseButton)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.ListOfAlarmClocks)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.addWidget(self.AddMusicButton)
        self.horizontalLayout_2.addWidget(self.AddressMusicLine)
        self.horizontalLayout_2.addWidget(self.MusicListComboBox)

        SpacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout = QGridLayout(self.ClockWidget)
        self.gridLayout.addWidget(self.AddAlarmButton, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.ListOfPastAlarmClocks, 2, 1, 1, 1)
        self.gridLayout.addLayout(self.formLayout, 6, 1, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 2, 1, 1)
        self.gridLayout.addLayout(self.verticalLayout, 2, 2, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 2)
        self.gridLayout.addItem(SpacerItem, 2, 1, 1, 1)

        # Интерфейс секундомера
        self.formLayout = QtWidgets.QFormLayout(self.StopWatchWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.lcdNumber = QtWidgets.QLCDNumber(self.StopWatchWidget)
        self.verticalLayout.addWidget(self.lcdNumber)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.verticalLayout)
        self.pushButton = QtWidgets.QPushButton(self.StopWatchWidget)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pushButton)
        self.listView = QtWidgets.QListView(self.StopWatchWidget)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.listView)

        # Добавление виджетов с устройствами в главное размещение
        self.MainLayout.addWidget(self.ClockWidget)
        self.MainLayout.addWidget(self.StopWatchWidget)

        # Прячем не нужные виджеты
        self.StopWatchWidget.hide()

        # Запуск таймера
        self.showDateTime()

        # 'C:/Users/gnebe/Desktop/Python/Universal-watch/Sounds/5Sta Family - Первый снег.mp3'
        pygame.mixer.init()

    def showDateTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]

        self.TimeNow.display(text)
        self.DateNow.setText(str(datetime.date.today()))

    def DeletePastClock(self):
        self.FileName = self.AddressMusicLine.text() + '/' + self.MusicListView.currentItem().text()

    def DialogAddMusic(self):
        try:
            fname = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
            files = os.listdir(fname)
            for i in files:
                if '.mp3' in i:
                    self.MusicListComboBox.addItem(i)
            self.AddressMusicLine.setText(fname)
        except:
            print('Что-то не так с музыкой')

    def StopCountTime(self):
        pygame.mixer.music.stop()

        self.StopAlarmButton.hide()
        self.PauseButton.hide()
        self.StartAlarmButton.show()
        self.MusicListComboBox.setEnabled(True)
        self.MinutesComboBox.setEnabled(True)
        self.HoursComboBox.setEnabled(True)
        self.AddAlarmButton.setEnabled(True)
        self.DeleteAlarmButton.setEnabled(True)
        self.AddressMusicLine.setEnabled(True)

    def AddAlarmsComboBoxItem(self):
        item = self.HoursComboBox.currentText() + ':' + self.MinutesComboBox.currentText()
        print(item)
        self.ListOfPastAlarmClocks.addItem(item)
        self.ListOfAlarmClocks.addItem('<(' + item + ')>')

    def OpenAlarmClock(self):
        self.StopWatchWidget.hide()
        self.ClockWidget.show()

    def OpenStopWatch(self):
        self.ClockWidget.hide()
        self.StopWatchWidget.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
