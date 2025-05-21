from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from PyQt5.QtWidgets import QStyledItemDelegate, QStyle
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRect

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

class CustomRowDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.icon = QPixmap(r"C:/Users/joshu/Documents/2ND_YEAR_NOTES/CC151/SISTONE/CCC151-Group--BH-Management-System/CCC151-Group--BH-Management-System/res/i-blue.png")

    def paint(self, painter, option, index):
        # Draw default item first
        super().paint(painter, option, index)

        # Check: selected + first column
        if option.state & QStyle.State_Selected and index.column() == 0:
            icon_rect = QRect(
                option.rect.left() + 6,  # left padding
                option.rect.top() + (option.rect.height() - 32) // 2,  # vertical center
                32, 32
            )
            painter.drawPixmap(icon_rect, self.icon)