import os
import sys
import datetime
import sqlite3

import pygame
from pygame.locals import *
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTime, QTimer, QUrl
from PyQt5.QtWidgets import QMainWindow, QLCDNumber, QPushButton, QWidget, QLineEdit, QStackedWidget, QGridLayout, \
    QComboBox, QFileDialog, QMessageBox, QLabel, QListWidget, QFormLayout, QHBoxLayout, QVBoxLayout, QDialog, \
    QErrorMessage, QInputDialog, QListView
from pygame.mixer import Sound

from AppInterface import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

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
        self.MusicListComboBox.addItem('<Выбрать песню>')
        self.MusicListComboBox.activated.connect(self.UpdateMusic)
        self.MusicListComboBox.setMaximumWidth(200)

        self.ListDeleteAlarmClocks = QListWidget(self.ClockWidget)
        self.ListDeleteAlarmClocks.setMaximumWidth(20)
        self.ListDeleteAlarmClocks.itemClicked.connect(self.DeleteAlarmClock)

        self.ListOfPastAlarmClocks = QListWidget(self.ClockWidget)
        self.ListOfPastAlarmClocks.itemActivated.connect(self.StartORStopAlarmClock)

        self.formLayout = QFormLayout()
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.MinutesComboBox)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.HoursComboBox)

        self.verticalLayout = QHBoxLayout()

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.addWidget(self.AddMusicButton)
        self.horizontalLayout_2.addWidget(self.AddressMusicLine)
        self.horizontalLayout_2.addWidget(self.MusicListComboBox)

        SpacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout = QGridLayout(self.ClockWidget)
        self.gridLayout.addWidget(self.AddAlarmButton, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.ListOfPastAlarmClocks, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.ListDeleteAlarmClocks, 2, 2, 1, 1)
        self.gridLayout.addLayout(self.formLayout, 6, 1, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 2, 1, 1)
        self.gridLayout.addLayout(self.verticalLayout, 2, 2, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 2)
        self.gridLayout.addItem(SpacerItem, 2, 1, 1, 1)

        # Интерфейс секундомера
        self.lcdNumber = QLCDNumber(self.StopWatchWidget)

        self.StartPushButton = QPushButton('Старт', self.StopWatchWidget)

        self.StopPushButton = QPushButton('Стоп', self.StopWatchWidget)

        self.listView = QListView(self.StopWatchWidget)
        self.listView.setMinimumHeight(400)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.addWidget(self.lcdNumber)

        self.formLayout = QFormLayout(self.StopWatchWidget)
        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.verticalLayout)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.StartPushButton)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.StopPushButton)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.listView)

        # Добавление виджетов с устройствами в главное размещение
        self.MainLayout.addWidget(self.ClockWidget)
        self.MainLayout.addWidget(self.StopWatchWidget)

        # Прячем не нужные виджеты
        self.StopWatchWidget.hide()

        # Запуск таймера
        self.showDateTime()
        self.LoadAlarmClocks()

        self.wid = QWidget()
        self.wid.resize(400, 300)
        self.verticalLayout = QVBoxLayout(self.wid)
        self.label = QLabel(self.wid)
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout()
        self.Ok_button = QPushButton('OK', self.wid)
        self.Ok_button.clicked.connect(self.OkPressed)
        self.horizontalLayout.addWidget(self.Ok_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        with open('AddressMusic.txt', 'r') as Address:
            add = Address.readline()
            self.AddressMusicLine.setText(add)

            for i in os.listdir(add):
                if '.mp3' in i:
                    self.MusicListComboBox.addItem(i)

            self.AddressMusic = add

        with open('SelectedMusic.txt', 'r') as Music:
            self.MusicListComboBox.currentIndex()
            self.FileName = self.AddressMusic + '/' + Music.read()

    def LoadAlarmClocks(self):
        con = sqlite3.connect('AlarmClock.db')
        cur = con.cursor()
        result = cur.execute("""SELECT Time FROM Clocks""").fetchall()
        for elem in result:
            self.ListOfPastAlarmClocks.addItem(''.join(elem))
            self.ListDeleteAlarmClocks.addItem('X')
        con.close()

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
        con = sqlite3.connect('AlarmClock.db')
        cur = con.cursor()
        if '<<(' in self.ListOfPastAlarmClocks.currentItem().text():
            self.ListOfPastAlarmClocks.currentItem().setText(a)
            cur.execute("""UPDATE Clocks set Time = ? WHERE Time = ?""", (a, '<<(' + a + ')>>'))
        else:
            self.ListOfPastAlarmClocks.currentItem().setText('<<(' + a + ')>>')
            cur.execute("""UPDATE Clocks set Time = ? WHERE Time = ?""", ('<<(' + a + ')>>', a))
        con.commit()
        con.close()

    def DeleteAlarmClock(self):
        Row = self.ListDeleteAlarmClocks.currentIndex().row()
        Item = self.ListOfPastAlarmClocks.item(Row).text()
        self.ListOfPastAlarmClocks.takeItem(Row)
        self.ListDeleteAlarmClocks.takeItem(Row)

        con = sqlite3.connect('AlarmClock.db')
        cur = con.cursor()
        cur.execute("""DELETE FROM Clocks WHERE Time = ?""", (Item,)).fetchall()
        con.commit()
        con.close()

    def AlarmIsRinging(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        ThisTime = '<<(' + text[:2] + ':' + text[3:] + ')>>'
        for index in range(self.ListOfPastAlarmClocks.count()):
            if ThisTime == self.ListOfPastAlarmClocks.item(index).text():
                b = self.ListOfPastAlarmClocks.item(index).text().replace('<<(', '')
                b = b.replace(')>>', '')

                con = sqlite3.connect('AlarmClock.db')
                cur = con.cursor()
                cur.execute("""UPDATE Clocks SET Time = ? WHERE Time = ?""", (b, ThisTime)).fetchall()
                con.commit()
                con.close()

                self.ListOfPastAlarmClocks.item(index).setText(b)

                pygame.mixer.init()
                pygame.mixer.music.load(self.FileName)
                pygame.mixer.music.play()

                path = 'ClockRiding.gif'
                gif = QtGui.QMovie(path)
                self.label.setMovie(gif)
                gif.start()

                self.wid.show()

    def OkPressed(self):
        pygame.mixer.music.stop()
        self.wid.hide()

    def UpdateMusic(self):
        self.FileName = self.AddressMusicLine.text() + '/' + self.MusicListComboBox.currentText()
        with open('SelectedMusic.txt', 'w') as Music:
            Music.write(self.MusicListComboBox.currentText())

    def DialogAddMusic(self):
        try:
            fname = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
            files = os.listdir(fname)
            self.MusicListComboBox.clear()
            for i in files:
                if '.mp3' in i:
                    self.MusicListComboBox.addItem(i)
            self.AddressMusicLine.setText(fname)
            self.MusicListComboBox.setCurrentIndex(1)

            with open('AddressMusic.txt', 'w') as file:
                file.write(fname)


            # con = sqlite3.connect('AlarmClock.db')
            # cur = con.cursor()
            # cur.execute("""UPDATE Clocks set""", (item, )).fetchall()
            # con.commit()
            # con.close()
        except:
            print('Музыка не была выбрана')

    def AddAlarmsComboBoxItem(self):
        Alarm = False
        if self.ListOfPastAlarmClocks.count() < 14:
            item = self.HoursComboBox.currentText() + ':' + self.MinutesComboBox.currentText()
            for i in range(self.ListOfPastAlarmClocks.count()):
                if item in self.ListOfPastAlarmClocks.item(i).text():
                    Alarm = True
            if Alarm == False:
                self.ListOfPastAlarmClocks.addItem('<<(' + item + ')>>')

                item = '<<(' + item + ')>>'
                con = sqlite3.connect('AlarmClock.db')
                cur = con.cursor()
                cur.execute("""INSERT INTO Clocks (Time) values(?)""", (item,)).fetchall()
                con.commit()
                con.close()

                self.ListDeleteAlarmClocks.addItem('X')
                Alarm = False
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
