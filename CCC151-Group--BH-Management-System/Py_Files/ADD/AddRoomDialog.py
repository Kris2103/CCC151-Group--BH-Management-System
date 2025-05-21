from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from .AddRoom import Ui_Dialog
from DATABASE.Functions import Select, Insert, update, Populate
from DATABASE.DB import DatabaseConnector

class AddRoomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.select = Select.Select()
        self.insert = Insert.Insert()
        self.update = update.update()
        self.populate = Populate.Populate()

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_room)

        self.populate.populate_sex_combobox(self.ui.TenantSexComboBox)
        self.ui.TenantSexComboBox.addItem("None")

        self.ui.TenantSexComboBox.setCurrentIndex(-1)

    def handle_add_room(self):
        room_number = self.ui.RoomNumberLineEdit.text()
        room_price = self.ui.PriceLineEdit.text()
        tenant_sex = self.ui.TenantSexComboBox.currentText()
        room_max = self.ui.MaxNoOccupantsLineEdit.text()
        
        if not room_number or not room_price or not room_max:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        try:
            existing_room =  self.select.SelectQuery("Room", spec_col = ["RoomNumber"], tag = "RoomNumber", key = room_number, limit = 1).retData()
            if existing_room:
                QMessageBox.warning(self, "Room Exists", f"Room {room_number} already exists.")
                return

            # Insert new room
            newRoom = [
                room_number,
                room_price,
                tenant_sex,
                room_max
            ]
            
            self.insert.InsertQuery("Room", newRoom)

            QMessageBox.information(self, "Success", f"Room {room_number} added successfully.")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))