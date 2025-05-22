from PyQt5 import QtCore, QtGui, QtWidgets

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
res_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../res'))
icon_path = os.path.join(res_folder, 'i-blue.png')

from PyQt5.QtWidgets import QStyledItemDelegate, QStyle
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRect, QObject, pyqtSignal

from INFO.TenantInfoDialog import TenantInfoDialog
from INFO.RoomInfoDialog import RoomInfoDialog


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
        self.icon = QPixmap(icon_path)
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
                self.row_id = index.data()  
                print(f"Icon clicked on: {self.row_id}")
                self.emitter.iconClicked.emit(self.row_id)
                return True

        return False

    def infoClicked(self, mw):
        self.mw = mw       
        current_widget_index = self.mw.stackedWidget.currentIndex()

        if current_widget_index == 0:
            dialog = TenantInfoDialog(self.mw, self.row_id)
            dialog.exec()

        elif current_widget_index == 1:
            dialog = RoomInfoDialog(self.mw, self.row_id)
            dialog.exec()