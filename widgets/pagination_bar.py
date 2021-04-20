from PySide6 import QtGui, QtWidgets

class PaginationBar(QtWidgets.QToolBar):
    def __init__(self, parent):
        super().__init__(parent)

        self.left_action = self.addAction(QtGui.QIcon("icons/left.png"), "Left")
        self.right_action = self.addAction(QtGui.QIcon("icons/right.png"), "Right")