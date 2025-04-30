import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QTableWidget
from ADD.AddTenantDialog import AddTenantDialog
from ADD.AddRoomDialog import AddRoomDialog
from ADD.AddRentDialog import AddRentDialog
from ADD.AddPaymentDialog import AddPaymentDialog
from ADD.AddEmergencyContactDialog import AddEmergencyContactDialog
from MainUI import Ui_MainWindow
from DATABASE.DB import DatabaseConnector  
from DATABASE.Functions.Select import Select

# =================
#   MAIN WINDOW
# =================

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.AddpushButton.clicked.connect(self.on_Add_clicked)
        self.tenantPushButton.clicked.connect(lambda: self.switch_tab(0))
        self.roomPushButton.clicked.connect(lambda: self.switch_tab(1))
        self.rentPushButton.clicked.connect(lambda: self.switch_tab(2))
        self.paymentPushButton.clicked.connect(lambda: self.switch_tab(3))
        self.emergencyPushButton.clicked.connect(lambda: self.switch_tab(4))

        self.table_widget = QTableWidget()
        self.switch_tab(0)

    def switch_tab(self, index):
        self.stackedWidget.setCurrentIndex(index)

        table_mapping = {
            0: ("Tenant", self.TenantTable, 0),
            1: ("Room", self.RoomTable, 1),
            2: ("Rents", self.RentTable, 2),
            3: ("Pays", self.PaymentTable, 3),
            4: ("EmergencyContact", self.EmergencyTable, 4)
        }
        table_name, widget, select_type = table_mapping.get(index)
        self.Populate_Table(table_name, widget, select_type)

    def Populate_Table(self, table_name, table_widget, select_type):
        selector = Select()
        data, columns = selector.SelectQuery(table_name, select_type)
        
        table_widget.clear()
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(columns))
        table_widget.setHorizontalHeaderLabels(columns)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell in enumerate(row_data):
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(cell)))

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
