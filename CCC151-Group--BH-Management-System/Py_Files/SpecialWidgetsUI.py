from PyQt5 import QtCore, QtGui, QtWidgets

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
res_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../res'))
infoicon_path = os.path.join(res_folder, 'i-blue.png')
sort_ASC_path = os.path.join(res_folder, 'sort_ASC.png')
sort_DESC_path = os.path.join(res_folder, 'sort_DESC.png')

from PyQt5.QtWidgets import QStyledItemDelegate, QStyle, QHeaderView, QStyleOptionHeader, QAbstractItemView
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtCore import Qt, QRect, QObject, pyqtSignal

from INFO.TenantInfoDialog import TenantInfoDialog
from INFO.RoomInfoDialog import RoomInfoDialog
from INFO.RentInfoDialog import RentInfoDialog
from INFO.PayInfoDialog import PayInfoDialog
from INFO.EMInfoDialog import EMInfoDialog


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
        self.sortHeaders = SortHeaders(Qt.Horizontal, self)
        self.setHorizontalHeader(self.sortHeaders)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)

    def updateHeaders(self, columns):
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)
        self.sortHeaders.repaint()

class IconClickEmitter(QObject):
    iconClicked = pyqtSignal(int)

class RowInfo(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.icon = QPixmap(infoicon_path)
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

        elif current_widget_index == 2:
            dialog = RentInfoDialog(self.mw, self.row_id)
            dialog.exec()

        elif current_widget_index == 3:
            dialog = PayInfoDialog(self.mw, self.row_id)
            dialog.exec()

        elif current_widget_index == 4:
            dialog = EMInfoDialog(self.mw, self.row_id)
            dialog.exec()

class SortHeaders(QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.emitter = IconClickEmitter()
        self.sort_states = {}  # Track state per column (True=ASC, False=DESC)
        self.icon_asc = QPixmap(sort_ASC_path)
        self.icon_desc = QPixmap(sort_DESC_path)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        self.sort_states[index] = not self.sort_states.get(index, True)
        self.emitter.iconClicked.emit(index)
        self.viewport().update() 
        # print("clicked header")
        super().mousePressEvent(event)

    def paintSection(self, painter, rect, logicalIndex):
        option = QStyleOptionHeader()
        self.initStyleOption(option)
        option.rect = rect
        option.section = logicalIndex
        option.text = self.model().headerData(logicalIndex, self.orientation(), Qt.DisplayRole)
        option.textAlignment = Qt.AlignCenter
        option.state |= QStyle.State_Enabled

        self.style().drawControl(QStyle.CE_Header, option, painter)

        icon = QIcon(self.icon_asc if self.sort_states.get(logicalIndex, True) else self.icon_desc)
        option.icon = icon
        option.iconAlignment = Qt.AlignRight | Qt.AlignVCenter

        self.style().drawControl(QStyle.CE_Header, option, painter)