from PyQt5.QtWidgets import QDialog
from AddEmergencyContact import Ui_Dialog

class AddEmergencyContactDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_EC)

    def handle_add_EC(self):
        ecFirst_name = self.ui.FirstNameLineEdit.text()
        ecMiddle_name= self.ui.MiddleNameLineEdit.text()
        ecLast_name = self.ui.LastNameLineEdit.text()
        relationship = self.ui.RelationshipLineEdit.text()
        contactID = self.ui.ContactIDLineEdit.text()
        tenant_EMID = self.ui.TenantEMIDLineEdit_2()
        EC_phoneNumber = self.ui.PhoneNumberLineEdit()

        print(f"First Name: {ecFirst_name}")
        print(f"Middle Name: {ecMiddle_name}")
        print(f"Last Name: {ecLast_name}")
        print(f"Relationship: {relationship}")
        print(f"Contact ID: {contactID}")
        print(f"TenantEM ID: {tenant_EMID}")
        print(f"Phone Number: {EC_phoneNumber}")

        self.accept()