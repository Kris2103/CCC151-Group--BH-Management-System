from PyQt5.QtWidgets import QDialog, QCompleter
from PyQt5.QtWidgets import QMessageBox
from ..EditRoom import Ui_Dialog
from PyQt5.QtCore import Qt
from DATABASE.Functions.update import update
from DATABASE.Functions.Select import Select

class editRoomDialog(QDialog):
    
    sexOptions = {
        "Male" : "Male",
        "Female" : "Female"
    }
        
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.fillSexComboBox()
        self.ui.CancelpushButton.clicked.connect(self.closeWindow)
        self.ui.UpdatepushButton.clicked.connect(self.updateRoom)

        
    def updateRoom(self):
        roomNumber = self.ui.RoomNumberLineEdit.text()
        
        price = self.ui.PriceLineEdit.text()
        tenantSex = self.ui.TenantSexComboBox.currentData()
        maximumAcceptedOccupants = self.ui.MaxNoOccupantsLineEdit.text()
        
        errors = []
        
        if not roomNumber:
            errors.append("Please select room number to edit.")
        if not price:
            errors.append("Please set room price.")
        if not maximumAcceptedOccupants:
            errors.append("Please assign the maximum number of occupants")
        
        if errors:
            errorMessage = "\n".join(errors)
            print("Validation Errors:\n" + errorMessage)
            QMessageBox.critical(self, "Validation Error", errorMessage, QMessageBox.Ok)
        
            return 
        
        print(f"Updating Room with Number: {roomNumber}")
        
        updater = update()
        
        setParameters = {
            "Price" : price,
            "TenantSex" : tenantSex,
            "MaximumCapacity" : maximumAcceptedOccupants,
        }
        
        updater.updateTableData("Room", setParameters, "RoomNumber", roomNumber)
        QMessageBox.information(self, "Update Successful", "Room information updated successfully.", QMessageBox.Ok)
        self.accept()
        
    def closeWindow(self):
        print("Closing the Edit Room Dialog")
        self.reject() 
        
    def fillSexComboBox(self):
        self.ui.TenantSexComboBox.clear()
        
        for label, data, in self.sexOptions.items():
            self.ui.TenantSexComboBox.addItem(label, data)
        
        self.ui.TenantSexComboBox.setCurrentIndex(-1)
            
    # def assignCurrentNumberOfOccupants(self):
    #     selector = Select()
    #     roomNumber = self.ui.RoomNumberComboBox.currentText()
        
    #     if roomNumber:
    #         print(roomNumber)
    #         selector.SelectQuery(table="Room", select_type=None, spec_col=["Room.MaximumCapacity"], tag="RoomNumber", key=roomNumber)
    #         resultBuilder = selector.retData()
            
    #         selector.SelectQuery(table="Room", select_type=None, spec_col=["Room.NoOfOccupants", "Room.MaximumCapacity", "Room.TenantSex", "Room.Price"], tag="RoomNumber", key=roomNumber)
    #         currentOccupants = selector.retData()
            
    #         print(f"Current Occupants: {currentOccupants}")
            
    #         if len(resultBuilder) != 1:
    #             resultBuilder = 0
    #             self.ui.PriceLineEdit.setText("")
    #             self.ui.MaxNoOccupantsLineEdit.setText("")
    #             self.ui.TenantSexComboBox.setCurrentIndex(-1)
    #         else:
    #             resultBuilder = resultBuilder[0][0]
    #             numberOfOccupants = currentOccupants[0][0]
    #             maximumCapacity = currentOccupants[0][1]
    #             tenantSex = currentOccupants[0][2]
    #             price = currentOccupants[0][3]
        
    #         print(f"Query Result: {resultBuilder}")
    #         self.ui.NoOfOccupantsComboBox.clear()

            
    #         if resultBuilder is not 0:
    #             for i in range(resultBuilder + 1):
    #                 self.ui.NoOfOccupantsComboBox.addItem(str(i))

    #             self.ui.PriceLineEdit.setText(str(price))
    #             self.ui.TenantSexComboBox.setCurrentText(tenantSex)
    #             self.ui.MaxNoOccupantsLineEdit.setText(str(maximumCapacity))
    #             self.ui.NoOfOccupantsComboBox.setCurrentText(str(numberOfOccupants))
        
    # def fillRoomNumber(self):
    #     self.ui.RoomNumberComboBox.clear()
    #     selector = Select()
    #     selector.SelectQuery(table="Rents", select_type=None, spec_col=["Rents.RentedRoom", "Rents.MoveOutDate"])
    #     resultBuilder = selector.retDict()
        
    #     roomNumbers = []
        
    #     for row in resultBuilder:
    #         roomNumber = next(iter(row.values()))
    #         self.ui.RoomNumberComboBox.addItem(str(roomNumber))
    #         roomNumbers.append(str(roomNumber))
            
    #     self.ui.RoomNumberComboBox.setCurrentIndex(-1)
    #     self.ui.RoomNumberComboBox.setEditable(True)
    #     completer = QCompleter(roomNumbers, self)
    #     completer.setCaseSensitivity(Qt.CaseInsensitive)
    #     completer.setFilterMode(Qt.MatchContains)
    #     self.ui.RoomNumberComboBox.setCompleter(completer)
        
    #     self.ui.RoomNumberComboBox.setFocus()
