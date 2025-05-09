from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from ..EditEmergencyContact import Ui_Dialog
from PyQt5.QtCore import Qt
from DATABASE.Functions.update import update
from DATABASE.Functions.Select import Select

class editEmergencyContactDialog(QDialog):
        
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.fillTenantEmId()
        
        self.ui.UpdatepushButton.clicked.connect(self.updateEmergencyContact)
        self.ui.CancelpushButton.clicked.connect(self.closeWindow)
        
    def updateEmergencyContact(self):
        firstName = self.ui.FirstNameLineEdit.text()
        middleName = self.ui.MibbleNameLineEdit.text()
        lastName = self.ui.LastNameLineEdit.text()
        relationship = self.ui.RelationshipLineEdit.text()
        phoneNumber = self.ui.PhoneNumberLineEdit.text()
        tenantEmId = self.ui.TenantEMIDComboBox.currentText()
        
        contactId = self.ui.ContactIDLineEdit.text()
        
        errors = []
        
        if not firstName:
            errors.append("First name is required.")
        if not middleName:
            errors.append("Middle name is required.")
        if not lastName:
            errors.append("Last name is required.")
        if not relationship:
            errors.append("Relationship with the Tenant is required.")
        if not phoneNumber:
            errors.append("Phone number is required.")
        if not tenantEmId:
            errors.append("Tenant Emergency ID is required.")
        if not contactId:
            errors.append("Emergency Contact ID is required.")
            
        if errors:
            errorMessage = "\n".join(errors)
            print("Validation Errors:\n" + errorMessage)
            QMessageBox.critical(self, "Validation Error", errorMessage, QMessageBox.Ok)
            
            return
        print(f"Updating emergency contact with ID: {tenantEmId}, Name {firstName} {middleName} {lastName}")
        
        updater = update()
        
        setParameters = {
            "FirstName" : firstName,
            "MiddleName" : middleName,
            "LastName" : lastName,
            "Relationship" : relationship,
            "PhoneNumber" : phoneNumber,
            "EMTenantID" : contactId
        }
        
        updater.updateTableData("EmergencyContact", setParameters, contactId)
        
    def closeWindow(self):
        print("Closing the Edit Emergency Contact Dialog")
        self.reject()
        
    def fillTenantEmId(self):
        self.ui.TenantEMIDComboBox.clear()
        selector = Select()
        selector.SelectQuery(table="Tenant", select_type=None, spec_col=["Tenant.TenantID"])
        
        resultBuilder = selector.retDict()
        for row in resultBuilder:
            roomNumber = next(iter(row.values()))
            self.ui.TenantEMIDComboBox.addItem(str(roomNumber))
        
        self.ui.TenantEMIDComboBox.setCurrentIndex(-1)
        