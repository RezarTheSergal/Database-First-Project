import sys
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication
# from frontend import MainWindow
from backend.utils.logger import setup_logging
from backend.database.init_db import init_database
# Перенёс все константы в файл настройки
from backend.settings import LOG_FILE_PATH, STYLESHEET_PATH
from backend.repository import DatabaseRepository

def keep_loop_running(app, engine):
    del engine
    exit_code = app.exec()

    if exit_code == 0:
        print(f"Program exited gracefully with code {exit_code}")
    else:
        print(f"Program crashed with error code: {exit_code}")

    sys.exit(exit_code)


def apply_stylesheet(app: QApplication):
    stylesheet = open(STYLESHEET_PATH, "r", encoding="utf8").read()
    app.setStyleSheet(stylesheet)


def setup_frontend():
    app = QApplication(sys.argv)
    apply_stylesheet(app)
    engine = QQmlApplicationEngine(app)

    main_window = MainWindow()
    main_window.show()

    keep_loop_running(app, engine)


if __name__ == "__main__":
    setup_logging(log_file=LOG_FILE_PATH)
    init_database()
    rep = DatabaseRepository()
    table_names = rep.get_tablenames().to_dict()['data']
    table_columns = rep.get_table_data()
    print(table_columns)
    # setup_frontend()
