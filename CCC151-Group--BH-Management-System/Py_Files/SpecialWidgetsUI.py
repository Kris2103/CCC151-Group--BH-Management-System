from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class ClickablePageLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("color: #630014;")
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignCenter)
        # self.setStyleSheet("padding: 4px; background-color: #fafafa;")
        self.setFixedWidth(25)
        self.setFixedHeight(25)

    def mousePressEvent(self, event):
        self.clicked.emit()

class PaginationTable(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(PaginationTable, self).__init__(parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

def test_case():
    app = QtWidgets.QApplication(sys.argv)

    # Main window
    main_window = QtWidgets.QMainWindow()
    main_window.setWindowTitle("Clickable Label Test")
    main_window.resize(400, 200)

    # Central widget and frame
    central_widget = QtWidgets.QWidget()
    main_window.setCentralWidget(central_widget)

    frame = QtWidgets.QFrame(central_widget)
    frame.setGeometry(20, 20, 360, 150)
    frame.setStyleSheet("background-color: #f0f0f0;")

    # Layout inside frame
    layout = QtWidgets.QVBoxLayout(frame)

    # Clickable label
    label = ClickablePageLabel("<<", frame)
    label.clicked.connect(lambda: print("Label clicked!"))
    layout.addWidget(label)

    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_case()
