from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from ..EditRent import Ui_Dialog
from PyQt5.QtCore import Qt
from DATABASE.Functions.update import update

class editRentDialog(QDialog):
    
    statusOptions = {
        "Active Tenant" : "Active",
        "Tenant Moved Out" : "Moved Out"
    }
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.fillRentStatusComboBox()
        
        self.ui.UpdatepushButton.clicked.connect(self.updateRent)
        self.ui.CancelpushButton.clicked.connect(self.closeWindow)
        
    def updateRent(self):
        moveInDate = self.ui.MoveInDateLineEdit.text()
        roomNumber = self.ui.RoomNumberLineEdit.text()
        moveOutDate = self.ui.MoveInDateLineEdit_2 #can be null
        if not moveOutDate:
            moveOutDate = ""
        status = self.ui.MoveStatuscomboBox.currentData()
        if not status:
            status = None
        
        rentingTenant = self.ui.RentingTenantIDLineEdit.text()
        
        errors = []
        
        if not moveInDate:
            errors.append("Move in date is required.")
        if not roomNumber:
            errors.append("Room number is required.")
        if not status:
            errors.append("Rent status can not be null")
        if not rentingTenant:
            errors.append("Please provide the tenant's ID")
            
        if errors:
            errorMessage = "\n".join(errors)
            print("Validation Errors:\n" + errorMessage)
            QMessageBox.critical(self, "Validation Error", errorMessage, QMessageBox.Ok)
            
            return
        
        print(f"Updating rent details with ID: {rentingTenant}")
        
        updater = update()
        
        setParameters = {
            "MoveInDate" : moveInDate,
            "MoveOutDate" : moveOutDate,
            "roomNumber" : roomNumber,
            "MoveStatus" : status
        }
        
        updater.updateTableData("Rents", setParameters, rentingTenant)
        
    def closeWindow(self):
        print("Closing the Edit Rent Dialog")
        self.reject()
        
    def fillRentStatusComboBox(self):
        self.ui.MoveStatuscomboBox.clear()
        
        for data, label, in self.statusOptions.items():
            self.ui.MoveStatuscomboBox.addItem(data, label)