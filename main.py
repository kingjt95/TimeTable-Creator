import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem,\
                            QAction, qApp, QApplication, QFileDialog
import pandas as pd
import numpy as np
from datetime import datetime, date, time
import json
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("mainWindow.ui", self)
        self.setWindowTitle('TimeTable Creator')
        self.getConfig()
        self.csv2table()
        self.setupMenubar()
        self.CurrentRadioButton.setChecked(True)
        self.NumberLineEdit.setEnabled(False)
        self.TimeLineEdit.setEnabled(False)
        self.DateLineEdit.setEnabled(False)
        self.CurrentRadioButton.clicked.connect(self.UpdateSettings)
        self.CustomRadioButton.clicked.connect(self.UpdateSettings)
        self.StartButton.clicked.connect(self.PressedStart)
        self.StopButton.clicked.connect(self.PressedStop)
        table = self.ShowDataTable
        table.itemSelectionChanged.connect(
             lambda: self.on_selection_changed(table.selectedItems()))
        self.UpdateSettings2()

    ### Config File
    def getConfig(self):

        try:
            with open('config.json', 'r') as file:
                data = json.load(file)
            self.workingFile = data['workingFile']
            self.backupFile = data['backupFile']
        except Exception as e:
            print('Config file is not valid! A valid config file will\
                    be created! If you have previous data on this directory,\
                     make sure you have a backup! Please load your desired csv file:')
            self.workingFile = 'workingFile.csv'
            self.backupFile = 'backupFile.csv'
            try:
                self.df = pd.read_csv(self.workingFile)
                self.workingFile = 'workingFile(BackupAfterConfigMiss).csv'
                self.backupFile = 'backupFile(BackupAfterConfigMiss).csv'
                self.df2csv()
            except:pass
            self.workingFile = 'workingFile.csv'
            self.backupFile = 'backupFile.csv'
            self.saveConfig()
    def saveConfig(self):
        data = {}
        data['workingFile'] = self.workingFile
        data['backupFile'] = self.backupFile
        with open('config.json', 'w') as file:
            json.dump(data, file)
    ### Setup menu bar
    def setupMenubar(self):
        self.action_New.triggered.connect(self.NewCsvFile)
        self.action_Save.triggered.connect(self.table2csv)
        self.action_Load.triggered.connect(self.loadCsvFile)
        self.action_Exit.triggered.connect(qApp.quit)
    ### New file
    def NewCsvFile(self):
        pass
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # fileName, _ = QFileDialog.getSaveFileName(self,"Create CSV File","",\
        #             "CSV Files (*csv)", options=options)
        #
        # if fileName:
        #     self.df = pd.DataFrame(columns=['Number', 'Category', 'Descrition', 'StartDate', 'StartTime', 'EndDate', 'EndTime'])
        #     self.workingFile = fileName
        #     self.saveConfig()
        #     self.df2csv()
        #     self.csv2table()
        #     self.UpdateSettings2()
    ### Loading
    def loadCsvFile(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(\
             self,"QFileDialog.getOpenFileName()", \
              "","CSV Files (*csv)", options=options)
        if fileName:
            self.workingFile = fileName
            self.saveConfig()
            self.csv2table()
            self.UpdateSettings2()



    def csv2table(self):
        self.csv2df()
        self.df2table()
        try:
            filename = self.workingFile.split('/')[-1]
        except:
            filename = self.workingFile
        self.setWindowTitle('TimeTable Creator: '+ filename)
        self.statusbar.showMessage('Loaded data from '+ filename  + '!', 2000)


    def csv2df(self):
        # print(self.workingFile)
        try:
            self.df = pd.read_csv(self.workingFile)
        except Exception as e:
            print('Cant load csv file due to following error:\n', e,\
                'please load another file')
            self.loadCsvFile()
    def df2table(self):
        table = self.ShowDataTable
        table.setRowCount(self.df.shape[0])
        table.setColumnCount(self.df.shape[1])
        table.setHorizontalHeaderLabels(self.df.columns)

        for i in range(self.df.shape[0]):
            for j in range(self.df.shape[1]):
                item = QTableWidgetItem(str(self.df.iloc[i,j]))
                table.setItem(i, j, item)
        self.resizeTableToContents()
        table.scrollToBottom()

    ### Saving
    def table2csv(self):
        self.table2df()
        self.df2csv()
    def table2df(self):
        self.dfBackup = self.df.copy()
        table = self.ShowDataTable
        # Get the number of rows and columns in the table
        num_rows = table.rowCount()
        num_cols = table.columnCount()

        # Create an empty dataframe with the same number of columns as the table
        self.df = pd.DataFrame(columns=[table.horizontalHeaderItem(i).text() for i in range(num_cols)])
        for row in range(num_rows):
            data = []
            for col in range(num_cols):
                item = table.item(row, col)
                if item is not None:
                    data.append(item.text())
                else:
                    data.append('')
            self.df.loc[row] = data
    def df2csv(self):
        try:
            self.dfBackup.to_csv(self.backupFile,index=False)
            self.df.to_csv(self.workingFile,index=False)

            try:
                filename = self.workingFile.split('/')[-1]
            except:
                filename = self.workingFile
            self.statusbar.showMessage('Saved on '+ filename  + '!', 2000)
        except:
            self.statusbar.showMessage('Warning! Unable to Save!', 2000)

    ### Buttons Trigger
    def PressedStart(self):
        table = self.ShowDataTable
        rowNumber = self.df.shape[0]
        table.insertRow(rowNumber)
        # Number
        try:
            item = table.item(rowNumber-1, self.df.columns.get_loc("Number"))\
                                                          .text()
            number = int(item) + 1
        except:
            number = 1

        item = QTableWidgetItem(str(number))
        table.setItem(rowNumber, self.df.columns.get_loc("Number"), item)
        self.NumberLineEdit.setText(str(number))
        # Category
        item = QTableWidgetItem(self.CategoryLineEdit.text())
        table.setItem(rowNumber, self.df.columns.get_loc("Category"), item)
        # Description
        item = QTableWidgetItem(self.DescriptionLineEdit.text())
        table.setItem(rowNumber, self.df.columns.get_loc("Description"), item)

        if self.CurrentRadioButton.isChecked():
            currentDateTime = datetime.now()
            currentDate = str(currentDateTime).split(' ')[0]
            currentTime = str(currentDateTime).split(' ')[1].split('.')[0]

            item = QTableWidgetItem(currentTime)
            table.setItem(rowNumber, self.df.columns.get_loc("StartTime"), item)

            item = QTableWidgetItem(currentDate)
            table.setItem(rowNumber, self.df.columns.get_loc("StartDate"), item)
        else:
            item = QTableWidgetItem(self.TimeLineEdit.text())
            table.setItem(rowNumber, self.df.columns.get_loc("StartTime"), item)

            item = QTableWidgetItem(self.DateLineEdit.text())
            table.setItem(rowNumber, self.df.columns.get_loc("StartDate"), item)

        self.table2df()
        self.df2csv()
        self.resizeTableToContents()
        table.scrollToBottom()
    def PressedStop(self):
        table = self.ShowDataTable
        rowNumber = self.df.shape[0] - 1
        if self.CurrentRadioButton.isChecked():
            currentDateTime = datetime.now()
            currentDate = str(currentDateTime).split(' ')[0]
            currentTime = str(currentDateTime).split(' ')[1].split('.')[0]

            item = QTableWidgetItem(currentTime)
            table.setItem(rowNumber, self.df.columns.get_loc("EndTime"), item)

            item = QTableWidgetItem(currentDate)
            table.setItem(rowNumber, self.df.columns.get_loc("EndDate"), item)
        else:
            item = QTableWidgetItem(self.TimeLineEdit.text())
            table.setItem(rowNumber, self.df.columns.get_loc("EndTime"), item)

            item = QTableWidgetItem(self.DateLineEdit.text())
            table.setItem(rowNumber, self.df.columns.get_loc("EndDate"), item)

        self.table2df()
        self.df2csv()
        self.resizeTableToContents()
        table.scrollToBottom()
    ### Update UpdateSettings
    def UpdateSettings(self):
        if self.CurrentRadioButton.isChecked():
            self.TimeLineEdit.setEnabled(False)
            self.DateLineEdit.setEnabled(False)
        else:
            self.TimeLineEdit.setEnabled(True)
            self.DateLineEdit.setEnabled(True)
    def UpdateSettings2(self):
        try:
            table = self.ShowDataTable
            row = self.df.shape[0] - 1

            Number = self.df.iloc[row,self.df.columns.get_loc("Number")]
            Category = self.df.iloc[row,self.df.columns.get_loc("Category")]
            Description = self.df.iloc[row,self.df.columns.get_loc("Description")]

            self.NumberLineEdit.setText(str(Number))
            self.CategoryLineEdit.setText(str(Category))
            self.DescriptionLineEdit.setText(str(Description))
        except:
            self.NumberLineEdit.setText('0')
    ### Selecting data in table
    def on_selection_changed(self, selectedItems):
        self.table2csv()
        self.resizeTableToContents()
    ### Resize Table Columns and rows
    def resizeTableToContents(self):
        table = self.ShowDataTable
        for i in range(self.df.shape[0]):
            table.resizeRowToContents(i)
        for j in range(self.df.shape[1]):
            table.resizeColumnToContents(j)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
