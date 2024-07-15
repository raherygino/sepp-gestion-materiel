from datetime import datetime
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QCursor
from qfluentwidgets import RoundMenu, Action, FluentIcon, MenuAnimationType
from .base_presenter import BasePresenter
from .menu_presenter import MenuAction
from ..models import Material, Mouvement
from ..view import MouvementMaterialDialog

class DepotPresenter(BasePresenter):
    
    def __init__(self, parent):
        self.model = parent.model
        self.moveModel = parent.moveModel
        super().__init__(self.model.fetch_all(),parent)
        self.setTableHeaderLabels(["ID", "DESIGNATION DE MATERIEL", "EN COMPTE", "EN BON", "EN MAGASIN", "BONNE ETAT", "PANNE", "DATE"])
        self.setTableContextMenu(self.mouseRightClick)
        self.view.parent.refresh.connect(lambda: self.fetchData(self.model.fetch_all()))
        
    def fetchData(self, data):
        gData = self.model.fetch_all(group="lot_name")
        bData = []
        for nItem in gData:
            bData.append(Material(lot_name=nItem.lot_name))
            bData.extend(self.model.fetch_all(lot_name=nItem.lot_name))
        return super().fetchData(bData)
        
    def handleResult(self, data: list[Material]):
        super().handleResult(data)
        table = self.view.tableView
        table.setRowCount(len(data))
        rows = []
        nRows = []
        for row, material in enumerate(data):
            nRows.append(row)
            if material.id > 0:
                keys = ['id', 'name','into_account', 'in_good', 'in_store', 'be', 'breakdown', 'date_reinteg']
                for i,  key in enumerate(keys):
                    table.setItem(row, i, QTableWidgetItem(str(material.get(key))))
            else:
                item = QTableWidgetItem(f'LOT: {material.lot_name}')
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, 0, item)
                rows.append(row)
        table.resizeColumnsToContents()
        for row in nRows:
            if row in rows:
                table.setSpan(row, 0, 1, 8)
            else:
                current_row_span = table.rowSpan(row, 0)
                current_col_span = table.columnSpan(row, 0)
                if current_row_span > 1 or current_col_span > 1:
                    table.setSpan(row, 0, 1, 1)  # Restoring to original span (1x1)
    
    def mouseRightClick(self, event):
        selectedItems = self.view.tableView.selectedItems()
        if (len(selectedItems) != 0):
            idItem = self.view.tableView.selectedItems()[0].text()
            if idItem.find('LOT') == -1:
                action = MenuAction(self)
                menu = RoundMenu(parent=self.view)
                selectedRows = self.view.tableView.selectedRows()
                if len(selectedRows) == 1:
                    menu.addAction(Action(FluentIcon.SHARE, 'Mouvement', triggered = lambda: self.showDialog(idItem)))
                    menu.addSeparator()
                menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda: action.confirmDelete(self.view.tableView, selectedRows)))

                self.posCur = QCursor().pos()
                cur_x = self.posCur.x()
                cur_y = self.posCur.y()
                menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
            
    def showDialog(self, selectedId):
        material : Material= self.model.fetch_item_by_id(selectedId)
        dialog = MouvementMaterialDialog(material, self.view)
        if dialog.exec():
            inGood = dialog.countInGood.spinbox.value()
            nInGood = str(int(material.in_good) + inGood)
            inStore = dialog.inStoreSpinBox.lineEdit.text()
            be = dialog.beSpinBox.lineEdit.text()
            breakdown = dialog.breakdownSpinBox.lineEdit.text()
            
            mouvement = Mouvement(
                material_id = material.id,
                in_good     = inGood,
                grade       = dialog.gradeEdit.text(),
                full_name   = dialog.fullNameEdit.text(),
                contact     = dialog.contactEdit.text(),
                motif       = dialog.motifEdit.text(),
                place       = dialog.placeEdit.text(),
                date_perc   = dialog.datePercEdit.text(),
                #date_reinteg= dialog.dateReintegEdit.text()
            )
            self.moveModel.create(mouvement)
            self.model.update_item(material.id, 
                                   in_good  = nInGood,
                                   in_store = inStore,
                                   be       = be,
                                   breakdown= breakdown
                                )
            self.view.parent.depot.emit()