import sys
import os
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings
from backend.database.init_db import init_database
from frontend.ui import MainWindow


STYLESHEET_PATH = os.getcwd() + "/frontend/ui/styles/style.css"


def exit_gracefully(app, engine):
    del engine
    exit_code = app.exec()
    print(f"Program exited gracefully with code {exit_code}")
    sys.exit(exit_code)


if __name__ == "__main__":
    # init_database()
    app = QApplication(sys.argv, styleSheet=STYLESHEET_PATH)

    engine = QQmlApplicationEngine(app)

    settings = QSettings()
    main_window = MainWindow()

    exit_gracefully(app, engine)
