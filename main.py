import os
import sys
import datetime
import time

import pygame
from pygame.locals import *
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTime, QTimer, QUrl
from PyQt5.QtWidgets import QMainWindow, QLCDNumber, QPushButton, QWidget, QLineEdit, QStackedWidget, QGridLayout, \
    QComboBox, QFileDialog, QMessageBox, QLabel, QListWidget, QFormLayout, QHBoxLayout, QVBoxLayout, QDialog, \
    QErrorMessage
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
        timer.timeout.connect(self.AlarmIsRinging)
        timer.start(1000)

        # Выравникание виджетов под размер окна
        self.MainLayout = QGridLayout(self.widget)
        self.ClockWidget = QWidget()
        self.StopWatchWidget = QWidget()

        # Интерфейс будильника

        self.AddAlarmButton = QtWidgets.QPushButton('ДОБАВИТЬ', self.ClockWidget)
        self.AddAlarmButton.clicked.connect(self.AddAlarmsComboBoxItem)

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
            if i < 10:
                self.HoursComboBox.addItem('0' + str(i))
            else:
                self.HoursComboBox.addItem(str(i))

        self.MusicListComboBox = QComboBox(self.ClockWidget)
        self.MusicListComboBox.addItem('<Музыка не выбрана>')
        self.MusicListComboBox.activated.connect(self.UpdateMusic)

        self.ListDeleteAlarmClocks = QListWidget(self.ClockWidget)
        self.ListDeleteAlarmClocks .setMaximumWidth(20)
        self.ListDeleteAlarmClocks.itemClicked.connect(self.DeleteAlarmClock)

        self.ListOfPastAlarmClocks = QListWidget(self.ClockWidget)
        self.ListOfPastAlarmClocks.itemActivated.connect(self.StartORStopAlarmClock)

        self.formLayout = QFormLayout()
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.MinutesComboBox)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.HoursComboBox)

        self.verticalLayout = QHBoxLayout()
        #self.verticalLayout.addWidget(self.ListOfAlarmClocks)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.addWidget(self.AddMusicButton)
        self.horizontalLayout_2.addWidget(self.AddressMusicLine)
        self.horizontalLayout_2.addWidget(self.MusicListComboBox)

        SpacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout = QGridLayout(self.ClockWidget)
        self.gridLayout.addWidget(self.AddAlarmButton, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.ListOfPastAlarmClocks, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.ListDeleteAlarmClocks , 2, 2, 1, 1)
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

    def showDateTime(self):
        timeNow = QTime.currentTime()
        text = timeNow.toString('hh:mm')
        if (timeNow.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]

        self.TimeNow.display(text)
        self.DateNow.setText(str(datetime.date.today()))

    def StartORStopAlarmClock(self):
        a = self.ListOfPastAlarmClocks.currentItem().text().replace('<<(', '')
        a = a.replace(')>>', '')
        if '<<(' in self.ListOfPastAlarmClocks.currentItem().text():
            self.ListOfPastAlarmClocks.currentItem().setText(a)
        else:
            self.ListOfPastAlarmClocks.currentItem().setText('<<(' + a + ')>>')

    def DeleteAlarmClock(self):
        Row = self.ListDeleteAlarmClocks.currentIndex().row()
        self.ListOfPastAlarmClocks.takeItem(Row)
        self.ListDeleteAlarmClocks.takeItem(Row)

    def AlarmIsRinging(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        a = '<<(' + text[:2] + ':' + text[3:] + ')>>'
        for index in range(self.ListOfPastAlarmClocks.count()):
            if a == self.ListOfPastAlarmClocks.item(index).text():
                b = self.ListOfPastAlarmClocks.item(index).text().replace('<<(', '')
                b = b.replace(')>>', '')
                self.ListOfPastAlarmClocks.item(index).setText(b)
                pygame.mixer.init()
                pygame.mixer.music.load(self.FileName)
                pygame.mixer.music.play()

                msg = QMessageBox()
                msg.setText(a)
                msg.setIcon(QMessageBox.Warning)
                msg.setInformativeText('Будильник>')
                msg.setWindowTitle("Будильник")
                msg.exec_()
                pygame.mixer.music.stop()

    def UpdateMusic(self):
        self.FileName = self.AddressMusicLine.text() + '/' + self.MusicListComboBox.currentText()

    def DialogAddMusic(self):
        try:
            fname = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
            files = os.listdir(fname)
            for i in files:
                if '.mp3' in i:
                    self.MusicListComboBox.addItem(i)
            self.AddressMusicLine.setText(fname)
            self.MusicListComboBox.setCurrentIndex(1)
        except:
            print('Что-то не так с музыкой')

    def AddAlarmsComboBoxItem(self):
        if self.ListOfPastAlarmClocks.count() < 14:
            item = self.HoursComboBox.currentText() + ':' + self.MinutesComboBox.currentText()
            if '<<(' + item + ')>>' not in self.ListOfPastAlarmClocks.selectedItems():
                self.ListOfPastAlarmClocks.addItem('<<(' + item + ')>>')
                self.ListDeleteAlarmClocks.addItem('X')
        else:
            msg = QMessageBox()
            msg.setText("Слишком много будильников.")
            msg.setIcon(QMessageBox.Critical)
            msg.setInformativeText('Нельзя добавить больше четырнадцати будильников.')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

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
