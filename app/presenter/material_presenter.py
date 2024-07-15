from PyQt5.QtWidgets import QFileDialog
from ..view import MaterialsInterface, NewMaterialDialog, InitialMaterialDialog, LotDialog
from ..models import Material, MaterialModel, MouvementModel, Mouvement, Lot, LotModel
from .depot_presenter import DepotPresenter
from .in_presenter import InPresenter
from .out_presenter import OutPresenter
from openpyxl import Workbook
import os

class MaterialPresenter:
    
    def __init__(self, view:MaterialsInterface, model: MaterialModel):
        self.view = view
        self.model = model
        self.moveModel = MouvementModel()
        self.lotModel = LotModel()
        self.__actions()
        self.depotPresenter = DepotPresenter(self)
        self.outPresenter = OutPresenter(self)
        
    def __actions(self):
        self.view.addAction.triggered.connect(lambda : self.showDialogNew())
        self.view.exportAction.triggered.connect(lambda: self.exportExcel())
        self.view.addLot.triggered.connect(lambda : self.showLotDialog())
        
    def showLotDialog(self):
        dialog = LotDialog(self.view)
        data = self.lotModel.fetch_all()
        lots = [[item.id, item.name] for item in data]
        dialog.table.setData(lots)
        dialog.yesBtn.clicked.connect(lambda: self.createUpdateLots(dialog))
        dialog.exec()
            
    def createUpdateLots(self, dialog: LotDialog):
        data = dialog.table.getData()
        ids = [int(item[0]) if item[0] != '' else 0 for item in data]
        lots = [Lot(id=int(item[0]) if item[0] != "" else 0, name=item[1]) for item in data]
        for item in self.lotModel.fetch_all():
            if item.id not in ids:
                self.lotModel.delete_item(item.id)
        for lot in lots:
            if lot.id == 0:self.lotModel.create(lot)
            else:self.lotModel.update_item(lot.id, name=lot.name)
        dialog.accept()
        
    def showDialogNew(self):
        dialog = InitialMaterialDialog(self.view)
        dialog.lot.combox.clear()
        dialog.lot.combox.addItem('')
        for lot in self.lotModel.fetch_all():
            dialog.lot.combox.addItem(lot.name)
        if dialog.exec():
            name = dialog.nameEdit.lineEdit.text()
            intoAccount = dialog.intoAccountSpinBox.spinbox.value()
            be = dialog.beSpinBox.spinbox.value()
            breakdown = dialog.breakdownSpinBox.spinbox.value()
            grade = dialog.gradeEdit.lineEdit.text()
            fullName = dialog.fullNameEdit.lineEdit.text()
            contact = dialog.contactEdit.lineEdit.text()
            dateReinteg = dialog.dateReintegEdit.lineEdit.text()
            lot = dialog.lot.combox.currentText()
            material = Material(
                name         = name,
                lot_name     = lot,
                into_account = intoAccount,
                be           = be,
                breakdown    = breakdown,
                in_store     = intoAccount,
                grade        = grade,
                full_name    = fullName,
                contact      = contact,
                date_reinteg = dateReinteg,
            )
            self.model.create(material)
            self.view.depot.emit()

    def exportExcel(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self.view,"Exporter",f"{os.path.expanduser('~')}/Materiels","Excel File (*.xlsx)", options=options)
        if fileName:
            dataDepot = self.view.depotInterface.tableView.getData()
            dataDepot.insert(0, self.view.depotInterface.tableView.getHeaderLabels())
            
            dataMove = self.view.outInterface.tableView.getData()
            dataMove.insert(0, self.view.outInterface.tableView.getHeaderLabels())
            # Create a new Workbook
            wb = Workbook()
            ws1 = wb.active
            ws1.title = 'Matériels en magasin'  # Optional: Rename the default sheet
            for row in dataDepot:
                ws1.append(row)

            # Create a new sheet
            ws2 = wb.create_sheet(title='Mouvements du Matériel')
            for row in dataMove:
                ws2.append(row)
                
            wb.save(fileName)
            os.startfile(fileName)