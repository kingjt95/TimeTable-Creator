import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
import pandas as pd
import numpy as np
from datetime import datetime, date, time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("mainWindow.ui", self)
        self.csv2table()
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

    ### Loading
    def csv2table(self):
        self.csv2df()
        self.df2table()
    def csv2df(self):
        # print(self.workingFile)
        self.workingFile = 'workingFile.csv'
        self.df = pd.read_csv(self.workingFile)
    def df2table(self):
        table = self.ShowDataTable
        table.setRowCount(self.df.shape[0])
        table.setColumnCount(self.df.shape[1])
        table.setHorizontalHeaderLabels(self.df.columns)

        for i in range(self.df.shape[0]):
            for j in range(self.df.shape[1]):
                item = QTableWidgetItem(str(self.df.iloc[i,j]))
                table.setItem(i, j, item)

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
        self.backupFile = 'backupFile.csv'
        self.dfBackup.to_csv(self.backupFile,index=False)
        self.df.to_csv(self.workingFile,index=False)
        self.statusbar.showMessage('Saved to ' + self.workingFile + '!', 2000)

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
        table.scrollToBottom()

    ### Update UpdateSettings
    def UpdateSettings(self):
        if self.CurrentRadioButton.isChecked():
            self.TimeLineEdit.setEnabled(False)
            self.DateLineEdit.setEnabled(False)
        else:
            self.TimeLineEdit.setEnabled(True)
            self.DateLineEdit.setEnabled(True)
    def UpdateSettings2(self): # :)
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

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
