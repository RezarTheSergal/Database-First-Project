from typing import List, Dict, Any, Optional
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from ..lib.TableDataProcessor import TableDataProcessor
from frontend.shared.ui import SizeAdjustPolicy
from ..lib.set_model import set_model


class DynamicTable(QTableWidget):
    """Таблица с управляющей логикой для отображения данных"""

    def __init__(self, model_class: Optional[type] = None):
        super().__init__()
        self.setSizeAdjustPolicy(SizeAdjustPolicy.AdjustToContents)
        self.setSortingEnabled(True)

        # Инициализируем бизнес-процессор
        self._data_processor = TableDataProcessor(model_class)

        # Если модель указана, устанавливаем модель
        if model_class:
            set_model(self, model_class)

        # Настройка колонок
        self._setup_columns()

    def _setup_columns(self) -> None:
        """Настройка заголовков колонок на основе метаданных"""
        columns = self._data_processor.get_columns()
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

    def load_data(self, data: List[Dict[str, Any]]) -> None:
        """Загружает данные в таблицу"""
        self.setRowCount(len(data))
        columns = self._data_processor.get_columns()

        for row_idx, row_data in enumerate(data):
            for col_idx, col_name in enumerate(columns):
                value = row_data.get(col_name)
                item = self._create_item_for_value(col_name, value)
                self.setItem(row_idx, col_idx, item)

        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def _create_item_for_value(self, col_name: str, value: Any) -> QTableWidgetItem:
        """Создает ячейку с правильным отображением значения"""
        display_text = self._data_processor.convert_to_ui_value(col_name, value)
        return QTableWidgetItem(display_text)

    def add_empty_row(self) -> None:
        """Добавляет пустую строку в конец таблицы"""
        row = self.rowCount()
        self.insertRow(row)
        columns = self._data_processor.get_columns()
        for col_idx, col_name in enumerate(columns):
            self.setItem(row, col_idx, QTableWidgetItem(""))

    def get_row_data(self, row: int) -> Dict[str, Any]:
        """Возвращает данные строки в виде словаря"""
        data = {}
        columns = self._data_processor.get_columns()

        for col_idx, col_name in enumerate(columns):
            item = self.item(row, col_idx)
            if not item:
                data[col_name] = None
                continue

            display_text = item.text()
            value = self._data_processor.convert_from_ui_value(col_name, display_text)
            data[col_name] = value

        return data

    def get_all_data(self) -> List[Dict[str, Any]]:
        """Возвращает все данные таблицы"""
        return [self.get_row_data(row) for row in range(self.rowCount())]

    def get_last_row_index(self) -> int:
        """Возвращает индекс последней строки"""
        return self.rowCount() - 1

    def append_row(self, data_dict: Dict[str, Any]) -> None:
        """Добавляет строку из словаря"""
        self.add_empty_row()
        row = self.get_last_row_index()
        columns = self._data_processor.get_columns()

        for col_idx, col_name in enumerate(columns):
            value = data_dict.get(col_name)
            item = self._create_item_for_value(col_name, value)
            self.setItem(row, col_idx, item)
