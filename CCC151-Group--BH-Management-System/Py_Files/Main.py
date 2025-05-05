import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QComboBox
from PyQt5.QtWidgets import QMessageBox
import SpecialWidgetsUI
from ADD.AddTenantDialog import AddTenantDialog
from ADD.AddRoomDialog import AddRoomDialog
from ADD.AddRentDialog import AddRentDialog
from ADD.AddPaymentDialog import AddPaymentDialog
from ADD.AddEmergencyContactDialog import AddEmergencyContactDialog
from MainUI import Ui_MainWindow
from DATABASE.Functions.Select import Select
from EDIT.editFunctions.editTenantDialog import editTenantDialog
from EDIT.editFunctions.editRoomDialog import editRoomDialog
from EDIT.editFunctions.editRentDialog import editRentDialog
from EDIT.editFunctions.editEmergencyContactDialog import editEmergencyContactDialog
from EDIT.editFunctions.editRoomDialog import editRoomDialog
from DATABASE.DB import DatabaseConnector
import math
from DATABASE.Functions.Populate import Populate


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.selector = Select()
        self.populator = Populate()

        self.button_base_style = """
        background-color: rgb(250, 255, 242); /* Inactive background */
        border: 1px solid #660000;
        border-radius: 4px;
        padding: 5px;
        font-family: 'Roboto', sans-serif;
        font-weight: 500;
        font-style: normal;
        font-size: 13px;
        color: #800000; 
        """

        self.active_style = self.button_base_style.replace("rgb(250, 255, 242)", "rgb(210, 235, 200)")  # Light green when active
        self.inactive_style = self.button_base_style

        self.AddpushButton.clicked.connect(self.on_Add_clicked)
        self.tenantPushButton.clicked.connect(lambda: self.switch_tab(0))
        self.roomPushButton.clicked.connect(lambda: self.switch_tab(1))
        self.rentPushButton.clicked.connect(lambda: self.switch_tab(2))
        self.paymentPushButton.clicked.connect(lambda: self.switch_tab(3))
        self.emergencyPushButton.clicked.connect(lambda: self.switch_tab(4))
        self.EditpushButton.clicked.connect(self.onEditClicked)

        self.jumpBox.activated.connect(lambda: self.jump())

        self.SearchpushButton.clicked.connect(lambda: self.perform_search())

        self.switch_tab(0)


    def switch_tab(self, index):
        self.stackedWidget.setCurrentIndex(index)
        
        if hasattr(self, "full_data"): del self.full_data

        # Reset all to inactive
        self.tenantPushButton.setStyleSheet(self.inactive_style)
        self.roomPushButton.setStyleSheet(self.inactive_style)
        self.rentPushButton.setStyleSheet(self.inactive_style)
        self.paymentPushButton.setStyleSheet(self.inactive_style)
        self.emergencyPushButton.setStyleSheet(self.inactive_style)

        # Highlight the clicked button
        if index == 0:
            self.tenantPushButton.setStyleSheet(self.active_style)
        elif index == 1:
            self.roomPushButton.setStyleSheet(self.active_style)
        elif index == 2:
            self.rentPushButton.setStyleSheet(self.active_style)
        elif index == 3:
            self.paymentPushButton.setStyleSheet(self.active_style)
        elif index == 4:
            self.emergencyPushButton.setStyleSheet(self.active_style)

        self.load_data(index)

        self.columns = self.populator.columns
        self.SearchField.clear()
        for col in self.columns: self.SearchField.addItem(str(col), col)

# =========================
#    SEARCH N SORT FUNCS
# ==========

    def perform_search(self):
        if hasattr(self.populator, "full_data"): del self.populator.full_data
        search_key = str(self.SearchLineEdit.text())
        search_column = self.SearchField.currentData()
        self.populator.Populate_Table(self.table_name, self.widget, self.select_type, 1, search_column, search_key)

# ===========
#    SEARCH N SORT FUNCS
# =========================

    def load_data(self, index):
        table_mapping = {
                    0: ("Tenant", self.TenantTable, "Tenant"),
                    1: ("Room", self.RoomTable, None),
                    2: ("Rents", self.RentTable, "Rents/Pays"),
                    3: ("Pays", self.PaymentTable, "Rents/Pays"),
                    4: ("EmergencyContact", self.EmergencyTable, None)
                }
        self.table_name, self.widget, self.select_type = table_mapping.get(index)
        self.populator.Populate_Table(self.table_name, self.widget, self.select_type)

    def on_Add_clicked(self):
        current_widget_index = self.stackedWidget.currentIndex()

        if current_widget_index == 0:
            dialog = AddTenantDialog(self)
            if dialog.exec() == QDialog.Accepted:
                self.load_data(0)

        elif current_widget_index == 1:
            dialog = AddRoomDialog(self)
            if dialog.exec() == QDialog.accepted:
                self.load_data(1)

        elif current_widget_index == 2:
            dialog = AddRentDialog(self)
            if dialog.exec() == QDialog.accepted:
                self.load_data(2)

        elif current_widget_index == 3:
            dialog = AddPaymentDialog(self)
            if dialog.exec() == QDialog.accepted:
                self.load_data(3)

        elif current_widget_index == 4:
            dialog = AddEmergencyContactDialog(self)
            if dialog.exec() == QDialog.accepted:
                self.load_data(4)

    def onEditClicked(self):
        current_widget_index = self.stackedWidget.currentIndex()

        if current_widget_index == 0:
            dialog = editTenantDialog(self)
            if dialog.exec() == QDialog.Accepted:
                self.load_data(0)

        elif current_widget_index == 1:
            dialog = editRoomDialog(self)
            if dialog.exec() == QDialog.accepted:
                self.load_data(1)

        elif current_widget_index == 2:
            dialog = editRentDialog(self)
            if dialog.exec() == QDialog.accepted:
                self.load_data(2)

        # elif current_widget_index == 3:
        #     dialog = editPaymentDialog(self)
        #     if dialog.exec() == QDialog.accepted:
        #         self.load_data(3)

        elif current_widget_index == 4:
            dialog = editEmergencyContactDialog(self)
            if dialog.exec() == QDialog.accepted:
                self.load_data(4)
        
        
if __name__ == "__main__":
    connection = DatabaseConnector.get_connection()
    if connection is not None:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
        
    else:
        app = QApplication(sys.argv) 
        QMessageBox.critical(None, "Connection Error", "Could not establish connection with the Database.", QMessageBox.Ok)
        sys.exit(1)