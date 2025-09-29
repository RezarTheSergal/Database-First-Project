import sys
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication
from frontend import MainWindow
from backend.utils.logger import logging, setup_logging
from backend.settings import LOG_FILE_PATH, STYLESHEET_PATH

logger = logging.getLogger()


def quit_gracefully(app, engine):
    del engine
    exit_code = app.exec()

    if exit_code == 0:
        logger.info(f"Program exited gracefully with code {exit_code}")
    else:
        logger.error(f"Program crashed with error code: {exit_code}")

    sys.exit(exit_code)


def apply_stylesheet(app: QApplication):
    stylesheet = open(STYLESHEET_PATH, "r", encoding="utf8").read()
    app.setStyleSheet(stylesheet)


def setup_frontend():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    apply_stylesheet(app)
    engine = QQmlApplicationEngine(app)

    main_window = MainWindow()
    main_window.show()

    quit_gracefully(app, engine)


if __name__ == "__main__":
    setup_logging(log_file=LOG_FILE_PATH)
    setup_frontend()
