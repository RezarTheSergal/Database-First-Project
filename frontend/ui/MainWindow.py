from PySide6 import QtWidgets, QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, title: str, icon: QtGui.QIcon):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(icon)
