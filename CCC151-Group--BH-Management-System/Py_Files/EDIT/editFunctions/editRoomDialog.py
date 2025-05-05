from PyQt5.QtWidgets import QDialog
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
        self.ui.RoomNumberLineEdit.textEdited.connect(self.assignCurrentNumberOfOccupants)
        self.ui.CancelpushButton.clicked.connect(self.closeWindow)
        self.ui.UpdatepushButton.clicked.connect(self.updateRoom)

        
    def updateRoom(self):
        roomNumber = self.ui.RoomNumberLineEdit.text()
        
        price = self.ui.PriceLineEdit.text()
        tenantSex = self.ui.TenantSexComboBox.currentData()
        maximumAcceptedOccupants = self.ui.MaxNoOccupantsLineEdit.text()
        numberOfOccupants = self.ui.NoOfOccupantsComboBox.currentText()
        
        errors = []
        
        if not roomNumber:
            errors.append("Please select room number to edit.")
        if not price:
            errors.append("Please set room price.")
        if not maximumAcceptedOccupants:
            errors.append("Please assign the maximum number of occupants")
        if not numberOfOccupants:
            errors.append("Please assign the number of occupants")
        
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
            "NoOfOccupants" : numberOfOccupants
        }
        
        updater.updateTableData("Room", setParameters, "RoomNumber", roomNumber)
        
    def closeWindow(self):
        print("Closing the Edit Room Dialog")
        self.reject() 
        
    def fillSexComboBox(self):
        self.ui.TenantSexComboBox.clear()
        
        for label, data, in self.sexOptions.items():
            self.ui.TenantSexComboBox.addItem(label, data)
            
    def assignCurrentNumberOfOccupants(self):
        selector = Select()
        roomNumber = self.ui.RoomNumberLineEdit.text()
        
        if roomNumber:
            print(roomNumber)
            selector.SelectQuery(table="Room", select_type=None, spec_col=["Room.MaximumCapacity"], tag="RoomNumber", key=roomNumber)
            resultBuilder = selector.retDict()
            print(f"Query Result: {resultBuilder}")
            self.ui.NoOfOccupantsComboBox.clear()
            
            if resultBuilder:
                value = list(resultBuilder[0].values())[0]
                for i in range(0, value + 1):
                    self.ui.NoOfOccupantsComboBox.addItem(str(i))
        