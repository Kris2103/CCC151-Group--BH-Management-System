from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from .AddRoom import Ui_Dialog
from DATABASE.Functions.Select import Select
from DATABASE.DB import DatabaseConnector

class AddRoomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

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
            select = Select()

            select.cursor.execute("SELECT RoomNumber FROM Room WHERE RoomNumber = %s", (room_number,))
            if select.cursor.fetchone():
                QMessageBox.warning(self, "Room Exists", f"Room {room_number} already exists.")
                return

            # Check if room has existing tenants and determine their sex
            query = """
                SELECT COUNT(*), Sex
                FROM Tenant
                WHERE RoomNumber = %s
                GROUP BY Sex
            """
            select.cursor.execute(query, (room_number,))
            result = select.cursor.fetchone()

            if result:
                occupant_count, existing_sex = result
                if tenant_sex != existing_sex:
                    QMessageBox.critical(self, "Sex Mismatch",
                        f"Room {room_number} already has {occupant_count} {existing_sex} tenant(s).\n"
                        f"You selected: {tenant_sex}")
                    return
                current_occupants = occupant_count
            else:
                current_occupants = 0

            # Insert new room
            insert_query = """
                INSERT INTO Room (RoomNumber, Price, TenantSex, MaximumCapacity, NoOfOccupants)
                VALUES (%s, %s, %s, %s, %s)
            """
            select.cursor.execute(insert_query, (
                room_number,
                room_price,
                tenant_sex,
                room_max,
                current_occupants
            ))

            select.conn.commit()
            select.cursor.close()

            QMessageBox.information(self, "Success", f"Room {room_number} added successfully.")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def refresh_room_combobox(self):
        # This method is responsible for refreshing the room combobox in the AddRentDialog
        # Here you would add logic to update the ComboBox in the Rent Dialog.
        pass