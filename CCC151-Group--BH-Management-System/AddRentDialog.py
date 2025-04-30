from PyQt5.QtWidgets import QDialog
from AddRent import Ui_Dialog

class AddRentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_rent)

    def handle_add_rent(self):
        move_inDate = self.ui.MoveInDateLineEdit.text()
        rStatus = self.ui.MoveStatuscomboBox.currentText()
        rNumber = self.ui.RoomNumberLineEdit.text()
        rTenantId = self.ui.RentingTenantIDLineEdit.text()

        print(f"Move-in Date: {move_inDate}")
        print(f"Status: {rStatus}")
        print(f"Room Number: {rNumber}")
        print(f"Renting Tenant ID: {rTenantId}")

        self.accept()
