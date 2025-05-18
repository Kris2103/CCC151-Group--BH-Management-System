from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from PyQt5.QtCore import QDate
from DATABASE.Functions import Select, Insert, update, Populate
from .AddRent import Ui_Dialog

class AddRentDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.select = Select.Select()
        self.insert = Insert.Insert()
        self.updater = update.update()
        self.populate = Populate.Populate(self)

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_rent)
        
        self.ui.MoveInDateEdit.setCalendarPopup(True)
        self.ui.MoveInDateEdit.setDate(QDate.currentDate())

        self.ui.MoveOutDateEdit.setCalendarPopup(True)
        self.ui.MoveOutDateEdit.setDate(QDate.currentDate().addMonths(1))
        
        self.populate.populate_movestatus_combobox(self.ui.MoveStatuscomboBox)
        self.populate.populate_room_combobox(self.ui.RoomNoComboBox)
        self.populate.populate_tenant_id_combobox(self.ui.RentingTenantIDComboBox)

        self.ui.MoveStatuscomboBox.setCurrentIndex(0)
        self.ui.MoveStatuscomboBox.setDisabled(True)
        self.ui.RoomNoComboBox.setCurrentIndex(-1)
        self.ui.RentingTenantIDComboBox.setCurrentIndex(-1)

    def handle_add_rent(self):
        move_in_date = self.ui.MoveInDateEdit.date().toString("yyyy-MM-dd")
        move_out_date = self.ui.MoveOutDateEdit.date().toString("yyyy-MM-dd")
        room_number = self.ui.RoomNoComboBox.currentText()
        tenant_id = self.ui.RentingTenantIDComboBox.currentText()

        if not room_number or not tenant_id:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        # Check current occupancy and maximum capacity of the room
        tenant_sex = self.select.SelectQuery(table     = "Tenant", 
                                            spec_col   = ["Sex"], 
                                            tag        = "TenantID", 
                                            key        = tenant_id, 
                                            limit      = 1).retData()[0][0]
        
        room_columns = ["MaximumCapacity",  
                        "NoOfOccupants",
                        "TenantSex"]
            
        room_data = self.select.SelectQuery(table      = "Room", 
                                            spec_col   = room_columns, 
                                            select_type= "Room",
                                            tag        = "RoomNumber", 
                                            key        = room_number, 
                                            limit      = 1).retData()
        try:
            renting_tenant, existing_rent_status, existing_rented_room = self.select.SelectQuery(
                table="Rents",
                spec_col=["Rents.RentingTenant, RentDuration.MoveStatus", "Rents.RentedRoom"],
                select_type="Rents",
                filters={"RentingTenant": tenant_id},
                limit=1
            ).retData()

            print(renting_tenant)
            print(existing_rent_status)
            print(existing_rented_room)

            if existing_rent_status == "Active":
                QMessageBox.warning(
                    self, "Rent duplicate",
                    f"Tenant {tenant_id} is still under an active contract with Room {existing_rented_room}."
                )
                return

        except IndexError as ie:
            print("No active contract existing, Rent is valid")

        if room_data:
            maximum_capacity, current_occupants, room_tsex = room_data[0]
            if room_tsex != tenant_sex and room_tsex != None:
                QMessageBox.warning(self, "Sex invalid", f"Room {room_number} only accepts {room_tsex} tenants.")
                return
            if current_occupants >= maximum_capacity:
                QMessageBox.warning(self, "Room Full", f"Room {room_number} has reached its maximum capacity of {current_occupants}/{maximum_capacity}.")
                return

        # Insert new rent record
        try:
            newRent = [
                        tenant_id,
                        room_number,
                        move_in_date,
                        move_out_date
                        ]
            
            self.insert.InsertQuery("Rents", newRent)
            self.updater.updateTableData("Room", {"NoOfOccupants" : current_occupants + 1, "TenantSex" : tenant_sex}, "RoomNumber", int(room_number))
            self.updater.updateTableData("Tenant", {"RoomNumber" : room_number}, "TenantID", tenant_id)

            # Repopulate UI elements after successful insertion
            self.populate.populate_room_combobox(self.ui.RoomNoComboBox)
            self.ui.RentingTenantIDComboBox.setCurrentIndex(0)
            self.ui.RoomNoComboBox.setCurrentIndex(0)

            QMessageBox.information(self, "Success", "Rent entry added successfully.")
            self.accept()
        except Exception as e:
            print("Add Rent Error:", e)
            QMessageBox.critical(self, "Database Error", str(e))