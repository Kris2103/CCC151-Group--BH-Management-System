from PyQt5 import QtCore, QtGui, QtWidgets

class ClickablePageLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, text=""):
        super().__init__(text)
        self.setStyleSheet("color: #630014;")
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        self.clicked.emit()

class PaginationTable(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(PaginationTable, self).__init__(parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)