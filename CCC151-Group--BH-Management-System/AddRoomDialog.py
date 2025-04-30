from PyQt5.QtWidgets import QDialog
from AddRoom import Ui_Dialog

class AddRoomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.CancelpushButton.clicked.connect(self.reject)
        self.ui.AddpushButton.clicked.connect(self.handle_add_room)

    def handle_add_room(self):
        room_number = self.ui.RoomNumberLineEdit.text()
        room_price = self.ui.PriceLineEdit.text()
        RtenantSex = self.ui.TenantSexCombobox.currentText()
        room_max = self.ui.MaxNoOccupantsLineEdit.text()
        room_occupants = self.ui.NoOfOccupants.currentText()

        print(f"Room Number: {room_number}")
        print(f"Room Price: {room_price}")
        print(f"Tenant Sex: {tenant_sex}")
        print(f"Max Occupants: {room_max}")
        print(f"Occupants: {room_occupants}")

        self.accept()
