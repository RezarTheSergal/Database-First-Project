from typing import Dict, List, Any, Optional, Tuple
from backend.repository import DatabaseRepository
from backend.utils.responce_types import ResponseStatus
from frontend.shared.lib import translate

class TableDataProcessor:
    """Обрабатывает бизнес-логику таблицы: метаданные, запросы к БД, преобразование типов"""

    def __init__(self, model_class: Optional[type]) -> None:
        self._column_info: Dict[str, Any] = {}
        self._foreign_key_data: Dict[str, List[Tuple[Any, str]]] = {}
        self._enum_values: Dict[str, List[Any]] = {}
        self._model_class = model_class
        self._load_metadata()

    def _load_metadata(self) -> None:
        """Загружает метаданные колонок из базы данных"""
        if not self._model_class:
            return

        repo = DatabaseRepository()
        table_name = self._model_class.__tablename__
        resp = repo.get_table_columns(table_name)

        if resp.status == ResponseStatus.SUCCESS and resp.data:
            self._column_info = resp.data
            # Извлекаем enum_values и foreign_keys
            for col_name, col_meta in self._column_info.items():
                if col_meta.get("enum_values"):
                    self._enum_values[col_name] = col_meta["enum_values"]
                if col_meta.get("foreign_keys"):
                    self._foreign_key_data[col_name] = []

    def _get_display_column_for_table(self, table_name: str) -> str:
        """Находит колонку для отображения в связанной таблице"""
        repo = DatabaseRepository()
        col_resp = repo.get_table_columns(table_name)
        if col_resp.status != ResponseStatus.SUCCESS:
            return "id"

        cols = col_resp.data
        candidates = ["name", "title", "label", "model", "type", "flavor"]
        for cand in candidates:
            if cand in cols:
                col_type = (cols[cand].get("type") or "").upper()
                if any(t in col_type for t in ("TEXT", "VARCHAR", "CHAR", "STRING")):
                    return cand

        if isinstance(cols, dict):
            for name, info in cols.items():
                if "TEXT" in (info.get("type") or "").upper():
                    return name
        return list(cols.keys())[0] if cols else "id"

    def _preload_foreign_key_data(self, col_name: str) -> None:
        """Предзагружает данные для внешних ключей"""
        if col_name not in self._foreign_key_data:
            return

        fk_info = self._column_info[col_name]["foreign_keys"][0]
        target_table = fk_info["target_table"]
        target_col = fk_info["target_column"]
        display_col = self._get_display_column_for_table(target_table)

        repo = DatabaseRepository()
        resp = repo.get_table_data(
            table_name=target_table,
            columns_list=(
                [target_col, display_col] if display_col != target_col else [target_col]
            ),
            limit=100,
        )

        if resp.status == ResponseStatus.SUCCESS and resp.data:
            items = []
            for row in resp.data:
                id_val = row[target_col]
                display_val = row.get(display_col, id_val)
                items.append((id_val, str(display_val)))
            self._foreign_key_data[col_name] = items

    def get_columns(self) -> List[str]:
        """Возвращает список имен колонок"""
        return list(self._column_info.keys())

    def get_column_info(self, col_name: str) -> Optional[Dict]:
        """Возвращает метаданные колонки"""
        return self._column_info.get(col_name)

    def convert_to_ui_value(self, col_name: str, value: Any) -> str:
        """Преобразует значение в строку для отображения в таблице"""
        if value is None:
            return ""

        col_info = self._column_info.get(col_name, {})
        col_type = (col_info.get("type") or "").upper()

        # Обработка ENUM
        if col_info.get("enum_values"):
            return str(value)

        # Обработка внешних ключей
        if col_info.get("foreign_keys"):
            fk_data = self._foreign_key_data.get(col_name, [])
            for id_val, display_val in fk_data:
                if id_val == value:
                    return display_val
            return f"ID: {value}"

        # Обработка дат
        if "DATE" in col_type:
            if isinstance(value, str):
                return value
            return value.strftime("%Y-%m-%d")

        # Обработка чисел
        if "INTEGER" in col_type:
            return str(int(value)) if value is not None else ""
        if any(t in col_type for t in ("NUMERIC", "DECIMAL", "FLOAT", "REAL")):
            return str(float(value)) if value is not None else ""

        # Обработка булево
        if "BOOLEAN" in col_type:
            return translate("Yes") if value else translate("No")

        # По умолчанию
        return str(value) if value is not None else ""

    def convert_from_ui_value(self, col_name: str, display_text: str) -> Any:
        """Преобразует строку из UI в бизнес-формат"""
        col_info = self._column_info.get(col_name, {})
        col_type = (col_info.get("type") or "").upper()

        # Обработка внешних ключей
        if col_info.get("foreign_keys"):
            fk_data = self._foreign_key_data.get(col_name, [])
            for id_val, display_val in fk_data:
                if display_val == display_text:
                    return id_val
            return None

        # Обработка ENUM
        if col_info.get("enum_values"):
            return display_text if display_text in col_info["enum_values"] else None

        # Обработка чисел
        if "INTEGER" in col_type:
            try:
                return int(display_text) if display_text else None
            except ValueError:
                return None
        if any(t in col_type for t in ("NUMERIC", "DECIMAL", "FLOAT", "REAL")):
            try:
                return float(display_text) if display_text else None
            except ValueError:
                return None

        # Обработка булево
        if "BOOLEAN" in col_type:
            return display_text.lower() in ("true", "1", "yes")

        # По умолчанию
        return display_text if display_text else None

    def preload_foreign_key_data(self, col_name: str) -> None:
        """Предзагружает данные для внешнего ключа (вызывается при необходимости)"""
        self._preload_foreign_key_data(col_name)
