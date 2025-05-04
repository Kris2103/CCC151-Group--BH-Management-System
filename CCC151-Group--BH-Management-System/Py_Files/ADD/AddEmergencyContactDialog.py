from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from .AddEmergencyContact import Ui_Dialog
from DATABASE.Functions.Select import Select
from DATABASE.DB import DatabaseConnector
import re

class AddEmergencyContactDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_EC)

        self.populate_tenant_id_completer()

    def populate_tenant_id_completer(self):
        try:
            select = Select()
            rows, _ = select.SelectQuery("Tenant", select_type=0, spec_col=["TenantID"])
            tenant_ids = [row[0] for row in rows]

            completer = QCompleter(tenant_ids, self)
            completer.setCaseSensitivity(False)
            completer.setFilterMode(Qt.MatchContains)
            self.ui.TenantEMIDComboBox.setCompleter(completer)

        except Exception as err:
            print(f"Completer Error: {err}")
            QMessageBox.critical(self, "Error", f"Could not load tenant IDs:\n{err}")

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
            select = Select()

            # Query to insert the emergency contact into the database
            insert_query = """
                INSERT INTO EmergencyContact (ContactID, FirstName, MiddleName, LastName, Relationship, PhoneNumber, EMTenantID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            # Execute the insert query
            select.cursor.execute(insert_query, (
                contactID,
                ecFirst_name,
                ecMiddle_name,
                ecLast_name,
                relationship,
                EC_phoneNumber,
                tenant_EMID
            ))

            # Commit the transaction
            select.conn.commit()
            select.cursor.close()

            QMessageBox.information(self, "Success", "Emergency Contact added successfully!")
            self.accept()

        except Exception as err:
            print(f"Error occurred while adding Emergency Contact: {err}")
            QMessageBox.critical(self, "Database Error", f"Failed to add Emergency Contact:\n{err}")