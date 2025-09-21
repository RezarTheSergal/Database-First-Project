from os import getcwd
from PySide6.QtWidgets import QMainWindow, QWidget

from backend.database.init_db import init_database
from .components import PushButton, VLayout, Alignment, Modal, Icon, H1

ICON_PATH = getcwd() + "/frontend/images/favicon.ico"
isDatabaseInitialized: bool = False


def setup_database():
    global isDatabaseInitialized

    if not isDatabaseInitialized:
        init_database()
        isDatabaseInitialized = True


class MainWindow(QMainWindow):
    def __init__(self, w=550, h=420):
        super().__init__()
        self.setFixedSize(w, h)
        self.setWindowIcon(Icon(ICON_PATH))
        self.setWindowTitle("Monster Energy Factory")
        self._setup_ui()

    def _setup_ui(self):
        add_entry_modal = Modal(title="Добавление данных")
        view_table_modal = Modal(title="Просмотр таблиц")

        widget = QWidget()
        self.setCentralWidget(widget)

        h1 = H1("Панель админа")

        create_scheme_btn = PushButton(
            "Создать схему и таблицы",
            callback=setup_database,
        )
        add_entry_btn = PushButton(
            "Внести данные",
            callback=lambda: add_entry_modal.show(),
        )
        view_table_btn = PushButton(
            "Показать данные",
            callback=lambda: view_table_modal.show(),
        )

        vbox = VLayout(children=[h1, create_scheme_btn, add_entry_btn, view_table_btn])
        vbox.setAlignment(Alignment.Center.value)
        widget.setLayout(vbox)


if __name__ == "__main__":
    print("This is not the main file.")
