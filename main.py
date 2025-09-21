import sys
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication
from const import STYLESHEET_PATH
from frontend.ui import MainWindow
from backend.utils.logger import setup_logging
from backend.settings import LOG_FILE_PATH

def keep_loop_running(app, engine):
    del engine
    exit_code = app.exec()

    if exit_code == 0:
        print(f"Program exited gracefully with code {exit_code}")
    else:
        print(f"Program crashed with error code: {exit_code}")

    sys.exit(exit_code)


if __name__ == "__main__":
    setup_logging(level=logging.INFO, log_file=LOG_FILE_PATH, console_log=True) # Не убирать отсюда, всё логгирование держится на этом!
    app = QApplication(sys.argv, styleSheet=STYLESHEET_PATH)
    engine = QQmlApplicationEngine(app)

    main_window = MainWindow()
    main_window.show()

    keep_loop_running(app, engine)