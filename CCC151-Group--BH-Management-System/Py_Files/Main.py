import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QWidget, QGridLayout, QVBoxLayout, QFrame
from PyQt5.QtCore import QRect
import SpecialWidgetsUI
from ADD.AddTenantDialog import AddTenantDialog
from ADD.AddRoomDialog import AddRoomDialog
from ADD.AddRentDialog import AddRentDialog
from ADD.AddPaymentDialog import AddPaymentDialog
from ADD.AddEmergencyContactDialog import AddEmergencyContactDialog
from MainUI import Ui_MainWindow
from DATABASE.DB import DatabaseConnector  
from DATABASE.Functions.Select import Select
from EDIT.editFunctions.editTenantDialog import editTenantDialog
import math


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Sorting enabled for all tables
        self.TenantTable.setSortingEnabled(True)
        self.RoomTable.setSortingEnabled(True)
        self.RentTable.setSortingEnabled(True)
        self.PaymentTable.setSortingEnabled(True)
        self.EmergencyTable.setSortingEnabled(True)

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

        table_mapping = {
            0: ("Tenant", self.TenantTable, 0),
            1: ("Room", self.RoomTable, 1),
            2: ("Rents", self.RentTable, 2),
            3: ("Pays", self.PaymentTable, 3),
            4: ("EmergencyContact", self.EmergencyTable, 4)
        }
        self.table_name, self.widget, self.select_type = table_mapping.get(index)
        self.Populate_Table(self.table_name, self.widget, self.select_type)


# =========================
#    PAGINATION TABLE
# ==========

    def Populate_Table(self, table_name, table_widget, select_type, current_page = 1):

        # Fetch ALL data with query, store for faster loading in page change...
        selector = Select()
        if not hasattr(self, "full_data"):
            self.full_data, self.columns = selector.SelectQuery(table_name, select_type)
        # Tradeoff: Takes up memory for faster loading(users want their current job done than more jobs done)

            # Configure pages information according to taste
            self.rows_per_page  = 12
            self.total_pages    = math.ceil(len(self.full_data)/self.rows_per_page)
        
        self.current_page = current_page

        start_index             = (current_page-1) * self.rows_per_page
        end_index               = start_index + self.rows_per_page
        self.page_data          = self.full_data[start_index:end_index]
        
        # refresh table widget(data is not refreshed)
        table_widget.clear()
        table_widget.setRowCount(len(self.page_data))
        table_widget.setColumnCount(len(self.columns))
        table_widget.setHorizontalHeaderLabels(self.columns)

        # load the data in TO EDIT: ignore first column(built-in id of widget)
        for row_idx, row_data in enumerate(self.page_data):
            for col_idx, cell in enumerate(row_data):
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(cell)))

        # array of pointers to the created buttons. I say buttons but they're actually modified labels my dudes
        while self.paginationButtonsGrid.count():
            item = self.paginationButtonsGrid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.PaginationButts = []
        buttCol = 0

        self.prevTenButt    = SpecialWidgetsUI.ClickablePageLabel("<<", self.paginationFrame)
        self.prevTenButt.clicked.connect(lambda: self.PrevTenPage())
        self.paginationButtonsGrid.addWidget(self.prevTenButt, 0, buttCol)
        buttCol += 1
        self.PaginationButts.append(self.prevTenButt)

        self.prevButt       = SpecialWidgetsUI.ClickablePageLabel("<", self.paginationFrame)
        self.prevButt.clicked.connect(lambda: self.PrevPage())
        self.paginationButtonsGrid.addWidget(self.prevButt, 0, buttCol)
        buttCol += 1
        self.PaginationButts.append(self.prevButt)

        for i in range(1, self.total_pages + 1):
            if (i <= 11 and self.current_page < 6) or i == self.current_page or ((i >= self.current_page - 5) and (i <= self.current_page + 5)) or (i >= self.total_pages - 10 and self.current_page > self.total_pages - 5):
                # print(f"Creating button for page {i}")
                numButt     = SpecialWidgetsUI.ClickablePageLabel(f"{i}", self.paginationFrame)
                numButt.clicked.connect(lambda x=i: self.GotoPage(x))
                self.paginationButtonsGrid.addWidget(numButt, 0, buttCol)
                buttCol += 1
                self.PaginationButts.append(numButt)

        self.nextButt       = SpecialWidgetsUI.ClickablePageLabel(">", self.paginationFrame)
        self.nextButt.clicked.connect(lambda: self.NextPage())
        self.paginationButtonsGrid.addWidget(self.nextButt, 0, buttCol)
        buttCol += 1
        self.PaginationButts.append(self.nextButt)

        self.nextTenButt    = SpecialWidgetsUI.ClickablePageLabel(">>", self.paginationFrame)
        self.nextTenButt.clicked.connect(lambda: self.NextTenPage())
        self.paginationButtonsGrid.addWidget(self.nextTenButt, 0, buttCol)
        buttCol += 1
        self.PaginationButts.append(self.nextTenButt)
        
        self.prevButt.setEnabled(self.current_page > 1)
        self.nextButt.setEnabled(self.current_page < self.total_pages)
        self.prevTenButt.setEnabled(self.current_page > 10)
        self.nextTenButt.setEnabled(self.current_page + 10 < self.total_pages)
    
    def NextPage(self):
        self.current_page += 1
        self.Populate_Table(self.table_name, self.widget, self.select_type, self.current_page)

    def NextTenPage(self):
        if self.current_page + 10 < self.total_pages:
            self.current_page += 10
        else: 
            self.current_page = self.total_pages
        self.Populate_Table(self.table_name, self.widget, self.select_type, self.current_page)

    def PrevPage(self):
        self.current_page -= 1
        self.Populate_Table(self.table_name, self.widget, self.select_type, self.current_page)

    def PrevTenPage(self):
        if self.current_page - 10 >= 1:
            self.current_page -= 10
        else:
            self.current_page = 1
        self.Populate_Table(self.table_name, self.widget, self.select_type, self.current_page)

    def GotoPage(self, page):
        self.Populate_Table(self.table_name, self.widget, self.select_type, page)

# ===========
#    PAGINATION TABLE
# =========================

    def on_Add_clicked(self):
        current_widget_index = self.stackedWidget.currentIndex()

        if current_widget_index == 0:
            dialog = AddTenantDialog(self)
            if dialog.exec() == QDialog.Accepted:
                self.load_tenant_data()

        elif current_widget_index == 1:
            dialog = AddRoomDialog(self)
            if dialog.exec() == QDialog.Accepted:
                self.load_room_data()

        elif current_widget_index == 2:
            dialog = AddRentDialog(self)
            if dialog.exec() == QDialog.Accepted:
                self.load_rent_data()

        elif current_widget_index == 3:
            dialog = AddPaymentDialog(self)
            if dialog.exec() == QDialog.Accepted:
                self.load_payment_data()

        elif current_widget_index == 4:
            dialog = AddEmergencyContactDialog(self)
            if dialog.exec() == QDialog.Accepted:
                self.load_emergency_data()

    def onEditClicked(self):
        dialog = editTenantDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.load_emergency_data()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())