#import the necessary imports
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QDate
from PyQt6 import uic
from PyQt6.QtGui import QKeyEvent
import os
from datetime import datetime
import sys
import win32file
import pywintypes
import subprocess

#create the pyqt6 application that the ui is put in
app = QApplication(sys.argv)

#define the Settings Menu class
class SettingsMenu(QMainWindow):
    ##initiate class with the name argument
    def __init__(self, name):
        super().__init__()
        #string for type check
        string = "ha"
        #load the window ui from the .ui file
        uic.loadUi("Code/UIs/Settings.ui", self)
        #type check the name with a string
        if type(name) == type(string):
            #set the title of the window if the name is a valid string
            self.setWindowTitle(name)
        #show the window
        self.show()
    #make sure that when the settings window closes it is freed from memory
    def close(self):
        del(self)
        return super().close()


#define the mainWindow class
class MainWindow(QMainWindow): 
    ##initiate class with the name argument
    def __init__(self, name):
        super().__init__()
        #string for type check
        string = "ha"
        #load the window ui from the .ui file
        uic.loadUi("Code/UIs/Mainapp.ui", self)
        #type check the name with a string
        if type(name) == type(string):
            #set the title of the window if the name is a valid string
            self.setWindowTitle(name)

        
        
        # define default values of class variables
        self.openFile = "Not Yet Saved"
        self.files = []
        self.filecontents = {}
        self.wsPath = "TestWorkSpace"
        self.iscalendaropen = False
        self.SaveName = ""
        self.date: QDate = self.calendar.selectedDate() #to get date in tuple form is self.date.getDate() returns in (yyyy, mm, dd)
        self.currentJournalPage = 2 # 2 is the journal edit and 1 is the md view
        #set the filename label text to the openfile name
        self.FileNameLabel.setText(self.openFile)
        #set the current mainview widget to the journal edit widget
        self.mainViewWidgets.setCurrentIndex(self.currentJournalPage)
        #populate the filebrowser with the .md files in the current directory.
        self.populateFileBrowser()

        #link all the neccessary buttons to their respective functions.
        self.FileList.itemClicked.connect(self.clickedFileItem)
        self.Save.clicked.connect(self.save)
        self.SaveButton1.clicked.connect(self.save)
        self.DeleteButton.clicked.connect(self.Delete)
        self.NewFile.clicked.connect(self.newFile)
        self.RefreshButton.clicked.connect(self.populateFileBrowser)
        self.OpenWorkspaceButton.clicked.connect(self.openWorkspace)
        self.CalendarButton.clicked.connect(self.openCalendarPage)
        self.JournalButton.clicked.connect(self.openJournalPage)
        self.mdeditor.textChanged.connect(self.markdownUpdate)
        self.mdeditor.textChanged.connect(self.tempsave)
        self.SetDateButton.clicked.connect(self.setDate)
        self.SendCommandButton.clicked.connect(self.SendCommand)
        self.Settingsbutton.clicked.connect(self.openSettings)

        #show the window
        self.show()

    #funtion to clear the markdown editor so the user can have a new entry
    def clearEdit(self):
        #set the text to an empty string
        self.mdeditor.setText("")

    #Function to send commands to the command line and return the output
    def SendCommand(self):
        #get the command from the line edit widget
        command = self.CommandLineEdit.text()
        #dont run if there is no command
        if command != "":
            try: 
                #try to run the command with subprocess, check checks for errors, capture output gives back the output, 
                #and shell makes it so it interprets strings as commands instead of an array of strings
                result = subprocess.run(command, check=True, capture_output=True, text=True, shell=True)
            #excepts if subprocess returns an error and stores the error as e
            except subprocess.CalledProcessError as e:
                #create a error message box and define its properties with the error text in it.
                msg = QMessageBox(self)
                msg.setWindowTitle("Error: Bad Command")
                msg.setText(f"The command you entered was: '{self.CommandLineEdit.text()}', \n the error was {e.stderr}")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                msg.setDefaultButton(QMessageBox.StandardButton.Ok)
                #excecute the message so it shows
                msg.exec()
                #return so the success messagebox doesnt show.
                return
            #if there is no error create a sucess error box and put the output in it.
            msg = QMessageBox(self)
            msg.setWindowTitle("Successfully executed")
            msg.setText(f"Output is {result.stdout}")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.setDefaultButton(QMessageBox.StandardButton.Ok)
            #excecute the message so it shows
            msg.exec()
            #set the line edit text to an empty string
            self.CommandLineEdit.setText("")

    #function to open the file that was clicked on in the file browser and get the file name from the clicked item
    def clickedFileItem(self, clickedItem):
        #get the name of the clicked and split it at the spaces
        filenamearr: list = clickedItem.text().split(" ")
        #define bool
        print(filenamearr)
        hasSpaceAtEnd = False
        #if the string has a space at the end set the above bool to true
        if clickedItem.text()[-1] == " ":
            hasSpaceAtEnd = True
        #remove the date from the string
        filenamearr.pop(-1)
        #define string
        filenamestr = ""
        #make the file name a complete string with spaces included
        for partOfName in filenamearr:
            filenamestr += partOfName
            filenamestr += " "
        #if the string doesnt have a space at the end remove it.
        if not hasSpaceAtEnd: 
            filenamestr = filenamestr[:-1]
        #assign the value to the open file
        self.openFile = filenamestr+".md"
        #set the current editor to show the text in the open file
        self.mdeditor.setText(self.filecontents[self.openFile])
        #change the filename label to be correct
        self.FileNameLabel.setText(self.openFile)
        
    #function to bring up the settings menu    
    def openSettings(self):
        #create the settigns menu
        self.settingsmenu = SettingsMenu("Menu")

    def openWorkspace(self):
        #open a file dialog
        directory_path = QFileDialog.getExistingDirectory(parent=self, caption="Select Directory", directory="")
        #if the path is valid
        if directory_path:
            #open that folder as a new workspace and show the .md files in that folder
            self.wsPath = directory_path
            self.populateFileBrowser()
            self.clearEdit()

    #create a new file
    def newFile(self):
        #clear the mdeditor
        self.clearEdit()
        #change the openfile
        self.openFile = "Not Yet Saved"
        #set the correct file label
        self.FileNameLabel.setText(self.openFile)

    #Function to change the date of the current diary entry.
    def setDate(self):
        #get selected date on the calendar and make it a tuple
        self.date: QDate = self.calendar.selectedDate()
        (year,month,day) = self.date.getDate()
        
        #change to timestamp type
        attributedate = datetime(year, month, day, 12,0,0,0).timestamp()
        
        #create file handle 
        handle = win32file.CreateFile(self.wsPath+"/"+self.openFile, win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, 0)
        #define new creation time
        filetime_creation = pywintypes.Time(attributedate)
        #set the creation time
        win32file.SetFileTime(handle, filetime_creation, None, None)
        #close the handle
        win32file.CloseHandle(handle)
        #refresh file browser
        self.populateFileBrowser()
        
    #function to delete a file
    def Delete(self):
            #open input dialog and check for the answer
            text, ok = QInputDialog.getText(self, "Input Dialog", "Do you want to delete "+"'"+self.openFile+"'"+"?(y/n)")
            if ok and text:
                if text == "y":
                    #if yes delete the entry from the file dictionary, delete it in the os, refresh the file browser, clear the mdeditor, and open a new file
                    del self.filecontents[self.openFile]
                    os.remove(self.wsPath+"/"+self.openFile)
                    self.populateFileBrowser()
                    self.clearEdit()
                    self.newFile()
            #handle other conditions of user not answering and user cancelled input
            elif ok and not text:
                print("User entered nothing.")
            else:
                print("User cancelled the input.")

    #Function to save a file
    def save(self):
        #if the file has an associated file just write over the file contents
        if self.openFile != "Not Yet Saved":
            with open(self.wsPath+"/"+self.openFile, "w") as openFile:
                openFile.write(self.filecontents[self.openFile])
        #else
        else:
            #open an input dialog and ask the user for a name
            text, ok = QInputDialog.getText(self, "Input Dialog", "Enter Note Name:")
            if ok and text:
                #add a new entry to the file dictionary
                self.filecontents[text+".md"] = self.mdeditor.toPlainText()
                #set the openfile
                self.openFile = text+".md"
                #save now goes tot he first option in the if statement and creates the new file
                self.save()
                #refresh file browser
                self.populateFileBrowser()
                #set label to correct file name
                self.FileNameLabel.setText(self.openFile)
            #if user enters no name or cancels the input dont save
            elif ok and not text:
                print("User entered nothing.")
            else:
                print("User cancelled the input.")

    #function to load nonsaved changes into cache(file dictionary)
    def tempsave(self):
        #make the dictionary entry to the current text the file has
        self.filecontents[self.openFile] = self.mdeditor.toPlainText()

    #Function to hanle keypresses
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        #if the key is escape then switch from mdeditor to mdviewer and back
        if key == Qt.Key.Key_Escape:
            self.changeJournalPage()

    #function to change journal pages (editor to viewer and vise versa)
    def changeJournalPage(self):
        #if the user is not on the editor page set to the editor page
        if self.mainViewWidgets.currentIndex() !=2:
            self.mainViewWidgets.setCurrentIndex(2)
        #else set to the mdviewer page
        else: 
            self.mainViewWidgets.setCurrentIndex(1)
    #Function to switch to journal pages from calendar
    def openJournalPage(self):
        #set calendar open to false
        self.iscalendaropen = False
        #open the journal edit view
        self.mainViewWidgets.setCurrentIndex(2)
        
    #funtion to switch to calendar from jorunal pages
    def openCalendarPage(self):
        #set calendar open to true
        self.iscalendaropen = True
        #open the calendar page
        self.mainViewWidgets.setCurrentIndex(0)

    #function to populate/refresh the file browser
    def populateFileBrowser(self):
        #clear the file list widget and reset the files list
        self.FileList.clear()
        self.files = []
        #get all files and folders in current dir
        filesAndFolders = os.listdir(self.wsPath)
        
        #check if the item is a markdown file and if it is add it to the files list
        for item in filesAndFolders:
            if item[-3:] == ".md":
                self.files.append(item)
        
        #iterate through files
        for file in self.files:
            #get the creation time of the file
            itemcreationtime = os.path.getctime(self.wsPath+"/"+ file)
            itemcreationdate = datetime.fromtimestamp(itemcreationtime)

            #create a list item from the name of the file and the date it was created
            item = QListWidgetItem(file[:-3] + f" {itemcreationdate.day}-{itemcreationdate.month}-{itemcreationdate.year}")
            #add the item to the listwidget
            self.FileList.addItem(item)
            #read the contents of the file and add it to a file dictionary with its name as the key and its contents as the content.
            with open(self.wsPath+"/"+file, "r") as openFile:
                self.filecontents[file] = openFile.read()
        
    #update the markdown viewer to editor text
    def markdownUpdate(self):
        #set the text of the mdview to that of the mdeditor but in a markdown interpreter
        self.mdView.setMarkdown(self.mdeditor.toPlainText())

#instantiate the main window
window = MainWindow("BergenTrücking")

#run the app and exit when the X button is clicked
sys.exit(app.exec())