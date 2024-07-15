from ..models import MaterialModel, MouvementModel
from qfluentwidgets import MessageDialog

class MenuAction:
    
    def __init__(self, presenter) -> None:
        self.presenter = presenter
        self.view = presenter.view
        self.model: MaterialModel= self.presenter.model
        self.moveModel: MouvementModel= self.presenter.moveModel
        
    def update(self, item):
        print(item)
        
    def confirmDelete(self, table, selectedRow):
        dialog = MessageDialog('Supprimer', 'Voulez vous le supprimer vraiment?', self.view.parent)
        dialog.yesButton.clicked.connect(lambda: self.delete(table, selectedRow))
        dialog.exec_()
        
    def delete(self, table, selectedRows):
        for row in selectedRows:
            itemId = table.item(row,0).text()
            self.model.delete_item(itemId)
            self.moveModel.delete_by(material_id=itemId)
        self.presenter.refresh.emit()
        
    def confirmDel(self, table, selectedRow):
        dialog = MessageDialog('Supprimer', 'Voulez vous le supprimer vraiment?', self.view.parent)
        dialog.yesButton.clicked.connect(lambda: self.deleteMove(table, selectedRow))
        dialog.exec_()
        
    def deleteMove(self, table, items: set):
        for item in items:
            itemId = table.item(item,0).text()
            move = self.moveModel.fetch_all(id=itemId)[0]
            material = self.model.fetch_all(id=move.material_id)[0]
            inGood = int(material.in_good)
            inStore = material.in_store
            be = material.be
            breakdown = material.breakdown
            if move.state_mat_integr == 'EN PANNE':
                breakdown = int(material.breakdown) - int(move.breakdown)
                be = int(material.be) + int(move.breakdown)
            elif move.state_mat_integr == 'BONNE ETAT':
                pass
            else:
                inStore = int(material.in_store)+ int(move.in_good)
                inGood = int(material.in_good) - int(move.in_good)
                be = int(material.be) + int(move.in_good)
            self.model.update_item(material.id, 
                                   in_good   = str(inGood),
                                   in_store  = str(inStore),
                                   be        = str(be),
                                   breakdown = str(breakdown))
            self.moveModel.delete_item(itemId)
        self.presenter.refresh.emit()
        