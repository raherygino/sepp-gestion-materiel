from PyQt5.QtGui import QCursor, QColor
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QTableWidgetItem
from qfluentwidgets import RoundMenu, Action, FluentIcon, MenuAnimationType
from ..models import MaterialModel, Mouvement, MouvementModel, Material
from .base_presenter import BasePresenter
from .menu_presenter import MenuAction
from ..view import OutTab, ReintMaterialDialog

class OutPresenter(BasePresenter):
    
    def __init__(self, parent):
        self.model: MaterialModel = parent.model
        self.moveModel: MouvementModel = parent.moveModel
        super().__init__([], parent)
        self.view: OutTab = parent.view.outInterface
        self.refresh.connect(lambda: self.fetchData([]))
        self.labels = ["ID", "DESIGNATION DE MATERIEL", "EN COMPTE", "EN BON", 
                                   "EN MAGASIN","EN MAGASIN\nBE","EN MAGASIN\nPANNE", "QTE","BE","PANNE", "GRADE", "NOM ET PRENOM", 
                                   "CONTACT", "MOTIF", "LIEU", "DATE DE PERCEPTION", 
                                   "DATE DE REINTEGRATION", "ETAT DU MAT LORS \nDE LA REINTEGRATION"]
        self.setTableHeaderLabels(self.labels)
        self.setTableContextMenu(self.mouseRightClick)
        
    def fetchData(self, data):
        columns = ['mouvements.id', 'materials.name', 'materials.into_account',
             'materials.in_good', 'materials.in_store', 
             'materials.be', 'materials.breakdown', 'mouvements.in_good', 'mouvements.be', 'mouvements.breakdown',
             'mouvements.grade','mouvements.full_name', 'mouvements.contact', 
             'mouvements.motif','mouvements.place', 'mouvements.date_perc',  
             'mouvements.date_reinteg', 'mouvements.state_mat_integr']
        columns.insert(1, 'materials.lot_name')
        nData = self.moveModel.select_join(columns, 'materials', 'material_id', order='materials.name', group='materials.lot_name')
        #"""gData = self.model.fetch_all(group="lot_name")
        bData = []
        columns.pop(1)
        for nItem in nData:
            bData.append([f'LOT: {nItem[1]}'])
            bData.extend(self.moveModel.select_join(columns, 'materials', 'material_id',
                                                    materials__lot_name=nItem[1], order='materials.name'))
            
        return super().fetchData(bData)
        
    def handleResult(self, data: list):
        vItems = []
        rows = []
        bRows = []
        nRows = []
        self.view.progressBar.setVisible(False)
        nData = [list(item) for item in data]
        self.view.tableView.setRowCount(0)
        self.view.tableView.setRowCount(len(nData))
        for i, item in enumerate(nData):
            nRows.append(i)
            if len(item) == 1:
                bRows.append(i)
            for j, nItem in enumerate(item):
                if j == 1:
                    if nItem not in vItems:
                        vItems.append(nItem)
                        rows.append(i)
                vItem = QTableWidgetItem(str(nItem))
                if len(item) == 1:
                    vItem.setTextAlignment(Qt.AlignCenter)
                self.view.tableView.setItem(i,j,vItem)
                if nItem == "" and j == len(item) - 2:
                    self.view.tableView.setColorRow(i, 'red')
                if nItem == "EN PANNE" and j == len(item) - 1:
                    self.view.tableView.setColorRow(i, 'red')
        rows.append(len(nData))
        differences = [rows[i] - rows[i-1] for i in range(1, len(rows))]
        for i, row in enumerate(rows):
            if i < len(differences) and differences[i] > 1:
                item = self.view.tableView.item(row+differences[i]-1, 0)
                if item != None:
                    vl = item.text()
                    if vl.find('LOT') != -1:
                        self.setRowSpan(row,differences[i]-1, 1,7) ### BUG TO FIX
                    else:
                        self.setRowSpan(row,differences[i], 1,7)
                
                
        self.view.tableView.resizeColumnsToContents()
        for row in nRows:
            if row in bRows:
                self.view.tableView.setSpan(row, 0, 1, len(self.labels))
            else:
                current_row_span = self.view.tableView.rowSpan(row, 0)
                current_col_span = self.view.tableView.columnSpan(row, 0)
                if current_row_span > 1 or current_col_span > 1:
                    self.view.tableView.setSpan(row, 0, 1, 1)  # Restoring to original span (1x1)
                    
    def setRowSpan(self, row, rowSpan, start, end):
        for i in range(start, end):
            self.view.tableView.setSpan(row, i, rowSpan, 1)
            #print(f'here -> i:{i} row:{row} rowSpan:{rowSpan}')
            
    def restoreRowSpan(self, row, col):
        current_row_span = self.view.tableView.rowSpan(row, 0)
        current_col_span = self.view.tableView.columnSpan(row, 0)
        if current_row_span > 1 or current_col_span > 1:
            self.view.tableView.setSpan(row, col, 1, 1) 
            
    def mouseRightClick(self, event):
        
        selectedItems = self.view.tableView.selectedItems()
        if (len(selectedItems) != 0):
            idItem = selectedItems[0].text()
            action = MenuAction(self)
            menu = RoundMenu(parent=self.view)
            selectedRows = self.view.tableView.selectedRows()
            if selectedItems[len(selectedItems)-2].text() == "" and len(selectedRows) == 1:
                menu.addAction(Action(FluentIcon.SHARE, 'Réintegration', triggered=lambda: self.showDialog(idItem)))
            menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered=lambda: action.confirmDel(self.view.tableView, selectedRows)))

            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
            
    def showDialog(self, idItem):
        move = self.moveModel.fetch_all(id=idItem)[0]
        material = self.model.fetch_all(id=move.material_id)[0]
        dialog = ReintMaterialDialog(material, self.view)
        dialog.countInGood.lineEdit.setText(str(move.in_good))
        dialog.countBe.spinbox.setValue(int(move.in_good))
        dialog.countBe.spinbox.setMaximum(int(move.in_good))
        dialog.countBreakdown.spinbox.setMaximum(int(move.in_good))
        dialog.gradeEdit.setText(str(move.grade))
        dialog.fullNameEdit.setText(str(move.full_name))
        dialog.contactEdit.setText(str(move.contact))
        if dialog.exec():
            inGood = dialog.countInGood.lineEdit.text()
            nInGood = str(int(material.in_good) - int(inGood))
            inStore = dialog.inStoreSpinBox.lineEdit.text()
            be = dialog.beSpinBox.lineEdit.text()
            breakdown = dialog.breakdownSpinBox.lineEdit.text()
            nBreakdown = dialog.countBreakdown.spinbox.value()
            nBe = dialog.countBe.spinbox.value()
            dateReinteg =  dialog.dateReintegEdit.text()
            state = 'EN PANNE' if nBreakdown > 0 else 'BONNE ETAT'
            self.moveModel.update_item(idItem,
                                       breakdown       = str(nBreakdown),
                                       be              = str(nBe),
                                       state_mat_integr= state,
                                       date_reinteg    = dateReinteg)
            self.model.update_item(material.id, 
                                   in_good  = nInGood,
                                   in_store = inStore,
                                   be       = be,
                                   breakdown= breakdown)
            self.view.parent.depot.emit()