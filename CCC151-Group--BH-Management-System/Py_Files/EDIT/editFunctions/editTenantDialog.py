from PyQt5.QtWidgets import QDialog, QMessageBox
from ..EditTenant import Ui_Dialog
from PyQt5.QtCore import Qt, QDate
from DATABASE.Functions.update import update
from DATABASE.Functions.Select import Select
from DATABASE.Functions.Insert import Insert
from .editEmergencyContactDialog import editEmergencyContactDialog

class editTenantDialog(QDialog):

    sexOptions = {
        "Male": "Male",
        "Female": "Female"
    }

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.fillSexComboBox()
        self.fillRoomNoComboBox()

        self.ui.UpdatepushButton.clicked.connect(self.updateTenant)
        self.ui.CancelpushButton.clicked.connect(self.closeWindow)

        self.ui.TenantIDLineEdit.editingFinished.connect(self.matchTenantIdToDetails)

        self.ui.TenantIDLineEdit.setFocus()
        self.previousRoomNumber = None

    def updateTenant(self):
        firstName = self.ui.FirstNameLineEdit.text()
        middleName = self.ui.MiddleNameLineEdit.text()
        lastName = self.ui.LastNameLineEdit.text()
        email = self.ui.EmailLineEdit.text()
        phoneNumber = self.ui.PhoneNumberLineEdit.text()
        roomNoText = self.ui.RoomNoComboBox.currentText().strip()
        roomNo = int(roomNoText) if roomNoText.isdigit() else None
        sex = self.ui.SexComboBox.currentData()
        tenantId = self.ui.TenantIDLineEdit.text()

        errors = []

        if not firstName:
            errors.append("First name is required.")
        if not middleName:
            errors.append("Middle name is required.")
        if not lastName:
            errors.append("Last name is required.")
        if not email:
            errors.append("Email is required.")
        if not phoneNumber:
            errors.append("Phone number is required.")
        if not sex:
            errors.append("Sex is required.")
        if not tenantId:
            errors.append("Tenant ID is required.")

        if errors:
            errorMessage = "\n".join(errors)
            print("Validation Errors:\n" + errorMessage)
            QMessageBox.critical(self, "Validation Error", errorMessage, QMessageBox.Ok)
            return

        print(f"Updating tenant with ID: {tenantId}, Name: {firstName} {middleName} {lastName}")

        updater = update()
        inserter = Insert()

        # Update tenant data
        setParameters = {
            "FirstName": firstName,
            "MiddleName": middleName,
            "LastName": lastName,
            "Email": email,
            "PhoneNumber": phoneNumber,
            "RoomNumber": roomNo,
            "Sex": sex
        }
        
        selector = Select()
        selector.SelectQuery("Room", select_type="Room", spec_col=["Occupants.Count", "Room.MaximumCapacity"], tag="RoomNumber", key=roomNo)
        occupantsCount, maximumCapacity = selector.retData()[0] 
        if occupantsCount > maximumCapacity:
            QMessageBox.warning(self, "Overloading of Room", "Maximum Occupants reached", QMessageBox.Ok)
            return
        
        addRentParameters = {
            tenantId : "RentingTenant",
            roomNo : "RentedRoom",
            QDate.currentDate().toString("yyyy-MM-dd") : "MoveInDate",
            QDate.currentDate().addMonths(1).toString("yyyy-MM-dd") : "MoveOutDate"
        }
        
        
        updater.updateTableData("Tenant", setParameters, "TenantID", tenantId)
        inserter.InsertQuery("Rents", addRentParameters)
        QMessageBox.information(self, "Update Done", "Update is successful", QMessageBox.Ok)
        self.accept()

    def closeWindow(self):
        print("Closing the Edit Tenant Dialog")
        self.reject()

    def fillSexComboBox(self):
        self.ui.SexComboBox.clear()
        for label, data in self.sexOptions.items():
            self.ui.SexComboBox.addItem(label, data)
        self.ui.SexComboBox.setCurrentIndex(-1)

    def openEditEmergencyContact(self):
        emergencyContactDialog = editEmergencyContactDialog(self)
        result = emergencyContactDialog.exec_()
        if result == QDialog.Accepted:
            print("Now editing tenant's emergency contact")

    def fillRoomNoComboBox(self):
        selector = Select()
        selector.SelectQuery(
            table="Room",
            select_type=None,
            spec_col=["Room.RoomNumber"],
            tag=None,
            key=None
        )
        roomNumbers = selector.retData()
        self.ui.RoomNoComboBox.clear()

        for room in roomNumbers:
            self.ui.RoomNoComboBox.addItem(str(room[0]))

        self.ui.RoomNoComboBox.setCurrentIndex(-1)

    def matchTenantIdToDetails(self):
        tenantId = self.ui.TenantIDLineEdit.text().strip()
        selector = Select()

        if tenantId:
            selector.SelectQuery(
                table="Tenant",
                select_type=None,
                spec_col=[
                    "Tenant.FirstName", "Tenant.MiddleName", "Tenant.LastName",
                    "Tenant.Email", "Tenant.PhoneNumber", "Tenant.RoomNumber", "Tenant.Sex"
                ],
                tag="TenantID",
                key=tenantId
            )
            resultBuilder = selector.retData()
            print(f"Query Result: {resultBuilder}")

            if resultBuilder:
                firstName, middleName, lastName, email, phone, roomNo, sex = resultBuilder[0]
                self.previousRoomNumber = roomNo

                self.ui.FirstNameLineEdit.setText(firstName)
                self.ui.MiddleNameLineEdit.setText(middleName)
                self.ui.LastNameLineEdit.setText(lastName)
                self.ui.EmailLineEdit.setText(email)
                self.ui.PhoneNumberLineEdit.setText(phone)
                self.ui.RoomNoComboBox.setCurrentText(str(roomNo))

                index = self.ui.SexComboBox.findData(sex)
                if index != -1:
                    self.ui.SexComboBox.setCurrentIndex(index)