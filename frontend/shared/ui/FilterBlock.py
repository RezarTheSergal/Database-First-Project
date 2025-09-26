from PySide6.QtWidgets import QWidget, QHBoxLayout
from frontend.shared.ui import VLayout, Widget
from frontend.shared.ui.ComboBox import ComboBoxClass
from backend.repository import DatabaseRepository
import logging

logger = logging.getLogger()
database = DatabaseRepository()

class FilterBlockClass(QWidget):
    def __init__(self, initial_tables=None, parent=None):
        super().__init__(parent)
        self.hor_layout = QHBoxLayout(self)
        self.hor_layout.setContentsMargins(0, 0, 0, 0)

        self.table_combo = ComboBoxClass(
            items=initial_tables or [],
            callback=self._on_table_changed
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
            widget = self._create_filter_widget(col_meta["type"], col_name)
            if widget:
                self.filters_widgets[col_name] = widget
                self.filters_container.layout().addWidget(widget)

    def _get_columns_info(self, table_name: str):
        response = database.get_table_columns(table_name)
        if response.status == "error" or response.data is None:
            logger.error(f"Не удалось получить колонки для таблицы {table_name}: {response.error}")
            return None
        return response.data

    def _create_filter_widget(self, col_type: str, col_name: str):
        """Фабрика виджетов фильтра по типу колонки"""
        # Пример маппинга типов → виджетов
        if col_type in ("TEXT", "VARCHAR", "STRING"):
            from frontend.shared.ui import LineEdit
            return LineEdit(placeholder=f"Фильтр по {col_name}")
        elif col_type in ("INTEGER", "REAL", "NUMERIC"):
            from frontend.shared.ui import SpinBox
            sb = SpinBox()
            sb.setPlaceholder(f"{col_name}")
            return sb
        elif col_type in ("BOOLEAN",):
            from PySide6.QtWidgets import QCheckBox
            cb = QCheckBox(f"{col_name}")
            return cb
        elif col_type in ("DATE", "DATETIME"):
            from PySide6.QtWidgets import QDateTimeEdit
            dt = QDateTimeEdit()
            dt.setCalendarPopup(True)
            return dt
        else:
            # fallback
            from frontend.shared.ui import LineEdit
            return LineEdit(placeholder=f"{col_name} ({col_type})")

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