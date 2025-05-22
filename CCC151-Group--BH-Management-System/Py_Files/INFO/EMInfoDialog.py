from PyQt5.QtWidgets import QDialog
from .EMInfo import Ui_Dialog
import re
from DATABASE.Functions import Select
from DATABASE.DB import DatabaseConnector

class EMInfoDialog(QDialog):
    def __init__(self, parent = None, row_id = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.select = Select.Select()
        self.row_id = row_id
        print("Dialog executed")
        self.extractInfo()

    def extractInfo(self):
        em_info = ["EmergencyContact.FirstName", "EmergencyContact.MiddleName", "EmergencyContact.LastName",
                   "EmergencyContact.PhoneNumber", "EmergencyContact.Relationship", "EmergencyContact.EMTenantID"]
        ten_info = ["Tenant.FirstName", "Tenant.MiddleName", "Tenant.LastName"]
        selected_EmergencyContact = {"ContactID" : self.row_id}
        print("Extraction executing")
        try:
            fname, mname, lname, pnum, rel, tenid  = self.select.SelectQuery(   table = "EmergencyContact",
                                                                                spec_col = em_info,
                                                                                filters = selected_EmergencyContact).retData()[0]
            
            selected_tenant = {"TenantID" : tenid}

            tenfname, tenmname, tenlname                    = self.select.SelectQuery(  table = "Tenant",
                                                                                        spec_col = ten_info,
                                                                                        filters = selected_tenant).retData()[0]
            
        except Exception as e:
            print(f"Some exception {e} in extracting information")

        print("Extraction complete")
        self.ui.ContactIDLine.setText(f"{self.row_id}")
        self.ui.NameLine.setText(f"{lname}, {fname} {mname}" if mname is not None else f"{lname}, {fname}")
        self.ui.PhoneLine.setText(f"{pnum}")
        self.ui.RelationshipLine.setText(f"{rel}")
        self.ui.EMTenantIDLine.setText(f"{tenid}")
        self.ui.TenantNameLine.setText(f"{tenlname}, {tenfname} {tenmname}" if tenmname is not None else f"{tenlname}, {tenfname}")
        