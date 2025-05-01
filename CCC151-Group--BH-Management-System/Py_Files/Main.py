import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QTableWidget
>>>>>>> dd22bb28b60a82b20a30c79905d568268d294b52
from ADD.AddTenantDialog import AddTenantDialog
from ADD.AddRoomDialog import AddRoomDialog
from ADD.AddRentDialog import AddRentDialog
from ADD.AddPaymentDialog import AddPaymentDialog
from ADD.AddEmergencyContactDialog import AddEmergencyContactDialog
from MainUI import Ui_MainWindow
from DATABASE.DB import DatabaseConnector  
from DATABASE.Functions.Select import Select
from EDIT.editFunctions.editTenantDialog import editTenantDialog

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

<<<<<<< HEAD
=======
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

    def switch_tab(self, index):
        self.stackedWidget.setCurrentIndex(index)

    def on_Add_clicked(self):
        current_widget_index = self.stackedWidget.currentIndex()
        print("Current stacked widget index:", current_widget_index)  # Debugging line to check the current index

        if current_widget_index == 0:  # Tenant tab
            print("Opening Tenant Dialog")
            dialog = AddTenantDialog(self)
            if dialog.exec() == QDialog.Accepted:
                print("Tenant dialog accepted")
                # collect fields from the dialog
                # call your insertTenantToDatabase()
                pass

        elif current_widget_index == 1:  # Room tab
            print("Opening Room Dialog")
            dialog = AddRoomDialog(self)
            if dialog.exec() == QDialog.Accepted:
                print("Room dialog accepted")
                # collect fields and insert
                pass

        elif current_widget_index == 2:  # Rent tab
            print("Opening Rent Dialog")
            dialog = AddRentDialog(self)
            if dialog.exec() == QDialog.Accepted:
                print("Rent dialog accepted")
                # collect fields and insert
                pass

        elif current_widget_index == 3:  # Payment tab
            print("Opening Payment Dialog")
            dialog = AddPaymentDialog(self)
            if dialog.exec() == QDialog.Accepted:
                print("Payment dialog accepted")
                # collect fields and insert
                pass

        elif current_widget_index == 4:  # Emergency tab
            print("Opening Emergency Dialog")
            dialog = AddEmergencyContactDialog(self)
            if dialog.exec() == QDialog.Accepted:
                print("Emergency dialog accepted")
                # collect fields and insert
                pass

<<<<<<< HEAD
    def switch_tab(self, index):
        self.stackedWidget.setCurrentIndex(index)

    def on_Add_clicked(self):
        current_widget_index = self.stackedWidget.currentIndex()
        print("Current stacked widget index:", current_widget_index)  # Debugging line to check the current index

        if current_widget_index == 0:  # Tenant tab
            print("Opening Tenant Dialog")
            dialog = AddTenantDialog(self)
            if dialog.exec() == QDialog.Accepted:
                print("Tenant dialog accepted")
                # collect fields from the dialog
                # call your insertTenantToDatabase()
                pass

        elif current_widget_index == 1:  # Room tab
            print("Opening Room Dialog")
            dialog = AddRoomDialog(self)
            if dialog.exec() == QDialog.Accepted:
                print("Room dialog accepted")
                # collect fields and insert
                pass

        elif current_widget_index == 2:  # Rent tab
            print("Opening Rent Dialog")
            dialog = AddRentDialog(self)
            if dialog.exec() == QDialog.Accepted:
                print("Rent dialog accepted")
                # collect fields and insert
                pass

        elif current_widget_index == 3:  # Payment tab
            print("Opening Payment Dialog")
            dialog = AddPaymentDialog(self)
            if dialog.exec() == QDialog.Accepted:
                print("Payment dialog accepted")
                # collect fields and insert
                pass

        elif current_widget_index == 4:  # Emergency tab
            print("Opening Emergency Dialog")
            dialog = AddEmergencyContactDialog(self)
            if dialog.exec() == QDialog.Accepted:
                print("Emergency dialog accepted")
                # collect fields and insert
                pass

=======
        self.table_widget = QTableWidget()
        self.switch_tab(0)
        # self.load_data_from_db("Tenant", self.table_widget)

    def switch_tab(self, index):
        self.stackedWidget.setCurrentIndex(index)

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
            0: ("Tenant", self.TenantTable),
            1: ("Room", self.RoomTable),
            2: ("Rents", self.RentTable),
            3: ("Pays", self.PaymentTable),
            4: ("EmergencyContact", self.EmergencyTable)
        }
        table_name, widget = table_mapping.get(index)
        self.load_data_from_db(table_name, widget)

    def load_data_from_db(self, table_name, table_widget):
        selector = Select()
        data = selector.SelectQuery(table_name)
        
        # Fetch column names
        conn = DatabaseConnector.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [col[0] for col in cursor.fetchall()]
        
        # Load into widget
        self.load_table_to_widget(table_widget, data, columns)

    def load_table_to_widget(self, table_widget, data, columns):
        table_widget.setSortingEnabled(False)  # Disable sorting while updating
        table_widget.clear()
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(columns))
        table_widget.setHorizontalHeaderLabels(columns)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell in enumerate(row_data):
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(cell)))

        table_widget.setSortingEnabled(True)

    def onEditClicked(self):
        dialog = editTenantDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.load_emergency_data()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
