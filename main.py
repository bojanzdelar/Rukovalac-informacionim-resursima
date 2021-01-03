import sys
import mysql.connector
from PySide2 import QtWidgets
from widgets.main_window import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()