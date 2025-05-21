from PyQt5.QtWidgets import QDialog
from .TenantInfo import Ui_Dialog
import re
from DATABASE.Functions import Select
from DATABASE.DB import DatabaseConnector

class TenantInfoDialog(QDialog):
    def __init__(self, parent = None, row_id = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.select = Select.Select()
        self.row_id = row_id
        print("Dialog executed")
        self.extractInfo()

    def extractInfo(self):
        tenant_info = ["Tenant.FirstName", "Tenant.MiddleName", "Tenant.LastName", "Tenant.Sex"
                     , "Tenant.PhoneNumber", "Tenant.Email", "RentDuration.MoveStatus", "RentDuration.RoomNumber"
                     , "PaymentStatus.PaymentStatus", "RemainingDue.RemainingDue", "PaidAmount.PaidAmount", "EmergencyContact.PhoneNumber"]
        selected_tenant = {"TenantID" : self.row_id}
        print("Extraction executing")
        try:
            fname, mname, lname, sex, pnum, email, movestat, roomn, paystat, remdue, paidamt, ecpnum = self.select.SelectQuery( table = "Tenant",
                                                                                                                        select_type = "Tenant",
                                                                                                                        spec_col = tenant_info,
                                                                                                                        filters = selected_tenant).retData()[0]
        except Exception as e:
            print(f"Some exception {e} in extracting information")

        print("Extraction complete")
        self.ui.NameLine.setText(f"{lname}, {fname} {mname}" if mname is not None else f"{lname}, {fname}")
        self.ui.SexLine.setText(f"{sex}")
        self.ui.PhoneLine.setText(f"{pnum}")
        self.ui.EmailLine.setText(f"{email}")
        self.ui.MoveLine.setText(f"{movestat}" if movestat is not None else "No Rental Contracts")
        self.ui.RoomLine.setText(f"{roomn}")
        self.ui.PayLine.setText(f"{paystat}")
        self.ui.RemainLine.setText(f"{remdue}")
        self.ui.PaidLine.setText(f"{paidamt}")
        self.ui.ECLine.setText(f"{ecpnum}" if ecpnum is not None else "None added")