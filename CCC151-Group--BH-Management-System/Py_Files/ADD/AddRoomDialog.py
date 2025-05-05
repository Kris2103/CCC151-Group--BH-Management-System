from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from .AddRoom import Ui_Dialog
from DATABASE.Functions import Select, Insert, update
from DATABASE.DB import DatabaseConnector

class AddRoomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.select = Select.Select()
        self.insert = Insert.Insert()
        self.update = update.update()

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_room)

        self.populate_sex_combobox()

    def populate_sex_combobox(self):
        self.ui.TenantSexComboBox.clear()
        self.ui.TenantSexComboBox.addItems(['Male', 'Female'])

    def handle_add_room(self):
        room_number = self.ui.RoomNumberLineEdit.text()
        room_price = self.ui.PriceLineEdit.text()
        tenant_sex = self.ui.TenantSexComboBox.currentText()
        room_max = self.ui.MaxNoOccupantsLineEdit.text()

        if not room_number or not room_price or not room_max:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        try:
            
            existing_room =  self.select.SelectQuery("Room", spec_col = ["RoomNumber"], tag = "Room.RoomNumber", key = room_number, limit = 1)
            if existing_room:
                QMessageBox.warning(self, "Room Exists", f"Room {room_number} already exists.")
                return

            # Check if room has existing tenants and determine their sex
            result = self.select.SelectQuery("Tenant", spec_col=["COUNT(*) AS OccupantCount", "Tenant.Sex"], tag="Room.RoomNumber", key=room_number, group="Sex", limit=1)

            if result:
                occupant_count, existing_sex = result[0]
                if tenant_sex != existing_sex and existing_sex != None:
                    QMessageBox.critical(self, "Sex Mismatch",
                        f"Room {room_number} already has {occupant_count} {existing_sex} tenant(s).\n"
                        f"You selected: {tenant_sex}")
                    return
                current_occupants = occupant_count
            else:
                current_occupants = 0

            # Insert new room
            newRoom = [
                room_number,
                room_price,
                tenant_sex,
                room_max,
                current_occupants
            ]
            
            self.insert.InsertQuery("Room", newRoom)

            QMessageBox.information(self, "Success", f"Room {room_number} added successfully.")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def refresh_room_combobox(self):
        # This method is responsible for refreshing the room combobox in the AddRentDialog
        # Here you would add logic to update the ComboBox in the Rent Dialog if needed.
        pass