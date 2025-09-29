# frontend/widgets/DynamicTable.py

from typing import List, Dict, Any, Optional
from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QComboBox,
    QDateEdit, QDoubleSpinBox, QSpinBox, QLineEdit, QCheckBox
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QBrush, QColor
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase

from backend.repository import DatabaseRepository
from backend.utils.responce_types import ResponseStatus
from frontend.shared.ui import SizeAdjustPolicy, Size
from .TableItem import TableItem  # если нужен, иначе используем QTableWidgetItem

# Алиасы для совместимости
TableRow = List[QTableWidgetItem]


class DynamicTable(QTableWidget):
    """
    Универсальная таблица для отображения и редактирования данных любой SQLAlchemy-модели.
    Поддерживает все типы колонок из твоей модели: FK, ENUM, Date, Numeric и т.д.
    """

    def __init__(self, model_class: Optional[type[DeclarativeBase]] = None):
        super().__init__()
        self.setMaximumSize(Size(1800, 900))
        self.setSizeAdjustPolicy(SizeAdjustPolicy.AdjustToContents)
        self.setSortingEnabled(True)
        
        self._model_class = None
        self._column_info = {}  # {col_name: col_metadata}
        self._foreign_key_data = {}  # {col_name: [(id, display), ...]}
        self._enum_values = {}  # {col_name: [values]}

        if model_class:
            self.set_model(model_class)

    def set_model(self, model_class: type[DeclarativeBase]):
        """Устанавливает модель SQLAlchemy и настраивает колонки"""
        self._model_class = model_class
        table_name = model_class.__tablename__
        
        # Получаем метаданные колонок
        repo = DatabaseRepository()
        col_resp = repo.get_table_columns(table_name)
        if col_resp.status != ResponseStatus.SUCCESS:
            raise ValueError(f"Не удалось загрузить колонки для {table_name}: {col_resp.message}")
        
        self._column_info = col_resp.data
        self._setup_columns()
        self._preload_foreign_key_data()

    def _setup_columns(self):
        """Настраивает заголовки и типы колонок"""
        columns = list(self._column_info.keys())
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

    def _preload_foreign_key_data(self):
        """Предзагружает данные для внешних ключей (если записей мало)"""
        for col_name, info in self._column_info.items():
            if info.get("foreign_keys"):
                fk = info["foreign_keys"][0]
                target_table = fk["target_table"]
                target_col = fk["target_column"]
                
                # Определяем display колонку
                display_col = self._get_display_column_for_table(target_table)
                
                # Загружаем данные
                repo = DatabaseRepository()
                resp = repo.get_table_data(
                    table_name=target_table,
                    columns_list=[target_col, display_col] if display_col != target_col else [target_col],
                    limit=100  # только если мало записей
                )
                if resp.status == ResponseStatus.SUCCESS:
                    items = []
                    for row in resp.data:
                        id_val = row[target_col]
                        display_val = row.get(display_col, id_val)
                        items.append((id_val, str(display_val)))
                    self._foreign_key_data[col_name] = items

    def _get_display_column_for_table(self, table_name: str) -> str:
        """Находит подходящую колонку для отображения в связанной таблице"""
        repo = DatabaseRepository()
        col_resp = repo.get_table_columns(table_name)
        if col_resp.status != ResponseStatus.SUCCESS:
            return "id"  # fallback
        
        cols = col_resp.data
        candidates = ["name", "title", "label", "model", "type", "flavor"]
        for cand in candidates:
            if cand in cols:
                col_type = (cols[cand].get("type") or "").upper()
                if any(t in col_type for t in ("TEXT", "VARCHAR", "CHAR", "STRING")):
                    return cand
        # Если не нашли — возвращаем первую текстовую колонку или id
        for name, info in cols.items():
            if "TEXT" in (info.get("type") or "").upper():
                return name
        return list(cols.keys())[0] if cols else "id"

    def load_data(self, data: List[Dict[str, Any]]):
        """Загружает данные в таблицу"""
        self.setRowCount(len(data))
        columns = list(self._column_info.keys())
        print(data)
        for row_idx, row_data in enumerate(data):
            for col_idx, col_name in enumerate(columns):
                value = row_data.get(col_name)
                item = self._create_item_for_value(col_name, value)
                self.setItem(row_idx, col_idx, item)

        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def _create_item_for_value(self, col_name: str, value) -> QTableWidgetItem:
        """Создаёт QTableWidgetItem с правильным отображением значения"""
        if value is None:
            return QTableWidgetItem("")
        
        col_info = self._column_info[col_name]
        col_type = (col_info.get("type") or "").upper()

        # Для ENUM и FK — отображаем человекочитаемое значение
        if col_info.get("enum_values"):
            return QTableWidgetItem(str(value))
        elif col_info.get("foreign_keys"):
            # Ищем display значение в предзагруженных данных
            fk_data = self._foreign_key_data.get(col_name, [])
            for id_val, display_val in fk_data:
                if id_val == value:
                    return QTableWidgetItem(display_val)
            return QTableWidgetItem(f"ID: {value}")
        elif "DATE" in col_type:
            if isinstance(value, str):
                return QTableWidgetItem(value)
            return QTableWidgetItem(value.strftime("%Y-%m-%d"))
        else:
            return QTableWidgetItem(str(value))

    def get_row_data(self, row: int) -> Dict[str, Any]:
        """Возвращает данные строки в виде словаря {col_name: value}"""
        data = {}
        columns = list(self._column_info.keys())
        for col_idx, col_name in enumerate(columns):
            item = self.item(row, col_idx)
            if not item:
                data[col_name] = None
                continue

            col_info = self._column_info[col_name]
            display_text = item.text()
            
            # Преобразуем обратно в значение
            if col_info.get("foreign_keys"):
                # Ищем ID по display тексту
                fk_data = self._foreign_key_data.get(col_name, [])
                for id_val, display_val in fk_data:
                    if display_val == display_text:
                        data[col_name] = id_val
                        break
                else:
                    data[col_name] = None
            elif col_info.get("enum_values"):
                data[col_name] = display_text if display_text in col_info["enum_values"] else None
            elif "INTEGER" in (col_info.get("type") or "").upper():
                try:
                    data[col_name] = int(display_text) if display_text else None
                except ValueError:
                    data[col_name] = None
            elif any(t in (col_info.get("type") or "").upper() for t in ("NUMERIC", "DECIMAL", "FLOAT", "REAL")):
                try:
                    data[col_name] = float(display_text) if display_text else None
                except ValueError:
                    data[col_name] = None
            elif "BOOLEAN" in (col_info.get("type") or "").upper():
                data[col_name] = display_text.lower() in ("true", "1", "yes")
            else:
                data[col_name] = display_text if display_text else None

        return data

    def add_empty_row(self):
        """Добавляет пустую строку в конец таблицы"""
        row = self.rowCount()
        self.insertRow(row)
        columns = list(self._column_info.keys())
        for col_idx, col_name in enumerate(columns):
            self.setItem(row, col_idx, QTableWidgetItem(""))

    def get_all_data(self) -> List[Dict[str, Any]]:
        """Возвращает все данные таблицы"""
        return [self.get_row_data(row) for row in range(self.rowCount())]

    # Утилиты для совместимости с твоим старым API (если нужно)
    def get_last_row_index(self) -> int:
        return self.rowCount() - 1

    def append_row(self, data_dict: Dict[str, Any]):
        """Добавляет строку из словаря"""
        self.add_empty_row()
        row = self.get_last_row_index()
        columns = list(self._column_info.keys())
        for col_idx, col_name in enumerate(columns):
            value = data_dict.get(col_name)
            item = self._create_item_for_value(col_name, value)
            self.setItem(row, col_idx, item)