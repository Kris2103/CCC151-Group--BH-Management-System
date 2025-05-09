from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from PyQt5.QtCore import Qt
from .AddEmergencyContact import Ui_Dialog
from DATABASE.Functions import Select, Insert
from DATABASE.DB import DatabaseConnector
import re

class AddECEmbedDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.select = Select.Select()
        self.insert = Insert.Insert()

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_EC)

    def handle_add_EC(self):
        ecFirst_name = self.ui.FirstNameLineEdit.text()
        ecMiddle_name = self.ui.MiddleNameLineEdit.text()
        ecLast_name = self.ui.LastNameLineEdit.text()
        relationship = self.ui.RelationshipLineEdit.text()
        contactID = self.ui.ContactIDLineEdit.text()
        EC_phoneNumber = self.ui.PhoneNumberLineEdit.text()

        # Validate required fields
        if not all([ecFirst_name, ecLast_name, relationship, contactID, EC_phoneNumber]):
            QMessageBox.warning(self, "Missing Input", "Please fill in all required fields.")
            return

        # Validate phone number format (you can adjust the pattern as needed)
        phone_pattern = r"^09\d{9}$"
        if not re.match(phone_pattern, EC_phoneNumber):
            QMessageBox.warning(self, "Invalid Phone Number", "Phone number must be 11 digits starting with 09.")
            return

        try:
            
            # Execute the insert query
            newEC = [contactID, ecFirst_name, ecMiddle_name, ecLast_name, relationship, EC_phoneNumber]
            self.insert.InsertQuery("EmergencyContact", newEC)


            QMessageBox.information(self, "Success", "Emergency Contact added successfully!")
            self.accept()

        except Exception as err:
            print(f"Error occurred while adding Emergency Contact: {err}")
            QMessageBox.critical(self, "Database Error", f"Failed to add Emergency Contact:\n{err}")