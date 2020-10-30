import sys
import datetime

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QMainWindow, QLCDNumber, QPushButton, QWidget, QLineEdit
from PyQt5.uic import loadUi

from YandexWatchProgect.AppInterface import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        timer = QTimer(self)
        timer.timeout.connect(self.showDateTime)
        timer.start(1000)

        self.AlarmClockBut.clicked.connect(self.OpenAlarmClock)
        self.StopWatchBut.clicked.connect(self.OpenStopWatch)

        self.showDateTime()

    def showDateTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]

        self.TimeNow.display(text)
        self.DateNow.setText(str(datetime.date.today()))

    def OpenAlarmClock(self):
        uic.loadUi('UI/Clock.ui', self.widget)

    def OpenStopWatch(self):
        uic.loadUi('UI/StopWatch.ui', self.widget)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
