from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

from qfluentwidgets import SegmentedWidget, TransparentDropDownPushButton, Action,\
    CommandBar, RoundMenu, FluentIcon, setFont, StrongBodyLabel , SearchLineEdit,\
    BodyLabel
from .tab import DepotTab, EntryTab, OutTab
from ...common import Function

class MaterialsInterface(QWidget):
    
    depot = pyqtSignal()
    refresh = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.func = Function()
        self.resize(400, 400)
        self.mainWindow = self.parent
        self.nParent = parent
        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout()

        self.depotInterface = DepotTab(self)
        self.outInterface = OutTab(self)

        # add items to pivot
        self.addSubInterface(self.depotInterface, 'depotInterface', 'Matériels en magasin')
        self.addSubInterface(self.outInterface, 'outInterface', 'Mouvements du Matériel')

        self.__initCommandBar()
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.addWidget(self.pivot)
        
        self.countLayout = QHBoxLayout()
        self.countLayout.setContentsMargins(0,0,0,0)
        self.countLayout.setAlignment(Qt.AlignRight)
        self.titleCount = StrongBodyLabel("Nombre")
        self.valueCount = BodyLabel("")
        self.countLayout.addWidget(self.titleCount)
        self.countLayout.addWidget(self.valueCount)        
        self.vBoxLayout.addLayout(self.countLayout)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.depotInterface)
        self.pivot.setCurrentItem(self.depotInterface.objectName())
        self.setObjectName("materielsTab")
        

    def createDropDownButton(self, title, icon, children:list, parent):
        button = TransparentDropDownPushButton(title, self, icon)
        button.setFixedHeight(34)
        setFont(button, 12)
        menu = RoundMenu(parent=parent)
        menu.addActions(children)
        button.setMenu(menu)
        return button
        
    def __initCommandBar(self):
        self.commandBar = CommandBar(self)
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commandBar.setButtonTight(True)
        setFont(self.commandBar, 14)
        
        self.addAction = Action(FluentIcon.APPLICATION, "Nouveau matériel", self)
        self.addLot = Action(FluentIcon.FOLDER, "LOT", self)
        self.exportAction = Action(FluentIcon.SHARE, "Exporter", self)
        self.deleteAction = Action(FluentIcon.DELETE, "Supprimer tous", self)   
        
        self.commandBar.addAction(self.addAction)
        self.commandBar.addAction(self.addLot)
        self.commandBar.addAction(self.exportAction)
        
        self.titleLabel = StrongBodyLabel("Matériels en magasin")
        
        self.hBoxLayout.addWidget(self.commandBar)
        self.hBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        
    def addSubInterface(self, widget: QLabel, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.titleLabel.setText(self.pivot.currentItem().text())
        self.pivot.setCurrentItem(widget.objectName())
        self.valueCount.setText(str(len(self.func.getTableData(widget.tableView))))