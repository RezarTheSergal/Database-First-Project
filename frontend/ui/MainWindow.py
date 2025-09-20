import os
from PySide6 import QtWidgets as Qw
from .components import PushButton, Text, Icon, Font, VLayout, Alignment


class MainWindow(Qw.QMainWindow):
    def __init__(self):
        super().__init__()

        PATH = os.getcwd()
        ICON_PATH = PATH + "/frontend/ui/images/icons8-monster-energy-32.ico"

        self.setWindowTitle("Monster Energy Factory")
        self.setWindowIcon(Icon(ICON_PATH))
        self.setMinimumSize(600, 450)

        self._setup_ui()

        self.show()

    def _setup_ui(self):
        widget = Qw.QWidget()
        self.setCentralWidget(widget)

        h1_font = Font(36)
        button_font = Font(12)

        h1 = Text("Панель админа", h1_font)
        h1.setMargin(40)

        create_scheme_btn = PushButton(
            "Создать схему и таблицы", button_font, callback=lambda: print("Created")
        )
        add_data_btn = PushButton(
            "Внести данные", button_font, callback=lambda: print("Added")
        )
        show_data_btn = PushButton(
            "Показать данные", button_font, callback=lambda: print("Showed")
        )

        vbox = VLayout(children=[h1, create_scheme_btn, add_data_btn, show_data_btn])
        vbox.setAlignment(Alignment.Center.value)
        widget.setLayout(vbox)
