# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Kristelle\Documents\CCC151-Group Project\CCC151-Group--BH-Management-System\UI_Files\MainUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import SpecialWidgetsUI


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1559, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 70, 1511, 771))
        self.frame.setStyleSheet("background-color: rgb(240, 240, 240);\n"
"border: 2px solid #800000;\n"
"border-radius: 6px;\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")


# =========================
#    SEARCHNSORT BUTTONS
# ==========

        # search
        self.SearchLineEdit = QtWidgets.QLineEdit(self.frame)
        self.SearchLineEdit.setGeometry(QtCore.QRect(720, 20, 561, 31))
        self.SearchLineEdit.setObjectName("SearchLineEdit")
        self.SearchpushButton = QtWidgets.QPushButton(self.frame)
        self.SearchpushButton.setGeometry(QtCore.QRect(1290, 20, 91, 31))
        self.SearchpushButton.setStyleSheet("background-color: #00796B;\n"
"color: white;\n"
"font-family: \"Cal Sans\", sans-serif;\n"
"font-weight: 500;\n"
"font-size: 16px;\n"
"border: none;\n"
"border-radius: 4px;\n"
"padding: 3px 6px;\n"
"")
        self.SearchpushButton.setObjectName("SearchpushButton")
        self.SearchField = QtWidgets.QComboBox(self.frame)
        self.SearchField.setGeometry(QtCore.QRect(570, 20, 151, 31))
        self.SearchField.setObjectName("SearchField")

        # sort
        # self.SortWith = QtWidgets.QComboBox(self.frame)
        # self.SortWith.setGeometry(QtCore.QRect(570, 20, 151, 31))
        # self.SortWith.setObjectName("SortWith")

        # self.SortBy = QtWidgets.QComboBox(self.frame)
        # self.SortBy.setGeometry(QtCore.QRect(570, 20, 151, 31))
        # self.SortBy.setObjectName("SortBy")

# ===========
#    SEARCHNSORT BUTTONS
# =========================

        self.RefreshpushButton = QtWidgets.QPushButton(self.frame)
        self.RefreshpushButton.setGeometry(QtCore.QRect(1390, 20, 91, 31))
        self.RefreshpushButton.setStyleSheet("background-color: rgb(255, 255, 253);\n"
"border: 1px solid #660000; \n"
"border-radius: 6px;\n"
"color: #00796B;\n"
"font-family: \"Cal Sans\", sans-serif;\n"
"font-weight: 500;\n"
"font-size: 16px;\n"
"padding: 3px 6px;\n"
"")
        self.RefreshpushButton.setObjectName("RefreshpushButton")
        self.AddpushButton = QtWidgets.QPushButton(self.frame)
        self.AddpushButton.setGeometry(QtCore.QRect(1380, 727, 93, 31))
        self.AddpushButton.setStyleSheet("background-color: #388E3C; /* Darker green */\n"
"color: white;\n"
"font-family: \"Cal Sans\", sans-serif;\n"
"font-weight: 700; /* Bold */\n"
"font-size: 16px;\n"
"border: none;\n"
"border-radius: 4px;\n"
"padding: 6px 12px;\n"
"")
        self.AddpushButton.setObjectName("AddpushButton")
        self.EditpushButton = QtWidgets.QPushButton(self.frame)
        self.EditpushButton.setGeometry(QtCore.QRect(1280, 727, 93, 31))
        self.EditpushButton.setStyleSheet("background-color: #1565C0; /* Darker blue */\n"
"color: white;\n"
"font-family: \"Cal Sans\", sans-serif;\n"
"font-weight: 700; /* Bold */\n"
"font-size: 16px;\n"
"border: none;\n"
"border-radius: 4px;\n"
"padding: 6px 12px;\n"
"")
        self.EditpushButton.setObjectName("EditpushButton")
        self.DeletepushButton = QtWidgets.QPushButton(self.frame)
        self.DeletepushButton.setGeometry(QtCore.QRect(130, 727, 93, 31))
        self.DeletepushButton.setStyleSheet("background-color: #C62828; /* Darker red */\n"
"color: white;\n"
"font-family: \"Cal Sans\", sans-serif;\n"
"font-weight: 700; /* Bold */\n"
"font-size: 16px;\n"
"border: none;\n"
"border-radius: 4px;\n"
"padding: 6px 12px;\n"
"")
        self.DeletepushButton.setObjectName("DeletepushButton")

