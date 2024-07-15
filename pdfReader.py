import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.createActions()
        self.createMenus()

        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)

    def createActions(self):
        self.openAction = QAction("&Open PDF...", self)
        self.openAction.triggered.connect(self.openPdf)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAction)

    def openPdf(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")

        if fileName:
            print(QUrl.fromLocalFile(fileName))
            self.webview.setUrl(QUrl.fromLocalFile(fileName))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = PDFViewer()
    mainWindow.show()
    sys.exit(app.exec_())
