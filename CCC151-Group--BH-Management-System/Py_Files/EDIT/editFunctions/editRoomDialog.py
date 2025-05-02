from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from ..EditRoom import Ui_Dialog
from PyQt5.QtCore import Qt
from DATABASE.Functions.update import update

class editRoomDialog(QDialog):
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
    def updateRoom(self):
        roomNumber = self.ui.RoomNumberLineEdit.text()
        price = self.ui.PriceLineEdit.text()
        tenantSex = self.ui.TenantSexComboBox.currentData()
        maximumAcceptedOccupants = self.ui.MaxNoOccupantsLineEdit.text()
        
        #shelfed until new PR
        
        