# =========================
#    PAGINATION BUTTONS
# ==========

        # Initialize and  a frame to hold the pagination buttons
        self.paginationFrame = QtWidgets.QFrame(self.frame)
        self.paginationFrame.setGeometry(QtCore.QRect(460, 727, 550, 31)) # in between delete and add
        self.paginationFrame.setStyleSheet("border: none; background-color: transparent;")
        self.paginationFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.paginationFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.paginationFrame.setObjectName("paginationFrame")

        # Grid to even space and hold buttons
        self.paginationButtonsGrid = QtWidgets.QGridLayout(self.paginationFrame)
        self.paginationButtonsGrid.setContentsMargins(100, 0, 100, 0)  
        self.paginationButtonsGrid.setHorizontalSpacing(2) 
        self.paginationButtonsGrid.setAlignment(QtCore.Qt.AlignCenter)
        self.paginationFrame.setLayout(self.paginationButtonsGrid)

        # Jump combobox
        self.jumpFrame = QtWidgets.QFrame(self.frame)
        self.jumpFrame.setGeometry(QtCore.QRect(1050, 727, 200, 31))
        self.jumpFrame.setStyleSheet("border: none; background-color: transparent;")
        self.jumpFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.jumpFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.jumpFrame.setObjectName("jumpFrame")

        self.jumpFrameGrid = QtWidgets.QGridLayout(self.jumpFrame)
        self.jumpFrameGrid.setContentsMargins(10, 0, 10, 0)  
        self.jumpFrameGrid.setHorizontalSpacing(2) 
        self.jumpFrameGrid.setAlignment(QtCore.Qt.AlignCenter)
        self.jumpFrame.setLayout(self.jumpFrameGrid)

        self.jumpLabel_Page = QtWidgets.QLabel("Page", self.jumpFrame)
        self.jumpFrameGrid.addWidget(self.jumpLabel_Page, 0, 0)

        self.jumpBox = QtWidgets.QComboBox(self.jumpFrame)
        self.jumpBox.setStyleSheet("background-color: rgb(250, 255, 242); border: 3px")
        self.jumpBox.setFixedWidth(50)
        self.jumpFrameGrid.addWidget(self.jumpBox, 0, 1)

        self.jumpLabel_of = QtWidgets.QLabel(" of ", self.jumpFrame)
        self.jumpFrameGrid.addWidget(self.jumpLabel_of, 0, 2)

        self.jumpLabel_totalpages = QtWidgets.QLabel(self.jumpFrame)
        self.jumpFrameGrid.addWidget(self.jumpLabel_totalpages, 0, 3)


# ===========
#    PAGINATION BUTTONS
# =========================

# =========================
#     TABLE PAGES
# ==========

        # Initialize table pages
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame)
        self.stackedWidget.setGeometry(QtCore.QRect(110, 60, 1381, 661))
        self.stackedWidget.setObjectName("stackedWidget")

        # Tenant Table page
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.TenantTable = SpecialWidgetsUI.PaginationTable(self.page_1)
        self.TenantTable.setGeometry(QtCore.QRect(10, 10, 1361, 641))
        self.TenantTable.setObjectName("TenantTable")
        self.TenantTable.setColumnCount(0)
        self.TenantTable.setRowCount(0)
        self.stackedWidget.addWidget(self.page_1)

        # Room Table page
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.RoomTable = SpecialWidgetsUI.PaginationTable(self.page_2)
        self.RoomTable.setGeometry(QtCore.QRect(10, 10, 1361, 641))
        self.RoomTable.setObjectName("RoomTable")
        self.RoomTable.setColumnCount(0)
        self.RoomTable.setRowCount(0)
        self.stackedWidget.addWidget(self.page_2)

        # Rent Table page
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.RentTable = SpecialWidgetsUI.PaginationTable(self.page_3)
        self.RentTable.setGeometry(QtCore.QRect(10, 10, 1361, 641))
        self.RentTable.setObjectName("RentTable")
        self.RentTable.setColumnCount(0)
        self.RentTable.setRowCount(0)
        self.stackedWidget.addWidget(self.page_3)

        # Payment Table page
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.PaymentTable = SpecialWidgetsUI.PaginationTable(self.page_4)
        self.PaymentTable.setGeometry(QtCore.QRect(10, 10, 1361, 641))
        self.PaymentTable.setObjectName("PaymentTable")
        self.PaymentTable.setColumnCount(0)
        self.PaymentTable.setRowCount(0)
        self.stackedWidget.addWidget(self.page_4)

        # Emergency Contact Table page
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.EmergencyTable = SpecialWidgetsUI.PaginationTable(self.page_5)
        self.EmergencyTable.setGeometry(QtCore.QRect(10, 10, 1361, 641))
        self.EmergencyTable.setObjectName("EmergencyTable")
        self.EmergencyTable.setColumnCount(0)
        self.EmergencyTable.setRowCount(0)
        self.stackedWidget.addWidget(self.page_5)

