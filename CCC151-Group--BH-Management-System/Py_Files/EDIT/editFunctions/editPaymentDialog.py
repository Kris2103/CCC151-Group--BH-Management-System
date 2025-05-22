from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from PyQt5.QtCore import QDate
from ..EditPayment import Ui_Dialog
from datetime import datetime
from DATABASE.Functions import Select, update, Insert, Populate
from dateutil.relativedelta import relativedelta


class editPaymentDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.select = Select.Select()
        self.insert = Insert.Insert()
        self.updater = update.update()
        self.populate = Populate.Populate(self)
        self.PayID = 0
        self.InitialAmount = 0.0

        self.populate.populate_room_combobox(self.ui.RoomNumberComboBox)
        self.populate.populate_tenant_id_combobox(self.ui.PayingTenantIDComboBox)
        self.ui.RoomNumberComboBox.currentTextChanged.connect(lambda: self.populate.sync_tenant_id_from_room(self.ui.RoomNumberComboBox, self.ui.PayingTenantIDComboBox))
        self.ui.PayingTenantIDComboBox.currentTextChanged.connect(lambda: self.populate.sync_room_from_tenant_id(self.ui.RoomNumberComboBox, self.ui.PayingTenantIDComboBox))
        self.ui.PaymentAmountLineEdit.textChanged.connect(lambda: self.Update_RemainingDue())
        self.ui.PayingTenantIDComboBox.currentTextChanged.connect(lambda: self.Update_RemainingDue())

        self.ui.UpdatepushButton.clicked.connect(self.updatePayment)
        self.ui.CancelpushButton_3.clicked.connect(self.closeWindow)

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
            remainingDue += self.InitialAmount
            self.ui.RemainingDue.setText(f"{remainingDue:.2f}")

        except Exception as e:
            print("Error fetching remaining due:", e)
            self.ui.RemainingDue.setText("0.00")

    def closeWindow(self):
        print("Closing the Edit Pay Dialog")
        self.close()

    def updatePayment(self):
        room_number = self.ui.RoomNumberComboBox.currentText()
        tenant_id = self.ui.PayingTenantIDComboBox.currentText()
        amount = self.ui.PaymentAmountLineEdit.text()
        payment_date = self.ui.dateEdit.date()

        if not payment_date.isValid():
            QMessageBox.warning(self, "Input Error", "Invalid payment date.")
            return

        formatted_payment_date = payment_date.toString("yyyy-MM-dd")

        if not room_number or not tenant_id or not amount or not formatted_payment_date:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        try:
            editedPays = { "PayingTenant" : tenant_id,
                        "PaidRoom" : room_number,    
                        "PaymentAmount" : float(amount),
                        "PaymentDate" : formatted_payment_date    
            }        
            
            self.updater.updateTableData("Pays", editedPays, "PayID", self.PayID)

            self.populate.populate_room_combobox(self.ui.RoomNumberComboBox)
            QMessageBox.information(self, "Success", "Payment entry added successfully.")
            self.accept()
        except Exception as e:
            print("Add Payment Error:", e)
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            pass