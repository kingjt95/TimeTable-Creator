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
        self.showTable()
    def showTable(self):
        table = self.ShowDataTable
        df = pd.read_csv('Far02.csv')

        table.setRowCount(df.shape[0])
        table.setColumnCount(df.shape[1])
        table.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[i,j]))
                table.setItem(i, j, item)
        self.updateFields(df, i,j, new=True)
        table.itemChanged.connect(lambda : self.writeToCsv(df))
        self.StartButton.clicked.connect(lambda : self.pressedStart(df, i, j))

    def updateFields(self, df, i, j, new=False):
        # if df.Number[i] is type(int):
        NewNumber = df.Number[i] + new
        self.NumberLineEdit.setText(str(NewNumber))

        NewCategory = df.Category[i]
        NewDescription = df.Description[i]
        NewStartDate = df.StartDate[i]
        NewStartTime = df.StartTime[i]
        NewEndDate = str(df.EndDate[i])
        NewEndTime = str(df.EndTime[i])
        self.CategoryLineEdit.setPlaceholderText(NewCategory)
        self.DescriptionLineEdit.setPlaceholderText(NewDescription)
        if not new:
            self.DateLineEdit.setPlaceholderText(NewStartDate)
            self.TimeLineEdit.setPlaceholderText(NewStartTime)
        print(df.EndDate[i], type(df.EndDate[i]))
        if (NewEndDate == 'nan' or NewEndDate == '') and (NewEndTime == 'nan' or NewEndTime == ''):
            self.StartButton.setEnabled(False)
            # pass

    def writeToCsv(self,dfOriginal):
        table = self.ShowDataTable
        # Get the number of rows and columns in the table
        num_rows = table.rowCount()
        num_cols = table.columnCount()

        # Create an empty dataframe with the same number of columns as the table
        df = pd.DataFrame(columns=[table.horizontalHeaderItem(i).text() for i in range(num_cols)])
        for row in range(num_rows):
            data = []
            for col in range(num_cols):
                item = table.item(row, col)
                if item is not None:
                    data.append(item.text())
                else:
                    data.append('')
            df.loc[row] = data
        dfOriginal.to_csv('Far02.bck.csv',index=False)
        df.to_csv('Far02.csv',index=False)

    def pressedStart(self, df, i, j):
        table = self.ShowDataTable
        if self.CurrentRadioButton.isEnabled():
            currentDateTime = datetime.now()
            currentDate = str(currentDateTime).split(' ')[0]
            currentTime = str(currentDateTime).split(' ')[1].split('.')[0]
            self.DateLineEdit.setText(currentDate)
            self.TimeLineEdit.setText(currentTime)

        LastStartDate = str(df.StartDate[i])
        LastStartTime = str(df.StartTime[i])
        print(LastStartDate, (LastStartDate == 'nan' or LastStartDate == '') and\
            (LastStartTime == 'nan' or LastStartTime == ''))
        if (LastStartDate == 'nan' or LastStartDate == '') and\
            (LastStartTime == 'nan' or LastStartTime == ''):
            item = QTableWidgetItem(self.TimeLineEdit.text())
            table.setItem(i, df.columns.get_loc("StartTime"), item)
            item = QTableWidgetItem(self.DateLineEdit.text())
            table.setItem(i, df.columns.get_loc("StartDate"), item)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
