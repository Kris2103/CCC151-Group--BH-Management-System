from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from PyQt5.QtCore import QDate
from DATABASE.Functions import Select, Insert, update, Populate
from .AddRent import Ui_Dialog

class AddRentDialog(QDialog):
        # self.ui.SexComboBox.setCurrentIndex(-1)
        # self.ui.RoomNoComboBox.setCurrentIndex(-1)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.select = Select.Select()
        self.insert = Insert.Insert()
        self.update = update.update()
        self.populate = Populate.Populate(self)

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_rent)
        
        self.ui.MoveInDateEdit.setCalendarPopup(True)
        self.ui.MoveInDateEdit.setDate(QDate.currentDate())
        
        self.populate.populate_movestatus_combobox(self.ui.MoveStatuscomboBox)
        self.populate.populate_room_combobox(self.ui.RoomNoComboBox)
        self.populate.populate_tenant_id_combobox(self.ui.RentingTenantIDComboBox)

        self.ui.RoomNoComboBox.currentTextChanged.connect(lambda: self.populate.sync_tenant_id_from_room(self.ui.RoomNoComboBox, self.ui.RentingTenantIDComboBox))
        self.ui.RentingTenantIDComboBox.currentTextChanged.connect(lambda: self.populate.sync_room_from_tenant_id(self.ui.RoomNoComboBox, self.ui.RentingTenantIDComboBox))

        self.ui.MoveStatuscomboBox.setCurrentIndex(-1)
        self.ui.RoomNoComboBox.setCurrentIndex(-1)
        self.ui.RentingTenantIDComboBox.setCurrentIndex(-1)

    def handle_add_rent(self):
        move_in_date = self.ui.MoveInDateEdit.date().toString("yyyy-MM-dd")
        rent_status = self.ui.MoveStatuscomboBox.currentText()
        room_number = self.ui.RoomNoComboBox.currentText()
        tenant_id = self.ui.RentingTenantIDComboBox.currentText()

        if not room_number or not tenant_id:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        # Check current occupancy and maximum capacity of the room
        tenant_sex = self.select.SelectQuery(table     = "Tenant", 
                                            spec_col   = "Sex", 
                                            tag        = "TenantID", 
                                            key        = tenant_id, 
                                            limit      = 1).retData()

        columns = ["MaximumCapacity", 
                    "NoOfOccupants", 
                    "TenantSex"]
            
        room_data = self.select.SelectQuery(table      = "Room", 
                                            spec_col   = columns, 
                                            tag        = "RoomNumber", 
                                            key        = room_number, 
                                            limit      = 1).retData()

        if room_data:
            maximum_capacity, current_occupants, room_tsex = room_data[0]
            if room_tsex != tenant_sex and room_tsex != None:
                QMessageBox.warning(self, "Sex invalid", f"Room {room_number} only accepts {room_tsex} tenants.")
                return
            if current_occupants >= maximum_capacity:
                QMessageBox.warning(self, "Room Full", f"Room {room_number} has reached its maximum capacity of {current_occupants}/{maximum_capacity}.")
                return
                
        # Check if room is already rented with status "Active"
        query = "SELECT * FROM Rents WHERE RentedRoom = %s AND MoveStatus = 'Active' AND MoveInDate = %s"
        self.select.cursor.execute(query, (room_number, move_in_date))
        
        if self.select.cursor.fetchone():
            QMessageBox.warning(self, "Room Occupied", f"The room is already rented on {move_in_date}.")
            return

        # Insert new rent record
        try:
            newRent = [
                        move_in_date, 
                        rent_status, 
                        room_number, 
                        tenant_id
                        ]
            
            self.insert.InsertQuery("Rents", newRent)

            # Repopulate UI elements after successful insertion
            self.populate.populate_room_combobox(self.ui.RoomNoComboBox)
            self.ui.RentingTenantIDComboBox.setCurrentIndex(0)
            self.ui.RoomNoComboBox.setCurrentIndex(0)

            QMessageBox.information(self, "Success", "Rent entry added successfully.")
            self.accept()
        except Exception as e:
            print("Add Rent Error:", e)
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            # Ensure the cursor is closed in case of error or success
            self.select.cursor.close()