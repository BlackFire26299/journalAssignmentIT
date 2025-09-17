from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QDate
from PyQt6 import uic
from PyQt6.QtGui import QKeyEvent, QStandardItemModel, QStandardItem, QTextCharFormat, QColor
import os
from datetime import datetime
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

        self.openFile = "Not Yet Saved"
        self.FileNameLabel.setText(self.openFile)
        self.files = []
        self.filecontents = {}
        self.wsPath = "TestWorkSpace"
        self.FileList.itemClicked.connect(self.clickedFileItem)
        self.Save.clicked.connect(self.save)
        self.SaveButton1.clicked.connect(self.save)
        self.SaveName = ""
        self.DeleteButton.clicked.connect(self.Delete)
        self.NewFile.clicked.connect(self.newFile)
        self.RefreshButton.clicked.connect(self.populateFileBrowser)
        self.OpenWorkspaceButton.clicked.connect(self.openWorkspace)

        self.populateFileBrowser()
        self.CalendarButton.clicked.connect(self.openCalendarPage)
        self.JournalButton.clicked.connect(self.openJournalPage)
        self.iscalendaropen = False
        self.currentJournalPage = 2 # 2 is the journal edit and 1 is the md view
        self.mainViewWidgets.setCurrentIndex(self.currentJournalPage)
        self.mdeditor.textChanged.connect(self.markdownUpdate)
        self.mdeditor.textChanged.connect(self.tempsave)
        self.SetDateButton.clicked.connect(self.setDate)
        
        self.date: QDate = self.calendar.selectedDate()
        #to get date in tuple form is self.date.getDate() returns in (yyyy, mm, dd)
        self.show()

    def clearEdit(self):
        self.mdeditor.setText("")

    def clickedFileItem(self, clickedItem):
        self.openFile = clickedItem.text()+".md"
        self.mdeditor.setText(self.filecontents[self.openFile])
        self.FileNameLabel.setText(self.openFile)
    
    def openWorkspace(self):
        directory_path = QFileDialog.getExistingDirectory(parent=self, caption="Select Directory", directory="")
        if directory_path:
            self.wsPath = directory_path
            self.populateFileBrowser()
            self.clearEdit()

    def newFile(self):
        self.clearEdit()
        self.openFile = "Not Yet Saved"
        self.FileNameLabel.setText(self.openFile)

    def setDate(self):
        self.date: QDate = self.calendar.selectedDate()
        (year,month,day) = self.date.getDate()
        datestr = f"{day}, {month}, {year}"
        
        
        

    def Delete(self):
            
            text, ok = QInputDialog.getText(self, "Input Dialog", "Do you want to delete "+"'"+self.openFile+"'"+"?(y/n)")
            if ok and text:
                if text == "y":
                    del self.filecontents[self.openFile]
                    os.remove(self.wsPath+"/"+self.openFile)
                    self.populateFileBrowser()
                    self.clearEdit()
                    self.openFile = "Not Yet Saved"
                    self.FileNameLabel.setText(self.openFile)


            elif ok and not text:
                print("User entered nothing.")
            else:
                print("User cancelled the input.")

    def save(self):
        if self.openFile != "Not Yet Saved":
            with open(self.wsPath+"/"+self.openFile, "w") as openFile:
                openFile.write(self.filecontents[self.openFile])
        else:
            text, ok = QInputDialog.getText(self, "Input Dialog", "Enter Note Name:")
            if ok and text:
                self.filecontents[text+".md"] = self.mdeditor.toPlainText()
                self.openFile = text+".md"
                
                self.save()
                self.populateFileBrowser()
                self.FileNameLabel.setText(self.openFile)

            elif ok and not text:
                print("User entered nothing.")
            else:
                print("User cancelled the input.")

        
    def tempsave(self):
        self.filecontents[self.openFile] = self.mdeditor.toPlainText()


    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key.Key_Escape:
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


    def populateFileBrowser(self, path= "PrePlanning"):
        self.FileList.clear()
        self.files = []
        filesAndFolders = os.listdir(self.wsPath)
        
        for item in filesAndFolders:
            if item[-3:] == ".md":
                self.files.append(item)
        
        for file in self.files:
            item = QListWidgetItem(file[:-3])
            self.FileList.addItem(item)
            with open(self.wsPath+"/"+file, "r") as openFile:
                self.filecontents[file] = openFile.read()
        

    def markdownUpdate(self):
        self.mdView.setMarkdown(self.mdeditor.toPlainText())

window = MainWindow("BergenTrücking")

sys.exit(app.exec())