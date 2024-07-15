# coding: utf-8
from PyQt5.QtCore import QUrl, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QVBoxLayout

from qfluentwidgets import NavigationItemPosition, FluentWindow, FluentStyleSheet, \
                            SplashScreen, TitleLabel, Dialog, BodyLabel, MessageDialog
from qfluentwidgets import FluentIcon as FIF

from qframelesswindow import TitleBar
#from .setting_interface import SettingInterface
from ..common.config import ZH_SUPPORT_URL, EN_SUPPORT_URL, cfg
from ..common.signal_bus import signalBus


from ..models import MaterialModel
from ..presenter import MaterialPresenter
from .material.materials_interface import MaterialsInterface

class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = TitleLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

class FluentTitleBar(TitleBar):
    """ Fluent title bar"""

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)

        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertWidget(0, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.subtitleLabel = BodyLabel(self)
        self.hBoxLayout.insertWidget(1, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.hBoxLayout.insertWidget(2, self.subtitleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.titleLabel.setObjectName('titleLabel')
        self.subtitleLabel.setObjectName('subtitleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.maxBtn)
        self.buttonLayout.addWidget(self.closeBtn)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)
        self.hBoxLayout.addLayout(self.vBoxLayout, 0)

        FluentStyleSheet.FLUENT_WINDOW.apply(self)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))
        
class MainWindow(FluentWindow):
    
    currentPromotion = pyqtSignal(int)
    refresh = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initWindow()
        
        self.materialsInterface = MaterialsInterface(self)
        #self.settingInterface = SettingInterface(self)
        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)
        self.connectSignalToSlot()

        
        self.materialModel = MaterialModel()
        self.materialPresenter = MaterialPresenter(self.materialsInterface, self.materialModel)

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.supportSignal.connect(self.onSupport)

    def initNavigation(self):
        self.addSubInterface(self.materialsInterface, FIF.APPLICATION, "Matériels")
        self.navigationInterface.addSeparator()

        '''self.addSubInterface(
            self.settingInterface, FIF.SETTING, 'Paramètres', NavigationItemPosition.BOTTOM)'''

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))
        self.fluentTitleBar = FluentTitleBar(self)
        #self.fluentTitleBar.setIcon(QIcon('app/resource/images/logo_eniap.png'))
        self.fluentTitleBar.titleLabel.setText('Gestion de materiel')
        self.setTitleBar(self.fluentTitleBar)

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIcon(QIcon('app/resource/images/logo_eniap.png'))
        self.splashScreen.setIconSize(QSize(240, 240))
        self.splashScreen.raise_()
        
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.showMaximized()
        QApplication.processEvents()

    def onSupport(self):
        language = cfg.get(cfg.language).value
        if language.name() == "zh_CN":
            QDesktopServices.openUrl(QUrl(ZH_SUPPORT_URL))
        else:
            QDesktopServices.openUrl(QUrl(EN_SUPPORT_URL))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())
            
    
    def closeEvent(self, event):

        exitDialog = Dialog(
            'Quitter', 'Voulez vous quitter vraiment?',
            self
        )
        exitDialog.setTitleBarVisible(False)
        exitDialog.yesButton.setText('Oui')
        exitDialog.cancelButton.setText('Non')
        if exitDialog.exec():
            event.accept()
        else:
            event.ignore()