from frontend.base import MainWindow
from PySide6.QtWidgets import QApplication
import sys
from backend.database.engine import DBSession
from backend.settings import PgConfig

DBSession.init(PgConfig().database_url())

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()