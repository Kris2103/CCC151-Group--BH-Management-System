from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from .AddTenant import Ui_Dialog
import re
from DATABASE.Functions import Select, Insert, update, Populate
from DATABASE.DB import DatabaseConnector
from .AddECEmbedDialog import AddECEmbedDialog
from datetime import datetime

class AddTenantDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.select = Select.Select()
        self.insert = Insert.Insert()
        self.update = update.update()
        self.populate = Populate.Populate()

        self.ui.AddECpushButton.clicked.connect(self.show_ec_dialog)
        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_tenant)

        self.populate.populate_sex_combobox(self.ui.SexComboBox)
        self.populate.populate_room_combobox(self.ui.RoomNoComboBox)
        
        # Set up tenant ID field
        self.ui.TenantIDLineEdit.setText(self.generate_tenant_id())
        self.ui.TenantIDLineEdit.setReadOnly(True)  # Make it read-only since we generate it
        
        self.ec_data = None

    def generate_tenant_id(self):
        # Get the current year
        current_year = datetime.now().year
        
        # Query the database for the highest tenant ID for the current year
        try:
            result = self.select.SelectQuery(
                "Tenant",
                spec_col=["MAX(TenantID)"],
                tag="TenantID",
                key=f"{current_year}-%",
                limit=1
            ).retData()
            
            if result and result[0][0]:
                # Extract the number part and increment it
                last_id = result[0][0]
                last_num = int(last_id.split('-')[1])
                new_num = last_num + 1
            else:
                # If no existing IDs for this year, start with 1
                new_num = 1
                
            # Format the new ID: YYYY-XXXX
            return f"{current_year}-{new_num:04d}"
            
        except Exception as err:
            print(f"Error generating tenant ID: {err}")
            # Fallback to a simple format if there's an error
            return f"{current_year}-0001"

    def show_ec_dialog(self):
        # Open the embedded emergency contact dialog
        self.ec_dialog = AddECEmbedDialog(self)
        if self.ec_dialog.exec_() == QDialog.Accepted:  # Only proceed if dialog is accepted
            ec_ui = self.ec_dialog.ui
            self.ec_data = {
                "first_name": ec_ui.FirstNameLineEdit.text(),
                "last_name": ec_ui.LastNameLineEdit.text(),
                "relationship": ec_ui.RelationshipLineEdit.text(),
                "phone": ec_ui.PhoneNumberLineEdit.text()
            }

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

        if not self.ec_data:  # Check if emergency contact data is available
            QMessageBox.warning(self, "Missing Emergency Contact Info", "Please add emergency contact info.")
            return
        
        ec_first_name = self.ec_data["first_name"]
        ec_last_name = self.ec_data["last_name"]
        ec_relationship = self.ec_data["relationship"]
        ec_phone = self.ec_data["phone"]

        if not re.match(phone_pattern, ec_phone):
            QMessageBox.warning(self, "Invalid Emergency Contact Phone", "Emergency contact phone number must be 11 digits.")
            return
        
        try:

            columns = ["MaximumCapacity", "NoOfOccupants", "TenantSex"]
            result = self.select.SelectQuery("Room", spec_col=columns, tag = "RoomNumber", key = tenant_room, limit = 1).retData()

            if result:
                maximum_capacity, current_occupants, room_tsex = result[0]
                if room_tsex != tenant_sex and room_tsex != None:
                    QMessageBox.warning(self, "Sex invalid", f"Room {tenant_room} only accepts {room_tsex} tenants.")
                if current_occupants >= maximum_capacity:
                    QMessageBox.warning(self, "Room Full", f"Room {tenant_room} has reached its maximum capacity of {current_occupants}/{maximum_capacity}.")
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
            
            # Insert Emergency Contact
            new_emergency_contact = [
                tenant_ID,
                ec_first_name,
                ec_last_name,
                ec_relationship,
                ec_phone
        ]
            self.insert.InsertQuery("EmergencyContact", new_emergency_contact)

            QMessageBox.information(self, "Success", f"Tenant added successfully!\nRoom {tenant_room} is now {current_occupants + 1}/{maximum_capacity}")
            self.accept()
            
        except Exception as err:
            print(f"Error occurred while adding tenant: {err}")
            QMessageBox.critical(self, "Database Error", f"Failed to add tenant:\n{err}")