import os
import sys
import datetime
import sqlite3
import pygame

from AppInterface import Ui_MainWindow
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QGridLayout, \
                            QComboBox, QFileDialog, QMessageBox, QLabel, QListWidget, \
                            QFormLayout, QHBoxLayout, QVBoxLayout


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Загружка основного интерфейса программы из отдельного файла
        self.setupUi(self)

        # Переменные для работы секундомера
        self.ms = 0
        self.sec = 0
        self.min = 0
        self.hour = 0

        self.FirstHour = 0
        self.FirstMin = 0
        self.FirstSec = 0
        self.FirstMs = 0

        # Кнопкам для переключения будильника и секундомера
        self.AlarmClockBut.clicked.connect(self.OpenAlarmClock)
        self.StopWatchBut.clicked.connect(self.OpenStopWatch)

        # Таймер для обновления времени на таблойде
        self.timerTime = QTimer(self)
        self.timerTime.timeout.connect(self.showDateTime)
        self.timerTime.timeout.connect(self.AlarmIsRinging)
        self.timerTime.start(1000)

        # Таймер секундомера
        self.timerStopWatch = QtCore.QTimer(self)
        self.timerStopWatch.setInterval(10)
        self.timerStopWatch.timeout.connect(self.displayTime)

        # Выравникание виджетов под размер окна
        self.MainLayout = QGridLayout(self.widget)
        self.ClockWidget = QWidget()
        self.StopWatchWidget = QWidget()

        # Интерфейс будильника
        self.AddAlarmButton = QtWidgets.QPushButton('ДОБАВИТЬ', self.ClockWidget)
        self.AddAlarmButton.clicked.connect(self.AddAlarmsComboBoxItem)
        self.AddAlarmButton.setStyleSheet('background-color: rgb(133, 133, 133);')

        self.MusicListComboBox = QComboBox(self.ClockWidget)
        self.MusicListComboBox.addItem('<Выбрать песню>')
        self.MusicListComboBox.activated.connect(self.UpdateMusic)
        self.MusicListComboBox.setMaximumWidth(200)
        self.MusicListComboBox.setStyleSheet('background-color: rgb(133, 133, 133);')

        self.AddMusicButton = QtWidgets.QPushButton('Добавить свою музыку', self.ClockWidget)
        self.AddMusicButton.clicked.connect(self.DialogAddMusic)
        self.AddMusicButton.setStyleSheet('background-color: rgb(133, 133, 133);')

        self.AddressMusicLine = QtWidgets.QLineEdit(self.ClockWidget)
        self.AddressMusicLine.setEnabled(False)
        self.AddressMusicLine.setStyleSheet('color: rgb(143, 143, 143);'
                                            'border: 0px solid #ccc')

        self.MinutesComboBox = QComboBox(self.ClockWidget)
        self.MinutesComboBox.setMinimumWidth(200)
        self.MinutesComboBox.setStyleSheet('background-color: rgb(63, 63, 63);')
        for i in range(0, 60):
            if i < 10:
                self.MinutesComboBox.addItem('0' + str(i))
            else:
                self.MinutesComboBox.addItem(str(i))

        self.HoursComboBox = QComboBox(self.ClockWidget)
        self.HoursComboBox.setMinimumWidth(100)
        self.HoursComboBox.setStyleSheet('background-color: rgb(63, 63, 63);')
        for i in range(0, 24):
            if i < 10:
                self.HoursComboBox.addItem('0' + str(i))
            else:
                self.HoursComboBox.addItem(str(i))

        self.ListDeleteAlarmClocks = QListWidget(self.ClockWidget)
        self.ListDeleteAlarmClocks.setMaximumWidth(20)
        self.ListDeleteAlarmClocks.itemClicked.connect(self.DeleteAlarmClock)
        self.ListDeleteAlarmClocks.setStyleSheet('border: 2px solid rgb(143, 143, 143);'
                                                 'background-color: rgb(63, 63, 63);')

        self.ListOfPastAlarmClocks = QListWidget(self.ClockWidget)
        self.ListOfPastAlarmClocks.itemActivated.connect(self.StartORStopAlarmClock)
        self.ListOfPastAlarmClocks.setStyleSheet('border: 2px solid rgb(143, 143, 143);'
                                                 'background-color: rgb(63, 63, 63);')

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
        self.LabelNumber = QLabel(self.StopWatchWidget)
        self.LabelNumber.setAlignment(QtCore.Qt.AlignCenter)
        self.LabelNumber.setGeometry(QtCore.QRect(222, 195, 299, 46))
        self.LabelNumber.setText('00:00:00:000')
        self.LabelNumber.setFont(QFont('Arial', 40))
        self.LabelNumber.setStyleSheet('color: rgb(143, 143, 143)')

        self.StartPushButton = QPushButton('СТАРТ', self.StopWatchWidget)
        self.StartPushButton.clicked.connect(self.StartStopWatchTimer)
        self.StartPushButton.setStyleSheet('background-color: rgb(133, 133, 133);')

        self.IntervalPushButton = QPushButton('ИНТЕРВАЛ', self.StopWatchWidget)
        self.IntervalPushButton.clicked.connect(self.AddInterval)
        self.IntervalPushButton.setStyleSheet('background-color: rgb(133, 133, 133);')
        self.IntervalPushButton.hide()

        self.ResetPushButton = QPushButton('СБРОС', self.StopWatchWidget)
        self.ResetPushButton.clicked.connect(self.reset)
        self.ResetPushButton.hide()
        self.ResetPushButton.setStyleSheet('background-color: rgb(133, 133, 133);')

        self.listView = QListWidget(self.StopWatchWidget)
        self.listView.setMinimumHeight(400)
        self.listView.setStyleSheet('border: 2px solid rgb(143, 143, 143);'
                                    'background-color: rgb(63, 63, 63);')

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.addWidget(self.LabelNumber)

        self.formLayout = QFormLayout(self.StopWatchWidget)
        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.verticalLayout)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.StartPushButton)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.ResetPushButton)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.IntervalPushButton)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.listView)

        # Добавление виджетов с устройствами в главное размещение
        self.MainLayout.addWidget(self.ClockWidget)
        self.MainLayout.addWidget(self.StopWatchWidget)

        # Прячем не нужные виджеты
        self.StopWatchWidget.hide()

        # Окно уведомления о сработанном будильнике
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

        # Загрузка информации о местоположении и названия выбранной музыки
        with open('MusicInfo/AddressMusic.txt', 'r') as Address:
            add = Address.readline()
            self.AddressMusicLine.setText(add)

            for i in os.listdir(add):
                if '.mp3' in i:
                    self.MusicListComboBox.addItem(i)

            self.AddressMusic = add

        with open('MusicInfo/SelectedMusic.txt', 'r') as Music:
            self.MusicListComboBox.currentIndex()
            self.FileName = self.AddressMusic + '/' + Music.read()

        self.showDateTime()
        self.LoadAlarmClocks()

    # Загрузка будильников из БД
    def LoadAlarmClocks(self):
        con = sqlite3.connect('AlarmClock.db')
        cur = con.cursor()
        result = cur.execute("""SELECT Time FROM Clocks""").fetchall()
        for elem in result:
            self.ListOfPastAlarmClocks.addItem(''.join(elem))
            self.ListDeleteAlarmClocks.addItem('X')
        con.close()

    # Вывод текущего времени на табло
    def showDateTime(self):
        timeNow = QTime.currentTime()
        text = timeNow.toString('hh:mm')
        if (timeNow.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]

        self.TimeNow.display(text)
        self.DateNow.setText(str(datetime.date.today()))

    # Включение и выключение будильника
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

    # Удаление будильника из списка
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

    # Срабатывание будильника
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

    # Кнопка ОК нажата
    def OkPressed(self):
        pygame.mixer.music.stop()
        self.wid.hide()

    # Обновить информацию о выбранной музыке
    def UpdateMusic(self):
        self.FileName = self.AddressMusicLine.text() + '/' + self.MusicListComboBox.currentText()
        with open('MusicInfo/SelectedMusic.txt', 'w') as Music:
            Music.write(self.MusicListComboBox.currentText())

    # Диалог выбора папки с музыкой и добавление mp3 из этой папки
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

            with open('MusicInfo/AddressMusic.txt', 'w') as file:
                file.write(fname)
        except:
            print('Музыка не была выбрана')

    # Добавление будильников из БД в виджет
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

    # Окрытие интерфейса с будильником
    def OpenAlarmClock(self):
        self.StopWatchWidget.hide()
        self.ClockWidget.show()

    # Открытие интерфейса с секундомером
    def OpenStopWatch(self):
        self.ClockWidget.hide()
        self.StopWatchWidget.show()

    # Перезапуск секундомера
    def reset(self):
        self.ms = 0
        self.sec = 0
        self.min = 0
        self.hour = 0
        self.LabelNumber.setText('00:00:00:00')
        self.ResetPushButton.hide()
        self.StartPushButton.setText('СТАРТ')
        self.listView.clear()

    # Обновление пройденого времени у секундомера
    def displayTime(self):
        self.LabelNumber.setText("%02d:%02d:%02d:%02d" % (self.hour, self.min, self.sec, self.ms))
        if self.ms != 99:
            self.ms += 1
        else:
            self.ms = 0
            if self.sec != 59:
                self.sec += 1
            else:
                self.sec = 0
                if self.min != 59:
                    self.min += 1
                else:
                    self.min = 0
                    if self.hour != 23:
                        self.hour += 1
                    else:
                        self.hour = 0

    # Вычисление интервала между промежутками времени
    def AddInterval(self):
        if self.ms < self.FirstMs:
            ms = 100 - abs(self.ms - self.FirstMs)
        else:
            ms = abs(self.FirstMs - self.ms)

        if self.sec < self.FirstSec:
            sec = 100 - abs(self.sec - self.FirstSec)
        else:
            sec = abs(self.FirstSec - self.sec)

        if self.min < self.FirstMin:
            min = 100 - abs(self.min - self.FirstMin)
        else:
            min = abs(self.FirstMin - self.min)

        if self.hour < self.FirstHour:
            hour = 100 - abs(self.hour - self.FirstHour)
        else:
            hour = abs(self.FirstHour - self.hour)

        if self.min > self.FirstMin:
            min -= 1
        elif self.sec > self.FirstSec:
            sec -= 1
        elif self.min > self.FirstMin:
            min -= 1
        elif self.hour > self.FirstHour:
            hour -= 1

        if self.listView.count() == 0:
            FirstItem = ("%02d:%02d:%02d:%02d" % (self.hour, self.min, self.sec, self.ms))
            self.listView.addItem('Время           Интервал')
            self.listView.addItem(FirstItem + '    ' + FirstItem)
        else:
            item = ("%02d:%02d:%02d:%02d" % (self.hour, self.min, self.sec, self.ms) +
                    '    ' + "%02d:%02d:%02d:%02d" % (hour, min,
                                                      sec, ms))
            self.listView.addItem(item)
        self.FirstHour = self.hour
        self.FirstMin = self.min
        self.FirstSec = self.sec
        self.FirstMs = self.ms

    # Управление секундомером
    def StartStopWatchTimer(self):
        if self.StartPushButton.text() == 'СТАРТ':
            self.timerStopWatch.start()
            self.IntervalPushButton.show()
            self.StartPushButton.setText('ОСТАНОВИТЬ')
        elif self.StartPushButton.text() == 'ОСТАНОВИТЬ':
            self.StartPushButton.setText('ВОЗОБНОВИТЬ')
            self.IntervalPushButton.hide()
            self.ResetPushButton.show()
            self.timerStopWatch.stop()
        elif self.StartPushButton.text() == 'ВОЗОБНОВИТЬ':
            self.timerStopWatch.start()
            self.StartPushButton.setText('ОСТАНОВИТЬ')
            self.IntervalPushButton.show()
            self.ResetPushButton.hide()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
