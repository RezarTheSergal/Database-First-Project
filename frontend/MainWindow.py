from frontend.modals import AddEntryModal, ViewTableModal
from frontend.utils.DBSetup import init_database_callback
from frontend.shared.ui import PushButton, VLayout, Icon, H1, Hr, Widget, PromptBox
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
        self.add_entry_modal = AddEntryModal()
        self.view_table_modal = ViewTableModal()

        self.widget = Widget(VLayout())
        self.setCentralWidget(self.widget)

        h1 = H1("ПАНЕЛЬ АДМИНА")
        hr = Hr()

        # Rezar: перенёс логику проверки на существование БД в бэк инициализации
        create_scheme_btn = PushButton(
            "создать схему и таблицы",
            callback=init_database_callback,
        )
        add_entry_btn = PushButton(
            "внести данные",
            callback=lambda: self.add_entry_modal.show(),
        )
        view_table_btn = PushButton(
            "показать данные",
            callback=lambda: self.view_table_modal.show(),
        )

        self.widget.set_children(
            [h1, hr, create_scheme_btn, add_entry_btn, view_table_btn]
        )

    # НЕ ПЕРЕИМЕНОВЫВАТЬ
    def closeEvent(self, event):
        """This method is automatically called when the window is about to close."""
        reply = PromptBox().prompt(
            self,
            "Подтвердить выход",
            "Вы точно хотите выйти из приложения? Любые несохраненные изменения будут утеряны.",
        )

        if reply == YesButton:
            event.accept()  # Allow the window to close, which will quit the app
            QApplication.quit()  # Closes whole application
        else:
            event.ignore()  # Keep the application running
