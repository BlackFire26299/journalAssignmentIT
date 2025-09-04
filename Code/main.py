from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6 import uic
import time
import sys
from math import pi, sqrt


app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self, name):
        super().__init__()
        string = "ha"
        uic.loadUi("Code/UIs/Mainapp.ui", self)
        if type(name) == type(string):
            self.setWindowTitle(name)
        self.show()


window = MainWindow("BergenTrücking")

sys.exit(app.exec())