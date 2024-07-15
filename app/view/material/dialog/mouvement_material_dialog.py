from PyQt5.QtWidgets import QHBoxLayout, QFrame
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from qfluentwidgets import Dialog, SubtitleLabel, StrongBodyLabel, PrimaryPushButton, FluentIcon, \
    RoundMenu, Action, MenuAnimationType
from ....components import LineEditWithLabel, DateEditWithLabel, SpinBoxEditWithLabel, TableView, ComboxEditWithLabel
from ....models import Material

class MouvementMaterialDialog(Dialog):

    def __init__(self, material:Material, parent=None):
        super().__init__("Ajouter un nouveau matériel", "", parent)
        self.setTitleBarVisible(False)
        self.titleLabel.setVisible(False)
        self.contentLabel.setVisible(False)
        self.titleLabel = StrongBodyLabel(f'PERCEPTION | {material.name}')
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
        
        self.inStoreSpinBox = LineEditWithLabel("EN MAGASIN")
        self.inStoreSpinBox.setWidth(90)
        self.inStoreSpinBox.lineEdit.setReadOnly(True)
        
        self.beSpinBox = LineEditWithLabel("BE")
        self.beSpinBox.setWidth(50)
        self.beSpinBox.lineEdit.setReadOnly(True)
        
        self.breakdownSpinBox = LineEditWithLabel("PANNE")
        self.breakdownSpinBox.setWidth(80)
        self.breakdownSpinBox.lineEdit.setReadOnly(True)
        
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
        self.countInGood = SpinBoxEditWithLabel('Nombre en bon')
        self.countInGood.spinbox.textChanged.connect(self.__inGoodChanged)
        self.datePercEdit = DateEditWithLabel("DATE DE PERCEPTION")
        self.datePercEdit.setDateNow()
        
        self.row_2.addLayout(self.countInGood)
        self.row_2.addLayout(self.datePercEdit)
    
        self.row_3 = QHBoxLayout()
        self.gradeEdit = LineEditWithLabel("GRADE")
        self.fullNameEdit = LineEditWithLabel("NOM ET PRENOMS")
        self.fullNameEdit.lineEdit.textChanged.connect(self.__isValid)
        self.contactEdit = LineEditWithLabel("CONTACT")
        self.row_3.addLayout(self.gradeEdit)
        self.row_3.addLayout(self.fullNameEdit)
        self.row_3.addLayout(self.contactEdit)
        self.row_4 = QHBoxLayout()
        self.motifEdit = LineEditWithLabel("MOTIF")
        self.placeEdit = LineEditWithLabel("LIEU")
        self.row_4.addLayout(self.motifEdit)
        self.row_4.addLayout(self.placeEdit)

        # add widget to view layout
        self.textLayout.addWidget(self.titleLabel)
        self.textLayout.addLayout(self.row)
        self.textLayout.addWidget(self.line)
        self.textLayout.addLayout(self.row_2)
        self.textLayout.addLayout(self.row_3)
        self.textLayout.addLayout(self.row_4)
        self.setFixedWidth(600)
        self.__setData(material)
        self.yesButton.setEnabled(False)
        
    def __setData(self, material:Material):
        self.nameEdit.setText(material.name)
        self.intoAccountSpinBox.lineEdit.setText(str(material.into_account))
        self.inStoreSpinBox.lineEdit.setText(str(material.in_store))
        self.beSpinBox.lineEdit.setText(str(material.be))
        self.countInGood.spinbox.setValue(int(material.be))
        self.countInGood.spinbox.setMaximum(int(material.be))
        self.breakdownSpinBox.lineEdit.setText(str(material.breakdown))
        
    def __inGoodChanged(self, value):
        inGood = self.countInGood.spinbox.value()
        self.inStoreSpinBox.lineEdit.setText(str(int(self.material.in_store) - int(inGood)))
        self.breakdownSpinBox.lineEdit.setText(str(self.material.breakdown))
        self.beSpinBox.lineEdit.setText(str(int(self.material.be) - int(inGood)))
        self.__isValid()
            
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
        inGood = self.countInGood.spinbox.value()
        isValid = True
        if inGood == 0:
            isValid = False
        if len(self.fullNameEdit.text()) < 3:
            isValid = False
        self.yesButton.setEnabled(isValid)
