from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from ..EditEmergencyContact import Ui_Dialog
from PyQt5.QtCore import Qt
from DATABASE.Functions.update import update

class editEmergencyContactDialog(QDialog):
        
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
    def updateEmergencyContact(self):
        firstName = self.ui.FirstNameLineEdit.text()
        middleName = self.ui.MibbleNameLineEdit.text()
        lastName = self.ui.LastNameLineEdit.text()
        relationship = self.ui.RelationshipLineEdit.text()
        phoneNumber = self.ui.PhoneNumberLineEdit.text()
        tenantEmId = self.ui.TenantEMIDLineEdit_2.text()
        
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
            print("Validation Erros:\n" + errorMessage)
            QMessageBox.critical(self, "Validation Error", errorMessage, QMessageBox.Ok)
            
            return
            