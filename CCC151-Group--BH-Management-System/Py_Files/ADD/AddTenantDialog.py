from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from .AddTenant import Ui_Dialog
import re
from DATABASE.Functions import Select, Insert, update, Populate
from DATABASE.DB import DatabaseConnector
from datetime import datetime

class AddTenantDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.select = Select.Select()
        self.insert = Insert.Insert()
        self.update = update.update()
        self.populate = Populate.Populate(self)

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_tenant)

        self.populate.populate_sex_combobox(self.ui.SexComboBox)

        self.ui.SexComboBox.setCurrentIndex(-1)
        
        # Set up tenant ID field
        self.ui.TenantIDLineEdit.setText(self.generate_tenant_id())
        self.ui.TenantIDLineEdit.setReadOnly(True)  # Make it read-only since we generate it
        
        # self.ec_data = None

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

    def handle_add_tenant(self):
        tenant_fname = self.ui.FirstNameLineEdit.text()
        tenant_mname = self.ui.MiddleNameLineEdit.text()
        tenant_lname = self.ui.LastNameLineEdit.text()
        tenant_email = self.ui.EmailLineEdit.text()
        tenant_phone = self.ui.PhoneNumberLineEdit.text()
        tenant_ID = self.ui.TenantIDLineEdit.text()
        tenant_sex = self.ui.SexComboBox.currentText()

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        phone_pattern = r"^09\d{9}$"

        if not all([tenant_ID, tenant_fname, tenant_lname, tenant_email, tenant_phone, tenant_sex]):
            QMessageBox.warning(self, "Missing Input", "Please fill in all required fields.")
            return
        
        if not re.match(email_pattern, tenant_email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return

        if not re.match(phone_pattern, tenant_phone):
            QMessageBox.warning(self, "Invalid Phone Number", "Phone number must be 11 digits.")
            return
        
        try:
                
            newTen = [
                        tenant_ID,
                        tenant_email,
                        tenant_fname,
                        tenant_mname,
                        tenant_lname,
                        tenant_sex,
                        tenant_phone
                    ]
            
            self.insert.InsertQuery("Tenant", newTen)

            self.accept()
            
        except Exception as err:
            print(f"Error occurred while adding tenant: {err}")
            QMessageBox.critical(self, "Database Error", f"Failed to add tenant:\n{err}")