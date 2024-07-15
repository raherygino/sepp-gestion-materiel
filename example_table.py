import sys
from PyQt5.QtWidgets import (QWidget, QTableWidget, QHBoxLayout, QApplication, QTableWidgetItem )
from PyQt5.QtGui     import QBrush, QColor #,  QFont 

class Table(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QTableWidget - Example of a cell merge")
        self.resize(660,300 );
        conLayout = QHBoxLayout()
        labels = ['DESIGNATION DE MATERIEL','EN COMPTE','EN BON', 'EN MAGASIN', 'ETAT', 'EN MAGASIN', 'GRADE NOM ET PRENOM'
                , 'CONTACT', 'MOTIF', 'LIEU', 'DATE DE PERCEPTION', 'DATE DE REINTEGRATION', 'ETAT DU MAT LORS DE LA REINTEGRATION']
        tableWidget = QTableWidget()
        tableWidget.setRowCount(8*3)
        tableWidget.setColumnCount(len(labels))
        
        for i in range(8):
            newItem = QTableWidgetItem(f"PALME {i}")  
            tableWidget.setItem(i, 0, newItem)
            
            newItem = QTableWidgetItem("10")  
            tableWidget.setItem(i, 1, newItem)
            
            newItem = QTableWidgetItem("01")  
            tableWidget.setItem(i, 2, newItem)
            
            newItem = QTableWidgetItem("09")  
            tableWidget.setItem(i, 3, newItem)
            
            newItem = QTableWidgetItem("BE")  
            tableWidget.setItem(i, 4, newItem)
            
            newItem = QTableWidgetItem("EN PANNE")  
            tableWidget.setItem(i, 5, newItem)
            
            newItem = QTableWidgetItem("08")  
            tableWidget.setItem(i+1, 4, newItem)
            
            newItem = QTableWidgetItem("01")  
            tableWidget.setItem(i+1, 5, newItem)
        
            tableWidget.setSpan(i, 0, 3, 1)   
            tableWidget.setSpan(i, 1, 3, 1) 
            tableWidget.setSpan(i, 2, 3, 1)    
            tableWidget.setSpan(i, 3, 3, 1)    
            '''tableWidget.setSpan(i, 4, 2, 1)    
            tableWidget.setSpan(i, 5, 2, 1)'''
        
        
        
        conLayout.addWidget(tableWidget)

        # Hide headers
        #tableWidget.horizontalHeader().setVisible(False)
        tableWidget.verticalHeader().setVisible(False)

        tableWidget.setHorizontalHeaderLabels(labels)  

        # Sets the span of the table element at (row , column ) to the number of rows 
        # and columns specified by (rowSpanCount , columnSpanCount ).
        '''tableWidget.setSpan(0, 0, 1, 6) 
        newItem = QTableWidgetItem("tableWidget.setSpan(0, 0, 1, 6)")  
        tableWidget.setItem(0, 0, newItem) 

        tableWidget.setSpan(3, 0, 3, 1)   
        newItem = QTableWidgetItem("tableWidget.setSpan(3, 0, 3, 1)")  
        tableWidget.setItem(3, 0, newItem)  

        newItem = QTableWidgetItem("Hello")  
        newItem.setForeground(QBrush(QColor(0, 255, 0)))
        tableWidget.setItem(3, 1, newItem)  

        newItem = QTableWidgetItem("pythoff") 
        newItem.setForeground(QBrush(QColor(255, 0, 0)))        
        tableWidget.setItem(3, 2, newItem)   '''
        tableWidget.resizeRowsToContents()
        
        self.setLayout(conLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = Table()  
    example.show()   
    sys.exit(app.exec_())