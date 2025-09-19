import sys
import os
from PySide6 import QtWidgets as Qw, QtCore as Qc
from frontend.ui import MainWindow


STYLESHEET_PATH = os.getcwd() + "/frontend/ui/styles/style.css"


if __name__ == "__main__":
    app = Qw.QApplication(styleSheet=STYLESHEET_PATH)
    settings = Qc.QSettings()

    main_window = MainWindow()

    sys.exit(app.exec())
