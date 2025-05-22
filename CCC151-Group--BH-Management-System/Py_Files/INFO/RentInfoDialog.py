from PyQt5.QtWidgets import QDialog
from .RentInfo import Ui_Dialog
import re
from DATABASE.Functions import Select
from DATABASE.DB import DatabaseConnector

class RentInfoDialog(QDialog):
    def __init__(self, parent = None, row_id = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.select = Select.Select()
        self.row_id = row_id
        print("Dialog executed")
        self.extractInfo()

    def extractInfo(self):
        rent_info = ["Rents.RentID", "Rents.RentingTenant", "Rents.RentedRoom", "Rents.MoveInDate",
                     "Rents.MoveOutDate", "RentDuration.Duration", "RentDuration.MoveStatus"]
        selected_rent = {"RentID" : self.row_id}

        print("Extraction executing")
        try:
            rentID, renten, rentrm, movein, moveout, movedur, movestat = self.select.SelectQuery(   table = "Rents",
                                                                                                    select_type = "Rents",
                                                                                                    spec_col = rent_info,
                                                                                                    filters = selected_rent).retData()[0]
            
            tenant_info = ["Tenant.FirstName", "Tenant.MiddleName", "Tenant.LastName", "Tenant.PhoneNumber", 
                       "PaymentStatus.PaymentStatus", "RemainingDue.RemainingDue"]
            selected_tenant = {"TenantID" : renten}

            fname, mname, lname, pnum, paystat, remdue = self.select.SelectQuery( table = "Tenant",
                                                                            select_type = "Tenant",
                                                                            spec_col = tenant_info,
                                                                            filters = selected_tenant).retData()[0]
        except Exception as e:
            print(f"Some exception {e} in extracting information")

        print("Extraction complete")
        self.ui.RentIDLine.setText(f"{rentID}")
        self.ui.RentTenLine.setText(f"{renten}")
        self.ui.RentRoomLine.setText(f"{rentrm}")
        self.ui.MoveInLine.setDate(movein)
        self.ui.MoveOutLine.setDate(moveout)
        self.ui.RentDurLine.setText(f"{movedur} Months")
        self.ui.RentTenNameLine.setText(f"{lname}, {fname} {mname}" if mname is not None else f"{lname}, {fname}")
        self.ui.MoveLine.setText(f"{movestat}" if movestat is not None else "No Rental Contracts")
        self.ui.PayLine.setText(f"{paystat}")
        self.ui.RemainLine.setText(f"{remdue}")
        self.ui.RentTenNumLine.setText(f"{pnum}")