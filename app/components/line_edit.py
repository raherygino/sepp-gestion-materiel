from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import QDate
from qfluentwidgets import LineEdit, BodyLabel, ComboBox, CompactSpinBox, DateEdit
from datetime import datetime

class LineEditWithLabel(QVBoxLayout):
    def __init__(self, label:str, parent=None):
        super().__init__(parent)
        self.setSpacing(2)
        self.lineEdit = LineEdit(parent)
        self.label = BodyLabel(label)
        self.addWidget(self.label)
        self.addWidget(self.lineEdit)
        
    def setVisible(self, visible:bool):
        self.lineEdit.setVisible(visible)
        self.label.setVisible(visible)
        
    def text(self) -> str:
        return self.lineEdit.text()

    def setText(self, text:str):
        self.lineEdit.setText(text)
    
    def setWidth(self, width:int):
        self.label.setFixedWidth(width)
        self.lineEdit.setFixedWidth(width)

class DateEditWithLabel(QVBoxLayout):
    def __init__(self, label:str, parent=None):
        super().__init__(parent)
        self.setSpacing(2)
        self.lineEdit = DateEdit(parent)
        self.lineEdit.setDate(QDate(1950,1,1))
        self.label = BodyLabel(label)
        self.addWidget(self.label)
        self.addWidget(self.lineEdit)
        
    def text(self) -> str:
        value = self.lineEdit.text()
        return value if value != "01/01/1950" else ""
    
    def setDateNow(self):
        cDate = datetime.now()
        self.lineEdit.setDate(QDate(cDate.year, cDate.month, cDate.day))
        
        
class ComboxEditWithLabel(QVBoxLayout):
    def __init__(self, label:str, data=[], parent=None):
        super().__init__(parent)
        self.setSpacing(2)
        self.combox = ComboBox(parent)
        self.combox.addItems(data)
        self.label = BodyLabel(label)
        self.addWidget(self.label)
        self.addWidget(self.combox)
        
class SpinBoxEditWithLabel(QVBoxLayout):
    def __init__(self, label:str, parent=None):
        super().__init__(parent)
        self.setSpacing(2)
        self.spinbox = CompactSpinBox(parent)
        self.label = BodyLabel(label)
        self.addWidget(self.label)
        self.addWidget(self.spinbox)
        