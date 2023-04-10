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
        self.StartButton.clicked.connect(self.PressedStart)
    ### Loading
    def csv2table(self):
        self.csv2df()
        self.df2table()
    def csv2df(self):
        self.df = pd.read_csv('Far02.csv')
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
        self.dfBackup.to_csv('Far02.bck.csv',index=False)
        self.df.to_csv('Far02.csv',index=False)
        self.statusbar.showMessage('Saved to Far02.csv!',2000)

    ### Buttons Trigger
    def PressedStart(self):
        table = self.ShowDataTable
        table.insertRow(self.df.shape[0])








    #
    #     self.writeFromCsvToTable()
    #     self.updateFields(rowNumber=self.df.shape[0] - 1)
    #     table = self.ShowDataTable
    #     # table.itemChanged.connect(lambda : self.writeFromTableToCsv())
    #     table.itemSelectionChanged.connect(lambda: self.on_selection_changed( \
    #                                                   table.selectedIndexes() ) )
    #     # self.StartButton.clicked.connect(lambda : self.pressedStart(self.df.shape[0]))
    #     # self.StopButton.clicked.connect(lambda : self.pressedStop(self.df.shape[0]))
    #
    # def writeFromCsvToTable(self):
    #     print('writeFromCsvToTable is executed!')
    #     table = self.ShowDataTable
    #     self.df = pd.read_csv('Far02.csv')
    #     table.setRowCount(self.df.shape[0])
    #     table.setColumnCount(self.df.shape[1])
    #     table.setHorizontalHeaderLabels(self.df.columns)
    #
    #     for i in range(self.df.shape[0]):
    #         for j in range(self.df.shape[1]):
    #             item = QTableWidgetItem(str(self.df.iloc[i,j]))
    #             table.setItem(i, j, item)
    #
    # def updateFields(self, rowNumber):
    #     print('updateFields is executed!')
    #
    #     i = rowNumber
    #     # if self.df.Number[i] is type(int):
    #
    #     LastNumber = str(self.df.Number[i])
    #     self.NumberLineEdit.setText(LastNumber)
    #     LastCategory = str(self.df.Category[i])
    #     self.CategoryLineEdit.setText(LastCategory)
    #     LastDescription = str(self.df.Description[i])
    #     self.DescriptionLineEdit.setText(LastDescription)
    #
    #     LastStartDate = str(self.df.StartDate[i])
    #     LastStartTime = str(self.df.StartTime[i])
    #     LastEndDate = str(self.df.EndDate[i])
    #     LastEndTime = str(self.df.EndTime[i])
    #     self.DateLineEdit.setText(LastStartDate)
    #     self.TimeLineEdit.setText(LastStartTime)
    #     # print(self.df.EndDate[i], type(self.df.EndDate[i]))
    #     lastStopExists = not ( (LastEndDate == 'nan' or LastEndDate == '') and\
    #                            (LastEndTime == 'nan' or LastEndTime == '') )
    #     print ('lastStopExists:', lastStopExists)
    #     if lastStopExists:
    #         self.StartButton.setEnabled(True)
    #     else:
    #         self.StartButton.setEnabled(False)
    #
    # def writeFromTableToCsv(self):
    #     print('writeFromTableToCsv is executed!')
    #
    #     dfOriginal = self.df
    #     table = self.ShowDataTable
    #     # Get the number of rows and columns in the table
    #     num_rows = table.rowCount()
    #     num_cols = table.columnCount()
    #
    #     # Create an empty dataframe with the same number of columns as the table
    #     self.df = pd.DataFrame(columns=[table.horizontalHeaderItem(i).text() for i in range(num_cols)])
    #     for row in range(num_rows):
    #         data = []
    #         for col in range(num_cols):
    #             item = table.item(row, col)
    #             if item is not None:
    #                 data.append(item.text())
    #             else:
    #                 data.append('')
    #         self.df.loc[row] = data
    #     dfOriginal.to_csv('Far02.bck.csv',index=False)
    #     self.df.to_csv('Far02.csv',index=False)
    #     self.statusbar.showMessage('Saved to Far02.csv!',2000)
    #     self.updateFields(num_rows - 1)
    #
    # def pressedStart(self, rowNumber):
    #     print('pressedStart is executed!')
    #     table = self.ShowDataTable
    #
    #     if rowNumber is None: rowNumber = self.df.copy().shape[0]
    #     if rowNumber == self.df.shape[0]: # Adds New Row
    #         table.insertRow(rowNumber)
    #     # if self.CurrentRadioButton.isChecked():
    #     #     currentDateTime = datetime.now()
    #     #     currentDate = str(currentDateTime).split(' ')[0]
    #     #     currentTime = str(currentDateTime).split(' ')[1].split('.')[0]
    #     #     print(currentDate,currentTime)
    #     #     self.DateLineEdit.setText(currentDate)
    #     #     self.TimeLineEdit.setText(currentTime)
    #
    #     # item = QTableWidgetItem(self.NumberLineEdit.text())
    #     # table.setItem(rowNumber, self.df.columns.get_loc("Number"), item)
    #     #
    #     # item = QTableWidgetItem(self.CategoryLineEdit.text())
    #     # table.setItem(rowNumber, self.df.columns.get_loc("Category"), item)
    #     #
    #     # item = QTableWidgetItem(self.DescriptionLineEdit.text())
    #     # table.setItem(rowNumber, self.df.columns.get_loc("Description"), item)
    #
    #     item = QTableWidgetItem(self.TimeLineEdit.text())
    #     table.setItem(rowNumber, self.df.columns.get_loc("StartTime"), item)
    #
    #     item = QTableWidgetItem(self.DateLineEdit.text())
    #     table.setItem(rowNumber, self.df.columns.get_loc("StartDate"), item)
    #
    # def pressedStop(self, rowNumber):
    #     print('pressedStop is executed!')
    #     table = self.ShowDataTable
    #
    #     if rowNumber is None: rowNumber = self.df.copy().shape[0]
    #     if rowNumber == self.df.shape[0]: # Adds New Row
    #         table.insertRow(rowNumber)
    #     # if self.CurrentRadioButton.isChecked():
    #     #     currentDateTime = datetime.now()
    #     #     currentDate = str(currentDateTime).split(' ')[0]
    #     #     currentTime = str(currentDateTime).split(' ')[1].split('.')[0]
    #     #     self.DateLineEdit.setText(currentDate)
    #     #     self.TimeLineEdit.setText(currentTime)
    #
    #     # item = QTableWidgetItem(self.NumberLineEdit.text())
    #     # table.setItem(rowNumber, self.df.columns.get_loc("Number"), item)
    #     #
    #     # item = QTableWidgetItem(self.CategoryLineEdit.text())
    #     # table.setItem(rowNumber, self.df.columns.get_loc("Category"), item)
    #     #
    #     # item = QTableWidgetItem(self.DescriptionLineEdit.text())
    #     # table.setItem(rowNumber, self.df.columns.get_loc("Description"), item)
    #
    #     item = QTableWidgetItem(self.TimeLineEdit.text())
    #     table.setItem(rowNumber, self.df.columns.get_loc("EndTime"), item)
    #
    #     item = QTableWidgetItem(self.DateLineEdit.text())
    #     table.setItem(rowNumber, self.df.columns.get_loc("EndDate"), item)
    #
    # def on_selection_changed(self, selectedItems):
    #
    #     for cell in selectedItems:
    #          row = cell.row()
    #          col = cell.column()
    #          print(row,col)
    #          self.updateFields(rowNumber=row)
    #          self.StartButton.clicked.connect(lambda : self.pressedStart(row))
    #          self.StopButton.clicked.connect(lambda : self.pressedStop(row))

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
