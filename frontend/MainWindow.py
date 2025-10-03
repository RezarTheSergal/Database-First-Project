from frontend.modals import AddEntryModal, ViewTableModal
from frontend.shared.utils.DBSetup import init_database_callback
from frontend.shared.ui import (
    PushButton,
    VLayout,
    Icon,
    H1,
    Hr,
    Widget,
    PromptBox,
    Modal,
)
from backend.settings import ICON_PATH
from PySide6.QtWidgets import QMainWindow, QApplication
from frontend.shared.ui.const import YesButton

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(550, 420)
        self.setWindowIcon(Icon(ICON_PATH))
        self.setWindowTitle("Monster Energy Factory - Admin Panel")
        self.activateWindow()  # Puts window on top
        self._setup_ui()

    def _setup_ui(self):
        self.add_entry_modal = AddEntryModal(self)
        self.view_table_modal = ViewTableModal(self)

        self.widget = Widget(VLayout())
        self.setCentralWidget(self.widget)

        h1 = H1("ПАНЕЛЬ АДМИНА")
        hr = Hr()

        # Rezar: перенёс логику проверки на существование БД в бэк инициализации
        create_scheme_btn = PushButton(
            "создать схему и таблицы",
            callback=lambda: init_database_callback(),
        )
        add_entry_btn = PushButton(
            "внести данные",
            callback=lambda: self.open_modal(self.add_entry_modal),
        )
        view_table_btn = PushButton(
            "показать данные",
            callback=lambda: self.open_modal(self.view_table_modal),
        )

        self.widget.layout.set_children(
            [h1, hr, create_scheme_btn, add_entry_btn, view_table_btn]
        )

    def open_modal(self, modal: Modal):
        # Disable the main window
        self.setEnabled(False)

        # Create and show the modal widget
        modal.show()

    # НЕ ПЕРЕИМЕНОВЫВАТЬ
    def closeEvent(self, event):
        """This method is automatically called when the window is about to close."""
        reply: int = PromptBox().prompt(
            "Подтвердить выход",
            "Вы точно хотите выйти из приложения? Любые несохраненные изменения будут утеряны.",
        )

        if reply == YesButton:
            event.accept()  # Allow the window to close, which will quit the app
            QApplication.quit()  # Closes whole application
        else:
            event.ignore()  # Keep the application running
