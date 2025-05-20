from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from PyQt5.QtCore import QDate
from ..EditRent import Ui_Dialog
from datetime import datetime
from DATABASE.Functions import Select, update, Insert, Populate
from dateutil.relativedelta import relativedelta


class editRentDialog(QDialog):

    statusOptions = {
        "Active Tenant": "Active",
        "Tenant Moved Out": "Moved Out"
    }

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.MoveInDateEdit.setCalendarPopup(True)
        self.ui.MoveOutDateEdit.setCalendarPopup(True)
        self.ui.MoveInDateEdit.setDate(QDate.currentDate())
        self.ui.MoveOutDateEdit.setDate(QDate.currentDate().addMonths(1))


        self.select = Select.Select()
        self.insert = Insert.Insert()
        self.updater = update.update()
        self.populate = Populate.Populate(self)

        self.roomChanged = False
        self.previousRoomNumber = None

        try:
            self.fillRentStatusComboBox()
            self.fillRentingTenantID()
            self.fillRoomNumber()
        except Exception as e:
            print("Error occurred while filling the combo boxes:", e)
            QMessageBox.critical(self, "Warning", "You currently have no rent data to edit", QMessageBox.Ok)

        self.ui.UpdatepushButton.clicked.connect(self.updateRent)
        self.ui.CancelpushButton.clicked.connect(self.closeWindow)

        self.ui.RentingTenantIDComboBox.currentTextChanged.connect(self.matchTenantIDToDetails)
        self.ui.RoomNumberComboBox.currentTextChanged.connect(self.onRoomNumberChanged)

        # self.ui.RoomNoComboBox.currentTextChanged.connect(lambda: self.populate.sync_tenant_id_from_room(self.ui.RoomNoComboBox, self.ui.RentingTenantIDComboBox))
        # self.ui.RentingTenantIDComboBox.currentTextChanged.connect(lambda: self.populate.sync_room_from_tenant_id(self.ui.RoomNoComboBox, self.ui.RentingTenantIDComboBox))

        self.matchTenantIDToDetails()

    def updateRent(self):
        moveInDateData = self.ui.MoveInDateEdit.date().toString("yyyy-MM-dd")
        moveOutDateData = self.ui.MoveOutDateEdit.date().toString("yyyy-MM-dd")

        try:
            moveInDate = datetime.strptime(moveInDateData, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Validation Error", "Move-in date is not in a valid format.", QMessageBox.Ok)
            return

        roomNumber = self.ui.RoomNumberComboBox.currentText()

        try:
            moveOutDate = datetime.strptime(moveOutDateData, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Validation Error", "Move-out date is not in a valid format.", QMessageBox.Ok)
            return

        moveInDateObj = datetime.strptime(moveInDate, "%Y-%m-%d")
        moveOutDateObj = datetime.strptime(moveOutDate, "%Y-%m-%d")

        rentingTenant = self.ui.RentingTenantIDComboBox.currentText()
        status = str(self.ui.MoveStatuscomboBox.currentData())

        errors = []

        if not moveInDate:
            errors.append("Move in date is required.")
        if not roomNumber:
            errors.append("Room number is required.")
        if not status:
            errors.append("Rent status can not be null")
        if not rentingTenant:
            errors.append("Please provide the tenant's ID")
        if moveOutDateObj < moveInDateObj:
            errors.append("Move-out date cannot be earlier than move-in date.")

        if errors:
            errorMessage = "\n".join(errors)
            print("Validation Errors:\n" + errorMessage)
            QMessageBox.critical(self, "Validation Error", errorMessage, QMessageBox.Ok)
            return

        print(f"Updating rent details with ID: {rentingTenant}")
        prevRoomSex, prevRoomMax, prevRoomOcc = self.select.SelectQuery(table = "Room", spec_col= ["TenantSex", "MaximuCapacity", "NoOfOccupants"], filter = {"RoomNumber" : self.previousRoomNumber}, limit = 1).retData()
        if self.roomChanged:
            print(f"Room was changed by user from {self.previousRoomNumber} to {roomNumber}")
            newRoomSex, newRoomMax, newRoomOcc = self.select.SelectQuery(table = "Room", spec_col= ["TenantSex", "MaximuCapacity", "NoOfOccupants"], filter = {"RoomNumber" : roomNumber}, limit = 1).retData()

        rentParameters = {
            "MoveInDate": moveInDate,
            "MoveOutDate": moveOutDate,
            "RentedRoom": roomNumber
        }
        if status == "Active":
            tenantParameters = {
                "RoomNumber" : roomNumber
            }
        elif status == "Moved Out":
            tenantParameters = {
                "RoomNumber" : None
            }
            roomParameters = [
                
            ]

        self.updater.updateTableData("Rents", rentParameters, "RentingTenant", rentingTenant)
        self.updater.updateTableData("Tenant", tenantParameters, "TenantID", rentingTenant)
        QMessageBox.information(self, "Update Successful", "Rent information updated successfully.", QMessageBox.Ok)
        self.accept()

    def closeWindow(self):
        print("Closing the Edit Rent Dialog")
        self.close()

    def fillRentStatusComboBox(self):
        self.ui.MoveStatuscomboBox.clear()
        for label, data in self.statusOptions.items():
            self.ui.MoveStatuscomboBox.addItem(label, data)

    def fillRentingTenantID(self):
        self.ui.RentingTenantIDComboBox.clear()
        self.select.SelectQuery(table="Rents", select_type=None, spec_col=["Rents.RentingTenant"])
        resultBuilder = self.select.retDict()
        print(f"Query Result: {resultBuilder}")

        for row in resultBuilder:
            tenantID = next(iter(row.values()))
            self.ui.RentingTenantIDComboBox.addItem(str(tenantID))

    def fillRoomNumber(self):
        self.ui.RoomNumberComboBox.clear()
        self.select.SelectQuery(table="Rents", select_type=None, spec_col=["Rents.RentedRoom", "Rents.MoveOutDate"])
        resultBuilder = self.select.retDict()
        #print(f"Query Result: {resultBuilder}")

        for row in resultBuilder:
            roomNumber = next(iter(row.values()))
            self.ui.RoomNumberComboBox.addItem(str(roomNumber))

    def matchTenantIDToDetails(self):
        tenantID = self.ui.RentingTenantIDComboBox.currentText()

        if tenantID:
            self.select.SelectQuery(
                table="Rents",
                select_type="Rents",
                spec_col=["Rents.RentedRoom", "Rents.MoveInDate", "Rents.MoveOutDate", "RentDuration.MoveStatus"],
                tag="RentingTenant",
                key=tenantID
            )
            resultBuilder = self.select.retData()
            print(f"\n\nMatch Query Result: {resultBuilder}")

            if resultBuilder:
                roomNumber, moveInDate, moveOutDate, status = resultBuilder[0]

                self.previousRoomNumber = str(roomNumber)  # Save for comparison
                self.roomChanged = False  # Reset on tenant switch

                self.ui.RoomNumberComboBox.blockSignals(True)  # prevent triggering onRoomNumberChanged
                self.ui.RoomNumberComboBox.setCurrentText(str(roomNumber))
                self.ui.RoomNumberComboBox.blockSignals(False)

                self.ui.MoveInDateEdit.setDate(moveInDate)

                if not moveOutDate:
                    nextYear = datetime.now() + relativedelta(years=1)
                    self.ui.MoveOutDateEdit.setDate(nextYear)
                else:
                    self.ui.MoveOutDateEdit.setDate(moveOutDate)

                index = self.ui.MoveStatuscomboBox.findData(status)
                if index != -1:
                    self.ui.MoveStatuscomboBox.setCurrentIndex(index)

    def onRoomNumberChanged(self, newValue):
        if self.previousRoomNumber is not None and newValue != self.previousRoomNumber:
            print(f"Room changed by user from {self.previousRoomNumber} to {newValue}")
            self.roomChanged = True
            
            self.select.SelectQuery(table="Room", select_type=None, spec_col=["Room.NoOfOccupants"], tag="RoomNumber", key=newValue)
            
            #decrement previous room's occupant count
            self.updater.updateTableData("Room", {"NoOfOccupants": 0}, "RoomNumber", self.previousRoomNumber)
            #increment new room's occupant count
            self.updater.updateTableData("Room", {"NoOfOccupants": 1}, "RoomNumber", newValue)
        else:
            self.roomChanged = False
