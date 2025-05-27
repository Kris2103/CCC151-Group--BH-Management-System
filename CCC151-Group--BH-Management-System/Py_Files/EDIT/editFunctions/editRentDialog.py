from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from PyQt5.QtCore import QDate
from ..EditRent import Ui_Dialog
from PyQt5.QtCore import Qt, QDate
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

        self.fillRentStatusComboBox()
        self.fillRentingTenantID()
        self.fillRoomNumber()
        self.ui.MoveInDateEdit.setCalendarPopup(True)
        self.ui.MoveOutDateEdit.setCalendarPopup(True)

        self.ui.UpdatepushButton.clicked.connect(self.updateRent)
        self.ui.CancelpushButton.clicked.connect(self.closeWindow)

        #self.ui.RentingTenantComboBox.currentTextChanged.connect(self.checkMoveinOrMoveOut)
        self.ui.RoomNumberComboBox.currentTextChanged.connect(self.onRoomNumberChanged)
        self.ui.MoveStatuscomboBox.currentTextChanged.connect(self.checkMoveinOrMoveOut)
        # self.ui.RoomNoComboBox.currentTextChanged.connect(lambda: self.populate.sync_tenant_id_from_room(self.ui.RoomNoComboBox, self.ui.RentingTenantComboBox))
        # self.ui.RentingTenantComboBox.currentTextChanged.connect(lambda: self.populate.sync_room_from_tenant_id(self.ui.RoomNoComboBox, self.ui.RentingTenantComboBox))

        self.matchTenantIDToDetails()

    def updateRent(self):
        moveInDateData = self.ui.MoveInDateEdit.date().toString("yyyy-MM-dd")
        moveOutDateData = self.ui.MoveOutDateEdit.date().toString("yyyy-MM-dd")
        roomNumber = self.ui.RoomNumberComboBox.currentText()
        rentingTenant = self.ui.RentingTenantComboBox.currentText()

        try:
            self.select.SelectQuery("Room", select_type="Room", spec_col=["Occupants.Count", "Room.MaximumCapacity", "Room.TenantSex"], tag="RoomNumber", key=roomNumber)
            occupantsCount, maximumCapacity, room_tsex = self.select.retData()[0]

            tenant_sex = self.select.SelectQuery(table     = "Tenant", 
                                                spec_col   = ["Sex"], 
                                                tag        = "TenantID", 
                                                key        = rentingTenant, 
                                                limit      = 1).retData()[0][0]
        except Exception as e:
            print(f"Error updating rent details: {e}")
            QMessageBox.critical(self, "Update Error", "Failed to update rent details.", QMessageBox.Ok)

        try:
            moveInDate = datetime.strptime(moveInDateData, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Validation Error", "Move-in date is not in a valid format.", QMessageBox.Ok)
            return


        try:
            moveOutDate = datetime.strptime(moveOutDateData, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Validation Error", "One of the dates is not in a valid format.", QMessageBox.Ok)
            return

        moveInDateObj = datetime.strptime(moveInDate, "%Y-%m-%d")
        moveOutDateObj = datetime.strptime(moveOutDate, "%Y-%m-%d")

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
        if self.roomChanged:
            print(f"Room was changed by user from {self.previousRoomNumber} to {roomNumber}")

        rentParameters = {
            "MoveInDate": moveInDate,
            "MoveOutDate": moveOutDate,
            "RentedRoom": roomNumber
        }
        if status == "Active":
            if occupantsCount >= maximumCapacity:
                if self.roomChanged:
                    QMessageBox.warning(self, "Overloading of Room", "Maximum Occupants reached", QMessageBox.Ok)
                    return
            tenantParameters = {
                "RoomNumber" : roomNumber
            }
            if room_tsex != tenant_sex and room_tsex != None:
                QMessageBox.warning(self, "Sex invalid", f"Room {roomNumber} only accepts {room_tsex} tenants.")
                return
            elif room_tsex is None:
                self.updater.updateTableData("Room", {"TenantSex" : tenant_sex}, "RoomNumber", int(roomNumber))

        
        if status == "Moved Out":
            tenantParameters = {
                "RoomNumber" : None
            }
            if occupantsCount - 1 == 0:
                self.updater.updateTableData("Room", {"TenantSex" : None}, "RoomNumber", int(roomNumber))

        try:
            self.updater.updateTableData("Rents", rentParameters, "RentingTenant", rentingTenant)
        except Exception as e:
            print(f"Error updating rent details: {e}")
            QMessageBox.critical(self, "Update Error", "Failed to update rent details.", QMessageBox.Ok)
        
        try:
            self.updater.updateTableData("Tenant", tenantParameters, "TenantID", rentingTenant)
            QMessageBox.information(self, "Update Successful", "Rent information updated successfully.", QMessageBox.Ok)
            self.accept()
        except Exception as e:
            print(f"Error updating rent details: {e}")
            QMessageBox.critical(self, "Update Error", "Failed to update rent details.", QMessageBox.Ok)

    def closeWindow(self):
        print("Closing the Edit Rent Dialog")
        self.close()

    def fillRentStatusComboBox(self):
        self.ui.MoveStatuscomboBox.clear()
        for label, data in self.statusOptions.items():
            self.ui.MoveStatuscomboBox.addItem(label, data)
            
        self.ui.MoveStatuscomboBox.setCurrentIndex(-1)

    def fillRentingTenantID(self):
        self.ui.RentingTenantComboBox.clear()
        self.select.SelectQuery(table="Tenant", select_type=None, spec_col=["Tenant.TenantID"])
        resultBuilder = self.select.retDict()
        print(f"Query Result: {resultBuilder}")

        for row in resultBuilder:
            tenantID = next(iter(row.values()))
            self.ui.RentingTenantComboBox.addItem(str(tenantID))
        
        self.ui.RentingTenantComboBox.setCurrentIndex(-1)

    def fillRoomNumber(self):
        self.ui.RoomNumberComboBox.clear()
        self.select.SelectQuery(table="Room", select_type=None, spec_col=["Room.RoomNumber"])
        resultBuilder = self.select.retDict()

        for row in resultBuilder:
            roomNumber = next(iter(row.values()))
            self.ui.RoomNumberComboBox.addItem(str(roomNumber))
            
        self.ui.RoomNumberComboBox.setCurrentIndex(-1)

    def matchTenantIDToDetails(self):
        tenantID = self.ui.RentingTenantComboBox.currentText()

        if tenantID:
            self.select.SelectQuery(
                table="Rents",
                select_type=None,
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
            
            self.select.SelectQuery(table="Room", select_type="Room", spec_col=["Occupants.Count"], tag="RoomNumber", key=newValue)
            
        else:
            self.roomChanged = False
            
    def checkMoveinOrMoveOut(self):     
        status = str(self.ui.MoveStatuscomboBox.currentData())
        
        if status != "Active":
            moveOutDateObj =  QDate.currentDate()
            self.ui.MoveOutDateEdit.setDate(moveOutDateObj)
            self.ui.MoveOutDateEdit.setReadOnly(True)
            
        else:
            self.ui.MoveOutDateEdit.setReadOnly(False)
