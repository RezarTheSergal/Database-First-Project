from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QLineEdit
from backend.repository import DatabaseRepository
from backend.utils.responce_types import ResponseStatus
from frontend.shared.ui.inputs import AutoComplete, ComboBox


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
        self.editTextChanged.connect(self._on_text_changed)
        self.currentIndexChanged.connect(self._on_selection)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._fetch_suggestions)

    def _on_text_changed(self, text: str):
        self.timer.start(300)  # debounce

    def _fetch_suggestions(self):
        text = self.currentText().strip()
        if len(text) < 2:
            return

        # Асинхронный запрос (в реальности — через QThread или async)
        results = DatabaseRepository().search_foreign_key(
            table=self.target_table,
            display_col=self.display_column,
            id_col=self.id_column,
            query=text,
            limit=30,
        )
        if results.data:
            self.blockSignals(True)
            self.clear()
            for item in results.data:
                self.addItem(item[self.display_column], item[self.id_column])
            self.blockSignals(False)

    def on_focus(self):
        if self.count() == 0:
            resp = DatabaseRepository.search_foreign_key(
                table=self.target_table,
                display_col=self.display_column,
                id_col=self.id_column,
                query="",  # пустой запрос → можно вернуть первые N
                limit=10,
            )
            if resp.status == ResponseStatus.SUCCESS and resp.data != None:
                for item in resp.data:
                    self.addItem(str(item["display"]), userData=item["id"])

    def _on_selection(self, index: int):
        if index >= 0:
            self.selected_id = self.itemData(index)
        else:
            self.selected_id = None

    def get_filter_value(self):
        return self.selected_id  # или None
