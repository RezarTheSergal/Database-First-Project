from frontend.shared.ui import Spinner, Widget, PushButton, VLayout, HLayout, Row, Size
from backend.repository import DatabaseRepository, logging
from frontend.shared.lib import translate

logger = logging.getLogger()
database = DatabaseRepository()

class AddEntryForm(Widget):
    def __init__(self):
        super().__init__(layout=VLayout())
        self.table_name_spinner_box = Spinner(
            database.get_tablenames().data, callback=self._set_inputs_by_table
        )
        # Изменили VLayout на HLayout!
        self.inputs_container = Widget(HLayout())  # ✅ Теперь в строчку
        self.submit_button = PushButton("Подтвердить", callback=self._request_entry_PUT)
        self.add_children(
            [self.table_name_spinner_box, self.inputs_container, self.submit_button]
        )
        
        self.current_rows = []

    def _set_inputs_by_table(self):
        if not self.table_name_spinner_box.get_current_item_text():
            return
        
        response = database.get_table_columns(
            self.table_name_spinner_box.get_current_item_text()
        )
        if response.status == "error" or response.data is None:
            logger.error("Колонки не были получены", response.error)
            return
        
        columns: dict[str, dict] = response.data
        self._rebuild_inputs_container(columns)

    def _rebuild_inputs_container(self, columns):
        """Полностью пересоздает контейнер с полями ввода"""
        # Удаляем старые виджеты
        for row in self.current_rows:
            row.setParent(None)
            row.deleteLater()
        self.current_rows.clear()
        
        # Очищаем layout контейнера
        layout = self.inputs_container.layout()
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                if item:
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
                        widget.deleteLater()
        
        # Создаем новые Row виджеты
        for key, data in columns.items():
            if data.get("primary_key", False):
                continue
            row = Row(key, translate(key), type=data["type"])
            self.current_rows.append(row)
            if layout:
                layout.addWidget(row)
        
        # Обновляем UI
        self.inputs_container.updateGeometry()
        self.updateGeometry()

    def _request_entry_PUT(self):
        data = {}
        for row in self.current_rows:
            if isinstance(row, Row):
                data[row.get_label("en")] = row.get_input_value()
        
        table_name = self.table_name_spinner_box.get_current_item_text()
        if table_name:
            database.insert_into_table(table_name, data)