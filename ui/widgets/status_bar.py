from PySide6 import QtCore, QtWidgets

class StatusBar(QtWidgets.QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)

    def show_time(self):
        time = QtCore.QDateTime.currentDateTime()
        time_display = time.toString('hh:mm:ss, yyyy-MM-dd')
        self.showMessage(time_display)