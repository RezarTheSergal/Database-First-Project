from PySide6.QtCore import QTimer
from backend.repository import DatabaseRepository
from frontend.shared.ui import Widget, ComboBox, Completer, HLayout
from backend.utils.responce_types import ResponseStatus


class ForeignKeySearchBox(Widget):
    def __init__(self, target_table: str, display_column: str, id_column: str):
        super().__init__(HLayout())
        self.target_table = target_table
        self.display_column = display_column
        self.id_column = id_column

        self.combo = ComboBox()
        self.combo.setCompleter(Completer())
        self.combo.setEditable(True)
        self.combo.setInsertPolicy(ComboBox.InsertPolicy.NoInsert)
        self.add_children([self.combo])

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._fetch_suggestions)

        self.combo.editTextChanged.connect(self._on_text_changed)

        self.selected_id = None
        self.combo.currentIndexChanged.connect(self._on_selection)

    def _on_text_changed(self, text: str):
        self.timer.start(300)  # debounce

    def _fetch_suggestions(self):
        text = self.combo.currentText().strip()
        if len(text) < 2:
            return

        # Асинхронный запрос (в реальности — через QThread или async)
        response = DatabaseRepository().search_foreign_key(
            table=self.target_table,
            display_col=self.display_column,
            id_col=self.id_column,
            query=text,
            limit=30,
        )
        if response.status == ResponseStatus.SUCCESS and response.data != None:
            self.combo.blockSignals(True)
            self.combo.clear()
            for item in response.data:
                self.combo.addItem(item[self.display_column], item[self.id_column])
            self.combo.blockSignals(False)

    def on_focus(self):
        if self.combo.count() == 0:
            response = DatabaseRepository.search_foreign_key(
                table=self.target_table,
                display_col=self.display_column,
                id_col=self.id_column,
                query="",  # пустой запрос → можно вернуть первые N
                limit=10,
            )
            if response.status == ResponseStatus.SUCCESS and response.data != None:
                for item in response.data:
                    self.combo.addItem(str(item["display"]), userData=item["id"])

    def _on_selection(self, index: int):
        if index >= 0:
            self.selected_id = self.combo.itemData(index)
        else:
            self.selected_id = None

    def get_filter_value(self):
        return self.selected_id  # или None
