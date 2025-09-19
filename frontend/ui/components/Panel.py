from PySide6 import QtWidgets as Qw, QtGui as Qg


class MainWindow(Qw.QWidget):
    def __init__(self, title: str, icon: Qg.QIcon):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(icon)
