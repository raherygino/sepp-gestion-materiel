from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from qfluentwidgets import Dialog, SubtitleLabel, BodyLabel, PrimaryPushButton, FluentIcon, \
    RoundMenu, Action, MenuAnimationType
from ....components import LineEditWithLabel, DateEditWithLabel, SpinBoxEditWithLabel, TableView, ComboxEditWithLabel

class InitialMaterialDialog(Dialog):

    def __init__(self, parent=None):
        super().__init__("Ajouter un nouveau matériel", "", parent)
        self.setTitleBarVisible(False)
        self.titleLabel.setVisible(False)
        self.contentLabel.setVisible(False)
        self.col = QVBoxLayout()
        self.col.setSpacing(0)
        self.col.addWidget(SubtitleLabel('Matériel initial'))
        self.col.addWidget(BodyLabel('Matériel initial dans le magasin'))
        self.textLayout.addLayout(self.col)
        self.accessory = []
        self.parent = parent
        self.row = QHBoxLayout()
        self.dateReintegEdit = DateEditWithLabel("DATE")
        self.dateReintegEdit.setDateNow()
        self.nameEdit = LineEditWithLabel("DESIGNATION")
        self.nameEdit.lineEdit.textChanged.connect(self.__isValid)
        self.lot = ComboxEditWithLabel('LOT', ['-', 'Nautique'])
        self.row.addLayout(self.dateReintegEdit)
        self.row.addLayout(self.nameEdit)
        self.row.addLayout(self.lot)
        
        self.intoAccountSpinBox = SpinBoxEditWithLabel("EN COMPTE")
        self.intoAccountSpinBox.spinbox.textChanged.connect(self.__setBeValue)
        self.beSpinBox = SpinBoxEditWithLabel("BE")
        self.beSpinBox.spinbox.textChanged.connect(self.__setBreakdownValue)
        self.breakdownSpinBox = SpinBoxEditWithLabel("PANNE")
        self.breakdownSpinBox.spinbox.textChanged.connect(self.__setBeValue)
        self.row_2 = QHBoxLayout()
        self.row_2.addLayout(self.intoAccountSpinBox)
        self.row_2.addLayout(self.beSpinBox)
        self.row_2.addLayout(self.breakdownSpinBox)
        self.row_3 = QHBoxLayout()
        self.gradeEdit = LineEditWithLabel("GRADE")
        self.fullNameEdit = LineEditWithLabel("NOM ET PRENOMS")
        self.contactEdit = LineEditWithLabel("CONTACT")
        self.row_3.addLayout(self.gradeEdit)
        self.row_3.addLayout(self.fullNameEdit)
        self.row_3.addLayout(self.contactEdit)
        
        # add widget to view layout
        self.textLayout.addLayout(self.row)
        self.textLayout.addLayout(self.row_2)
        self.textLayout.addLayout(self.row_3)
        self.setFixedWidth(600)
        self.yesButton.setEnabled(False)
    
    def __setBeValue(self, value):
        self.__isValid()
        nValue = self.intoAccountSpinBox.spinbox.value()
        breakdown = self.breakdownSpinBox.spinbox.value()
        self.beSpinBox.spinbox.setValue(int(nValue) - int(breakdown))
    
    def __setBreakdownValue(self, value):
        nValue = self.intoAccountSpinBox.spinbox.value()
        be = self.beSpinBox.spinbox.value()
        self.breakdownSpinBox.spinbox.setValue(int(nValue) - int(be))
    
    def addAccessory(self):
        labelEdit = self.accessoryEdit.lineEdit
        self.accessory.append([self.accCountSpinBox.spinbox.value(),labelEdit.text()])
        labelEdit.setText("")
        self.accTable.setData(self.accessory)
        
    def mouseRightClick(self, event):
        selectedItems = self.accTable.selectedItems()
        if (len(selectedItems) != 0):
            menu = RoundMenu(parent=self.parent)
            menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda: self.__deleteAccessory(selectedItems)))
            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
            
    def __deleteAccessory(self, items: list):
        for i, acc in enumerate(self.accessory):
            if acc[0] == int(items[0].text()) and acc[1] == items[1].text():
                self.accessory.remove(acc)
        self.accTable.setData(self.accessory)
        
    def __isAccValid(self, value):
        cnt = self.accCountSpinBox.spinbox.value()
        text = self.accessoryEdit.lineEdit.text()
        if len(text) > 3 and cnt > 0:
            self.btnAddAccessory.setEnabled(True)
        else:
            self.btnAddAccessory.setEnabled(False)
            
    def __isValid(self, text = None):
        intoAccount = self.intoAccountSpinBox.spinbox.value()
        isValid = True
        if intoAccount == 0:
            isValid = False
        if len(self.nameEdit.text()) < 3:
            isValid = False
        self.yesButton.setEnabled(isValid)