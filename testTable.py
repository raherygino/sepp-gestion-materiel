#----------------------------------------------------------------------------------------------
#                                  Table Of Contents/Overview
#----------------------------------------------------------------------------------------------
# Imports
 
# GUI
# - Button Actions
# - Table Display
# -- Button Functions
# --- Retranslate UI
# Run Program
#----------------------------------------------------------------------------------------------
 
#-------------------------------------------------------------------------------------
#                                  Imports
#-------------------------------------------------------------------------------------
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMainWindow, 
                                QLabel, QLineEdit, QTableWidget, QTableWidgetItem, 
                                QGridLayout, QVBoxLayout, QSizePolicy, QSpacerItem, 
                                QMessageBox,QSpinBox, QComboBox, QTableView,QStyledItemDelegate)
from PyQt5.QtCore import Qt, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont
 
 
import sqlite3
 
#-------------------------------------------------------------------------------------
#                                  GUI
#-------------------------------------------------------------------------------------
class Ui_SettingsMenu(QMainWindow):
    def __init__(self, parent = None):
        super(Ui_SettingsMenu, self).__init__(parent)
        self.setObjectName("SettingsMenu")
        self.resize(1123, 903)
        self.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"background-color: rgb(50, 50, 50);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.AddItemButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Android Insomnia")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.AddItemButton.setFont(font)
        self.AddItemButton.setStyleSheet("background-color: rgb(85, 255, 0);\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 15px;\n"
"border-color: black;\n"
"padding: 4px;\n"
"\n"
"")
        self.AddItemButton.setObjectName("AddItemButton")
        self.verticalLayout.addWidget(self.AddItemButton)
        self.DeleteItemButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Android Insomnia")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.DeleteItemButton.setFont(font)
        self.DeleteItemButton.setStyleSheet("background-color: rgb(255, 65, 68);\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 15px;\n"
"border-color: black;\n"
"padding: 4px;\n"
"")
        self.DeleteItemButton.setObjectName("DeleteItemButton")
        self.verticalLayout.addWidget(self.DeleteItemButton)
        self.MoreInfoButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Android Insomnia")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.MoreInfoButton.setFont(font)
        self.MoreInfoButton.setStyleSheet("background-color: rgb(196, 17, 255);\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 15px;\n"
"border-color: black;\n"
"padding: 4px;")
        self.MoreInfoButton.setObjectName("MoreInfoButton")
        self.verticalLayout.addWidget(self.MoreInfoButton)
        self.RefreshButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Android Insomnia")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.RefreshButton.setFont(font)
        self.RefreshButton.setStyleSheet("background-color: rgb(0, 255, 255);\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 15px;\n"
"border-color: black;\n"
"padding: 4px;\n"
"\n"
"")
        self.RefreshButton.setObjectName("RefreshButton")
        self.verticalLayout.addWidget(self.RefreshButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.BackButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Android Insomnia")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.BackButton.setFont(font)
        self.BackButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 15px;\n"
"border-color: black;\n"
"padding: 4px;\n"
"")
        self.BackButton.setObjectName("BackButton")
        self.verticalLayout.addWidget(self.BackButton)
        self.gridLayout.addLayout(self.verticalLayout, 4, 3, 1, 1)
        self.Header = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Android Insomnia")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Header.setFont(font)
        self.Header.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 15px;\n"
