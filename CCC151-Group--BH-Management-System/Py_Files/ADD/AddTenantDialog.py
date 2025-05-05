from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from .AddTenant import Ui_Dialog
import re
from DATABASE.Functions import Select, Insert, update
from DATABASE.DB import DatabaseConnector

class AddTenantDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.select = Select.Select()
        self.insert = Insert.Insert()
        self.update = update.update()

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_tenant)

        self.populate_sex_combobox()
        self.populate_room_combobox()

    def populate_sex_combobox(self):
        self.ui.SexComboBox.clear()
        self.ui.SexComboBox.addItems(['Male', 'Female'])

    def populate_room_combobox(self):
        try:
            # Querying for room numbers
            rows = self.select.SelectQuery("Room", spec_col=["RoomNumber"]).retData()

            # Debugging: Print the query result
            # print(f"Rows: {rows}, Columns: {columns}")

            if not rows:
                QMessageBox.warning(self, "No Data", "No room numbers found.")
                return

            # Extract room numbers from the query result
            room_list = [str(row[0]) for row in rows]  # Assuming row[0] contains RoomNumber

            # Populate the combo box with room numbers
            self.ui.RoomNoComboBox.clear()
            self.ui.RoomNoComboBox.addItems(room_list)

            # Make combo box searchable
            self.ui.RoomNoComboBox.setEditable(True)
            completer = QCompleter(room_list, self.ui.RoomNoComboBox)
            completer.setCaseSensitivity(False)
            self.ui.RoomNoComboBox.setCompleter(completer)

        except Exception as err:
            print(f"Database Error: {err}")
            QMessageBox.critical(self, "Database Error", f"Failed to load rooms:\n{err}")
        
    def handle_add_tenant(self):
        tenant_fname = self.ui.FirstNameLineEdit.text()
        tenant_mname = self.ui.MiddleNameLineEdit.text()
        tenant_lname = self.ui.LastNameLineEdit.text()
        tenant_email = self.ui.EmailLineEdit.text()
        tenant_phone = self.ui.PhoneNumberLineEdit.text()
        tenant_ID = self.ui.TenantIDLineEdit.text()
        tenant_room = self.ui.RoomNoComboBox.currentText()
        tenant_sex = self.ui.SexComboBox.currentText()

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        phone_pattern = r"^09\d{9}$"

        if not all([tenant_fname, tenant_lname, tenant_email, tenant_phone, tenant_ID, tenant_room]):
            QMessageBox.warning(self, "Missing Input", "Please fill in all required fields.")
            return
        
        if not re.match(email_pattern, tenant_email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return

        if not re.match(phone_pattern, tenant_phone):
            QMessageBox.warning(self, "Invalid Phone Number", "Phone number must be 11 digits.")
            return

        try:
            # Create an instance of the Select class

            columns = ["MaximumCapacity", "NoOfOccupants", "TenantSex"]
            result = self.select.SelectQuery("Room", spec_col=columns, tag = "RoomNumber", key = tenant_room, limit = 1).retData()
            print(result)

            if result:
                maximum_capacity, current_occupants, room_tsex = result[0]
                if room_tsex != tenant_sex and room_tsex != None:
                    QMessageBox.warning(self, "Sex invalid", f"Room {tenant_room} only accepts {room_tsex} tenants.")
                if current_occupants >= maximum_capacity:
                    QMessageBox.warning(self, "Room Full", "The room has reached its maximum capacity.")
                    return
                
            newTen = [
                            tenant_ID,
                            tenant_email,
                            tenant_fname,
                            tenant_mname,
                            tenant_lname,
                            tenant_sex,
                            tenant_phone,
                            int(tenant_room)
                    ]
            
            self.insert.InsertQuery("Tenant", newTen)

            self.update.updateTableData("Room", {"NoOfOccupants" : (current_occupants + 1), "TenantSex" : tenant_sex}, "RoomNumber", tenant_room)

            QMessageBox.information(self, "Success", "Tenant added successfully!")
            self.accept()

        except Exception as err:
            print(f"Error occurred while adding tenant: {err}")
            QMessageBox.critical(self, "Database Error", f"Failed to add tenant:\n{err}")