from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from .AddTenant import Ui_Dialog
import mysql.connector
import re

class AddTenantDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_tenant)

        self.populate_sex_combobox()
        self.populate_room_combobox()

    def populate_sex_combobox(self):
        self.ui.SexComboBox.clear()
        self.ui.SexComboBox.addItems(['Male', 'Female'])

    def populate_room_combobox(self):
        try:
            con = mysql.connector.connect(
                host="web-bedford.gl.at.ply.gg",
                user="sistoreOwner",
                password="aVerySecurePassword",
                database="SISTORE",
                port=6340
            )
            cursor = con.cursor()
            cursor.execute("SELECT RoomNumber FROM Room")
            rooms = cursor.fetchall()

            room_list = [str(room[0]) for room in rooms] # Fixed variable name

            self.ui.RoomNoComboBox.clear()
            self.ui.RoomNoComboBox.addItems(room_list)

            # Make combo box searchable
            self.ui.RoomNoComboBox.setEditable(True)
            completer = QCompleter(room_list, self.ui.RoomNoComboBox)
            completer.setCaseSensitivity(False)
            self.ui.RoomNoComboBox.setCompleter(completer)

            cursor.close()
            con.close()

        except mysql.connector.Error as err:
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
            con = mysql.connector.connect(
                host="web-bedford.gl.at.ply.gg",
                user="sistoreOwner",
                password="aVerySecurePassword",
                database="SISTORE",
                port=6340
            )
            cursor = con.cursor()

            insert_query = """
                INSERT INTO Tenant (TenantID, Email, FirstName, MiddleName, LastName, Sex, PhoneNumber, RoomNumber)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                tenant_ID,
                tenant_email,
                tenant_fname,
                tenant_mname,
                tenant_lname,
                tenant_sex,
                tenant_phone,
                int(tenant_room)
            ))

            con.commit()
            cursor.close()
            con.close()

            QMessageBox.information(self, "Success", "Tenant added successfully!")
            self.accept()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Failed to add tenant:\n{err}")