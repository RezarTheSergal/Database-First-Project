from typing import Any, Dict, List
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QSpinBox, QCheckBox, QComboBox, QDateEdit, QDoubleSpinBox
from frontend.shared.ui import VLayout, HLayout, Widget
from frontend.shared.ui.inputs.ComboBox import ComboBox
from backend.repository import DatabaseRepository
import logging

logger = logging.getLogger()
database = DatabaseRepository()

class FilterBlockClass(QWidget):
    def __init__(self, initial_tables=None, parent=None):
        super().__init__(parent)
        self.hor_layout = QHBoxLayout(self)
        self.hor_layout.setContentsMargins(0, 0, 0, 0)

        self.table_combo = ComboBox(
            items=initial_tables or [], callback=self._on_table_changed
        )

        self.filters_container = Widget(VLayout())
        self.filters_widgets = {}  # {column_name: widget}

        self.hor_layout.addWidget(self.table_combo)
        self.hor_layout.addWidget(self.filters_container)

        # Инициализация: если есть хотя бы одна таблица — подгрузим фильтры
        if initial_tables:
            self._on_table_changed(initial_tables[0])

    def _on_table_changed(self, table_name: str):
        """Обновляет фильтры под выбранную таблицу"""
        self.clear_filters()
        columns_info = self._get_columns_info(table_name)
        if not columns_info:
            return

        for col_name, col_meta in columns_info.items():
            logger.info(col_meta)
            widget = self._create_filter_widget(col_name, col_meta)
            if widget:
                self.filters_widgets[col_name] = widget
                self.filters_container.layout().addWidget(widget)

    def _get_columns_info(self, table_name: str) -> Dict[str, dict]:
        response = database.get_table_columns(table_name)
        if response.status == "error" or response.data is None:
            logger.error(f"Не удалось получить колонки для таблицы {table_name}: {response.error}")
            return None
        return response.data

    def _create_filter_widget(self, col_name: str, col_info: Dict[str, Any]) -> QWidget:
        """Создаёт виджет фильтра на основе полной информации о колонке."""
        container = QWidget()
        layout = HLayout()  # предполагается, что это QHBoxLayout или аналог
        container.setLayout(layout)

        label = QLabel(f"{col_name}:")
        layout.addWidget(label)

        input_widget = None

        # 1. ENUM — выпадающий список
        if col_info.get("enum_values"):
            combo = QComboBox()
            combo.addItem("— не выбрано —", None)
            for value in col_info["enum_values"]:
                combo.addItem(str(value), value)
            input_widget = combo

        # # 2. FOREIGN KEY — выпадающий список с загрузкой данных
        # elif col_info.get("foreign_keys"):
        #     # Берём первую FK (обычно одна)
        #     fk = col_info["foreign_keys"][0]
        #     target_table = fk["target_table"]
        #     target_column = fk["target_column"]

        #     combo = ComboBox()
        #     combo.addItem("— не выбрано —", None)
        #     combo.setProperty("foreign_key", {"table": target_table, "column": target_column})
        #     input_widget = combo

        #     try:
        #         # Пример: загружаем {id: ..., name: ...} из связанной таблицы
        #         # Ты должен реализовать этот метод!
        #         options = self._load_foreign_key_options(target_table)
        #         for item in options:
        #             display = item.get("name") or item.get("type") or str(item.get("id"))
        #             combo.addItem(display, item["id"])
        #     except Exception as e:
        #         combo.addItem(f"Ошибка загрузки: {e}", None)

        # 3. Стандартные типы
        else:
            col_type_upper = (col_info.get("type") or "").upper()

            if any(t in col_type_upper for t in ("TEXT", "VARCHAR", "CHAR", "STRING", "NAME", "FLAVOR", "LOCATION", "DESCRIPTION", "CLIENT", "TECHNICIAN", "RECOMMENDATION")):
                edit = QLineEdit()
                edit.setPlaceholderText("введите текст...")
                input_widget = edit

            elif any(t in col_type_upper for t in ("INTEGER", "BIGINT", "SERIAL")):
                spin = QSpinBox()
                spin.setRange(-9999999, 9999999)
                spin.setSpecialValueText("— не задано —")
                input_widget = spin

            elif any(t in col_type_upper for t in ("NUMERIC", "DECIMAL", "FLOAT", "REAL")):
                spin = QDoubleSpinBox()
                spin.setRange(-9999999.99, 9999999.99)
                spin.setDecimals(2)
                spin.setSpecialValueText("— не задано —")
                input_widget = spin

            elif "BOOLEAN" in col_type_upper:
                cb = QCheckBox()
                input_widget = cb

            elif any(t in col_type_upper for t in ("DATE", "DATETIME", "TIMESTAMP")):
                dt = QDateEdit()
                dt.setCalendarPopup(True)
                dt.setSpecialValueText("— не задано —")
                # Можно установить режим "без даты", но проще — использовать флаг
                input_widget = dt

            else:
                # Fallback
                edit = QLineEdit()
                edit.setPlaceholderText(f"({col_info.get('type', 'unknown')})")
                input_widget = edit

        if input_widget is not None:
            layout.addWidget(input_widget)
            container.input_widget = input_widget  # для последующего get_filters()
            container.col_info = col_info  # сохраняем метаданные

        return container

    def clear_filters(self):
        """Очищает все фильтры"""
        while self.filters_container.layout().count():
            child = self.filters_container.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.filters_widgets.clear()

    def get_filters(self) -> dict:
        """Возвращает текущие значения фильтров в виде {col: value}"""
        result = {}
        for col, widget in self.filters_widgets.items():
            if hasattr(widget, 'text'):
                val = widget.text()
            elif hasattr(widget, 'value'):
                val = widget.value()
            elif hasattr(widget, 'isChecked'):
                val = widget.isChecked()
            elif hasattr(widget, 'dateTime'):
                val = widget.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            else:
                val = None
            if val not in (None, "", 0, False):  # можно настроить логику
                result[col] = val
        return result

    def get_selected_table(self) -> str:
        return self.table_combo.currentText()
