from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from PyQt5.QtCore import QDate
from DATABASE.Functions.Select import Select
from .AddRent import Ui_Dialog

class AddRentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_rent)
        
        self.ui.MoveInDateEdit.setCalendarPopup(True)
        self.ui.MoveInDateEdit.setDate(QDate.currentDate())
        
        self.select = Select()
        self.populate_movestatus_combobox()
        self.populate_room_combobox()
        self.populate_tenant_id_combobox()

        self.ui.RoomNumberComboBox.currentTextChanged.connect(self.sync_tenant_id_from_room)
        self.ui.RentingTenantIDComboBox.currentTextChanged.connect(self.sync_room_from_tenant_id)

    def populate_movestatus_combobox(self):
        self.ui.MoveStatuscomboBox.clear()
        self.ui.MoveStatuscomboBox.addItems(["Active"])

    def populate_room_combobox(self):
        self.ui.RoomNumberComboBox.clear()
        query = "SELECT DISTINCT RoomNumber FROM Tenant"
        select = Select()
        select.cursor.execute(query)
        rooms = [str(row[0]) for row in select.cursor.fetchall()]
        self.ui.RoomNumberComboBox.addItems(rooms)

    def populate_tenant_id_combobox(self):
        self.ui.RentingTenantIDComboBox.clear()
        query = "SELECT TenantID FROM Tenant"
        self.select.cursor.execute(query)
        tenant_ids = [str(row[0]) for row in self.select.cursor.fetchall()]
        self.ui.RentingTenantIDComboBox.addItems(tenant_ids)

    def sync_tenant_id_from_room(self):
        room = self.ui.RoomNumberComboBox.currentText()
        if not room:
            return
        query = "SELECT TenantID FROM Tenant WHERE RoomNumber = %s"
        self.select.cursor.execute(query, (room,))
        result = self.select.cursor.fetchone()
        if result:
            tenant_id = str(result[0])
            self.ui.RentingTenantIDComboBox.setCurrentText(tenant_id)
        else:
            self.ui.RentingTenantIDComboBox.setCurrentText("")

    def sync_room_from_tenant_id(self):
        tenant_id = self.ui.RentingTenantIDComboBox.currentText()
        if not tenant_id:
            return

        # Clear any unread result before the new query
        while self.select.cursor.nextset():
            pass

        query = "SELECT RoomNumber FROM Tenant WHERE TenantID = %s"
        self.select.cursor.execute(query, (tenant_id,))
        result = self.select.cursor.fetchone()

        if result:
            room_number = str(result[0])
            index = self.ui.RoomNumberComboBox.findText(room_number)
            if index != -1:
                self.ui.RoomNumberComboBox.setCurrentIndex(index)


    def handle_add_rent(self):
        move_in_date = self.ui.MoveInDateEdit.date().toString("yyyy-MM-dd")
        rent_status = self.ui.MoveStatuscomboBox.currentText()
        room_number = self.ui.RoomNumberComboBox.currentText()
        tenant_id = self.ui.RentingTenantIDComboBox.currentText()

        if not room_number or not tenant_id:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        # Check current occupancy and maximum capacity of the room
        capacity_query = """
            SELECT MaximumCapacity, NoOfOccupants
            FROM Room
            WHERE RoomNumber = %s
        """
        self.select.cursor.execute(capacity_query, (room_number,))
        result = self.select.cursor.fetchone()

        if result:
            maximum_capacity, current_occupants = result
            print(f"Maximum Capacity: {maximum_capacity}, Current Occupants: {current_occupants}")

            if current_occupants >= maximum_capacity:
                QMessageBox.warning(self, "Room Full", "The room has reached its maximum capacity.")
                return

        # Check if room is already rented with status "Active"
        query = "SELECT * FROM Rents WHERE RentedRoom = %s AND MoveStatus = 'Active' AND MoveInDate = %s"
        self.select.cursor.execute(query, (room_number, move_in_date))
        if self.select.cursor.fetchone():
            QMessageBox.warning(self, "Room Occupied", f"The room is already rented on {move_in_date}.")
            return

        # Insert new rent record
        try:
            insert_query = """
                INSERT INTO Rents (MoveInDate, MoveStatus, RentedRoom, RentingTenant)
                VALUES (%s, %s, %s, %s)
            """
            self.select.cursor.execute(insert_query, (
                move_in_date, rent_status, room_number, tenant_id
            ))

            # Update the number of occupants in the Room table
            update_occupants_query = """
                UPDATE Room
                SET NoOfOccupants = NoOfOccupants + 1
                WHERE RoomNumber = %s
            """
            self.select.cursor.execute(update_occupants_query, (room_number,))

            # Commit the changes and close the cursor
            self.select.conn.commit()

            # Repopulate UI elements after successful insertion
            self.populate_room_combobox()
            self.ui.RentingTenantIDComboBox.setCurrentIndex(0)
            self.ui.RoomNumberComboBox.setCurrentIndex(0)

            QMessageBox.information(self, "Success", "Rent entry added successfully.")
            self.accept()
        except Exception as e:
            print("Add Rent Error:", e)
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            # Ensure the cursor is closed in case of error or success
            self.select.cursor.close()