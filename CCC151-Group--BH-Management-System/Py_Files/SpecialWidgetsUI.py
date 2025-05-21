from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from PyQt5.QtWidgets import QStyledItemDelegate, QStyle
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRect, QObject, pyqtSignal

from INFO.TenantInfoDialog import TenantInfoDialog

class ClickablePageLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("color: #630014; border: none; background-color: transparent;")
        self.setFixedWidth(25)
        self.setFixedHeight(25)

    def mousePressEvent(self, event):
        self.clicked.emit()

class PaginationTable(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(PaginationTable, self).__init__(parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("""
            QTableWidget::item:selected {
                background-color: #d9796f;  /* Highlight color */
                color: #ffffff;             /* Text color when selected */
            }
        """)

class IconClickEmitter(QObject):
    iconClicked = pyqtSignal(int)

class CustomRowDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.icon = QPixmap(r"C:/Users/joshu/Documents/2ND_YEAR_NOTES/CC151/SISTONE/CCC151-Group--BH-Management-System/CCC151-Group--BH-Management-System/res/i-blue.png")
        self.emitter = IconClickEmitter()

    def paint(self, painter, option, index):
        # Draw default item first
        super().paint(painter, option, index)

        # Check: selected + first column
        if option.state & QStyle.State_Selected and index.column() == 0:
            self.icon_rect = QRect(
                option.rect.left() + 6,  # left padding
                option.rect.top() + (option.rect.height() - 32) // 2,  # vertical center
                32, 32
            )
            painter.drawPixmap(self.icon_rect, self.icon)

    def editorEvent(self, event, model, option, index):
        if index.column() != 0:
            return False

        if event.type() == event.MouseButtonRelease and self.icon_rect.contains(event.pos()):
                tenant_id = index.data()  
                print(f"Icon clicked on tenant: {tenant_id}")
                self.emitter.iconClicked.emit(tenant_id)
                return True

        return False

    def infoClicked(self, mw):
        self.mw = mw       
        current_widget_index = self.mw.stackedWidget.currentIndex()

        if current_widget_index == 0:
            dialog = TenantInfoDialog(self.mw)
            dialog.exec()

        # elif current_widget_index == 1:
        #     dialog = AddRoomDialog(self)
        #     if dialog.exec() == QDialog.accepted:
        #         self.load_data(1)

        # elif current_widget_index == 2:
        #     dialog = AddRentDialog(self)
        #     if dialog.exec() == QDialog.accepted:
        #         self.load_data(2)

        # elif current_widget_index == 3:
        #     dialog = AddPaymentDialog(self)
        #     if dialog.exec() == QDialog.accepted:
        #         self.load_data(3)

        # elif current_widget_index == 4:
        #     dialog = AddEmergencyContactDialog(self)
        #     if dialog.exec() == QDialog.accepted:
        #         self.load_data(4)