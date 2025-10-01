from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QLineEdit
from frontend.shared.ui.inputs import AutoComplete, ComboBox
from frontend.shared.ui.inputs.lib.populate_with_suggestions import populate_with_suggestions
from .lib.fetch_suggestions import fetch_suggestions

class ForeignKeySearchBox(ComboBox):
    target_table: str
    display_column: str
    id_column: str
    selected_id: None | str = None

    def __init__(self, target_table: str, display_column: str, id_column: str):
        super().__init__()
        self.target_table = target_table
        self.display_column = display_column
        self.id_column = id_column

        self.setLineEdit(QLineEdit())
        self.lineEdit().setPlaceholderText("Поиск...")  # type: ignore

        self.setEditable(True)
        self.setInsertPolicy(ComboBox.InsertPolicy.NoInsert)
        self.setCompleter(AutoComplete())
        self.editTextChanged.connect(self.debounce)
        self.currentIndexChanged.connect(self.get_selection)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda _: fetch_suggestions(self))

    def debounce(self, text: str):
        self.timer.start(300)

    def on_focus(self):
        populate_with_suggestions(self)

    def get_selection(self, index: int):
        if index >= 0:
            self.selected_id = self.itemData(index)
        else:
            self.selected_id = None

    def get_filter_value(self):
        return self.selected_id  # или None
