import sys
import os
from PySide6 import QtWidgets as Qw, QtCore as Qc
from frontend.ui import MainWindow


STYLESHEET_PATH = os.getcwd() + "/frontend/ui/styles/style.css"


if __name__ == "__main__":
    init_database()
    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])

    app = Qw.QApplication(sys.argv, styleSheet=STYLESHEET_PATH)
    settings = Qc.QSettings()
    main_window = MainWindow()

    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine

    sys.exit(exit_code)
