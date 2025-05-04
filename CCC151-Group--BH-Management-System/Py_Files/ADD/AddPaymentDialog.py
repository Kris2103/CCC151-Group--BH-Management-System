from PyQt5.QtWidgets import QDialog, QMessageBox
from .AddPayment import Ui_Dialog
from PyQt5.QtCore import QDate
from DATABASE.Functions.Select import Select

class AddPaymentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_payment)

        self.ui.dateEdit.setCalendarPopup(True)
        self.ui.dateEdit.setDate(QDate.currentDate())

        self.select = Select()

        self.populate_room_combobox()
        self.populate_paymentstatus_combobox()  
        self.ui.RoomNumberComboBox.currentTextChanged.connect(self.sync_tenant_id_from_room)
        self.ui.PayingTenantIDComboBox.currentTextChanged.connect(self.sync_room_from_tenant_id)
        self.ui.PaymentAmountLineEdit.textChanged.connect(self.update_payment_status)
        self.ui.PaymentStatusComboBox.currentTextChanged.connect(self.update_payment_status)

    def populate_paymentstatus_combobox(self):
        self.ui.PaymentStatusComboBox.clear()  # Clear existing items
        self.ui.PaymentStatusComboBox.addItems(['Paid', 'Pending', 'Overdue'])
        self.ui.PaymentStatusComboBox.setCurrentIndex(0)

    def populate_room_combobox(self):
        self.ui.RoomNumberComboBox.clear()
        query = "SELECT DISTINCT RoomNumber FROM Room"
        self.select.cursor.execute(query)
        rooms = [str(row[0]) for row in self.select.cursor.fetchall()]
        self.ui.RoomNumberComboBox.addItems(rooms)

    def populate_tenant_id_combobox(self, room_number):
        self.ui.PayingTenantIDComboBox.clear()
        query = "SELECT TenantID FROM Tenant WHERE RoomNumber = %s"
        self.select.cursor.execute(query, (room_number,))
        tenant_ids = [str(row[0]) for row in self.select.cursor.fetchall()]
        self.ui.PayingTenantIDComboBox.addItems(tenant_ids)

    def sync_tenant_id_from_room(self):
        # Sync the tenant ID when a room is selected.
        room_number = self.ui.RoomNumberComboBox.currentText()
        if room_number:
            self.populate_tenant_id_combobox(room_number)

    def sync_room_from_tenant_id(self):
        # Sync the room number when a tenant is selected.
        tenant_id = self.ui.PayingTenantIDComboBox.currentText()
        if tenant_id:
            query = "SELECT RoomNumber FROM Tenant WHERE TenantID = %s"
            self.select.cursor.execute(query, (tenant_id,))
            result = self.select.cursor.fetchone()
            if result:
                room_number = str(result[0])
                index = self.ui.RoomNumberComboBox.findText(room_number)
                if index != -1:
                    self.ui.RoomNumberComboBox.setCurrentIndex(index)

    def update_payment_status(self): # This method will update the payment status based on payment amount and date, 
        try:
            amount = float(self.ui.PaymentAmountLineEdit.text())
        except ValueError:
            amount = 0

        tenant_id = self.ui.PayingTenantIDComboBox.currentText()
        room_number = self.ui.RoomNumberComboBox.currentText()

        # Fetch the price of the selected room
        room_price_query = "SELECT Price FROM Room WHERE RoomNumber = %s"
        self.select.cursor.execute(room_price_query, (room_number,))
        room_data = self.select.cursor.fetchone()

        if room_data:
            room_price = room_data[0]

            # Automatically update status based on the payment amount
            if amount >= room_price:
                if self.ui.PaymentStatusComboBox.currentText() != "Paid":
                    self.ui.PaymentStatusComboBox.setCurrentText('Paid')
            else:
                if self.ui.PaymentStatusComboBox.currentText() != "Pending":
                    self.ui.PaymentStatusComboBox.setCurrentText('Pending')

            # Check for overdue status based on the rent start date
            rent_query = "SELECT MoveInDate FROM Rents WHERE RentedRoom = %s AND RentingTenant = %s"
            self.select.cursor.execute(rent_query, (room_number, tenant_id))
            rent_data = self.select.cursor.fetchone()

            if rent_data:
                # Convert the datetime.date object to a string in the format "yyyy-MM-dd"
                move_in_date_str = rent_data[0].strftime("%Y-%m-%d")
                move_in_date = QDate.fromString(move_in_date_str, "yyyy-MM-dd") 

                # Get the payment date from the dateEdit widget
                payment_date_str = self.ui.dateEdit.text()
                payment_date = QDate.fromString(payment_date_str, "yyyy-MM-dd")

                # Check if the move-in date is overdue and set status to 'Overdue'
                if move_in_date.addMonths(1) < payment_date:
                    if self.ui.PaymentStatusComboBox.currentText() != "Overdue":
                        self.ui.PaymentStatusComboBox.setCurrentText('Overdue')

    def handle_add_payment(self):
        room_number = self.ui.RoomNumberComboBox.currentText()
        tenant_id = self.ui.PayingTenantIDComboBox.currentText()
        amount = self.ui.PaymentAmountLineEdit.text()
        
        # Get the payment date in the correct format
        payment_date_str = self.ui.dateEdit.text()
        payment_date = QDate.fromString(payment_date_str, "yyyy-MM-dd")

        if not payment_date.isValid():
            QMessageBox.warning(self, "Input Error", "Invalid payment date format.")
            return

        formatted_payment_date = payment_date.toString("yyyy-MM-dd")

        
        status = self.ui.PaymentStatusComboBox.currentText()

        if not room_number or not tenant_id or not amount or not formatted_payment_date:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        try:
            # Insert payment record into the Payments table
            insert_query = """
                INSERT INTO Pays (PaymentDate, PaymentAmount, PaymentStatus, PaidRoom, PayingTenant)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.select.cursor.execute(insert_query, (formatted_payment_date, amount, status, room_number, tenant_id))

            # Update the PaymentStatus in the Room table
            if status == "Paid":
                update_status_query = """
                    UPDATE Room
                    SET PaymentStatus = 'Paid'
                    WHERE RoomNumber = %s
                """
                self.select.cursor.execute(update_status_query, (room_number,))

            self.select.conn.commit()

            # Repopulate the combo boxes and reset the form
            self.populate_room_combobox()
            self.ui.PayingTenantIDComboBox.setCurrentIndex(0)
            self.ui.RoomNumberComboBox.setCurrentIndex(0)

            QMessageBox.information(self, "Success", "Payment entry added successfully.")
            self.accept()
        except Exception as e:
            print("Add Payment Error:", e)
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            self.select.cursor.close()
