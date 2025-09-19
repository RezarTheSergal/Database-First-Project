import sys
import os
from PySide6 import QtWidgets as Qw, QtCore as Qc
from frontend.ui import PushButton, VLayout, MainWindow, Icon, Alignment, Font, Text


PATH = os.getcwd()
STYLESHEET_PATH = PATH + "/frontend/ui/styles/style.css"
ICON_PATH = PATH + "/frontend/ui/images/icons8-monster-energy-32.ico"


def create_main_window():
    main_window = MainWindow("Monster Energy Factory", Icon(ICON_PATH))
    main_window.setMinimumSize(600, 450)
    main_window.show()
    return main_window


def setup_ui(main_window):
    widget = Qw.QWidget()
    main_window.setCentralWidget(widget)

    h1_font = Font(36)
    button_font = Font(12)

    h1 = Text("Панель админа", h1_font)
    h1.setMargin(40)

    create_scheme_btn = PushButton("Создать схему и таблицы", button_font)
    add_data_btn = PushButton("Внести данные", button_font)
    show_data_btn = PushButton("Показать данные", button_font)

    vbox = VLayout(children=[h1, create_scheme_btn, add_data_btn, show_data_btn])
    vbox.setAlignment(Alignment.Center.value)
    widget.setLayout(vbox)


if __name__ == "__main__":
    app = Qw.QApplication(styleSheet=STYLESHEET_PATH)
    settings = Qc.QSettings()

    main_window = create_main_window()
    setup_ui(main_window)

    sys.exit(app.exec())
