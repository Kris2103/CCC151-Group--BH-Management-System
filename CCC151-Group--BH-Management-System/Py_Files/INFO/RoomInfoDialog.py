from PyQt5.QtWidgets import QDialog
from .RoomInfo import Ui_Dialog
import re
from DATABASE.Functions import Select
from DATABASE.DB import DatabaseConnector

class RoomInfoDialog(QDialog):
    def __init__(self, parent = None, row_id = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.select = Select.Select()
        self.row_id = row_id
        print("Dialog executed")
        self.extractInfo()

    def extractInfo(self):
        room_info = ["Room.RoomNumber", "Room.Price", "Occupants.Count", "Room.MaximumCapacity"]
        selected_room = {"RoomNumber" : self.row_id}

        print("Extraction executing")
        try:
            roomnum, roomprc, roomocc, roomcap = self.select.SelectQuery(   table = "Room",
                                                                            select_type = "Room",
                                                                            spec_col = room_info,
                                                                            filters = selected_room).retData()[0]
            totalremdue = self.select.SelectQuery(  table = "Tenant",
                                                    select_type = "Tenant",
                                                    spec_col = ["SUM(RemainingDue.RemainingDue)"],
                                                    filters =  selected_room).retData()[0][0]
            if totalremdue != 0 and totalremdue is not None:
                paymstat = "Pending Payments" 
            elif totalremdue is None:
                paymstat = "No Payments"
            else:
                paymstat = "Paid"

        except Exception as e:
                print(f"Some exception {e} in extracting information")

        print("Extraction complete")
        self.ui.RoomIDLine.setText(f"{roomnum}")
        self.ui.RoomPriceLine.setText(f"{roomprc}")
        self.ui.OccupantsLine.setText(f"{roomocc}")
        self.ui.CapacityLine.setText(f"{roomcap}")
        self.ui.ContractsLine.setText(f"{roomocc}")
        self.ui.RemainLine.setText(f"{totalremdue}")
        self.ui.PayLine.setText(f"{paymstat}")