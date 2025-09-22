from PySide6.QtWidgets import QMainWindow, QWidget
from backend.database.init_db import init_database
from frontend.modals import AddEntryModal, ViewTableModal
from .shared.ui import PushButton, VLayout, Alignment, Icon, H1
from backend.settings import ICON_PATH


class MainWindow(QMainWindow):
    def __init__(self, w=550, h=420):
        super().__init__()
        self.setFixedSize(w, h)
        self.setWindowIcon(Icon(ICON_PATH))
        self.setWindowTitle("Monster Energy Factory")
        self._setup_ui()

    def _setup_ui(self):
        self.add_entry_modal = AddEntryModal()
        self.view_table_modal = ViewTableModal()

        widget = QWidget()
        self.setCentralWidget(widget)

        h1 = H1("Панель админа")

        # Rezar: перенёс логику проверки на существование БД в бэк инициализации
        create_scheme_btn = PushButton(
            "Создать схему и таблицы",
            callback=init_database,
        )
        add_entry_btn = PushButton(
            "Внести данные",
            callback=lambda: self.add_entry_modal.show(),
        )
        view_table_btn = PushButton(
            "Показать данные",
            callback=lambda: self.view_table_modal.show(),
        )

        vbox = VLayout(children=[h1, create_scheme_btn, add_entry_btn, view_table_btn])
        vbox.setAlignment(Alignment.Center.value)
        widget.setLayout(vbox)


if __name__ == "__main__":
    print("This is not the main file.")