# ===========
#     TABLE PAGES
# =========================

        self.tenantPushButton = QtWidgets.QPushButton(self.frame)
        self.tenantPushButton.setGeometry(QtCore.QRect(10, 60, 91, 41))
        self.tenantPushButton.setStyleSheet("background-color: rgb(250, 255, 242); /* Soft light green background */\n"
"border: 1px solid #660000; /* Darker maroon border */\n"
"border-radius: 4px;\n"
"padding: 5px;\n"
"font-family: \'Roboto\', sans-serif;\n"
"font-weight: 500; /* Normal weight */\n"
"font-style: normal;\n"
"font-size: 16px;\n"
"color: #800000; /* Maroon text color */\n"
"")
        self.tenantPushButton.setObjectName("tenantPushButton")
        self.roomPushButton = QtWidgets.QPushButton(self.frame)
        self.roomPushButton.setGeometry(QtCore.QRect(10, 110, 91, 41))
        self.roomPushButton.setStyleSheet("background-color: rgb(250, 255, 242); /* Soft light green background */\n"
"border: 1px solid #660000; /* Darker maroon border */\n"
"border-radius: 4px;\n"
"padding: 5px;\n"
"font-family: \'Roboto\', sans-serif;\n"
"font-weight: 500; /* Normal weight */\n"
"font-style: normal;\n"
"font-size: 16px;\n"
"color: #800000; /* Maroon text color */\n"
"")
        self.roomPushButton.setObjectName("roomPushButton")
        self.rentPushButton = QtWidgets.QPushButton(self.frame)
        self.rentPushButton.setGeometry(QtCore.QRect(10, 160, 91, 41))
        self.rentPushButton.setStyleSheet("background-color: rgb(250, 255, 242); /* Soft light green background */\n"
"border: 1px solid #660000; /* Darker maroon border */\n"
"border-radius: 4px;\n"
"padding: 5px;\n"
"font-family: \'Roboto\', sans-serif;\n"
"font-weight: 500; /* Normal weight */\n"
"font-style: normal;\n"
"font-size: 16px;\n"
"color: #800000; /* Maroon text color */\n"
"")
        self.rentPushButton.setObjectName("rentPushButton")
        self.paymentPushButton = QtWidgets.QPushButton(self.frame)
        self.paymentPushButton.setGeometry(QtCore.QRect(10, 210, 91, 41))
        self.paymentPushButton.setStyleSheet("background-color: rgb(250, 255, 242); /* Soft light green background */\n"
"border: 1px solid #660000; /* Darker maroon border */\n"
"border-radius: 4px;\n"
"padding: 5px;\n"
"font-family: \'Roboto\', sans-serif;\n"
"font-weight: 500; /* Normal weight */\n"
"font-style: normal;\n"
"font-size: 16px;\n"
"color: #800000; /* Maroon text color */\n"
"\n"
"")
        self.paymentPushButton.setObjectName("paymentPushButton")
        self.emergencyPushButton = QtWidgets.QPushButton(self.frame)
        self.emergencyPushButton.setGeometry(QtCore.QRect(10, 260, 91, 41))
        self.emergencyPushButton.setStyleSheet("background-color: rgb(250, 255, 242); /* Soft light green background */\n"
"border: 1px solid #660000; /* Darker maroon border */\n"
"border-radius: 4px;\n"
"padding: 5px;\n"
"font-family: \'Roboto\', sans-serif;\n"
"font-weight: 500; /* Normal weight */\n"
"font-style: normal;\n"
"font-size: 14px;\n"
"color: #800000; /* Maroon text color */\n"
"\n"
"")
        self.emergencyPushButton.setObjectName("emergencyPushButton")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(30, 10, 1511, 61))
        self.frame_2.setStyleSheet("background-color: #800000;  /* Maroon background */\n"
"                border: 1px solid #660000;  /* Darker maroon border */\n"
"                border-radius: 4px;\n"
"                padding: 5px;\n"
"                font-family: \'Times New Roman\', serif;  /* Formal font */\n"
"                font-size: 14px;\n"
"                color: white;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 1471, 41))
        self.label_2.setStyleSheet("background-color: rgb(250, 255, 242); /* Soft light green background */\n"
"    border: none;\n"
"    padding: 2px; \n"
"    font-family: \'Cal Sans\', sans-serif;\n"
"    font-weight: 800;\n"
"    font-style: normal; \n"
"    font-size: 34px;\n"
"    color: #800000; /* Maroon text color */\n"
"    text-align: center; \n"
"    qproperty-alignment: \'AlignCenter\'; \n"
"    letter-spacing: 5px; \n"
"    ")
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1559, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sistore Boarding House Management System"))
        self.SearchpushButton.setText(_translate("MainWindow", "Search"))
        self.RefreshpushButton.setText(_translate("MainWindow", "Refresh"))
        self.AddpushButton.setText(_translate("MainWindow", "Add"))
        self.EditpushButton.setText(_translate("MainWindow", "Edit"))
        self.DeletepushButton.setText(_translate("MainWindow", "Delete"))
        self.tenantPushButton.setText(_translate("MainWindow", "Tenant"))
        self.roomPushButton.setText(_translate("MainWindow", "Room"))
        self.rentPushButton.setText(_translate("MainWindow", "Rent Data"))
        self.paymentPushButton.setText(_translate("MainWindow", "Payment"))
        self.emergencyPushButton.setText(_translate("MainWindow", "Emergency"))
        self.label_2.setText(_translate("MainWindow", "Sistore Boarding House Management System"))
