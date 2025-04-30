import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from ADD.AddTenantDialog import AddTenantDialog
from ADD.AddRoomDialog import AddRoomDialog
from ADD.AddRentDialog import AddRentDialog
from ADD.AddPaymentDialog import AddPaymentDialog
from ADD.AddEmergencyContactDialog import AddEmergencyContactDialog
from MainUI import Ui_MainWindow


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
