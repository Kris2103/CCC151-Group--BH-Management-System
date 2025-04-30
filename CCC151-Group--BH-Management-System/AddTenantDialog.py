from PyQt5.QtWidgets import QDialog
from AddTenant import Ui_Dialog

class AddTenantDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_tenant)

    def handle_add_tenant(self):
        tenant_fname = self.ui.FirstNameLineEdit.text()
        tenant_mname = self.ui.MiddleNameLineEdit.text()
        tenant_lname = self.ui.LastNameLineEdit.text()
        tenant_email = self.ui.EmailLineEdit.text()
        tenant_phone = self.ui.PhoneNumberLineEdit.text()
        tenant_ID = self.ui.TenantIDLineEdit.text()
        tenant_room = self.ui.RoomNoComboBox.currenttext()
        tenant_sex = self.ui.SexComboBox.currentText()

        print(f"First Name: {tenant_fname}")
        print(f"Middle Name: {tenant_mname}")
        print(f"Last Name: {tenant_lname}")
        print(f"Email: {tenant_email}")
        print(f"Phone: {tenant_phone}")
        print(f"Tenant ID:{tenant_fname}")
        print(f"Room No.:{tenant_room}")
        print(f"Sex: {tenant_sex}")

        self.accept()
