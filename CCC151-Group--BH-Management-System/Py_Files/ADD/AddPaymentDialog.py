from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from .AddPayment import Ui_Dialog
from PyQt5.QtCore import QDate, QTimer
from DATABASE.Functions import Select, Insert, update, Populate

class AddPaymentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_payment)

        self.ui.dateEdit.setCalendarPopup(True)
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.dateEdit.setDisplayFormat("yyyy-MM-dd")

        self.select = Select.Select()
        self.insert = Insert.Insert()
        self.updater = update.update()
        self.populate = Populate.Populate(self)

        self.populate.populate_room_combobox(self.ui.RoomNumberComboBox)
        self.populate.populate_tenant_id_combobox(self.ui.PayingTenantIDComboBox)
        self.ui.RoomNumberComboBox.currentTextChanged.connect(lambda: self.populate.sync_tenant_id_from_room(self.ui.RoomNumberComboBox, self.ui.PayingTenantIDComboBox))
        self.ui.PayingTenantIDComboBox.currentTextChanged.connect(lambda: self.populate.sync_room_from_tenant_id(self.ui.RoomNumberComboBox, self.ui.PayingTenantIDComboBox))
        self.ui.PaymentAmountLineEdit.textChanged.connect(lambda: self.Update_RemainingDue())
        self.ui.PayingTenantIDComboBox.currentTextChanged.connect(lambda: self.Update_RemainingDue())

        self.ui.RoomNumberComboBox.setCurrentIndex(-1)
        self.ui.PayingTenantIDComboBox.setCurrentIndex(-1)

        # self.update_timer = QTimer(self)
        # self.update_timer.setSingleShot(True)
        # self.update_timer.timeout.connect(self.Update_RemainingDue)
        # self.debounce_interval = 500 # milliseconds - adjust as needed

    def Update_RemainingDue(self):
        tenant_id = self.ui.PayingTenantIDComboBox.currentText()

        if not tenant_id:
            self.ui.RemainingDue.setText("0.00")
            return

        try:
            price = float(self.ui.PaymentAmountLineEdit.text())
        except ValueError:
            price = 0.0

        try:
            remaining_due_data = self.select.SelectQuery(
                "Tenant",
                select_type="Tenant",
                spec_col=["RemainingDue.RemainingDue"],
                filters={"TenantID": tenant_id}
            ).retData()

            if remaining_due_data:
                remainingDue = float(remaining_due_data[0][0])
            else:
                remainingDue = 0.0

            remainingDue -= price
            self.ui.RemainingDue.setText(f"{remainingDue:.2f}")

        except Exception as e:
            print("Error fetching remaining due:", e)
            self.ui.RemainingDue.setText("0.00")


    # def delayed_Update_RemainingDue(self):
    #     self.update_timer.start(self.debounce_interval)
        # self.Update_RemainingDue()

    def handle_add_payment(self):
        room_number = self.ui.RoomNumberComboBox.currentText()
        tenant_id = self.ui.PayingTenantIDComboBox.currentText()
        amount = self.ui.PaymentAmountLineEdit.text()

        # Get the payment date in the correct format
        payment_date_str = self.ui.dateEdit.text()
        payment_date = QDate.fromString(payment_date_str, "yyyy-MM-dd")

        if not payment_date.isValid():
            QMessageBox.warning(self, "Input Error", "Invalid payment date.")
            return

        formatted_payment_date = payment_date.toString("yyyy-MM-dd")

        if not room_number or not tenant_id or not amount or not formatted_payment_date:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        try:
            newPays = [ tenant_id,
                        room_number,    
                        amount,
                        formatted_payment_date    
                    ]              
            
            self.insert.InsertQuery("Pays", newPays)

            self.populate.populate_room_combobox(self.ui.RoomNumberComboBox)
            QMessageBox.information(self, "Success", "Payment entry added successfully.")
            self.accept()
        except Exception as e:
            print("Add Payment Error:", e)
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            pass