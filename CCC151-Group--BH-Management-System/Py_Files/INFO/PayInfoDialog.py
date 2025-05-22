from PyQt5.QtWidgets import QDialog
from .PayInfo import Ui_Dialog
import re
from DATABASE.Functions import Select
from DATABASE.DB import DatabaseConnector

class PayInfoDialog(QDialog):
    def __init__(self, parent = None, row_id = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.select = Select.Select()
        self.row_id = row_id
        print("Dialog executed")
        self.extractInfo()

    def extractInfo(self):
        pay_info = ["Pays.PayID", "Pays.PayingTenant", "Pays.PaidRoom", "PaidAmount.PaidAmount", "Pays.PaymentDate",
                    "RentDuration.Duration", "PaymentStatus.PaymentStatus", "RemainingDue.RemainingDue", "Pays.PaymentAmount"]
        selected_pay = {"PayID" : self.row_id}

        print("Extraction executing")
        try:
            PayID, Payten, Payrm, Pdam, Pdt, movedur, paystat, remdue, pyam = self.select.SelectQuery(  table = "Pays",
                                                                                                        select_type = "Pays",
                                                                                                        spec_col = pay_info,
                                                                                                        filters = selected_pay).retData()[0]
            
            tenant_info = ["Tenant.FirstName", "Tenant.MiddleName", "Tenant.LastName", "Tenant.PhoneNumber", 
                       "RentDuration.MoveStatus"]
            selected_tenant = {"TenantID" : Payten}

            fname, mname, lname, pnum, movestat = self.select.SelectQuery(  table = "Tenant",
                                                                            select_type = "Tenant",
                                                                            spec_col = tenant_info,
                                                                            filters = selected_tenant).retData()[0]
        except Exception as e:
            print(f"Some exception {e} in extracting information")

        print("Extraction complete")
        self.ui.PayIDLine.setText(f"{PayID}")
        self.ui.PayTenLine.setText(f"{Payten}")
        self.ui.PayRoomLine.setText(f"{Payrm}")
        self.ui.PaidLine.setText(f"{Pdam}")
        self.ui.PaymLine.setDate(Pdt)
        self.ui.RentDurLine.setText(f"{movedur} Months")
        self.ui.PayTenNameLine.setText(f"{lname}, {fname} {mname}" if mname is not None else f"{lname}, {fname}")
        self.ui.MoveLine.setText(f"{movestat}" if movestat is not None else "Not tied to a Contract")
        self.ui.PayLine.setText(f"{paystat}")
        self.ui.RemainLine.setText(f"{remdue}")
        self.ui.PayTenNumLine.setText(f"{pnum}")
        self.ui.SpecPaidLine.setText(f"{pyam}")