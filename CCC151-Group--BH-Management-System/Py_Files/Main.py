import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QTableWidget, QFrame, QPushButton, QLayout, QVBoxLayout
from ADD.AddTenantDialog import AddTenantDialog
from ADD.AddRoomDialog import AddRoomDialog
from ADD.AddRentDialog import AddRentDialog
from ADD.AddPaymentDialog import AddPaymentDialog
from ADD.AddEmergencyContactDialog import AddEmergencyContactDialog
from MainUI import Ui_MainWindow
from DATABASE.DB import DatabaseConnector  
from DATABASE.Functions.Select import Select
import math

# =================
#   MAIN WINDOW
# =================

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

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
        table_name, widget, select_type = table_mapping.get(index)
        self.Populate_Table(table_name, widget, select_type)

    def Populate_Table(self, table_name, table_widget, select_type, current_page = 1):
        
        # Fetch ALL data with query, store for faster loading in page change...
        selector = Select()
        if not hasattr(self, "full_data"):
            self.full_data, self.columns = selector.SelectQuery(table_name, select_type)
        # Tradeoff: Takes up memory for faster loading(users want their current job done than more jobs done)

            # Configure pages information according to taste
            self.rows_per_page  = 12
            self.total_pages    = math.ceil(len(self.full_data)/self.rows_per_page)

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


        self.button = QPushButton('Click Me', self)

        # Connect the button to an action (slot)
        self.button.clicked.connect(self.on_button_click)

    # Define what happens when the button is clicked
    def on_button_click(self):
        print("Button clicked!")

    def on_Add_clicked(self):
        current_widget_index = self.stackedWidget.currentIndex()

        if current_widget_index == 0:
            dialog = AddTenantDialog(self)
            if dialog.exec() == QDialog.Accepted:
                pass  # Insert logic

        elif current_widget_index == 1:
            dialog = AddRoomDialog(self)
            if dialog.exec() == QDialog.Accepted:
                pass

        elif current_widget_index == 2:
            dialog = AddRentDialog(self)
            if dialog.exec() == QDialog.Accepted:
                pass

        elif current_widget_index == 3:
            dialog = AddPaymentDialog(self)
            if dialog.exec() == QDialog.Accepted:
                pass

        elif current_widget_index == 4:
            dialog = AddEmergencyContactDialog(self)
            if dialog.exec() == QDialog.Accepted:
                pass

# =================
#   MAIN WINDOW
# =================


# =================
#   MAIN WINDOW
# =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
