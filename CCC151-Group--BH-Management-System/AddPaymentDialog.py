from PyQt5.QtWidgets import QDialog
from AddPayment import Ui_Dialog

class AddPaymentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.CancelpushButton.clicked.connect(self.reject)  # closes the dialog
        self.ui.AddpushButton.clicked.connect(self.handle_add_payment)

    def handle_add_payment(self):
        room_number = self.ui.RoomNumberComboBox.currentText()
        tenant_id = self.ui.PayingTenantIDComboBox.currentText()
        amount = self.ui.PaymentAmountLineEdit.text()
        date = self.ui.PaymentDateLineEdit.text()
        status = self.ui.PaymentStatusComboBox.currentText()

        print(f"Room: {room_number}, Tenant ID: {tenant_id}, Amount: {amount}, Date: {date}, Status: {status}")

        self.accept()
