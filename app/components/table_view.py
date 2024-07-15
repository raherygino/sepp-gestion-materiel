from typing import Iterable
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from ..common.config import cfg
import darkdetect

class TableView(QTableWidget):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWordWrap(False)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.header = self.horizontalHeader()
        self.verticalHeader().hide()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setContentsMargins(0,0,0,0)
        self.setQss(cfg.get(cfg.theme))
        
    def setColorRow(self, row:int, color:str):
        for col in range(len(self.getHeaderLabels())):
            item = self.item(row,col)
            if item != None:
                item.setForeground(QColor(color))
    
    def setQss(self, newTheme: str):
        theme = newTheme.lower()
        themeColor = f'rgba{str(cfg.get(cfg.themeColor).getRgb())}'
        if theme == "auto":
            theme = "light" if darkdetect.isLight() else "dark"
        with open(f'app/resource/qss/{theme}/table_view.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read().replace("#327bcc", themeColor))
    
    def setHorizontalHeaderLabels(self, labels: Iterable[str | None]) -> None:
        self.setColumnCount(len(labels))
        #self.header.setSectionResizeMode(len(labels) - 1, QHeaderView.Stretch)
        return super().setHorizontalHeaderLabels(labels)
    
    def selectedRows(self):
        selected_rows = set()  # Use a set to store unique row indices
        for item in self.selectedItems():
            selected_rows.add(item.row())
        return selected_rows
            
    def getHeaderLabels(self):
        header_labels = []
        for column in range(self.columnCount()):
            header_item = self.horizontalHeaderItem(column)
            if header_item is not None:
                header_labels.append(header_item.text())
            else:
                header_labels.append(f"Column {column}")  # Default label if item is None
        return header_labels
        
    def setData(self, items):
        self.setRowCount(0)
        for row, item in enumerate(items):
            self.insertRow(row)
            for col, value in enumerate(item):
                self.setItem(row, col, QTableWidgetItem(str(value)))
                
        self.resizeColumnsToContents()
    
                        
    def getData(self) -> list:
        row_count = self.rowCount()
        column_count = self.columnCount()
        table_data = []
        for row in range(row_count):
            row_data = []
            for column in range(column_count):
                item = self.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            table_data.append(row_data)
        return table_data