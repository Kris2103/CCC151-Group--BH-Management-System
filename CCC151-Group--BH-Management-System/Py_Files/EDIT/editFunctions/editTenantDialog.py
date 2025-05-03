from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from ..EditTenant import Ui_Dialog
from PyQt5.QtCore import Qt
from DATABASE.Functions.update import update
from DATABASE.Functions.Select import Select
from .editEmergencyContactDialog import editEmergencyContactDialog

class editTenantDialog(QDialog):
    
    sexOptions = {
    "Male" : "Male",
    "Female" : "Female"
    }
            
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.fillSexComboBox()
        self.fillRoomNoComboBox()

        self.ui.UpdatepushButton.clicked.connect(self.updateTenant)
        self.ui.CancelpushButton.clicked.connect(self.closeWindow)
        self.ui.EditECpushButton.clicked.connect(self.openEditEmergencyContact)

    def updateTenant(self):

        firstName = self.ui.FirstNameLineEdit.text()
        middleName = self.ui.MibbleNameLineEdit.text()
        lastName = self.ui.LastNameLineEdit.text()
        email = self.ui.EmailLineEdit.text()
        phoneNumber = self.ui.PhoneNumberLineEdit.text()
        roomNo = self.ui.RoomNoComboBox.currentData()
        if not roomNo:  
            roomNo = None 
        sex = self.ui.SexComboBox.currentData()
        if not sex:
            sex = None

        tenantId = self.ui.TenantIDLineEdit.text()
        
        errors = []

        if not firstName:
            errors.append("First name is required.")
        if not middleName:
            errors.append("Middle name is required.")
        if not lastName:
            errors.append("Last name is required.")
        if not email:
            errors.append("Email is required.")
        if not phoneNumber:
            errors.append("Phone number is required.")
        if not roomNo:
            errors.append("Room number is required.")
        if not sex:
            errors.append("Sex is required.")
        if not tenantId:
            errors.append("Tenant ID is required.")

        if errors:
            errorMessage = "\n".join(errors)
            print("Validation Errors:\n" + errorMessage)
            QMessageBox.critical(self, "Validation Error", errorMessage, QMessageBox.Ok)
        
            return  # Skip further execution

        print(f"Updating tenant with ID: {tenantId}, Name: {firstName} {middleName} {lastName}")
        
        updater = update()
        
        setParameters = {
            "FirstName" : firstName,
            "MiddleName" : middleName,
            "LastName" : lastName,
            "Email" : email,
            "PhoneNumber" : phoneNumber,
            "RoomNumber" : roomNo,
            "Sex" : sex
        }
        
        updater.updateTableData("Tenants", setParameters, "TenantID", tenantId)
        
    def closeWindow(self):
        print("Closing the Edit Tenant Dialog")
        self.reject() 
        
    def fillSexComboBox(self):
        self.ui.SexComboBox.clear()
        
        for data, label, in self.sexOptions.items():
            self.ui.SexComboBox.addItem(label, data)
            
    def openEditEmergencyContact(self):
        emergencyContactDialog = editEmergencyContactDialog(self)
        result = emergencyContactDialog.exec_()
        if result == QDialog.accepted:
            print("Now editing tenant's emergency contact")
                    
    def fillRoomNoComboBox(self):
         selector = Select()
        
         selector.SelectQuery(table="Room", select_type=None, spec_col=["Room.RoomNumber"], tag=None, key=None)
         roomNumbers = selector.retData()
         self.ui.RoomNoComboBox.clear()
         
         for room in roomNumbers:
             self.ui.RoomNoComboBox.addItem(str(room[0]))