"border-color: black;\n"
"padding: 4px;")
        self.Header.setAlignment(QtCore.Qt.AlignCenter)
        self.Header.setObjectName("Header")
        self.gridLayout.addWidget(self.Header, 0, 1, 1, 3)
        self.SearchFilter = QComboBox(self.centralwidget)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.SearchFilter.setFont(font)
        self.SearchFilter.setStyleSheet("background-color: rgb(211, 211, 211);")
        self.SearchFilter.setObjectName("SearchFilter")
        self.gridLayout.addWidget(self.SearchFilter, 2, 1, 1, 1)
        self.SearchBar = QLineEdit(self.centralwidget)
        self.SearchBar.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.SearchBar.setObjectName("SearchBar")
        self.gridLayout.addWidget(self.SearchBar, 2, 2, 1, 1)
        self.TableDisplay = QtWidgets.QTableWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Android Insomnia")
        font.setBold(False)
        font.setWeight(50)
        self.TableDisplay.setFont(font)
        self.TableDisplay.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.TableDisplay.setObjectName("TableDisplay")
        self.TableDisplay.setColumnCount(0)
        self.TableDisplay.setRowCount(0)
        self.gridLayout.addWidget(self.TableDisplay, 4, 1, 1, 2)
        self.TableComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.TableComboBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.TableComboBox.setObjectName("TableComboBox")
        self.gridLayout.addWidget(self.TableComboBox, 2, 3, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
 
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
 
 
#----------------------------------------------------------------------------------------------------
#                                      Button Actions
#----------------------------------------------------------------------------------------------------
        #------------------------------------------
        #               Back Button
        #------------------------------------------
        #When the Back button is clicked -> BackClicked Function
        BackButton = self.BackButton
        BackButton.clicked.connect(self.BackClicked)
        #------------------------------------------
        #------------------------------------------
                        #Add Item Button
        #------------------------------------------
        #When the AddItem button is clicked -> AddItem Function
        AddItemButton = self.AddItemButton
        AddItemButton.clicked.connect(self.AddItemClicked)
        #------------------------------------------
        #------------------------------------------
                     #Remove Item Button
        #------------------------------------------
        #When the RemoveItem button is clicked -> RemoveItem Function
        RemoveItemButton = self.DeleteItemButton
        RemoveItemButton.clicked.connect(self.RemoveItemClicked)
        #------------------------------------------
        #------------------------------------------
                     #Refresh Button
        #------------------------------------------
        #When the More Info button is clicked -> MoreInfo Function
        RefreshButton = self.RefreshButton
        RefreshButton.clicked.connect(self.RefreshClicked)
        #------------------------------------------
 
#----------------------------------------------------------------------------------------------------
#                                       Table Display
#----------------------------------------------------------------------------------------------------
        #Connect to Database
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('Database.db') #Connect to the Database ('Database.db')
        self.model = QSqlTableModel()
        self.delrow = -1
 
        self.sbar = self.statusBar()
 
        self.TableDisplay = QTableView()
        self.TableDisplay.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.TableDisplay.setModel(self.model)
        self.TableDisplay.clicked.connect(self.findrow)
        self.TableDisplay.selectionModel().selectionChanged.connect(self.getCellText)
 
        self.gridLayout.addWidget(self.TableDisplay, 4, 1, 1, 2)
        self.setCentralWidget(self.centralwidget)
 
        #Only Selects Rows (Can still edit cells by double-clicking)
        self.TableDisplay.setSelectionBehavior(1)
        # 0 Selecting single items.
        # 1 Selecting only rows.
        # 2 Selecting only columns.
 
        #Sort Columns From A->Z When Their Headers are Clicked
        self.TableDisplay.horizontalHeader().sectionClicked.connect(self.header_clicked)
 
        #------------------------------------------
        #               Display Tables
        #------------------------------------------
        #Display the Appropriate Table based on the User's Selection from the TableComboBox
 
        #Add The Table Names to TableComboBox
        self.TableComboBox.addItems(TableNames)
 
        #When the User Selects a Table -> initializeModel Which Displays the Selected Table
        CurrentSelection = self.TableComboBox
        CurrentSelection.currentTextChanged.connect(self.initializeModel)
 
    def initializeModel(self):
        SelectedTable = self.TableComboBox.currentText() #Get currentText from TableComboBox
        self.model.setTable(SelectedTable)#Display the Table Based on the Table Name the User Selected
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
 
        #------------------------------------------
        #               Search/Filter
        #------------------------------------------
        #Allows the user to search for items
        self.SearchFilter.clear()
        for i in range(self.model.columnCount()):
                self.SearchFilter.addItem(self.model.headerData(i, QtCore.Qt.Horizontal))
        self.SearchFilter.setCurrentIndex(1)
         
        self.SearchBar.textChanged.connect(self.filter_table)
  
    def filter_table(self, text):
        userQuery = " {} LIKE '%{}%'".format(self.SearchFilter.currentText(), text.lower()) if text else text
        self.model.setFilter(userQuery)
        self.model.select()
    #------------------------------------------
 
    #------------------------------------------
    #      Sort Columns by A->Z
    #------------------------------------------
    def header_clicked(self, index):
        self.TableDisplay.sortByColumn(index, Qt.AscendingOrder)
    #------------------------------------------
         
#----------------------------------
#       Update Inventory
#---------------------------------- 
    def findrow(self, i):
        self.delrow = i.row()
 
    def getCellText(self):
        if self.TableDisplay.selectedIndexes():
            model = self.TableDisplay.model()
            row = self.selectedRow()
            column = 0 #Get item name (column 0)
            name = model.data(model.index(row, column))
            #Shows the item name on the bottom left corner of the screen
            self.sbar.showMessage(str(name))
  
    def selectedRow(self):
        if self.TableDisplay.selectionModel().hasSelection():
            row =  self.TableDisplay.selectionModel().selectedIndexes()[0].row()
            return int(row)
  
    def selectedColumn(self):
        column =  self.TableDisplay.selectionModel().selectedIndexes()[0].column()
        return int(column)
#----------------------------------
 
#----------------------------------------------------------------------------------------------------
#                                      Button Functions
#----------------------------------------------------------------------------------------------------
#----------------------------------
#       Back Mode Function
#----------------------------------
    def BackClicked(self):
        #Print in terminal for testing:
        #print("Back Button Engaged")
        #Return back to the Main Menu
        from BX_GUI_MainMenu import Ui_MainMenu
        self.win = Ui_MainMenu()
        self.win.show() #Show the Main Menu
        self.close() #Quit this GUI
#----------------------------------
#----------------------------------
#      Add Item Function
#----------------------------------
    def AddItemClicked(self):
        #Print in terminal for testing:
        print("The Add Item Button was clicked")
 
        tableWidget = QTableWidget()
        currentRowCount = tableWidget.rowCount()
        tableWidget.setItem(currentRowCount, 0, QTableWidgetItem("Some text"))
#----------------------------------
#----------------------------------
#      Remove Item Function
#----------------------------------
    def RemoveItemClicked(self):
        #Print in terminal for testing:
        print("The Delete Item Button was clicked")
 
        if self.TableDisplay.selectedIndexes():
            self.DeleteConfirmation()
        else:
            msgBox = QMessageBox.warning(None, "Error", 
                                     "No row is selected!\nPlease select a row", 
                                     QMessageBox.Close)
    #----------------------------------
    #   Delete Item Confirmation
    #----------------------------------
    def DeleteConfirmation(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Are you sure you want to delete this item?")
        msgBox.setInformativeText("*This cannot be undone")
        msgBox.setWindowTitle("Delete Item Confirmation")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
   
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes:
                row = self.TableDisplay.currentIndex().row()
                self.model.removeRow(row)
                self.initializeModel()
                self.TableDisplay.selectRow(row) 
#----------------------------------
#----------------------------------
#       Refresh Function
#----------------------------------
    def RefreshClicked(self):
        #Print in terminal for testing:
        print("The Refresh Button was clicked")
        #Close and reopen the app (Refresh)
        self.win = Ui_SettingsMenu()
        self.win.show()
        self.close()
#----------------------------------
 
#----------------------------------------------------------------------------------------------------
#                                      Retranslate Ui
#----------------------------------------------------------------------------------------------------
    def retranslateUi(self, MainDisplay):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainDisplay", "Settings Menu"))
        self.AddItemButton.setText(_translate("MainDisplay", "Add Item"))
        self.DeleteItemButton.setText(_translate("MainDisplay", "Delete Item"))
        self.MoreInfoButton.setText(_translate("MainDisplay", "More Info"))
        self.RefreshButton.setText(_translate("MainDisplay", "Refresh"))
        self.BackButton.setText(_translate("MainDisplay", "Back"))
        self.Header.setText(_translate("MainDisplay", "Settings"))
 
#----------------------------------------------------------------------------------------------------
#                                       Run this Program
#----------------------------------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    win = Ui_SettingsMenu()
    win.show()
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
#----------------------------------------------------------------------------------------------------