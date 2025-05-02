from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class ClickablePageLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("color: #630014;")
        self.setFixedWidth(25)
        self.setFixedHeight(25)

    def mousePressEvent(self, event):
        self.clicked.emit()

class PaginationTable(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(PaginationTable, self).__init__(parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
