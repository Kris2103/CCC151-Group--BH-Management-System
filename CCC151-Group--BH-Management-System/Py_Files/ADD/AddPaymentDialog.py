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
        # self.populate_paymentstatus_combobox()
        self.ui.RoomNumberComboBox.currentTextChanged.connect(lambda: self.populate.sync_tenant_id_from_room(self.ui.RoomNumberComboBox, self.ui.PayingTenantIDComboBox))
        self.ui.PayingTenantIDComboBox.currentTextChanged.connect(lambda: self.populate.sync_room_from_tenant_id(self.ui.RoomNumberComboBox, self.ui.PayingTenantIDComboBox))
        # self.ui.PaymentAmountLineEdit.textChanged.connect(self.delayed_update_payment_status) # Use delayed function
        # self.ui.PaymentStatusComboBox.currentTextChanged.connect(self.delayed_update_payment_status) # Use delayed function
        self.ui.RemainingDueLabel.currentTextChanged.connect(lambda: self.delayed_Update_RemainingDue())

        self.ui.RoomNumberComboBox.setCurrentIndex(-1)
        self.ui.PayingTenantIDComboBox.setCurrentIndex(-1)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_payment_status)
        self.debounce_interval = 500 # milliseconds - adjust as needed

    def Update_RemainingDue(self):
        tenant_id = self.ui.PayingTenantIDComboBox.currentText()
        remainingDue = str(self.select.SelectQuery("Pays", select_type = "Pays", spec_col = ["RemainingDue"], filter = {"PayingTenant" : tenant_id}).retData())

        self.ui.RemainingDue.setText(remainingDue)

    def delayed_Update_RemainingDue(self):
        self.update_timer.start(self.debounce_interval)
        self.Update_RemainingDue()

    # def populate_room_combobox(self):
    #     self.ui.RoomNumberComboBox.clear()
    #     self.select.SelectQuery(table="Room", spec_col=["RoomNumber"])
    #     rooms = [str(row[0]) for row in self.select.retData()]
    #     self.ui.RoomNumberComboBox.addItems(rooms)

    #     self.ui.RoomNumberComboBox.setEditable(True)
    #     completer = QCompleter(rooms)
    #     completer.setCaseSensitivity(False)
    #     self.ui.RoomNumberComboBox.setCompleter(completer)

    # def populate_tenant_id_combobox(self, room_number):
    #     self.ui.PayingTenantIDComboBox.clear()
    #     self.select.SelectQuery(table="Tenant", spec_col=["TenantID"], tag="RoomNumber", key=room_number)
    #     tenant_ids = [str(row[0]) for row in self.select.retData()]
    #     if tenant_ids:  # If there are tenants, populate the combo box
    #         self.ui.PayingTenantIDComboBox.addItems(tenant_ids)

    #     self.ui.PayingTenantIDComboBox.setEditable(True)
    #     completer = QCompleter(tenant_ids)
    #     completer.setCaseSensitivity(False)
    #     self.ui.PayingTenantIDComboBox.setCompleter(completer)

    # def sync_tenant_id_from_room(self):
    #     # Sync the tenant ID when a room is selected.
    #     room_number = self.ui.RoomNumberComboBox.currentText()
    #     if room_number:
    #         self.populate_tenant_id_combobox(room_number)
    #         #self.ui.PayingTenantIDComboBox.setCurrentIndex(-1)

    # def sync_room_from_tenant_id(self):
    #     # Sync the room number when a tenant is selected.
    #     tenant_id = self.ui.PayingTenantIDComboBox.currentText()
    #     if tenant_id:
    #         self.select.SelectQuery(table="Tenant", spec_col=["RoomNumber"], tag="TenantID", key=tenant_id)
    #         result = self.select.retData()
    #         if result:
    #             room_number = str(result[0])
    #             index = self.ui.RoomNumberComboBox.findText(room_number)
    #             if index != -1:
    #                 self.ui.RoomNumberComboBox.setCurrentIndex(index)

    # def update_payment_status(self): # This method will update the payment status based on payment amount and date,
    #     self.update_timer.stop() # Stop any pending timers
    #     try:
    #         amount = float(self.ui.PaymentAmountLineEdit.text())
    #     except ValueError:
    #         amount = 0

    #     tenant_id = self.ui.PayingTenantIDComboBox.currentText()
    #     room_number = self.ui.RoomNumberComboBox.currentText()

    #     # Fetch the monthly price of the selected room
    #     self.select.SelectQuery(table="Room", spec_col=["Price"], tag="RoomNumber", key=room_number)
    #     room_data = self.select.retData()

    #     if room_data and len(room_data) > 0 and room_data[0][0] is not None:
    #         monthly_price = room_data[0][0]

    #         # Automatically update status based on the payment amount relative to the monthly price
    #         if amount >= monthly_price:
    #             if self.ui.PaymentStatusComboBox.currentText() != "Paid":
    #                 self.ui.PaymentStatusComboBox.setCurrentText('Paid')
    #         else:
    #             if self.ui.PaymentStatusComboBox.currentText() != "Pending":
    #                 self.ui.PaymentStatusComboBox.setCurrentText('Pending')

    #         # Check for overdue status based on the rent start date (still relevant)
    #         self.select.SelectQuery(table="Rents", spec_col=["MoveInDate"], tag="RentedRoom", key=room_number, limit=1) # Assuming one rent record per tenant-room
    #         rent_data = self.select.retData()

    #         if rent_data and len(rent_data) > 0 and rent_data[0][0] is not None:
    #             move_in_date = rent_data[0][0]
    #             payment_date_str = self.ui.dateEdit.text()
    #             payment_date = QDate.fromString(payment_date_str, "yyyy-MM-dd")

    #             # Calculate the expected payment date (one month after move-in)
    #             expected_payment_date = QDate(move_in_date.year, move_in_date.month, move_in_date.day).addMonths(1)

    #             # Check if the payment date is after the expected payment date AND the payment is less than the monthly rent
    #             if payment_date > expected_payment_date and amount < monthly_price:
    #                 if self.ui.PaymentStatusComboBox.currentText() != "Overdue":
    #                     self.ui.PaymentStatusComboBox.setCurrentText('Overdue')
    #             elif payment_date <= expected_payment_date and amount >= monthly_price:
    #                 if self.ui.PaymentStatusComboBox.currentText() != "Paid":
    #                     self.ui.PaymentStatusComboBox.setCurrentText('Paid')
    #             elif payment_date <= expected_payment_date and amount < monthly_price:
    #                 if self.ui.PaymentStatusComboBox.currentText() != "Pending":
    #                     self.ui.PaymentStatusComboBox.setCurrentText('Pending')
    #             elif payment_date > expected_payment_date and amount >= monthly_price:
    #                 if self.ui.PaymentStatusComboBox.currentText() != "Paid":
    #                     self.ui.PaymentStatusComboBox.setCurrentText('Paid')
    #         else:
    #             print(f"Warning: Could not fetch rent start date for room number: {room_number}, tenant: {tenant_id}")
    #     else:
    #         print(f"Warning: Could not fetch monthly room price for room number: {room_number}")

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

        # status = self.ui.PaymentStatusComboBox.currentText()

        if not room_number or not tenant_id or not amount or not formatted_payment_date:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        try:
            # --- TEMPORARY DEBUGGING CODE ---
            # print("Checking table structure before insert...")
            # self.select.cursor.execute("DESCRIBE Pays;")
            # columns = self.select.cursor.fetchall()
            # for col in columns:
            #     print(col[0])
            # print("--- END DEBUGGING CODE ---")

            # Insert payment record into the Pays table
            # insert_query = """
            #     INSERT INTO Pays (PaymentDate, PaymentAmount, PaymentStatus, PaidRoom, PayingTenant)
            #     VALUES (%s, %s, %s, %s, %s)
            # """
            # self.select.cursor.execute(insert_query, (formatted_payment_date, amount, room_number, tenant_id))
            # self.select.conn.commit()

            newPays = [ tenant_id,
                        room_number,    
                        amount,
                        formatted_payment_date    
                    ]              
            
            self.insert.InsertQuery("Pays", newPays)

            # Potentially update the PaymentStatus in the Room table (consider if this is always tied to the latest payment)
            # if status == "Paid":
            #     update_status_query = """
            #         UPDATE Room
            #         SET PaymentStatus = 'Paid'
            #         WHERE RoomNumber = %s
            #     """
            #     self.select.cursor.execute(update_status_query, (room_number,))
            #     self.select.conn.commit()
            # elif status == "Pending" or status == "Overdue":
            #     update_status_query = """
            #         UPDATE Room
            #         SET PaymentStatus = %s
            #         WHERE RoomNumber = %s
            #     """
            #     self.select.cursor.execute(update_status_query, (status, room_number,))
            #     self.select.conn.commit()

            self.populate.populate_room_combobox(self.ui.RoomNumberComboBox)
            QMessageBox.information(self, "Success", "Payment entry added successfully.")
            self.accept()
        except Exception as e:
            print("Add Payment Error:", e)
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            pass