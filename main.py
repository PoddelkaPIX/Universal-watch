import sys
import datetime
from pygame import mixer

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTime, QTimer, QUrl
from PyQt5.QtWidgets import QMainWindow, QLCDNumber, QPushButton, QWidget, QLineEdit, QStackedWidget, QGridLayout, \
    QComboBox, QFileDialog, QMessageBox

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
        timer.start(1000)

        # Выравникание виджетов под размер окна
        self.MainLayout = QGridLayout(self.widget)
        self.ClockWidget = QWidget()
        self.StopWatchWidget = QWidget()

        # Интерфейс будильника
        self.AddAlarmButton = QtWidgets.QPushButton('ДОБАВИТЬ', self.ClockWidget)
        self.AddAlarmButton.clicked.connect(self.AddAlarmsComboBoxItem)

        self.DeleteAlarmButton = QtWidgets.QPushButton('УДАЛИТЬ', self.ClockWidget)
        self.DeleteAlarmButton.clicked.connect(self.AddAlarmsComboBoxItem)

        self.StartAlarmButton = QtWidgets.QPushButton('СТАРТ', self.ClockWidget)
        self.StartAlarmButton.clicked.connect(self.StartCountTime)

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

        self.AlarmsComboBox = QtWidgets.QComboBox(self.ClockWidget)
        self.AlarmsComboBox.addItem('<Не выбрано>')

        self.TimeLeft = QtWidgets.QLCDNumber(self.ClockWidget)
        self.TimeLeft.setMinimumWidth(400)

        self.MusicListView = QtWidgets.QListView(self.ClockWidget)

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.MinutesComboBox)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.HoursComboBox)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.addWidget(self.StartAlarmButton)
        self.horizontalLayout.addWidget(self.StopAlarmButton)
        self.horizontalLayout.addWidget(self.PauseButton)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.addWidget(self.TimeLeft)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.addWidget(self.AddMusicButton)
        self.horizontalLayout_2.addWidget(self.AddressMusicLine)

        SpacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout = QGridLayout(self.ClockWidget)
        self.gridLayout.addWidget(self.AddAlarmButton, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.DeleteAlarmButton, 5, 1, 1, 1)
        self.gridLayout.addWidget(self.MusicListView, 2, 1, 1, 1)
        self.gridLayout.addLayout(self.formLayout, 6, 1, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 2, 1, 1)
        self.gridLayout.addWidget(self.AlarmsComboBox, 3, 1, 1, 1)
        self.gridLayout.addLayout(self.verticalLayout, 2, 2, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 2)
        self.gridLayout.addItem(SpacerItem, 2, 1, 1, 1)

        # Интерфейс секундомера
        self.formLayout = QtWidgets.QFormLayout(self.StopWatchWidget)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lcdNumber = QtWidgets.QLCDNumber(self.StopWatchWidget)
        self.lcdNumber.setObjectName("lcdNumber")
        self.verticalLayout.addWidget(self.lcdNumber)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.verticalLayout)
        self.pushButton = QtWidgets.QPushButton(self.StopWatchWidget)
        self.pushButton.setObjectName("pushButton")
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

    def showDateTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]

        self.TimeNow.display(text)
        self.DateNow.setText(str(datetime.date.today()))

    def DialogAddMusic(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Выбрать папку', '')[0]
            self.AddressMusicLine.setText(fname)
            mixer.init()
            mixer.music.load(fname)
            mixer.music.play()
        except:
            pass

    def StartCountTime(self):
        if self.AlarmsComboBox.currentText() != '<Не выбрано>':
            self.StartAlarmButton.hide()
            self.StopAlarmButton.show()
            self.PauseButton.show()
            self.AlarmsComboBox.setEnabled(False)
            self.MinutesComboBox.setEnabled(False)
            self.HoursComboBox.setEnabled(False)
            self.AddAlarmButton.setEnabled(False)
            self.DeleteAlarmButton.setEnabled(False)
            self.MusicListView.setEnabled(False)
            self.AddMusicButton.setEnabled(False)
            self.AddressMusicLine.setEnabled(False)
        else:
            QMessageBox.critical(self, "Не выбрано время", "Укажите время срабатывания будильника", QMessageBox.Ok)

    def StopCountTime(self):
        self.StopAlarmButton.hide()
        self.PauseButton.hide()
        self.StartAlarmButton.show()
        self.AlarmsComboBox.setEnabled(True)
        self.MinutesComboBox.setEnabled(True)
        self.HoursComboBox.setEnabled(True)
        self.AddAlarmButton.setEnabled(True)
        self.DeleteAlarmButton.setEnabled(True)
        self.MusicListView.setEnabled(True)
        self.AddMusicButton.setEnabled(True)
        self.AddressMusicLine.setEnabled(True)

    def AddAlarmsComboBoxItem(self):
        item = self.HoursComboBox.currentText() + ':' + self.MinutesComboBox.currentText()
        print(item)
        self.AlarmsComboBox.addItem(item)
        self.AlarmsComboBox.setCurrentText(item)
        self.TimeLeft.display(item)

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
