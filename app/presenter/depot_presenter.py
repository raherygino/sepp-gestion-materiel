from datetime import datetime
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QCursor
from ..models import Material, Mouvement
from .menu_presenter import MenuAction
from qfluentwidgets import RoundMenu, Action, FluentIcon, MenuAnimationType
from ..view import MouvementMaterielDialog
from .base_presenter import BasePresenter

class DepotPresenter(BasePresenter):
    
    def __init__(self, parent):
        self.model = parent.model
        super().__init__(self.model.fetch_all(),parent)
        self.setTableHeaderLabels(["Id", "Date", "Rubriques", "Types", "Marques", "Modele", "Nombre", 
                            "Accessoires", "Etat", "Fonctionnalité", "Motif", "Observation", ""])
        self.setTableContextMenu(self.mouseRightClick)
        
    def handleResult(self, data: list):
        super().handleResult(data)
        listData = []
        for material in data:
            listData.append(
                [material.id, material.date, material.name, 
                 material.type, material.brand, material.model,
                 material.count, material.accessory, material.state,  
                 material.fonctionality,material.motif, material.observation])
        self.view.tableView.setData(listData)
    
    def mouseRightClick(self, event):
        selectedItems = self.view.tableView.selectedItems()
        if (len(selectedItems) != 0):
            idItem = self.view.tableView.selectedItems()[0].text()
            action = MenuAction(self)
            menu = RoundMenu(parent=self.view)
            #menu.addAction(Action(FluentIcon.FOLDER, 'Voir', triggered = lambda:action.show(matricule_item)))
            menu.addAction(Action(FluentIcon.EDIT, 'Modifier', triggered = lambda: action.update(idItem)))
            menu.addAction(Action(FluentIcon.SHARE, 'Mouvement', triggered = lambda: self.showDialog(idItem)))
            menu.addSeparator()
            menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda: action.confirmDelete(idItem)))

            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
            
    def showDialog(self, selectedId):
        material : Material= self.model.fetch_item_by_id(selectedId)
        dialog = MouvementMaterielDialog(material, self.view)
        if dialog.exec():
            # Current date and time
            now = datetime.now()
            today = now.strftime("%d/%m/%Y")
            count = dialog.count.getValue()
            moveType = dialog.typeCombox.combox.text()
            
            self.moveModel.create(Mouvement(
                material_id=selectedId, 
                type=moveType,
                date=today,
                count=count))
            updatedCount = material.count + count
            if moveType == "Sortie" :
                updatedCount = material.count - count
            self.model.update_item(selectedId, count=str(updatedCount))
            self.view.parent.nParent.refresh.emit()