from PySide6 import QtCore, QtGui, QtWidgets

class PaginationBar(QtWidgets.QWidget):
    display_page = QtCore.Signal(int, int)

    def __init__(self, page_size, total_pages, parent):
        super().__init__(parent)

        self.text = QtWidgets.QLabel("")
        self.tool_bar = QtWidgets.QToolBar()
                
     
        self.page_size = page_size
        self.total_pages = total_pages
        self.page = 0
        self.set_page(0)

        left_action = self.tool_bar.addAction(QtGui.QIcon("icons/left.png"), "Left")
        right_action = self.tool_bar.addAction(QtGui.QIcon("icons/right.png"), "Right")

        left_action.triggered.connect(lambda: self.set_page(self.page - 1))
        right_action.triggered.connect(lambda: self.set_page(self.page + 1))


        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.text, alignment=QtCore.Qt.AlignRight)
        layout.addWidget(self.tool_bar, alignment=QtCore.Qt.AlignLeft)
        self.setLayout(layout)

    def set_page(self, page):
        if page < 0 or page > self.total_pages:
            return
        self.page = page
        self.text.setText(f"Stranica: {self.page + 1} / {int(self.total_pages) + 1}")
        self.display_page.emit(self.page, self.page_size)