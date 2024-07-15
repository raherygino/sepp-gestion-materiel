from PyQt5.QtWidgets import QHBoxLayout, QFrame
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from qfluentwidgets import Dialog, SubtitleLabel, StrongBodyLabel, PrimaryPushButton, FluentIcon, \
    RoundMenu, Action, MenuAnimationType
from ....components import LineEditWithLabel, DateEditWithLabel, SpinBoxEditWithLabel, TableView, ComboxEditWithLabel
from ....models import Material

class ReintMaterialDialog(Dialog):

    def __init__(self, material:Material, parent=None):
        super().__init__("Ajouter un nouveau matériel", "", parent)
        self.setTitleBarVisible(False)
        self.titleLabel.setVisible(False)
        self.contentLabel.setVisible(False)
        self.titleLabel = StrongBodyLabel(f'REINTEGRATION | {material.name}')
        self.accessory = []
        self.parent = parent
        self.material = material
        self.row = QHBoxLayout()
        self.nameEdit = LineEditWithLabel("DESIGNATION")
        self.nameEdit.lineEdit.setReadOnly(True)
        self.nameEdit.setEnabled(False)
        
        self.intoAccountSpinBox = LineEditWithLabel("EN COMPTE")
        self.intoAccountSpinBox.lineEdit.setReadOnly(True)
        self.intoAccountSpinBox.setWidth(80)
        self.intoAccountSpinBox.setVisible(False)
        
        self.inStoreSpinBox = LineEditWithLabel("EN MAGASIN")
        self.inStoreSpinBox.setWidth(90)
        self.inStoreSpinBox.lineEdit.setReadOnly(True)
        
        self.beSpinBox = LineEditWithLabel("BE")
        self.beSpinBox.setWidth(50)
        self.beSpinBox.lineEdit.setReadOnly(True)
        self.beSpinBox.setVisible(False)
        
        self.breakdownSpinBox = LineEditWithLabel("PANNE")
        self.breakdownSpinBox.setWidth(80)
        self.breakdownSpinBox.lineEdit.setReadOnly(True)
        self.breakdownSpinBox.setVisible(False)
        
        self.row.addLayout(self.nameEdit)
        self.row.addLayout(self.intoAccountSpinBox)
        self.row.addLayout(self.inStoreSpinBox)
        self.row.addLayout(self.beSpinBox)
        self.row.addLayout(self.breakdownSpinBox)
        
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        
        self.row_2 = QHBoxLayout()
        self.gradeEdit = LineEditWithLabel("GRADE")
        self.fullNameEdit = LineEditWithLabel("NOM ET PRENOMS")
        self.fullNameEdit.lineEdit.textChanged.connect(self.__isValid)
        self.contactEdit = LineEditWithLabel("CONTACT")
        self.gradeEdit.lineEdit.setReadOnly(True)
        self.fullNameEdit.lineEdit.setReadOnly(True)
        self.contactEdit.lineEdit.setReadOnly(True)
        self.row_2.addLayout(self.gradeEdit)
        self.row_2.addLayout(self.fullNameEdit)
        self.row_2.addLayout(self.contactEdit)
        
        self.row_3 = QHBoxLayout()
        self.countInGood = LineEditWithLabel('Nombre')
        self.countInGood.lineEdit.setReadOnly(True)
        self.countInGood.lineEdit.textChanged.connect(self.__inGoodChanged)
        
        self.countBe= SpinBoxEditWithLabel('BE')
        self.countBe.spinbox.textChanged.connect(self.__beOnChanged)
        
        self.countBreakdown= SpinBoxEditWithLabel('EN PANNE')
        self.countBreakdown.spinbox.textChanged.connect(self.__breakdownOnChanged)
        
        
        self.dateReintegEdit = DateEditWithLabel("DATE DE REINTEGRATION")
        self.dateReintegEdit.setDateNow()
        '''self.stateMatIntegr = ComboxEditWithLabel("ETAT DU MAT LORS DE LA REINTEGRATION", ['BONNE ETAT', 'EN PANNE'])
        self.stateMatIntegr.combox.currentTextChanged.connect(self.__inGoodChanged)'''
        self.row_3.addLayout(self.countInGood)
        self.row_3.addLayout(self.countBe)
        self.row_3.addLayout(self.countBreakdown)
        self.row_3.addLayout(self.dateReintegEdit)
        #self.row_3.addLayout(self.stateMatIntegr)

        # add widget to view layout
        self.textLayout.addWidget(self.titleLabel)
        self.textLayout.addLayout(self.row)
        self.textLayout.addLayout(self.row_2)
        self.textLayout.addWidget(self.line)
        self.textLayout.addLayout(self.row_3)
        self.setFixedWidth(600)
        self.__setData(material)
        self.yesButton.setEnabled(False)
        
    def __setData(self, material:Material):
        self.nameEdit.setText(material.name)
        self.intoAccountSpinBox.lineEdit.setText(str(material.into_account))
        self.inStoreSpinBox.lineEdit.setText(str(material.in_store))
        self.beSpinBox.lineEdit.setText(str(material.be))
        self.breakdownSpinBox.lineEdit.setText(str(material.breakdown))
        
    def __inGoodChanged(self, value):
        inGood = self.countInGood.lineEdit.text()
        '''state = self.stateMatIntegr.combox.currentText()
        self.inStoreSpinBox.lineEdit.setText(str(int(self.material.in_store) + int(inGood)))
        if state == 'BONNE ETAT':
            self.beSpinBox.lineEdit.setText(str(int(self.material.be) + int(inGood)))
            self.breakdownSpinBox.lineEdit.setText(str(self.material.breakdown))
        else:
            self.breakdownSpinBox.lineEdit.setText(str(int(self.material.breakdown) + int(inGood)))
            self.beSpinBox.lineEdit.setText(str(self.material.be))'''
        self.__isValid()
        
    def __beOnChanged(self, value):
        inGood = self.countInGood.lineEdit.text()
        breakdown = int(inGood) - int(value)
        self.countBreakdown.spinbox.setValue(breakdown)
        self.breakdownSpinBox.lineEdit.setText(str(int(self.material.breakdown) + int(breakdown)))
        self.beSpinBox.lineEdit.setText(str(int(self.material.be) + int(value)))
        self.inStoreSpinBox.lineEdit.setText(str(int(self.material.in_store) + int(inGood)))
        #print(f'old:{self.material.breakdown} new:{int(self.material.breakdown) + int(breakdown)}')
        
    def __breakdownOnChanged(self, value):
        inGood = self.countInGood.lineEdit.text()
        be = int(inGood) - int(value)
        self.countBe.spinbox.setValue(be)
        self.breakdownSpinBox.lineEdit.setText(str(int(self.material.breakdown) + int(value)))
        self.beSpinBox.lineEdit.setText(str(int(self.material.be) + int(be)))
        self.inStoreSpinBox.lineEdit.setText(str(int(self.material.in_store) + int(inGood)))
            
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
            
    def __isValid(self, value = None):
        inGood = int(self.countInGood.lineEdit.text())
        isValid = True
        if inGood == 0:
            isValid = False
        self.yesButton.setEnabled(isValid)