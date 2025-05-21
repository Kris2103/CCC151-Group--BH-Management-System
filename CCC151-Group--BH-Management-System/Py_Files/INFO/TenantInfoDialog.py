from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from .TenantInfo import Ui_Dialog
import re
from DATABASE.Functions import Select, Insert, update, Populate
from DATABASE.DB import DatabaseConnector
from datetime import datetime

class TenantInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.select = Select.Select()
        self.populate = Populate.Populate(self)

    