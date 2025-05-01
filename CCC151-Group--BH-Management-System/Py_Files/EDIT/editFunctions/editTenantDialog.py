from PyQt5.QtWidgets import QDialog
from ..EditTenant import Ui_Dialog
from PyQt5.QtCore import Qt
from DATABASE.Functions.update import update

class editTenantDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.UpdatepushButton.clicked.connect(self.updateTenant)
        self.ui.CancelpushButton.clicked.connect(self.closeWindow)

    def updateTenant(self):

        firstName = self.ui.FirstNameLineEdit.text()
        middleName = self.ui.MiddleNameLineEdit.text()
        lastName = self.ui.LastNameLineEdit.text()
        email = self.ui.EmailLineEdit.text()
        phoneNumber = self.ui.PhoneNumberLineEdit.text()
        roomNo = self.ui.RoomNoComboBox.text()
        sex = self.ui.SexComboBox.text()

        tenantId = self.ui.TenantIDLineEdit.text()

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
        print("Closing the Dialog")
        self.reject()