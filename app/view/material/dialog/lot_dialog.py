from PyQt5.QtWidgets import QHBoxLayout, QTableWidgetItem
from PyQt5.QtCore import QPoint, Qt, QModelIndex
from PyQt5.QtGui import QCursor, QKeyEvent

from qfluentwidgets import Dialog, Action, RoundMenu, MenuAnimationType, \
     PrimaryPushButton, PushButton, FluentIcon, SubtitleLabel, ToolButton, PrimaryToolButton
from ....components.table_view import TableView
from ....components import LineEditWithLabel

class LotDialog(Dialog):

    def __init__(self, parent=None):
        super().__init__("", "", parent)
        self.setTitleBarVisible(False)
        self.titleLabel.setVisible(False)
        self.contentLabel.setVisible(False)
        self.rowEdit = None
        self.row = QHBoxLayout()
        #self.btnGroup = QHBoxLayout()
        self.title = SubtitleLabel("Lot")
        self.row.addWidget(self.title, 0, Qt.AlignLeft)
        
        '''self.btnImport = ToolButton(FluentIcon.DOWNLOAD)
        self.btnExport= ToolButton(FluentIcon.SHARE)'''
        '''self.btnGroup.addWidget(self.btnImport)
        self.btnGroup.addWidget(self.btnExport)
        self.btnGroup.setAlignment(Qt.AlignRight)
        self.row.addLayout(self.btnGroup)'''
        
        self.row_2 = QHBoxLayout()
        self.name = LineEditWithLabel("Nouveau lot")
        self.name.lineEdit.setClearButtonEnabled(True)
        self.name.lineEdit.textChanged.connect(self.__nameChange)
        self.btnClear = ToolButton(FluentIcon.CLOSE)
        self.btnClear.clicked.connect(lambda: self.clearEdit())
        self.btnClear.setVisible(False)
        self.btnAdd = PrimaryToolButton(FluentIcon.ACCEPT)
        self.btnAdd.clicked.connect(lambda: self.__addItem(self.name.text()))
        self.btnAdd.setEnabled(False)
        self.row_2.addLayout(self.name)
        self.row_2.addWidget(self.btnClear, 0, Qt.AlignBottom)
        self.row_2.addWidget(self.btnAdd, 0, Qt.AlignBottom)
        
        self.table = TableView(self)
        self.table.contextMenuEvent = lambda event: self.contextMenu(event)
        '''self.table.itemClicked.connect(self.itemClicked)
        self.table.keyPressEvent = self.keyPress'''
        self.table.setHorizontalHeaderLabels(["ID", "Rubrique"])
        #self.table.setRowCount(1)
        self.table.setColumnCount(2)
        self.table.setMinimumHeight(300)
        #self.table.itemChanged.connect(lambda item: self.table.validateInput(3, item, "1"))
        
        self.yesBtn = PrimaryPushButton("Ok")
        self.cancelBtn = PushButton("Annuler")
        self.cancelBtn.clicked.connect(self.yesBtnClicked)
        self.textLayout.addLayout(self.row)
        self.textLayout.addLayout(self.row_2)
        self.textLayout.addWidget(self.table)
        
        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        
        self.buttonLayout.addWidget(self.yesBtn)
        self.buttonLayout.addWidget(self.cancelBtn)
        self.setFixedWidth(450)
        
    def __addItem(self, text):
        if self.rowEdit == None:
            data = self.table.getData()
            self.table.setRowCount(len(data)+1)
            self.table.setItem(len(data), 1, QTableWidgetItem(str(text)))
        else:
            self.table.setItem(self.rowEdit, 1, QTableWidgetItem(str(text)))
            
        self.table.resizeColumnsToContents()
        self.clearEdit()
        
    def __nameChange(self, value):
        self.btnAdd.setEnabled(len(value) > 2)
        
    def yesBtnClicked(self):
        self.close()

    ''''def keyPress(self, event: QKeyEvent | None) -> None:
        if event.key() == Qt.Key_Delete:
            items = self.table.selectionModel().selectedRows()
            if len(items) > 0:
                self.deleteSubject(items)
        
    def itemClicked(self, item: QTableWidgetItem):
        if item.column() == 0:
            for i in range(self.table.columnCount()):
                self.table.item(item.row(), i).setSelected(True)
        
    def itemRightClicked(self, item: QTableWidgetItem):
        for i in range(0, self.table.columnCount()):
            self.table.item(item.row(), i).setSelected(True)
    '''    
    def contextMenu(self, event):
        '''for item in self.table.selectedItems():
            self.itemRightClicked(item)'''
        items = self.table.selectionModel().selectedRows()
        if len(items) > 0:
            menu = RoundMenu(parent=self)
            menu.addAction(Action(FluentIcon.EDIT, 'Modifier', triggered = lambda:self.editLot(items)))
            menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda:self.deleteLot(items)))
            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
        
    def editLot(self, item: list[QModelIndex]):
        self.btnClear.setVisible(True)
        self.rowEdit = item[0].row()
        self.name.setText(self.table.item(item[0].row(), 1).text())
        
    def clearEdit(self):
        self.rowEdit = None
        self.name.setText('')
        self.btnClear.setVisible(False)
        
    def deleteLot(self, items):
        dialog = Dialog("Supprimer?", "Voulez vous supprimer vraiment?", self)
        dialog.setTitleBarVisible(False)
        if dialog.exec():
            for index in sorted(items, key=lambda x: x.row(), reverse=True):
                self.table.removeRow(index.row())

 

        