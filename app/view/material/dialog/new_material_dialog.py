from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from qfluentwidgets import Dialog, SubtitleLabel, StrongBodyLabel, PrimaryPushButton, FluentIcon, \
    RoundMenu, Action, MenuAnimationType
from ....components import LineEditWithLabel, DateEditWithLabel, SpinBoxEditWithLabel, TableView, ComboxEditWithLabel

class NewMaterialDialog(Dialog):

    def __init__(self, parent=None):
        super().__init__("Ajouter un nouveau matériel", "", parent)
        self.setTitleBarVisible(False)
        self.titleLabel.setVisible(False)
        self.contentLabel.setVisible(False)
        self.titleLabel = SubtitleLabel('Matériels entrants')
        self.accessory = []
        self.parent = parent
        self.row = QHBoxLayout()
        self.nameEdit = LineEditWithLabel("DESIGNATION")
        self.intoAccountSpinBox = SpinBoxEditWithLabel("EN COMPTE")
        self.inGoodSpinBox = SpinBoxEditWithLabel("EN BON")
        self.inStoreSpinBox = SpinBoxEditWithLabel("EN MAGASIN")
        self.beSpinBox = SpinBoxEditWithLabel("BE")
        self.breakdownSpinBox = SpinBoxEditWithLabel("PANNE")
        self.row.addLayout(self.nameEdit)
        self.row.addLayout(self.intoAccountSpinBox)
        self.row.addLayout(self.inGoodSpinBox)
        self.row.addLayout(self.inStoreSpinBox)
        self.row.addLayout(self.beSpinBox)
        self.row.addLayout(self.breakdownSpinBox)
        self.row_2 = QHBoxLayout()
        self.gradeEdit = LineEditWithLabel("GRADE")
        self.fullNameEdit = LineEditWithLabel("NOM ET PRENOMS")
        self.contactEdit = LineEditWithLabel("CONTACT")
        self.row_2.addLayout(self.gradeEdit)
        self.row_2.addLayout(self.fullNameEdit)
        self.row_2.addLayout(self.contactEdit)
        self.row_3 = QHBoxLayout()
        self.motifEdit = LineEditWithLabel("MOTIF")
        self.placeEdit = LineEditWithLabel("LIEU")
        self.row_3.addLayout(self.motifEdit)
        self.row_3.addLayout(self.placeEdit)
        self.row_4 = QHBoxLayout()
        self.datePercEdit = DateEditWithLabel("DATE DE PERCEPTION")
        self.datePercEdit.setDateNow()
        self.dateReintegEdit = DateEditWithLabel("DATE DE REINTEGRATION")
        self.dateReintegEdit.setDateNow()
        self.stateMatIntegr = ComboxEditWithLabel("ETAT DU MAT LORS DE LA REINTEGRATION", ['BONNE ETAT', 'EN PANNE'])
        self.row_4.addLayout(self.datePercEdit)
        self.row_4.addLayout(self.dateReintegEdit)
        self.row_4.addLayout(self.stateMatIntegr)
        
        # add widget to view layout
        self.textLayout.addWidget(self.titleLabel)
        self.textLayout.addLayout(self.row)
        self.textLayout.addLayout(self.row_2)
        self.textLayout.addLayout(self.row_3)
        self.textLayout.addLayout(self.row_4)
        self.setFixedWidth(600)
    
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
            
    def __isValid(self, text):
        name = self.nameEdit.lineEdit.text()
        nType = self.typeEdit.lineEdit.text()
        count = self.countSpinBox.spinbox.value()
        self.yesButton.setEnabled(len(name) > 2 and len(nType) > 2 and count > 0)