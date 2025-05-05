from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from ..EditRent import Ui_Dialog
from datetime import datetime
from DATABASE.Functions.update import update
from DATABASE.Functions.Select import Select

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

        
        self.fillRentingTenantID()
        self.fillRoomNumber()
        
        self.ui.RentingTenantIDComboBox.currentTextChanged.connect(self.matchTenantIDToRoomNumber)
        
    def updateRent(self):
        moveInDateData = self.ui.MoveInDateLineEdit.date().toString("yyyy-MM-dd")
        moveOutDateData = self.ui.MoveInDateLineEdit_2.date().toString("yyyy-MM-dd")
        
        try:
            moveInDate = datetime.strptime(moveInDateData, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Validation Error", "Move-in date is not in a valid format.", QMessageBox.Ok)
            return
            
        roomNumber = self.ui.RoomNumberComboBox.currentText()
        
        try:
            moveOutDate = datetime.strptime(moveOutDateData, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Validation Error", "Move-out date is not in a valid format.", QMessageBox.Ok)
            return
        
        rentingTenant = self.ui.RentingTenantIDComboBox.currentText()
        status = str(self.ui.MoveStatuscomboBox.currentData())
        
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
            "RentedRoom" : roomNumber,
            "MoveStatus" : status
        }
        
        updater.updateTableData("Rents", setParameters, "RentingTenant", rentingTenant)
        
    def closeWindow(self):
        print("Closing the Edit Rent Dialog")
        self.reject()
        
    def fillRentStatusComboBox(self):
        self.ui.MoveStatuscomboBox.clear()
        
        for label, data in self.statusOptions.items():
            self.ui.MoveStatuscomboBox.addItem(label, data)
        
    def fillRentingTenantID(self):
        self.ui.RentingTenantIDComboBox.clear()
        
        selector = Select()
        
        selector.SelectQuery(table="Rents", select_type=None, spec_col=["Rents.RentingTenant"])
        resultBuilder = selector.retDict()
        print(f"Query Result: {resultBuilder}")
        
        for row in resultBuilder:
            tenantID = next(iter(row.values()))
            self.ui.RentingTenantIDComboBox.addItem(str(tenantID))
            
    def fillRoomNumber(self):
        self.ui.RoomNumberComboBox.clear()
        
        selector = Select()
        
        selector.SelectQuery(table="Rents", select_type=None, spec_col=["Rents.RentedRoom"])
        resultBuilder = selector.retDict()
        print(f"Query Result: {resultBuilder}")
        
        for row in resultBuilder:
            roomNumber = next(iter(row.values()))
            self.ui.RoomNumberComboBox.addItem(str(roomNumber))
            
    def matchTenantIDToRoomNumber(self):
        tenantID = self.ui.RentingTenantIDComboBox.currentText()
        
        if tenantID:
            selector = Select()
            
            selector.SelectQuery(table="Rents", select_type=None, spec_col=["Rents.RentedRoom", "Rents.MovedInDate"], tag="RentingTenant", key=tenantID)
            resultBuilder = selector.retData()
            print(f"Query Result: {resultBuilder}")
            
            if resultBuilder:
                roomNumber = resultBuilder[0][0]
                self.ui.RoomNumberComboBox.setCurrentText(str(roomNumber))
                
    #def matchTenantIDToMoveInDate(self):
        
