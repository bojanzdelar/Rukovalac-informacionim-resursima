from PySide6 import QtCore, QtWidgets

class TableView(QtWidgets.QTableView):
    row_selected = QtCore.Signal(QtCore.QModelIndex)
    set_page = QtCore.Signal(int)

    def __init__(self, model, parent):
        super().__init__(parent)

        self.model = model
        self.proxy_model = QtCore.QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)
        self.filtered = False

        self.setModel(self.proxy_model)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.setSortingEnabled(True)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.horizontalHeader().sectionClicked.connect(lambda: self.set_page.emit(0))
        self.clicked.connect(lambda: self.row_selected.emit(self.selectionModel().selectedIndexes()[0]))

    def filter(self):
        filter_action_position = 5 if self.type == "main_entity_widget" else 0 # FIXME FIXME FIXME FIXME FIXME OUCH

        if self.filtered:
            if isinstance(self. information_resource, Database):
                self.model.layoutAboutToBeChanged.emit()
                self.model.information_resource.data = self.model.information_resource.read_data()
                self.model.layoutChanged.emit()
            self.tool_bar.actions()[filter_action_position].setIcon(QtGui.QIcon("icons/filter.png"))
        else:
            if isinstance(self.model.information_resource, SerialFile):
                self.filter_indexes = self.model.information_resource.filter(self.filter_values)
                for i, index in enumerate(self.filter_indexes):
                    self.filter_indexes[i] = self.proxy_model.mapFromSource(self.model.index(index, 0)).row()
                self.filter_indexes.sort()
            elif isinstance(self.model.information_resource, Database):
                self.model.layoutAboutToBeChanged.emit()
                self.model.information_resource.filter(self.filter_values)
                self.model.layoutChanged.emit()
            self.tool_bar.actions()[filter_action_position].setIcon(QtGui.QIcon("icons/filter_enabled.png"))

        self.filtered = not self.filtered
        self.set_page.emit(0)

    def refilter(self):
        if self.filtered:
            for i in range(2):
                self.filter()

    def display_page(self, page, page_size):
        index = None
        page_empty = True
        for i in range(self.model.rowCount()):
            self.hideRow(i)

        if self.filtered and isinstance(self.model.information_resource, SerialFile):
            self.filter_indexes = self.model.information_resource.filter(self.filter_values)
            for i, index in enumerate(self.filter_indexes):
                self.filter_indexes[i] = self.proxy_model.mapFromSource(self.model.index(index, 0)).row()
            self.filter_indexes.sort()
            for i in self.filter_indexes[page * page_size: (page + 1) * page_size]:
                self.showRow(i)
                page_empty = False

            if len(self.filter_indexes):
                index = self.filter_indexes[0]
        else:
            for i in range(page * page_size, (page + 1) * page_size):
                if i >= len(self.model.information_resource.data):
                    break
                self.showRow(i)
                page_empty = False

            index = page * page_size

        self.row_selected.emit(self.proxy_model.index(-1,-1))

        if index is not None and not page_empty: # FIXME: VEROVATNO NE TREBA NOT PAGE_EMPTY
            self.selectRow(index)
            self.row_selected.emit(self.selectionModel().selectedIndexes()[0])