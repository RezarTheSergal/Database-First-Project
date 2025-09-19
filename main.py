from frontend.base import MainWindow
from PySide6.QtWidgets import QApplication
import sys
from backend.database.database import Database
from backend.settings import PgConfig
from backend.database.init_db import init_database
def main():
    init_database()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()