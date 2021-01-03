import sys
import mysql.connector
from PySide2 import QtWidgets
from widgets.main_window import MainWindow

if __name__ == "__main__":
    # connection = mysql.connector.connect(user="root", password="root", host="127.0.0.1", database="univerzitet")
    # csor = connection.cursor()

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()

    # connection.commit()
    # csor.close()
    # connection.close()