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
from EDIT.editFunctions.editPaymentDialog import editPaymentDialog
from DATABASE.DB import DatabaseConnector
import math
from DATABASE.Functions.Populate import Populate
from PyQt5.QtCore import Qt, QDate


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.selector = Select()
        self.populator = Populate(self)

        self.button_base_style = """
        background-color: rgb(250, 255, 242); 
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

        self.tenantPushButton.clicked.connect(lambda: self.switch_tab(0))
        self.roomPushButton.clicked.connect(lambda: self.switch_tab(1))
        self.rentPushButton.clicked.connect(lambda: self.switch_tab(2))
        self.paymentPushButton.clicked.connect(lambda: self.switch_tab(3))
        self.emergencyPushButton.clicked.connect(lambda: self.switch_tab(4))

        self.AddpushButton.clicked.connect(self.on_Add_clicked)
        self.EditpushButton.clicked.connect(self.on_Edit_clicked)
        self.DeletepushButton.clicked.connect(self.on_Delete_clicked)

        self.RefreshpushButton.clicked.connect(lambda: self.load_data(self.index))
        self.SearchpushButton.clicked.connect(lambda: self.perform_search())

        self.switch_tab(0)

    def switch_tab(self, index):
        self.stackedWidget.setCurrentIndex(index)
        self.index = index

        # Reset all to inactive
        self.tenantPushButton.setStyleSheet(self.inactive_style)
        self.roomPushButton.setStyleSheet(self.inactive_style)
        self.rentPushButton.setStyleSheet(self.inactive_style)
        self.paymentPushButton.setStyleSheet(self.inactive_style)
        self.emergencyPushButton.setStyleSheet(self.inactive_style)

        # Highlight the clicked button
        if self.index == 0:
            self.tenantPushButton.setStyleSheet(self.active_style)
        elif self.index == 1:
            self.roomPushButton.setStyleSheet(self.active_style)
        elif self.index == 2:
            self.rentPushButton.setStyleSheet(self.active_style)
        elif self.index == 3:
            self.paymentPushButton.setStyleSheet(self.active_style)
        elif self.index == 4:
            self.emergencyPushButton.setStyleSheet(self.active_style)

        self.load_data(index)

# =========================
#    SEARCH N SORT FUNCS
# ==========

    def perform_search(self):
        if hasattr(self.populator, "full_data"): del self.populator.full_data
        search_key = str(self.SearchLineEdit.text())
        search_column = self.SearchField.currentData()
        self.populator.Populate_Table(table_name = self.table_name, table_widget = self.widget, select_type = self.select_type, search_column = search_column, search_key = search_key)

    def perform_sort(self, column_index):
        # Get the current table widget
        table = self.widget
        
        # Get the current sort order
        current_order = table.horizontalHeader().sortIndicatorOrder()
        table.sortItems(column_index, Qt.AscendingOrder if current_order == Qt.DescendingOrder else Qt.DescendingOrder)
        table.horizontalHeader().setSortIndicator(column_index, current_order)

# ===========
#    SEARCH N SORT FUNCS
# =========================

    def map_indextotable(self, index):
        table_mapping = {
                    0: ("Tenant", self.TenantTable, None),
                    1: ("Room", self.RoomTable, "Room"),
                    2: ("Rents", self.RentTable, "Rents"),
                    3: ("Pays", self.PaymentTable, "Pays"),
                    4: ("EmergencyContact", self.EmergencyTable, None)
                }
        return table_mapping.get(index)
        
    def load_data(self, index):
        
        if hasattr(self.populator, "full_data"): del self.populator.full_data
        
        self.table_name, self.widget, self.select_type = self.map_indextotable(index)
        self.populator.Populate_Table(self.table_name, self.widget, self.select_type)

        self.columns = self.populator.columns
        self.SearchField.clear()
        self.SearchLineEdit.clear()
        self.SearchField.addItem("Search All", None)
        for col in self.columns: 
            self.SearchField.addItem(str(col), col)
        # Connect header click events for sorting
        self.widget.horizontalHeader().sectionClicked.connect(self.perform_sort)

# =========================
#    CRUDL BUTTONS FUNCS
# ==========

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

    def on_Edit_clicked(self):
        current_widget_index = self.stackedWidget.currentIndex()

        if current_widget_index == 0:
            
            selectedItems = self.TenantTable.selectedItems()
            if not selectedItems:
                QMessageBox.warning(self, "No Selection", "Please select a tenant to edit.", QMessageBox.Ok)
                return
                
            selectedRow = self.TenantTable.currentRow()
            columnCount = self.TenantTable.columnCount()
            
            rowData = {
                self.TenantTable.horizontalHeaderItem(col).text(): self.TenantTable.item(selectedRow, col).text()
                for col in range(columnCount)
            }
            
            tenantIdItem = rowData["TenantID"]
            tenantEmailItem = rowData["Email"]
            tenantFirstNameItem = rowData["FirstName"]
            tenantMiddleNameItem = rowData["MiddleName"]
            tenantLastNameItem = rowData["LastName"]
            tenantSexItem = rowData["Sex"]
            tenantPhoneNumberItem = rowData["PhoneNumber"]
            tenantRoomNumberItem = rowData["RoomNumber"]

            dialog = editTenantDialog(self)
            dialog.ui.TenantIDLineEdit.setText(tenantIdItem)
            dialog.ui.FirstNameLineEdit.setText(tenantFirstNameItem)
            dialog.ui.MiddleNameLineEdit.setText(tenantMiddleNameItem)
            dialog.ui.LastNameLineEdit.setText(tenantLastNameItem)
            dialog.ui.EmailLineEdit.setText(tenantEmailItem)
            dialog.ui.PhoneNumberLineEdit.setText(tenantPhoneNumberItem)
            dialog.ui.SexComboBox.setCurrentText(tenantSexItem)
            dialog.ui.RoomNoComboBox.setCurrentText(tenantRoomNumberItem)
            
            self.TenantTable.clearSelection()

            if dialog.exec() == QDialog.Accepted:
                self.load_data(0)

        elif current_widget_index == 1:
            
            selectedItems = self.RoomTable.selectedItems()
            if not selectedItems:
                QMessageBox.warning(self, "No Selection", "Please select a tenant to edit.", QMessageBox.Ok)
                return
            
            selectedRow = self.RoomTable.currentRow()
            columnCount = self.RoomTable.columnCount()
            
            rowData = {
                self.RoomTable.horizontalHeaderItem(col).text(): self.RoomTable.item(selectedRow, col).text()
                for col in range(columnCount)
            }
            
            roomNumberItem = rowData["RoomNumber"]
            priceItem = rowData["Price"]
            tenantSexItem = rowData["TenantSex"]
            maximumCapacityItem = rowData["MaximumCapacity"]
            
            
            dialog = editRoomDialog(self)
            dialog.ui.RoomNumberLineEdit.setText(roomNumberItem)
            dialog.ui.PriceLineEdit.setText(priceItem)
            dialog.ui.TenantSexComboBox.setCurrentText(tenantSexItem)
            dialog.ui.MaxNoOccupantsLineEdit.setText(maximumCapacityItem)
            
            self.RoomTable.clearSelection()

            
            if dialog.exec() == QDialog.accepted:
                self.load_data(1)

        elif current_widget_index == 2:
            dialog = editRentDialog(self)
            if dialog.exec() == QDialog.accepted:
                self.load_data(2)

        elif current_widget_index == 3:
            dialog = editPaymentDialog(self)

            selectedItems = self.PaymentTable.selectedItems()
            if not selectedItems:
                QMessageBox.warning(self, "No Selection", "Please select a payment to edit.", QMessageBox.Ok)
                return
                
            selectedRow = self.PaymentTable.currentRow()
            columnCount = self.PaymentTable.columnCount()
            
            rowData = {
                self.PaymentTable.horizontalHeaderItem(col).text(): self.PaymentTable.item(selectedRow, col).text()
                for col in range(columnCount)
            }
            
            PayIDItem = rowData["PayID"]
            PayingTenantItem = rowData["PayingTenant"]
            PaidRoomItem = rowData["PaidRoom"]
            PaymentAmountItem = rowData["PaymentAmount"]
            PaymentDateItem = QDate.fromString(rowData["PaymentDate"], "yyyy-MM-dd")
            RemainingDueItem = rowData["RemainingDue"]

            dialog = editPaymentDialog(self)
            dialog.ui.PayingTenantIDComboBox.setCurrentText(PayingTenantItem)
            dialog.ui.RoomNumberComboBox.setCurrentText(PaidRoomItem)
            dialog.ui.PaymentAmountLineEdit.setText(PaymentAmountItem)
            dialog.ui.dateEdit.setDate(PaymentDateItem)
            dialog.ui.RemainingDue.setText(RemainingDueItem)
            
            dialog.PayID = PayIDItem
            dialog.InitialAmount = float(PaymentAmountItem)
            
            self.PaymentTable.clearSelection()

            if dialog.exec() == QDialog.accepted:
                self.load_data(3)

        elif current_widget_index == 4:
            dialog = editEmergencyContactDialog(self)
            if dialog.exec() == QDialog.accepted:
                self.load_data(4)
                
    # still working on this
    def on_Delete_clicked(self):
        current_widget_index = self.stackedWidget.currentIndex()
        table_name, table_widget, _ = self.map_indextotable(current_widget_index)

        selected_row = table_widget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a row to delete.", QMessageBox.Ok)
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete the selected record?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            primary_key_column = self.populator.primary_key  # this assumes `Populate` has set this

            if not primary_key_column:
                QMessageBox.critical(self, "Error", "No primary key found for the table.", QMessageBox.Ok)
                return

            primary_key_value = table_widget.item(selected_row, 0).text()  # assumes PK is in the first column
            delete_query = f"DELETE FROM {table_name} WHERE {primary_key_column} = %s"

            try:
                self.selector.cursor.execute(delete_query, (primary_key_value,))
                self.selector.connection.commit()
                QMessageBox.information(self, "Deleted", "Record deleted successfully.", QMessageBox.Ok)
                self.load_data(current_widget_index)
            except Exception as e:
                QMessageBox.critical(self, "Delete Failed", f"An error occurred:\n{e}", QMessageBox.Ok)



# ===========
#    CRUDL BUTTONS FUNCS
# =========================
        
if __name__ == "__main__":
    connection = DatabaseConnector.getConnection()
    if connection is not None:
        app = QApplication(sys.argv)    
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
        
    else:
        app = QApplication(sys.argv) 
        QMessageBox.critical(None, "Connection Error", "Could not establish connection with the Database.", QMessageBox.Ok)
        sys.exit(1)

    