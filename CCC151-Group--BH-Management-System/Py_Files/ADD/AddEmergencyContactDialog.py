from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from PyQt5.QtCore import Qt
from .AddEmergencyContact import Ui_Dialog
from DATABASE.Functions import Select, Insert, Populate
from DATABASE.DB import DatabaseConnector
import re
from datetime import datetime

class AddEmergencyContactDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.select = Select.Select()
        self.insert = Insert.Insert()
        self.populate = Populate.Populate()

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_EC)

        self.ui.TenantEMIDComboBox.setEditable(True)
        self.populate.populate_tenant_id_combobox(self.ui.TenantEMIDComboBox)

        self.ui.TenantEMIDComboBox.setCurrentIndex(-1)

        contact_id = self.generate_contact_id()
        self.ui.ContactIDLineEdit.setText(contact_id)
        self.ui.ContactIDLineEdit.setReadOnly(True)

    def generate_contact_id(self):
        current_year = datetime.now().year

        try:
            result = self.select.SelectQuery(
                "EmergencyContact",
                spec_col=["MAX(ContactID)"],
                tag="ContactID",
                key=f"{current_year}-%",
                limit=1
            ).retData()

            if result and result[0][0]:
                last_id = result[0][0]
                last_num = int(last_id.split('-')[1])
                new_num = last_num + 1
            else:
                new_num = 1

            return f"{current_year}-{new_num:04d}"

        except Exception as err:
            print(f"Error generating contact ID: {err}")
            return f"{current_year}-0001"

    def handle_add_EC(self):
        ecFirst_name = self.ui.FirstNameLineEdit.text()
        ecMiddle_name = self.ui.MiddleNameLineEdit.text()
        ecLast_name = self.ui.LastNameLineEdit.text()
        relationship = self.ui.RelationshipLineEdit.text()
        contactID = self.ui.ContactIDLineEdit.text()
        tenant_EMID = self.ui.TenantEMIDComboBox.currentText()
        EC_phoneNumber = self.ui.PhoneNumberLineEdit.text()

        # Validate required fields
        if not all([ecFirst_name, ecLast_name, relationship, contactID, tenant_EMID, EC_phoneNumber]):
            QMessageBox.warning(self, "Missing Input", "Please fill in all required fields.")
            return

        # Validate phone number format (you can adjust the pattern as needed)
        phone_pattern = r"^09\d{9}$"
        if not re.match(phone_pattern, EC_phoneNumber):
            QMessageBox.warning(self, "Invalid Phone Number", "Phone number must be 11 digits starting with 09.")
            return

        try:
            
            # Execute the insert query
            newEC = [contactID, ecFirst_name, ecMiddle_name, ecLast_name, relationship, EC_phoneNumber, tenant_EMID]
            self.insert.InsertQuery("EmergencyContact", newEC)


            QMessageBox.information(self, "Success", "Emergency Contact added successfully!")
            self.accept()

        except Exception as err:
            print(f"Error occurred while adding Emergency Contact: {err}")
            QMessageBox.critical(self, "Database Error", f"Failed to add Emergency Contact:\n{err}")