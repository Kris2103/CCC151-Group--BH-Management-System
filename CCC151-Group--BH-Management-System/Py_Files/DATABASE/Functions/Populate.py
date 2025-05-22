import math
import SpecialWidgetsUI
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QCompleter, QAbstractItemView, QHeaderView
from PyQt5.QtCore import Qt
from . import Select, Insert

# =========================
#    PAGINATION TABLE
# ==========

class Populate:
    def __init__(self, main_window = None):
        self.mw = main_window
        self.selector = Select.Select()
        self.inserter = Insert.Insert()
        self.primary_key = None
    
    def Populate_Table(self, table_name, table_widget, select_type, current_page = 1, search_column = None, search_key = None, group = None, sort_column = None, sort_order = None):
        
        self.table_name = table_name
        self.table_widget = table_widget
        self.select_type = select_type
        self.current_page = current_page
        self.search_column = search_column
        self.search_key = search_key
        self.sort_column = sort_column
        self.sort_order = sort_order
        self.group_by = group

        # Fetch ALL data with query, store for faster loading in page change...
        self.columns = self.selector.SelectQuery(table_name, select_type).retCols()

        # Set primary key
        primary_keys = {
            "Tenant": "TenantID",
            "Room": "RoomNumber",
            "Rents": "RentID",
            "Pays": "PayID",
            "EmergencyContact": "ContactID"
        }
        self.primary_key = primary_keys.get(table_name)
        if self.primary_key is None and self.columns:
            # fallback to first column as primary key if not set
            self.primary_key = self.columns[0]

        # Fetch full data for pagination and filtering
        if not hasattr(self, "full_data") or self.table_name != table_name \
           or self.search_key != search_key:
            self.full_data = self.selector.SelectQuery(
                table_name, select_type,
                tag=search_column, key=search_key,
                sort_column=sort_column, sort_order=sort_order,
                group=group).retData()
        # Tradeoff: Takes up memory for faster loading(users want their current job done than more jobs done)

            # Configure pages information according to taste
            self.rows_per_page  = 15
            self.total_pages    = math.ceil(len(self.full_data)/self.rows_per_page)

        self.current_page = current_page
        self.mw.jumpLabel_totalpages.setText(str(self.total_pages))

        start_index             = (current_page-1) * self.rows_per_page
        end_index               = start_index + self.rows_per_page
        self.page_data          = self.full_data[start_index:end_index]

        # refresh table widget(data is not refreshed)
        table_widget.clear()
        table_widget.setRowCount(len(self.page_data))
        table_widget.setColumnCount(len(self.columns))
        table_widget.setHorizontalHeaderLabels(self.columns)
        table_widget.verticalHeader().setVisible(False)

        # Load the data in TO EDIT: ignore first column (built-in id of widget)
        for row_idx, row_data in enumerate(self.page_data):
            for col_idx, cell in enumerate(row_data):
                item = QTableWidgetItem(str(cell))
                item.setTextAlignment(Qt.AlignCenter)
                table_widget.setItem(row_idx, col_idx, item)

        # Add an additional row for more Info buttons


        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # array of pointers to the created buttons. I say buttons but they're actually modified labels my dudes
        while self.mw.paginationButtonsGrid.count():
            item = self.mw.paginationButtonsGrid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.mw.jumpBox.clear()

        self.PaginationButts = []
        buttCol = 0

        self.prevTenButt    = SpecialWidgetsUI.ClickablePageLabel("<<", self.mw.paginationFrame)
        self.prevTenButt.clicked.connect(lambda: self.PrevTenPage())
        self.mw.paginationButtonsGrid.addWidget(self.prevTenButt, 0, buttCol)
        buttCol += 1
        self.PaginationButts.append(self.prevTenButt)

        self.prevButt       = SpecialWidgetsUI.ClickablePageLabel("<", self.mw.paginationFrame)
        self.prevButt.clicked.connect(lambda: self.PrevPage())
        self.mw.paginationButtonsGrid.addWidget(self.prevButt, 0, buttCol)
        buttCol += 1
        self.PaginationButts.append(self.prevButt)

        for i in range(1, self.total_pages + 1):
            self.mw.jumpBox.addItem(str(i), i)

            if (i <= 11 and self.current_page < 6) or i == self.current_page or ((i >= self.current_page - 5) and (i <= self.current_page + 5)) or (i >= self.total_pages - 10 and self.current_page > self.total_pages - 5):
                # print(f"Creating button for page {i}")
                numButt     = SpecialWidgetsUI.ClickablePageLabel(f"{i}", self.mw.paginationFrame)
                numButt.clicked.connect(lambda x=i: self.GotoPage(x))
                self.mw.paginationButtonsGrid.addWidget(numButt, 0, buttCol)
                buttCol += 1
                self.PaginationButts.append(numButt)

        self.nextButt       = SpecialWidgetsUI.ClickablePageLabel(">", self.mw.paginationFrame)
        self.nextButt.clicked.connect(lambda: self.NextPage())
        self.mw.paginationButtonsGrid.addWidget(self.nextButt, 0, buttCol)
        buttCol += 1
        self.PaginationButts.append(self.nextButt)

        self.nextTenButt    = SpecialWidgetsUI.ClickablePageLabel(">>", self.mw.paginationFrame)
        self.nextTenButt.clicked.connect(lambda: self.NextTenPage())
        self.mw.paginationButtonsGrid.addWidget(self.nextTenButt, 0, buttCol)
        buttCol += 1
        self.PaginationButts.append(self.nextTenButt)
        
        self.prevButt.setEnabled(self.current_page > 1)
        self.nextButt.setEnabled(self.current_page < self.total_pages)
        self.prevTenButt.setEnabled(self.current_page > 1)
        self.nextTenButt.setEnabled(self.current_page < self.total_pages)

        index = self.mw.jumpBox.findData(self.current_page)
        if index != -1:
            self.mw.jumpBox.setCurrentIndex(index)
        
        self.mw.jumpBox.activated.connect(lambda: self.jump())

        infoIcon = SpecialWidgetsUI.CustomRowDelegate(self.table_widget)
        self.table_widget.setItemDelegate(infoIcon)
        infoIcon.emitter.iconClicked.connect(lambda: infoIcon.infoClicked(self.mw))

    def jump(self):
        page = self.mw.jumpBox.currentData()
        if page is not None: self.GotoPage(page) 

    def NextPage(self):
        self.current_page += 1
        self.Populate_Table(self.table_name, self.table_widget, self.select_type, self.current_page)

    def NextTenPage(self):
        if self.current_page + 10 < self.total_pages:
            self.current_page += 10
        else: 
            self.current_page = self.total_pages
        self.Populate_Table(self.table_name, self.table_widget, self.select_type, self.current_page)

    def PrevPage(self):
        self.current_page -= 1
        self.Populate_Table(self.table_name, self.table_widget, self.select_type, self.current_page)

    def PrevTenPage(self):
        if self.current_page - 10 >= 1:
            self.current_page -= 10
        else:
            self.current_page = 1
        self.Populate_Table(self.table_name, self.table_widget, self.select_type, self.current_page)

    def GotoPage(self, page):
        self.Populate_Table(self.table_name, self.table_widget, self.select_type, page)

