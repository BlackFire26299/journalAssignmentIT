from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6 import uic
from PyQt6.QtGui import QKeyEvent
import time
import sys
from math import pi, sqrt
import keyboard


app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self, name):
        super().__init__()
        string = "ha"
        uic.loadUi("Code/UIs/Mainapp.ui", self)
        if type(name) == type(string):
            self.setWindowTitle(name)

        self.CalendarButton.clicked.connect(self.openCalendarPage)
        self.JournalButton.clicked.connect(self.openJournalPage)
        self.iscalendaropen = False
        self.currentJournalPage = 2 # 2 is the journal edit and 1 is the md view
        self.mainViewWidgets.setCurrentIndex(self.currentJournalPage)
        
        self.mdeditor.textChanged.connect(self.markdownUpdate)


        self.show()


    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key.Key_Control:
            self.changeJournalPage()

    
    def changeJournalPage(self):
        if self.mainViewWidgets.currentIndex() !=2:
            self.mainViewWidgets.setCurrentIndex(2)
        else: 
            self.mainViewWidgets.setCurrentIndex(1)

    def openJournalPage(self):
        self.iscalendaropen = False
        self.mainViewWidgets.setCurrentIndex(2)
        

    def openCalendarPage(self):
        self.iscalendaropen = True
        self.mainViewWidgets.setCurrentIndex(0)

    def markdownUpdate(self):
        self.mdView.setMarkdown(self.mdeditor.toPlainText())

window = MainWindow("BergenTrücking")

sys.exit(app.exec())