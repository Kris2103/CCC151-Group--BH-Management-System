from PyQt5.QtWidgets import QDialog
from ..EditTenant import Ui_Dialog
from PyQt5.QtCore import Qt

class editTenantDialog(QDialog):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.UpdatepushButton.clicked.connect(self.updateTenant)

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

            