# ===========
#    PAGINATION TABLE
# =========================

# =========================
#    COMBOBOXES POPULATE
# ==========

    def populate_room_combobox(self, room_combobox):
        
        self.room_combobox = room_combobox
        
        try:
            # Querying for room numbers
            rows = self.selector.SelectQuery("Room", spec_col=["RoomNumber"]).retData()

            if not rows:
                QMessageBox.warning(self, "No Data", "No room numbers found.")
                return

            # Extract room numbers from the query result
            room_list = [str(row[0]) for row in rows]  

            # Populate the combo box with room numbers
            self.room_combobox.clear()
            self.room_combobox.addItems(room_list)

            # Make combo box searchable
            self.room_combobox.setEditable(True)
            completer = QCompleter(room_list, self.room_combobox)
            completer.setCaseSensitivity(False)
            self.room_combobox.setCompleter(completer)

        except Exception as err:
            print(f"Database Error: {err}")
            QMessageBox.critical(self, "Database Error", f"Failed to load rooms:\n{err}") 

    def populate_sex_combobox(self, sex_combobox):
        self.sex_combobox = sex_combobox
        self.sex_combobox.clear()

        self.sex_combobox.addItems(["Male", "Female"])

    # typo with self.move_combobox
    def populate_movestatus_combobox(self, move_combobox):
        self.move_combobox = move_combobox
        self.move_combobox.clear()
        self.move_combobox.addItems(["Active", "Moved Out"])

    def populate_tenant_id_combobox(self, tenant_combobox):
        try:    
            self.tenant_combobox = tenant_combobox
            self.tenant_combobox.clear()
            tenant_ids = [str(row[0]) for row in self.selector.SelectQuery("Tenant", None, ["Tenant.TenantID"]).retData()]

            self.tenant_combobox.setEditable(True)
            self.tenant_combobox.addItems(tenant_ids)
            completer = QCompleter(tenant_ids, self.tenant_combobox)
            completer.setCaseSensitivity(False)
            completer.setFilterMode(Qt.MatchContains)
            self.tenant_combobox.setCompleter(completer)

        except Exception as err:
            print(f"Completer Error: {err}")
            QMessageBox.critical(self, "Error", f"Could not load tenant IDs:\n{err}")
    
    def sync_moveout_movein(self, moveout_combobox, movein_combobox):
        self.moveout_combobox = moveout_combobox
        self.movein_combobox = movein_combobox
        movein = self.movein_combobox.currentText()
        moveout = self.moveout_combobox.currentText()
        
        if movein and not moveout:
            #self.tenantid_combobox.setCurrentText()
            if hasattr(self, 'tenantid_combobox'):
                self.tenantid_combobox.setCurrentText("")

    def sync_tenant_id_from_room(self, roomnum_combobox, tenantid_combobox):
        self.roomnum_combobox = roomnum_combobox
        self.tenantid_combobox = tenantid_combobox
        room = self.roomnum_combobox.currentText()
        tenant = self.tenant_combobox.currentText()
        if room == "" or not room or tenant != "": # room combobox has no entry, or tenant combobox has already been filled, do not autosync
            return
        
        result = self.selector.SelectQuery("Tenant", None, ["Tenant.TenantID"], tag = "RoomNumber", key = room, limit = 1).retData()
        if result:
            tenant_id = str(result[0][0])
            self.tenantid_combobox.setCurrentText(tenant_id)

    def sync_room_from_tenant_id(self, roomnum_combobox, tenantid_combobox):
        self.roomnum_combobox = roomnum_combobox
        room = self.roomnum_combobox.currentText()
        self.tenantid_combobox = tenantid_combobox        
        tenant_id = self.tenantid_combobox.currentText()
        if tenant_id == "" or not tenant_id or room != "": # tenant combobox has no entry, or room combobox has already been filled, do not autosync
            return
        
        result = self.selector.SelectQuery("Tenant", None, ["Tenant.RoomNumber"], tag = "TenantID", key = tenant_id, limit = 1).retData()
        if result:
            room_number = str(result[0][0])
            index = self.roomnum_combobox.findText(room_number)
            if index != -1:
                self.roomnum_combobox.setCurrentIndex(index)

# ===========
#    COMBOBOXES POPULATE   
# =========================


# =========================
#    COMBOBOXES POPULATE
# ==========

    # def load_data(self, index):
        
    #     if hasattr(self.mw.populator, "full_data"): del self.mw.populator.full_data
        
    #     self.table_name, self.widget, self.select_type = self.map_indextotable(index)
    #     self.populator.Populate_Table(self.table_name, self.widget, self.select_type)

    #     self.columns = self.populator.columns
    #     self.SearchField.clear()
    #     self.SearchLineEdit.clear()
    #     for col in self.columns: self.SearchField.addItem(str(col), col)

# ===========
#    COMBOBOXES POPULATE   
# =========================