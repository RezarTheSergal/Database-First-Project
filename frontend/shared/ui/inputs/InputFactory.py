from typing import Dict, Any

from frontend.shared.ui.filters.ForeignKeyFilterWidget import ForeignKeyFilterWidget
from frontend.shared.ui.inputs import StringInput, DateInput, FloatInput, IntInput, BoolInput, EnumInput


class InputFactory:
    """Фабрика для создания виджетов фильтров"""

    @staticmethod
    def create_filter_widget(
        column_name: str, column_info: Dict[str, Any]
    ):
        """
        Создает подходящий виджет фильтра на основе информации о колонке
        """
        # 1. ENUM - выпадающий список
        if column_info.get("enum_values"):
            return EnumInput(column_info.get("enum_values"))

        # 2. FOREIGN KEY - поиск с автодополнением
        elif column_info.get("foreign_keys"):
            return ForeignKeyFilterWidget(column_name, column_info)

        # 3. Стандартные типы
        else:
            col_type_upper = (column_info.get("type") or "").upper()

            if any(t in col_type_upper for t in ("TEXT", "VARCHAR", "CHAR", "STRING")):
                return StringInput()

            elif any(t in col_type_upper for t in ("INTEGER", "BIGINT", "SERIAL")):
                return IntInput()

            elif any(
                t in col_type_upper for t in ("NUMERIC", "DECIMAL", "FLOAT", "REAL")
            ):
                return FloatInput()

            elif "BOOLEAN" in col_type_upper:
                return BoolInput()

            elif any(t in col_type_upper for t in ("DATE", "DATETIME", "TIMESTAMP")):
                return DateInput()

            else:
                # Fallback для неизвестных типов
                return StringInput()
