from os import getcwd
from PySide6.QtWidgets import QMainWindow, QWidget

from backend.database.init_db import init_database
from .components import PushButton, Text, VLayout, Alignment, Font, Modal, Icon

# Перенёс все константы в файл настройки
from backend.settings import ICON_PATH

class MainWindow(QMainWindow):
    def __init__(self, w=550, h=420):
        super().__init__()
        self.setFixedSize(w, h)
        self.setWindowIcon(Icon(ICON_PATH))
        self.setWindowTitle("Monster Energy Factory")
        self._setup_ui()

    def _setup_ui(self):
        add_entry_modal = Modal(icon_path=ICON_PATH, title="Добавление данных")
        view_table_modal = Modal(icon_path=ICON_PATH, title="Просмотр таблиц")

        widget = QWidget()
        self.setCentralWidget(widget)

        h1_font = Font(36, family="Rubik Wet Paint")
        h1 = Text("Панель админа", h1_font)

        # Rezar: перенёс логику проверки на существование БД в бэк инициализации
        create_scheme_btn = PushButton(
            "Создать схему и таблицы",
            callback=init_database,
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
